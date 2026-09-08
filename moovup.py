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

# Funcao que guarda o cadastro feito pelo usuario, e depois aplica na lista usuarios[] e depois coloca no json 


def cadastrar_usuario(usuarios, nome, email):
    try:
        if nome.strip() == "":
            raise ValueError("Nome não pode ser vazio.")
        if not validar_email(email):
            raise ValueError("Email inválido.")
        if buscar_usuario(usuarios, email):
            raise ValueError("Email já cadastrado.")
 
        usuarios.append({
            "nome": nome,
            "email": email,
            "pontos": 0,
            "historico": []
        })
    except ValueError as erro:
        print(f"Erro: {erro}")
        return usuarios
    else:
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

def editar_usuario():
    try:
        usuario = buscar_usuario(usuarios, email_atual)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if novo_email != email_atual:
            if not validar_email(novo_email):
                raise ValueError("Novo email inválido.")
            if buscar_usuario(usuarios, novo_email):
                raise ValueError("Esse email já pertence a outro usuário.")

        usuario["nome"] = novo_nome
        usuario["email"] = novo_email

    except ValueError as erro:
        print(f"Erro: {erro}")
        return usuarios
    else:
        print("Usuário atualizado com sucesso!")
        return usuarios
    finally:
        salvar_usuarios()

def mostrar_saldo():
    email = input("Seu email: ").strip().lower()
    usuario = buscar_usuario(email)
    if not usuario:
        print("Usuário não encontrado.")
        return



# Função que registra as postagens feitas pelos usuarios e converte em pontos que estão guardados em uma tupla

def registrar_postagem():
    email = input("Seu email: ").strip().lower()
    usuario = buscar_usuario(email)
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
    email = input("Seu email: ").strip().lower()
    usuario = buscar_usuario(email)
    if not usuario:
        print("Usuário não encontrado.")
        return
    print(f"\nNome: {usuario['nome']}\nPontos: {usuario['pontos']}\n\nHistórico:")
    if not usuario["historico"]:
        print("Nenhuma movimentação.")
    for item in usuario["historico"]:
        print("-", item)


#funcao do menu feito para interacao do usuario, atraves do match case. case_ utilizado caso o usuario digite uma opcao invalida e case 0 para sair do progama. c
def menu_crud():
    print("\n===== Menu de usuario =====")
    print("1 - Cadastrar usuario")
    print("2 - mostrar o saldo atual do usuario")
    print("3 - Editar o usuario")
    print("4 - Deletar conta")
    print("0 - Voltar ao menu principal")
    op_crud = input("Insira sua opção: ")
    match op_crud:
        case "1":
            cadastrar_usuario()
        case "2":
            mostrar_saldo()
        case "3":
            editar_usuario()
        case "4":
            deletar_usuario()
        case "0":
            return menu()

def menu():
    while True:
        print("\n===== MOVE-UP =====")
        print("1 - CRUD de usuarios (nome temporário)")
        print("2 - Registrar postagem")
        print("3 - Converter passagem")
        print("4 - Consultar saldo")
        print("0 - Sair")
        op = input("Insira sua opção: ")
        match op:
            case "1":
                menu_crud()
            case "2":
                registrar_postagem()
            case "3":
                 converter_passagem()
            case "4":
                consultar_saldo()
            case "0":
                print("Saindo...")
                break
            case _: print("Opção inválida.")

if __name__ == "__main__":
    carregar_usuarios()
    menu()
