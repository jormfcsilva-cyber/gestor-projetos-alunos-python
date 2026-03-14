import json

projetos = []
proximo_id = 1


def mostrar_menu():
    print("\n===== GESTOR DE PROJETOS DE ALUNOS =====")
    print("1 - Adicionar projeto")
    print("2 - Listar projetos")
    print("3 - Pesquisar projeto por aluno")
    print("4 - Alterar estado do projeto")
    print("5 - Guardar projetos em ficheiro")
    print("6 - Carregar projetos do ficheiro")
    print("7 - Sair")


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

    aluno = input("Nome do aluno: ")
    turma = input("Turma: ")
    titulo = input("Título do projeto: ")
    tipo = input("Tipo de projeto (PAP / Trabalho / Outro): ")
    data_inicio = input("Data de início: ")
    estado = escolher_estado()
    observacoes = input("Observações: ")

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

    print("Projeto adicionado com sucesso.")


def listar_projetos():
    if len(projetos) == 0:
        print("Não existem projetos registados.")
    else:
        print("\n===== LISTA DE PROJETOS =====")
        for projeto in projetos:
            print(f"ID: {projeto['id']}")
            print(f"Aluno: {projeto['aluno']}")
            print(f"Turma: {projeto['turma']}")
            print(f"Título: {projeto['titulo']}")
            print(f"Tipo: {projeto['tipo']}")
            print(f"Data de início: {projeto['data_inicio']}")
            print(f"Estado: {projeto['estado']}")
            print(f"Observações: {projeto['observacoes']}")
            print("-" * 40)


def pesquisar_projeto():
    nome = input("Introduza o nome do aluno a pesquisar: ")
    encontrou = False

    for projeto in projetos:
        if projeto["aluno"].lower() == nome.lower():
            print("\nProjeto encontrado:")
            print(f"ID: {projeto['id']}")
            print(f"Aluno: {projeto['aluno']}")
            print(f"Turma: {projeto['turma']}")
            print(f"Título: {projeto['titulo']}")
            print(f"Tipo: {projeto['tipo']}")
            print(f"Data de início: {projeto['data_inicio']}")
            print(f"Estado: {projeto['estado']}")
            print(f"Observações: {projeto['observacoes']}")
            print("-" * 40)
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

    encontrou = False

    for projeto in projetos:
        if projeto["id"] == id_projeto:
            print(f"Projeto encontrado: {projeto['titulo']}")
            projeto["estado"] = escolher_estado()
            print("Estado atualizado com sucesso.")
            encontrou = True
            break

    if not encontrou:
        print("Projeto não encontrado.")


def guardar_ficheiro():
    try:
        with open("projetos.json", "w", encoding="utf-8") as ficheiro:
            json.dump(projetos, ficheiro, ensure_ascii=False, indent=4)
        print("Projetos guardados com sucesso em 'projetos.json'.")
    except Exception as erro:
        print("Erro ao guardar ficheiro:", erro)


def carregar_ficheiro():
    global projetos, proximo_id

    try:
        with open("projetos.json", "r", encoding="utf-8") as ficheiro:
            projetos = json.load(ficheiro)

        if len(projetos) > 0:
            maior_id = 0
            for projeto in projetos:
                if projeto["id"] > maior_id:
                    maior_id = projeto["id"]
            proximo_id = maior_id + 1
        else:
            proximo_id = 1

        print("Projetos carregados com sucesso.")
    except FileNotFoundError:
        print("O ficheiro 'projetos.json' ainda não existe.")
    except Exception as erro:
        print("Erro ao carregar ficheiro:", erro)


# Programa principal
while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_projeto()
    elif opcao == "2":
        listar_projetos()
    elif opcao == "3":
        pesquisar_projeto()
    elif opcao == "4":
        alterar_estado()
    elif opcao == "5":
        guardar_ficheiro()
    elif opcao == "6":
        carregar_ficheiro()
    elif opcao == "7":
        print("A sair do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")