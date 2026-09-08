import json

ARQUIVO = "usuarios.json"

# Cadastro inicial solicitado; será gravado em usuarios.json na primeira execução.
usuarios = [
    {"nome": "Ana Silva", "email": "ana.silva@exemplo.com", "pontos": 0, "historico": []}
]

taxas = {"energia": 0.05, "metro": 10, "trem": 10, "onibus": 8}
postagens = {"foto": 5, "video": 15, "story": 3, "reels": 20}


def salvar_usuarios():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)


def carregar_usuarios():
    global usuarios
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        salvar_usuarios()


def buscar_usuario(email):
    for usuario in usuarios:
        if usuario["email"].lower() == email.lower():
            return usuario
    return None


def validar_email(email):
    if "@" not in email:
        return False
    nome, *dominios = email.split("@")
    return len(dominios) == 1 and bool(nome) and "." in dominios[0]


def validar_nome(nome):
    """Aceita somente letras (inclusive acentuadas) e espaços."""
    return bool(nome) and all(parte.isalpha() for parte in nome.split())


def escolher_numero(msg, minimo, maximo):
    while True:
        try:
            valor = int(input(msg))
            if minimo <= valor <= maximo:
                return valor
            print("Número inválido.")
        except ValueError:
            print("Digite apenas números.")


# CREATE
def cadastrar_usuario():
    print("\n--- Cadastrar usuário ---")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    if not validar_nome(nome):
        print("Nome inválido. Use somente letras e espaços.")
    elif not validar_email(email):
        print("E-mail inválido.")
    elif buscar_usuario(email):
        print("E-mail já cadastrado.")
    else:
        usuarios.append({"nome": nome, "email": email, "pontos": 0, "historico": []})
        salvar_usuarios()
        print("Usuário cadastrado com sucesso!")


# READ
def listar_usuarios():
    print("\n--- Usuários cadastrados ---")
    if not usuarios:
        print("Não há usuários cadastrados.")
        return
    for indice, usuario in enumerate(usuarios, 1):
        print(f"{indice} - {usuario['nome']} | {usuario['email']} | {usuario['pontos']} pontos")


def consultar_usuario():
    email = input("E-mail do usuário: ").strip()
    usuario = buscar_usuario(email)
    if not usuario:
        print("Usuário não encontrado.")
        return
    print(f"Nome: {usuario['nome']}")
    print(f"E-mail: {usuario['email']}")
    print(f"Pontos: {usuario['pontos']}")


# UPDATE
def editar_usuario():
    print("\n--- Editar usuário ---")
    usuario = buscar_usuario(input("E-mail atual: ").strip())
    if not usuario:
        print("Usuário não encontrado.")
        return
    novo_nome = input(f"Novo nome [{usuario['nome']}]: ").strip()
    novo_email = input(f"Novo e-mail [{usuario['email']}]: ").strip().lower()
    if novo_nome and not validar_nome(novo_nome):
        print("Nome inválido. Use somente letras e espaços.")
        return
    if novo_email:
        if not validar_email(novo_email):
            print("E-mail inválido. Nenhuma alteração foi salva.")
            return
        outro_usuario = buscar_usuario(novo_email)
        if outro_usuario and outro_usuario is not usuario:
            print("E-mail já cadastrado. Nenhuma alteração foi salva.")
            return
    if novo_nome:
        usuario["nome"] = novo_nome
    if novo_email:
        usuario["email"] = novo_email
    salvar_usuarios()
    print("Usuário atualizado com sucesso!")


# DELETE
def excluir_usuario():
    print("\n--- Excluir usuário ---")
    usuario = buscar_usuario(input("E-mail do usuário: ").strip())
    if not usuario:
        print("Usuário não encontrado.")
        return
    if input(f"Excluir {usuario['nome']}? (S/N): ").strip().upper() == "S":
        usuarios.remove(usuario)
        salvar_usuarios()
        print("Usuário excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


def menu_usuarios():
    """Submenu CRUD acessado ao selecionar 'Cadastrar usuário'."""
    while True:
        print("\n===== CRUD DE USUÁRIOS =====")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Consultar usuário")
        print("4 - Editar usuário")
        print("5 - Excluir usuário")
        print("0 - Voltar ao menu principal")
        match input("Insira sua opção: ").strip():
            case "1": cadastrar_usuario()
            case "2": listar_usuarios()
            case "3": consultar_usuario()
            case "4": editar_usuario()
            case "5": excluir_usuario()
            case "0": break
            case _: print("Opção inválida.")


def registrar_postagem():
    usuario = buscar_usuario(input("Seu e-mail: ").strip())
    if not usuario:
        print("Usuário não encontrado.")
        return
    tipos = list(postagens)
    print("\nTipos de postagem:")
    for i, tipo in enumerate(tipos, 1):
        print(f"[{i}] {tipo} (+{postagens[tipo]} pts)")
    tipo = tipos[escolher_numero("Escolha: ", 1, len(tipos)) - 1]
    qtd = escolher_numero("Quantidade (1-5): ", 1, 5)
    pontos = postagens[tipo] * qtd
    usuario["pontos"] += pontos
    usuario["historico"].append(f"{qtd}x {tipo} (+{pontos} pts)")
    salvar_usuarios()
    print(f"Você ganhou {pontos} pontos!")


def converter_passagem():
    usuario = buscar_usuario(input("Seu e-mail: ").strip())
    if not usuario:
        print("Usuário não encontrado.")
        return
    pontos = usuario["pontos"]
    if pontos == 0:
        print("Sem pontos.")
        return
    modais = ["metro", "trem", "onibus"]
    print("\nTipo de transporte:")
    for i, modal in enumerate(modais, 1):
        print(f"[{i}] {modal} ({taxas[modal]} pts = R$ 1,00)")
    modal = modais[escolher_numero("Escolha: ", 1, len(modais)) - 1]
    usar = escolher_numero(f"Quantos pontos deseja converter? (1-{pontos}): ", 1, pontos)
    usuario["pontos"] -= usar
    salvar_usuarios()
    print(f"Crédito gerado: R$ {usar / taxas[modal]:.2f}")


def consultar_saldo():
    usuario = buscar_usuario(input("Seu e-mail: ").strip())
    if not usuario:
        print("Usuário não encontrado.")
        return
    print(f"\nNome: {usuario['nome']}\nPontos: {usuario['pontos']}\n\nHistórico:")
    if not usuario["historico"]:
        print("Nenhuma movimentação.")
    for item in usuario["historico"]:
        print("-", item)


def menu():
    while True:
        print("\n===== MOVE-UP =====")
        print("1 - Cadastrar usuário")
        print("2 - Registrar postagem")
        print("3 - Converter passagem")
        print("4 - Consultar saldo")
        print("0 - Sair")
        match input("Insira sua opção: ").strip():
            case "1": menu_usuarios()
            case "2": registrar_postagem()
            case "3": converter_passagem()
            case "4": consultar_saldo()
            case "0":
                print("Saindo...")
                break
            case _: print("Opção inválida.")

if __name__ == "__main__":
    carregar_usuarios()
    menu()
