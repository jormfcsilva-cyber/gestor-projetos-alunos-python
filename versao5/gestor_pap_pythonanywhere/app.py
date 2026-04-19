# =============================================================
#  Gestor de Projetos de Alunos - V5 Relacional (Flask + SQLite)
#  Autor: Jorge Costa e Silva  |  Escola Sec. Vergílio Ferreira
#  Versão: PythonAnywhere com Login e Gestão de Utilizadores
# =============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os, hashlib, secrets

app = Flask(__name__)
app.secret_key = "gestor_pap_relacional_2026_seguro"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOME_BD  = os.path.join(BASE_DIR, "projetos_pap.db")


# --------------------------------------------------
# Utilitários de password
# --------------------------------------------------

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{h}"

def verificar_password(password, hash_guardado):
    try:
        salt, _ = hash_guardado.split(":", 1)
        return hash_password(password, salt) == hash_guardado
    except Exception:
        return False


# --------------------------------------------------
# Base de dados
# --------------------------------------------------

def ligar_bd():
    conn = sqlite3.connect(NOME_BD)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    conn = ligar_bd()
    c = conn.cursor()

    # Tabela UTILIZADORES
    c.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT NOT NULL UNIQUE,
            password  TEXT NOT NULL,
            nome      TEXT NOT NULL,
            role      TEXT NOT NULL DEFAULT 'user',
            ativo     INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Criar admin padrão se não existir nenhum utilizador
    existe = c.execute("SELECT COUNT(*) FROM utilizadores").fetchone()[0]
    if existe == 0:
        pw = hash_password("pap2026")
        c.execute("""
            INSERT INTO utilizadores (username, password, nome, role)
            VALUES (?, ?, ?, ?)
        """, ("jorge", pw, "Jorge Silva", "admin"))

    # Tabela ALUNOS
    c.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT NOT NULL,
            numero      TEXT,
            turma       TEXT NOT NULL,
            curso       TEXT,
            email       TEXT,
            ano_letivo  TEXT,
            observacoes TEXT
        )
    """)

    # Tabela PROJETOS
    c.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id     INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
            titulo       TEXT NOT NULL,
            tipo         TEXT NOT NULL DEFAULT 'PAP',
            data_inicio  TEXT,
            estado_geral TEXT NOT NULL DEFAULT 'Por iniciar',
            orientador   TEXT,
            observacoes  TEXT
        )
    """)

    # Tabela FASES
    c.execute("""
        CREATE TABLE IF NOT EXISTS fases (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id          INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
            nome_fase           TEXT NOT NULL,
            data_reuniao        TEXT,
            descricao           TEXT,
            ficheiros_entregues TEXT,
            avaliacao           TEXT,
            estado              TEXT NOT NULL DEFAULT 'Em curso',
            observacoes         TEXT
        )
    """)

    conn.commit()
    conn.close()


criar_tabelas()


