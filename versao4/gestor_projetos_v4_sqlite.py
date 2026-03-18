import sqlite3
import os

NOME_BD = "projetos.db"


# --------------------------------------------------
# Funções auxiliares
# --------------------------------------------------

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPrima ENTER para continuar...")


def mostrar_menu():
    print("=" * 50)
    print(f"{'GESTOR DE PROJETOS DE ALUNOS - V4':^50}")
    print("=" * 50)
    print("1 - Adicionar projeto")
    print("2 - Listar projetos")
    print("3 - Pesquisar projeto por aluno")
    print("4 - Alterar estado do projeto")
    print("5 - Remover projeto")
    print("6 - Mostrar estatísticas")
    print("0 - Sair")
    print("=" * 50)


def escolher_estado():
    while True:
        print("\nEscolha o estado do projeto:")
        print("1 - Por iniciar")
        print("2 - Em desenvolvimento")
        print("3 - Concluído")

        opcao = input("Opção: ")

        if opcao == "1":
            return "Por iniciar"
        elif opcao == "2":
            return "Em desenvolvimento"
        elif opcao == "3":
            return "Concluído"
        else:
            print("Opção inválida. Tente novamente.")


# --------------------------------------------------
# Base de dados
# --------------------------------------------------

def ligar_bd():
    return sqlite3.connect(NOME_BD)


def criar_tabela():
    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            turma TEXT NOT NULL,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            estado TEXT NOT NULL,
            observacoes TEXT
        )
    """)

    ligacao.commit()
    ligacao.close()


# --------------------------------------------------
# Funcionalidades principais
# --------------------------------------------------

def adicionar_projeto():
    print("\n===== ADICIONAR PROJETO =====")

    aluno = input("Nome do aluno: ").strip()
    turma = input("Turma: ").strip()
    titulo = input("Título do projeto: ").strip()
    tipo = input("Tipo de projeto (PAP / Trabalho / Outro): ").strip()
    data_inicio = input("Data de início: ").strip()
    estado = escolher_estado()
    observacoes = input("Observações: ").strip()

    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("""
        INSERT INTO projetos (aluno, turma, titulo, tipo, data_inicio, estado, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (aluno, turma, titulo, tipo, data_inicio, estado, observacoes))

    ligacao.commit()
    ligacao.close()

    print("\nProjeto adicionado com sucesso.")


def listar_projetos():
    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("SELECT * FROM projetos")
    projetos = cursor.fetchall()

    ligacao.close()

    print("\n===== LISTA DE PROJETOS =====")

    if len(projetos) == 0:
        print("Não existem projetos registados.")
        return

    for projeto in projetos:
        print(f"\nID: {projeto[0]}")
        print(f"Aluno: {projeto[1]}")
        print(f"Turma: {projeto[2]}")
        print(f"Título: {projeto[3]}")
        print(f"Tipo: {projeto[4]}")
        print(f"Data de início: {projeto[5]}")
        print(f"Estado: {projeto[6]}")
        print(f"Observações: {projeto[7]}")
        print("-" * 50)


def pesquisar_projeto():
    nome = input("Introduza o nome do aluno a pesquisar: ").strip()

    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("""
        SELECT * FROM projetos
        WHERE lower(aluno) = lower(?)
    """, (nome,))

    projetos = cursor.fetchall()
    ligacao.close()

    print("\n===== PESQUISA DE PROJETOS =====")

    if len(projetos) == 0:
        print("Não foi encontrado nenhum projeto para esse aluno.")
        return

    for projeto in projetos:
        print(f"\nID: {projeto[0]}")
        print(f"Aluno: {projeto[1]}")
        print(f"Turma: {projeto[2]}")
        print(f"Título: {projeto[3]}")
        print(f"Tipo: {projeto[4]}")
        print(f"Data de início: {projeto[5]}")
        print(f"Estado: {projeto[6]}")
        print(f"Observações: {projeto[7]}")
        print("-" * 50)


def alterar_estado():
    try:
        id_projeto = int(input("Introduza o ID do projeto: "))
    except ValueError:
        print("Erro: deve introduzir um número inteiro.")
        return

    novo_estado = escolher_estado()

    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("SELECT * FROM projetos WHERE id = ?", (id_projeto,))
    projeto = cursor.fetchone()

    if projeto is None:
        ligacao.close()
        print("Projeto não encontrado.")
        return

    cursor.execute("""
        UPDATE projetos
        SET estado = ?
        WHERE id = ?
    """, (novo_estado, id_projeto))

    ligacao.commit()
    ligacao.close()

    print("Estado atualizado com sucesso.")


def remover_projeto():
    try:
        id_projeto = int(input("Introduza o ID do projeto a remover: "))
    except ValueError:
        print("Erro: deve introduzir um número inteiro.")
        return

    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("SELECT * FROM projetos WHERE id = ?", (id_projeto,))
    projeto = cursor.fetchone()

    if projeto is None:
        ligacao.close()
        print("Projeto não encontrado.")
        return

    cursor.execute("DELETE FROM projetos WHERE id = ?", (id_projeto,))
    ligacao.commit()
    ligacao.close()

    print("Projeto removido com sucesso.")


def mostrar_estatisticas():
    ligacao = ligar_bd()
    cursor = ligacao.cursor()

    cursor.execute("SELECT COUNT(*) FROM projetos")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projetos WHERE estado = 'Por iniciar'")
    por_iniciar = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projetos WHERE estado = 'Em desenvolvimento'")
    em_desenvolvimento = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projetos WHERE estado = 'Concluído'")
    concluidos = cursor.fetchone()[0]

    ligacao.close()

    print("\n===== ESTATÍSTICAS =====")
    print(f"Total de projetos: {total}")
    print(f"Por iniciar: {por_iniciar}")
    print(f"Em desenvolvimento: {em_desenvolvimento}")
    print(f"Concluídos: {concluidos}")


# --------------------------------------------------
# Programa principal
# --------------------------------------------------

criar_tabela()

while True:
    limpar_terminal()
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_projeto()
        pausar()

    elif opcao == "2":
        listar_projetos()
        pausar()

    elif opcao == "3":
        pesquisar_projeto()
        pausar()

    elif opcao == "4":
        alterar_estado()
        pausar()

    elif opcao == "5":
        remover_projeto()
        pausar()

    elif opcao == "6":
        mostrar_estatisticas()
        pausar()

    elif opcao == "0":
        print("A sair do programa...")
        break

    else:
        print("Opção inválida. Tente novamente.")
        pausar()