# Projeto Final Python
# Gestor de Projetos de Alunos (PAP / Trabalhos)

projetos = []
proximo_id = 1


def mostrar_menu():
    print("\n===== GESTOR DE PROJETOS DE ALUNOS =====")
    print("1 - Adicionar projeto")
    print("2 - Listar projetos")
    print("3 - Pesquisar projeto por aluno")
    print("4 - Alterar estado do projeto")
    print("5 - Sair")


def adicionar_projeto():
    global proximo_id

    aluno = input("Nome do aluno: ")
    turma = input("Turma: ")
    titulo = input("Título do projeto: ")
    tipo = input("Tipo de projeto (PAP / Trabalho / Outro): ")
    data_inicio = input("Data de início: ")
    estado = input("Estado do projeto: ")
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
            encontrou = True

    if not encontrou:
        print("Não foi encontrado nenhum projeto para esse aluno.")


def alterar_estado():
    id_projeto = int(input("Introduza o ID do projeto: "))
    novo_estado = input("Novo estado do projeto: ")
    encontrou = False

    for projeto in projetos:
        if projeto["id"] == id_projeto:
            projeto["estado"] = novo_estado
            print("Estado atualizado com sucesso.")
            encontrou = True

    if not encontrou:
        print("Projeto não encontrado.")


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
        print("A sair do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")