# --------------------------------------------------
# Decoradores de proteção
# --------------------------------------------------

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("autenticado"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("autenticado"):
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Acesso reservado ao administrador.", "erro")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def get_aluno(id):
    conn = ligar_bd()
    row = conn.execute("SELECT * FROM alunos WHERE id=?", (id,)).fetchone()
    conn.close()
    return row

def get_projeto(id):
    conn = ligar_bd()
    row = conn.execute("""
        SELECT p.*, a.nome as aluno_nome, a.turma
        FROM projetos p JOIN alunos a ON a.id = p.aluno_id
        WHERE p.id=?
    """, (id,)).fetchone()
    conn.close()
    return row

def get_fase(id):
    conn = ligar_bd()
    row = conn.execute("SELECT * FROM fases WHERE id=?", (id,)).fetchone()
    conn.close()
    return row


# --------------------------------------------------
# LOGIN / LOGOUT
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("autenticado"):
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("utilizador", "").strip()
        password = request.form.get("password", "").strip()
        conn = ligar_bd()
        user = conn.execute(
            "SELECT * FROM utilizadores WHERE username=? AND ativo=1", (username,)
        ).fetchone()
        conn.close()
        if user and verificar_password(password, user["password"]):
            session["autenticado"] = True
            session["username"]    = user["username"]
            session["nome"]        = user["nome"]
            session["role"]        = user["role"]
            return redirect(url_for("index"))
        else:
            flash("Utilizador ou password incorretos.", "erro")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------------
# GESTÃO DE UTILIZADORES (só admin)
# --------------------------------------------------

@app.route("/utilizadores")
@admin_required
def utilizadores_lista():
    conn = ligar_bd()
    utilizadores = conn.execute(
        "SELECT * FROM utilizadores ORDER BY role DESC, nome"
    ).fetchall()
    conn.close()
    return render_template("utilizadores.html", utilizadores=utilizadores)


@app.route("/utilizadores/novo", methods=["GET", "POST"])
@admin_required
def utilizador_novo():
    if request.method == "POST":
        f = request.form
        username = f["username"].strip()
        nome     = f["nome"].strip()
        password = f["password"].strip()
        role     = f["role"]

        if not username or not nome or not password:
            flash("Todos os campos são obrigatórios.", "erro")
            return render_template("utilizador_form.html", utilizador=None)

        conn = ligar_bd()
        existe = conn.execute(
            "SELECT id FROM utilizadores WHERE username=?", (username,)
        ).fetchone()
        if existe:
            flash(f"O utilizador '{username}' já existe.", "erro")
            conn.close()
            return render_template("utilizador_form.html", utilizador=None)

        pw = hash_password(password)
        conn.execute("""
            INSERT INTO utilizadores (username, password, nome, role)
            VALUES (?,?,?,?)
        """, (username, pw, nome, role))
        conn.commit()
        conn.close()
        flash(f"Utilizador '{username}' criado com sucesso!", "sucesso")
        return redirect(url_for("utilizadores_lista"))

    return render_template("utilizador_form.html", utilizador=None)


@app.route("/utilizadores/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def utilizador_editar(id):
    conn = ligar_bd()
    utilizador = conn.execute(
        "SELECT * FROM utilizadores WHERE id=?", (id,)
    ).fetchone()
    conn.close()
    if not utilizador:
        flash("Utilizador não encontrado.", "erro")
        return redirect(url_for("utilizadores_lista"))

    if request.method == "POST":
        f = request.form
        nome  = f["nome"].strip()
        role  = f["role"]
        ativo = 1 if f.get("ativo") else 0
        nova_password = f["password"].strip()

        conn = ligar_bd()
        if nova_password:
            pw = hash_password(nova_password)
            conn.execute("""
                UPDATE utilizadores SET nome=?, role=?, ativo=?, password=?
                WHERE id=?
            """, (nome, role, ativo, pw, id))
        else:
            conn.execute("""
                UPDATE utilizadores SET nome=?, role=?, ativo=?
                WHERE id=?
            """, (nome, role, ativo, id))
        conn.commit()
        conn.close()
        flash("Utilizador atualizado.", "sucesso")
        return redirect(url_for("utilizadores_lista"))

    return render_template("utilizador_form.html", utilizador=utilizador)


@app.route("/utilizadores/<int:id>/remover")
@admin_required
def utilizador_remover(id):
    # Não permitir remover o próprio admin
    conn = ligar_bd()
    utilizador = conn.execute(
        "SELECT * FROM utilizadores WHERE id=?", (id,)
    ).fetchone()
    if not utilizador:
        flash("Utilizador não encontrado.", "erro")
        conn.close()
        return redirect(url_for("utilizadores_lista"))
    if utilizador["username"] == session.get("username"):
        flash("Não podes remover a tua própria conta.", "erro")
        conn.close()
        return redirect(url_for("utilizadores_lista"))
    conn.execute("DELETE FROM utilizadores WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash(f"Utilizador '{utilizador['username']}' removido.", "sucesso")
    return redirect(url_for("utilizadores_lista"))


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/")
@login_required
def index():
    conn = ligar_bd()
    total_alunos   = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    total_projetos = conn.execute("SELECT COUNT(*) FROM projetos").fetchone()[0]
    total_fases    = conn.execute("SELECT COUNT(*) FROM fases").fetchone()[0]
    por_iniciar    = conn.execute("SELECT COUNT(*) FROM projetos WHERE estado_geral='Por iniciar'").fetchone()[0]
    em_curso       = conn.execute("SELECT COUNT(*) FROM projetos WHERE estado_geral='Em desenvolvimento'").fetchone()[0]
    concluidos     = conn.execute("SELECT COUNT(*) FROM projetos WHERE estado_geral='Concluído'").fetchone()[0]
    alunos_resumo  = conn.execute("""
        SELECT a.id, a.nome, a.turma,
               p.id AS proj_id, p.titulo AS proj_titulo, p.tipo AS proj_tipo, p.estado_geral,
               (SELECT COUNT(*) FROM fases f WHERE f.projeto_id = p.id) AS num_fases,
               (SELECT f2.nome_fase FROM fases f2 WHERE f2.projeto_id = p.id
                ORDER BY f2.id DESC LIMIT 1) AS ultima_fase
        FROM alunos a LEFT JOIN projetos p ON p.aluno_id = a.id
        ORDER BY a.nome
    """).fetchall()
    conn.close()
    return render_template("index.html",
        total_alunos=total_alunos, total_projetos=total_projetos,
        total_fases=total_fases, por_iniciar=por_iniciar,
        em_curso=em_curso, concluidos=concluidos,
        alunos_resumo=alunos_resumo)


# --------------------------------------------------
# ALUNOS
# --------------------------------------------------

@app.route("/alunos/novo", methods=["GET","POST"])
@login_required
def aluno_novo():
    if request.method == "POST":
        f = request.form
        if not f["nome"].strip():
            flash("O nome do aluno é obrigatório.", "erro")
            return render_template("aluno_form.html", aluno=None)
        conn = ligar_bd()
        conn.execute("""
             INSERT INTO alunos (nome, numero, turma, curso, email, ano_letivo, observacoes)
             VALUES (?,?,?,?,?,?,?)
        """, (f["nome"].strip(), f["numero"].strip(), f["turma"].strip(), f["curso"].strip(),
              f["email"].strip(), f["ano_letivo"].strip(), f["observacoes"].strip()))
        conn.commit()
        conn.close()
        flash(f"Aluno {f['nome']} adicionado com sucesso!", "sucesso")
        return redirect(url_for("index"))
    return render_template("aluno_form.html", aluno=None)


@app.route("/alunos/<int:id>/editar", methods=["GET","POST"])
@login_required
def aluno_editar(id):
    aluno = get_aluno(id)
    if not aluno:
        flash("Aluno não encontrado.", "erro")
        return redirect(url_for("index"))
    if request.method == "POST":
        f = request.form
        conn = ligar_bd()
        conn.execute("""
            UPDATE alunos SET nome=?, numero=?, turma=?, curso=?, email=?, ano_letivo=?, observacoes=?
            WHERE id=?
        """, (f["nome"].strip(), f["numero"].strip(), f["turma"].strip(), f["curso"].strip(),
              f["email"].strip(), f["ano_letivo"].strip(), f["observacoes"].strip(), id))
        conn.commit()
        conn.close()
        flash("Dados do aluno atualizados.", "sucesso")
        return redirect(url_for("aluno_detalhe", id=id))
    return render_template("aluno_form.html", aluno=aluno)


@app.route("/alunos/<int:id>")
@login_required
def aluno_detalhe(id):
    aluno = get_aluno(id)
    if not aluno:
        flash("Aluno não encontrado.", "erro")
        return redirect(url_for("index"))
    conn = ligar_bd()
    projetos = conn.execute("""
        SELECT p.*, COUNT(f.id) AS num_fases
        FROM projetos p LEFT JOIN fases f ON f.projeto_id = p.id
        WHERE p.aluno_id = ? GROUP BY p.id ORDER BY p.id
    """, (id,)).fetchall()
    conn.close()
    return render_template("aluno_detalhe.html", aluno=aluno, projetos=projetos)


@app.route("/alunos/<int:id>/remover")
@login_required
def aluno_remover(id):
    aluno = get_aluno(id)
    if aluno:
        conn = ligar_bd()
        conn.execute("DELETE FROM alunos WHERE id=?", (id,))
        conn.commit()
        conn.close()
        flash(f"Aluno {aluno['nome']} removido.", "sucesso")
    else:
        flash("Aluno não encontrado.", "erro")
    return redirect(url_for("index"))


# --------------------------------------------------
# PROJETOS
# --------------------------------------------------

@app.route("/projetos/novo", methods=["GET","POST"])
@login_required
def projeto_novo():
    conn = ligar_bd()
    alunos = conn.execute("SELECT id, nome, turma FROM alunos ORDER BY nome").fetchall()
    conn.close()
    if request.method == "POST":
        f = request.form
        if not f["titulo"].strip():
            flash("O título do projeto é obrigatório.", "erro")
            return render_template("projeto_form.html", projeto=None, alunos=alunos)
        conn = ligar_bd()
        cur = conn.execute("""
            INSERT INTO projetos (aluno_id, titulo, tipo, data_inicio, estado_geral, orientador, observacoes)
            VALUES (?,?,?,?,?,?,?)
        """, (f["aluno_id"], f["titulo"].strip(), f["tipo"], f["data_inicio"].strip(),
              f["estado_geral"], f["orientador"].strip(), f["observacoes"].strip()))
        novo_id = cur.lastrowid
        conn.commit()
        conn.close()
        flash("Projeto criado com sucesso!", "sucesso")
        return redirect(url_for("projeto_detalhe", id=novo_id))
    aluno_id_pre = request.args.get("aluno_id")
    return render_template("projeto_form.html", projeto=None, alunos=alunos, aluno_id_pre=aluno_id_pre)


@app.route("/projetos/<int:id>")
@login_required
def projeto_detalhe(id):
    projeto = get_projeto(id)
    if not projeto:
        flash("Projeto não encontrado.", "erro")
        return redirect(url_for("index"))
    conn = ligar_bd()
    fases = conn.execute("SELECT * FROM fases WHERE projeto_id=? ORDER BY id", (id,)).fetchall()
    conn.close()
    return render_template("projeto_detalhe.html", projeto=projeto, fases=fases)


@app.route("/projetos/<int:id>/editar", methods=["GET","POST"])
@login_required
def projeto_editar(id):
    projeto = get_projeto(id)
    if not projeto:
        flash("Projeto não encontrado.", "erro")
        return redirect(url_for("index"))
    conn = ligar_bd()
    alunos = conn.execute("SELECT id, nome, turma FROM alunos ORDER BY nome").fetchall()
    conn.close()
    if request.method == "POST":
        f = request.form
        conn = ligar_bd()
        conn.execute("""
            UPDATE projetos SET aluno_id=?, titulo=?, tipo=?, data_inicio=?,
                                estado_geral=?, orientador=?, observacoes=? WHERE id=?
        """, (f["aluno_id"], f["titulo"].strip(), f["tipo"], f["data_inicio"].strip(),
              f["estado_geral"], f["orientador"].strip(), f["observacoes"].strip(), id))
        conn.commit()
        conn.close()
        flash("Projeto atualizado.", "sucesso")
        return redirect(url_for("projeto_detalhe", id=id))
    return render_template("projeto_form.html", projeto=projeto, alunos=alunos, aluno_id_pre=None)


@app.route("/projetos/<int:id>/remover")
@login_required
def projeto_remover(id):
    projeto = get_projeto(id)
    if projeto:
        aluno_id = projeto["aluno_id"]
        conn = ligar_bd()
        conn.execute("DELETE FROM projetos WHERE id=?", (id,))
        conn.commit()
        conn.close()
        flash("Projeto removido.", "sucesso")
        return redirect(url_for("aluno_detalhe", id=aluno_id))
    flash("Projeto não encontrado.", "erro")
    return redirect(url_for("index"))


# --------------------------------------------------
# FASES
# --------------------------------------------------

@app.route("/fases/nova", methods=["GET","POST"])
@login_required
def fase_nova():
    projeto_id = request.args.get("projeto_id") or request.form.get("projeto_id")
    projeto = get_projeto(projeto_id) if projeto_id else None
    if request.method == "POST":
        f = request.form
        if not f["nome_fase"].strip():
            flash("O nome da fase é obrigatório.", "erro")
            return render_template("fase_form.html", fase=None, projeto=projeto)
        conn = ligar_bd()
        conn.execute("""
            INSERT INTO fases (projeto_id, nome_fase, data_reuniao, descricao,
                               ficheiros_entregues, avaliacao, estado, observacoes)
            VALUES (?,?,?,?,?,?,?,?)
        """, (f["projeto_id"], f["nome_fase"].strip(), f["data_reuniao"].strip(),
              f["descricao"].strip(), f["ficheiros_entregues"].strip(),
              f["avaliacao"].strip(), f["estado"], f["observacoes"].strip()))
        conn.commit()
        conn.close()
        flash(f"Fase '{f['nome_fase']}' registada!", "sucesso")
        return redirect(url_for("projeto_detalhe", id=f["projeto_id"]))
    return render_template("fase_form.html", fase=None, projeto=projeto)


@app.route("/fases/<int:id>/editar", methods=["GET","POST"])
@login_required
def fase_editar(id):
    fase = get_fase(id)
    if not fase:
        flash("Fase não encontrada.", "erro")
        return redirect(url_for("index"))
    projeto = get_projeto(fase["projeto_id"])
    if request.method == "POST":
        f = request.form
        conn = ligar_bd()
        conn.execute("""
            UPDATE fases SET nome_fase=?, data_reuniao=?, descricao=?,
                             ficheiros_entregues=?, avaliacao=?, estado=?, observacoes=?
            WHERE id=?
        """, (f["nome_fase"].strip(), f["data_reuniao"].strip(), f["descricao"].strip(),
              f["ficheiros_entregues"].strip(), f["avaliacao"].strip(),
              f["estado"], f["observacoes"].strip(), id))
        conn.commit()
        conn.close()
        flash("Fase atualizada.", "sucesso")
        return redirect(url_for("projeto_detalhe", id=fase["projeto_id"]))
    return render_template("fase_form.html", fase=fase, projeto=projeto)


@app.route("/fases/<int:id>/remover")
@login_required
def fase_remover(id):
    fase = get_fase(id)
    if fase:
        projeto_id = fase["projeto_id"]
        conn = ligar_bd()
        conn.execute("DELETE FROM fases WHERE id=?", (id,))
        conn.commit()
        conn.close()
        flash("Fase removida.", "sucesso")
        return redirect(url_for("projeto_detalhe", id=projeto_id))
    flash("Fase não encontrada.", "erro")
    return redirect(url_for("index"))


# --------------------------------------------------
# PESQUISA
# --------------------------------------------------

@app.route("/pesquisar")
@login_required
def pesquisar():
    termo = request.args.get("termo", "").strip()
    resultados = []
    if termo:
        conn = ligar_bd()
        resultados = conn.execute("""
            SELECT a.id AS aluno_id, a.nome, a.turma,
                   p.id AS proj_id, p.titulo, p.tipo, p.estado_geral
            FROM alunos a LEFT JOIN projetos p ON p.aluno_id = a.id
            WHERE lower(a.nome) LIKE lower(?) OR lower(p.titulo) LIKE lower(?)
            ORDER BY a.nome
        """, (f"%{termo}%", f"%{termo}%")).fetchall()
        conn.close()
    return render_template("pesquisar.html", resultados=resultados, termo=termo)


# --------------------------------------------------
# ARRANQUE LOCAL
# --------------------------------------------------

if __name__ == "__main__":
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
    except Exception:
        ip_local = "???.???.???.???"
    print("=" * 55)
    print("  Gestor PAP - com Gestão de Utilizadores")
    print(f"  Local : http://127.0.0.1:5000")
    print(f"  Wi-Fi : http://{ip_local}:5000")
    print("  Admin padrão: jorge / pap2026")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=False)
