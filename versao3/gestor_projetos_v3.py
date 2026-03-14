import json
import os

projetos = []
proximo_id = 1
NOME_FICHEIRO = "projetos.json"


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPrima ENTER para continuar...")


def mostrar_menu():
    print("=" * 45)
    print(f"{'GESTOR DE PROJETOS DE ALUNOS':^45}")
    print("=" * 45)
    print("1 - Adicionar projeto")
    print("2 - Listar projetos")
    print("3 - Pesquisar projeto por aluno")
    print("4 - Alterar estado do projeto")
    print("5 - Remover projeto")
    print("6 - Listar projetos por estado")
    print("7 - Mostrar estatísticas")
    print("8 - Guardar projetos em ficheiro JSON")
    print("9 - Carregar projetos do ficheiro JSON")
    print("0 - Sair")
    print("=" * 45)


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


def adicionar_projeto():
    global proximo_id

    print("\n===== ADICIONAR PROJETO =====")

    aluno = input("Nome do aluno: ").strip()
    turma = input("Turma: ").strip()
    titulo = input("Título do projeto: ").strip()
    tipo = input("Tipo de projeto (PAP / Trabalho / Outro): ").strip()
    data_inicio = input("Data de início: ").strip()
    estado = escolher_estado()
    observacoes = input("Observações: ").strip()

    projeto = {
        "id": proximo_id,
        "aluno": aluno,
        "turma": turma,
        "titulo": titulo,
        "tipo": tipo,
        "data_inicio": data_inicio,
        "estado": estado,
        "observacoes": observacoes
    }

    projetos.append(projeto)
    proximo_id += 1

    print("\nProjeto adicionado com sucesso.")


def listar_projetos():
    print("\n===== LISTA DE PROJETOS =====")

    if len(projetos) == 0:
        print("Não existem projetos registados.")
        return

    for projeto in projetos:
        print(f"\nID: {projeto['id']}")
        print(f"Aluno: {projeto['aluno']}")
        print(f"Turma: {projeto['turma']}")
        print(f"Título: {projeto['titulo']}")
        print(f"Tipo: {projeto['tipo']}")
        print(f"Data de início: {projeto['data_inicio']}")
        print(f"Estado: {projeto['estado']}")
        print(f"Observações: {projeto['observacoes']}")
        print("-" * 45)


def pesquisar_projeto():
    nome = input("Introduza o nome do aluno a pesquisar: ").strip()
    encontrou = False

    for projeto in projetos:
        if projeto["aluno"].lower() == nome.lower():
            if not encontrou:
                print("\n===== PROJETO(S) ENCONTRADO(S) =====")
            print(f"\nID: {projeto['id']}")
            print(f"Aluno: {projeto['aluno']}")
            print(f"Turma: {projeto['turma']}")
            print(f"Título: {projeto['titulo']}")
            print(f"Tipo: {projeto['tipo']}")
            print(f"Data de início: {projeto['data_inicio']}")
            print(f"Estado: {projeto['estado']}")
            print(f"Observações: {projeto['observacoes']}")
            print("-" * 45)
            encontrou = True

    if not encontrou:
        print("Não foi encontrado nenhum projeto para esse aluno.")


def alterar_estado():
    if len(projetos) == 0:
        print("Não existem projetos registados.")
        return

    try:
        id_projeto = int(input("Introduza o ID do projeto: "))
    except ValueError:
        print("Erro: deve introduzir um número inteiro.")
        return

    for projeto in projetos:
        if projeto["id"] == id_projeto:
            print(f"\nProjeto encontrado: {projeto['titulo']}")
            projeto["estado"] = escolher_estado()
            print("Estado atualizado com sucesso.")
            return

    print("Projeto não encontrado.")


def remover_projeto():
    if len(projetos) == 0:
        print("Não existem projetos registados.")
        return

    try:
        id_projeto = int(input("Introduza o ID do projeto a remover: "))
    except ValueError:
        print("Erro: deve introduzir um número inteiro.")
        return

    for projeto in projetos:
        if projeto["id"] == id_projeto:
            projetos.remove(projeto)
            print("Projeto removido com sucesso.")
            return

    print("Projeto não encontrado.")


def listar_por_estado():
    if len(projetos) == 0:
        print("Não existem projetos registados.")
        return

    estado = escolher_estado()
    encontrou = False

    print(f"\n===== PROJETOS COM ESTADO: {estado.upper()} =====")

    for projeto in projetos:
        if projeto["estado"] == estado:
            print(f"\nID: {projeto['id']}")
            print(f"Aluno: {projeto['aluno']}")
            print(f"Título: {projeto['titulo']}")
            print(f"Estado: {projeto['estado']}")
            print("-" * 45)
            encontrou = True

    if not encontrou:
        print("Não existem projetos com esse estado.")


def mostrar_estatisticas():
    total = len(projetos)
    por_iniciar = 0
    em_desenvolvimento = 0
    concluido = 0

    for projeto in projetos:
        if projeto["estado"] == "Por iniciar":
            por_iniciar += 1
        elif projeto["estado"] == "Em desenvolvimento":
            em_desenvolvimento += 1
        elif projeto["estado"] == "Concluído":
            concluido += 1

    print("\n===== ESTATÍSTICAS =====")
    print(f"Total de projetos: {total}")
    print(f"Por iniciar: {por_iniciar}")
    print(f"Em desenvolvimento: {em_desenvolvimento}")
    print(f"Concluídos: {concluido}")


def guardar_ficheiro():
    try:
        with open(NOME_FICHEIRO, "w", encoding="utf-8") as ficheiro:
            json.dump(projetos, ficheiro, ensure_ascii=False, indent=4)
        print(f"Projetos guardados com sucesso em '{NOME_FICHEIRO}'.")
    except Exception as erro:
        print("Erro ao guardar ficheiro:", erro)


def carregar_ficheiro():
    global projetos, proximo_id

    try:
        with open(NOME_FICHEIRO, "r", encoding="utf-8") as ficheiro:
            projetos = json.load(ficheiro)

        if len(projetos) > 0:
            maior_id = 0
            for projeto in projetos:
                if projeto["id"] > maior_id:
                    maior_id = projeto["id"]
            proximo_id = maior_id + 1
        else:
            proximo_id = 1

        print(f"Projetos carregados com sucesso de '{NOME_FICHEIRO}'.")
    except FileNotFoundError:
        print(f"O ficheiro '{NOME_FICHEIRO}' ainda não existe.")
    except Exception as erro:
        print("Erro ao carregar ficheiro:", erro)


# Programa principal
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
        listar_por_estado()
        pausar()

    elif opcao == "7":
        mostrar_estatisticas()
        pausar()

    elif opcao == "8":
        guardar_ficheiro()
        pausar()

    elif opcao == "9":
        carregar_ficheiro()
        pausar()

    elif opcao == "0":
        print("A sair do programa...")
        break

    else:
        print("Opção inválida. Tente novamente.")
        pausar()