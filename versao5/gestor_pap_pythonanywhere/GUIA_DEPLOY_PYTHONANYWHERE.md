# 🚀 Guia de Deploy — Gestor PAP no PythonAnywhere
**Autor:** Jorge Costa e Silva  
**Data:** Abril 2026

---

## O que vais fazer
Colocar o Gestor PAP online de forma gratuita no PythonAnywhere.  
Após estes passos, a app ficará acessível em:  
👉 `https://TEUUSERNAME.pythonanywhere.com`

Tempo estimado: **15 a 20 minutos**

---

## PASSO 1 — Criar conta gratuita

1. Vai a **https://www.pythonanywhere.com**
2. Clica em **"Start running Python online in less than a minute!"**
3. Escolhe **"Create a Beginner account"** (gratuito)
4. Preenche:
   - Username (ex: `jorgepap` — vai fazer parte do URL)
   - Email
   - Password
5. Confirma o email e faz login

---

## PASSO 2 — Abrir a Bash Console

1. No painel do PythonAnywhere, clica em **"Consoles"**
2. Clica em **"Bash"** (nova consola)
3. Vai aparecer um terminal — é aqui que escreves os comandos

---

## PASSO 3 — Criar a pasta do projeto

Na consola Bash, escreve estes comandos um a um:

```bash
mkdir ~/gestor_pap
cd ~/gestor_pap
mkdir templates
mkdir static
```

---

## PASSO 4 — Fazer upload dos ficheiros

### 4a. Upload do app.py
1. No painel principal, clica em **"Files"**
2. Navega até à pasta `gestor_pap`
3. Clica em **"Upload a file"**
4. Faz upload de: `app.py`

### 4b. Upload dos templates
1. Clica na pasta `templates`
2. Faz upload de todos os ficheiros `.html`:
   - `base.html` ← usa a versão fornecida (sem botão Sair)
   - `index.html`
   - `aluno_form.html`
   - `aluno_detalhe.html`
   - `projeto_form.html`
   - `projeto_detalhe.html`
   - `fase_form.html`
   - `pesquisar.html`

### 4c. Upload do CSS
1. Clica na pasta `static`
2. Faz upload do teu ficheiro `style.css`

---

## PASSO 5 — Criar a Web App

1. No painel, clica em **"Web"**
2. Clica em **"Add a new web app"**
3. Clica **"Next"**
4. Escolhe **"Flask"**
5. Escolhe **"Python 3.10"**
6. No campo do caminho, apaga o que está e escreve:
   ```
   /home/TEUUSERNAME/gestor_pap/app.py
   ```
   ⚠️ Substitui `TEUUSERNAME` pelo teu username real
7. Clica **"Next"** e depois **"Next"** novamente

---

## PASSO 6 — Configurar o caminho dos ficheiros estáticos

Ainda na página "Web", procura a secção **"Static files"**:

| URL       | Directory                                      |
|-----------|------------------------------------------------|
| `/static` | `/home/TEUUSERNAME/gestor_pap/static`          |

Clica em **"Save** (guardar) nessa linha.

---

## PASSO 7 — Recarregar e testar

1. Clica no botão verde **"Reload"** no topo da página Web
2. Clica no link `TEUUSERNAME.pythonanywhere.com`
3. O Gestor PAP deve abrir no browser! 🎉

---

## PASSO 8 — Verificar se está tudo bem

Se aparecer um erro, clica em **"Error log"** na página Web para ver o que falhou.

Os erros mais comuns são:
- Caminho do `app.py` errado → verifica o PASSO 5
- Falta um ficheiro `.html` na pasta `templates`
- O `style.css` não foi para a pasta `static`

---

## ⚠️ Limitações da conta gratuita

| Limitação | Detalhe |
|-----------|---------|
| 1 web app | Suficiente para este projeto |
| CPU limitada | Suficiente para uso pessoal/escolar |
| Sem domínio próprio | URL fica `username.pythonanywhere.com` |
| A app "dorme" | Após 3 meses sem login, precisas de reativar |

Para reativar: basta fazer login no PythonAnywhere → Web → Reload.

---

## 📁 Estrutura final de ficheiros no PythonAnywhere

```
/home/TEUUSERNAME/gestor_pap/
├── app.py
├── projetos_pap.db        ← criado automaticamente
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── aluno_form.html
│   ├── aluno_detalhe.html
│   ├── projeto_form.html
│   ├── projeto_detalhe.html
│   ├── fase_form.html
│   └── pesquisar.html
└── static/
    └── style.css
```

---

## 🔄 Como manter as duas versões (local + online)

| | Versão Local (VS Code) | Versão Online (PythonAnywhere) |
|---|---|---|
| Acesso | Só no teu PC | Qualquer computador |
| Dados | `projetos_pap.db` local | `projetos_pap.db` no servidor |
| Arranque | `python app.py` no terminal | Sempre ativa |
| Internet | Não precisa | Precisa |

⚠️ **As duas bases de dados são independentes.**  
Se inserires dados localmente e queres que apareçam online (ou vice-versa), precisas de copiar o ficheiro `projetos_pap.db` entre os dois ambientes via "Files" no PythonAnywhere.

---

*Guia preparado com Claude · Abril 2026*
