import json

# =========================================
# Moov-up - Sistema de Conversão de Pontos
# =========================================

ARQUIVO = "usuarios.json"

usuarios = []

taxas = {
    "energia": 0.05,
    "metro": 10,
    "trem": 10,
    "onibus": 8
}

postagens = {
    "foto": 5,
    "video": 15,
    "story": 3,
    "reels": 20
}


#abre o arquivo json que guarda a informação dos usuarios e def carregar_usuarios() --> busca no json se o usuario esta cadastrado no sistema

def salvar_usuarios():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)


def carregar_usuarios():
    global usuarios
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []

# função que busca e o usuario e checa se ele esta cadastrado no json 

def buscar_usuario(email):
    for usuario in usuarios:
        if usuario["email"] == email:
            return usuario
    return None

# Função para validar os caracteres do email, e retornar a o mesmo para inserir os caracteres corretos

def validar_email(email):
    if "@" not in email:
        return False

    partes = email.split("@")
    if len(partes) != 2:
        return False

    nome, dominio = partes
    if nome == "" or dominio == "":
        return False

    if "." not in dominio:
        return False

    return True



def escolher_numero(msg, minimo, maximo):
    while True:
        try:
            valor = int(input(msg))
            if minimo <= valor <= maximo:
                return valor
            print("Número inválido.")
        except:
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
        return usuarios
    finally:
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
    print("\nTipos de postagem:")
    tipos = list(postagens.keys())
    for i, tipo in enumerate(tipos, 1):
        print(f"[{i}] {tipo} (+{postagens[tipo]} pts)")
    opcao = escolher_numero("Escolha: ", 1, len(tipos))
    tipo = tipos[opcao - 1]
    qtd = escolher_numero("Quantidade (1-5): ", 1, 5)
    pontos = postagens[tipo] * qtd
    usuario["pontos"] += pontos
    usuario["historico"].append(
        f"{qtd}x {tipo} (+{pontos} pts)"
    )
    salvar_usuarios()
    print(f"Você ganhou {pontos} pontos!")


#funcao de alteracao de energia onde email e usuario sao inseridos e caso n encontrados na lista usuarios o usuario nao pode utilizar o progama, caso haja cadastro. Caso haja usuario o sistema continua normalmente, sistema verifica pontos dentra da estrutuira usuario onde seus pontos do site ficam armazenados,se pontos for = 0 retorna que voce ainda nao possui pontos. depois a funcao escolher_numero abre o usuario a requisicao para ele escolher os pontos 

def converter_passagem():
    email = input("Seu email: ")
    usuario = buscar_usuario(email)
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
    opcao = escolher_numero("Escolha: ", 1, len(modais))
    modal_escolhido = modais[opcao - 1]
    usar = escolher_numero(
        f"Quantos pontos deseja converter? (1-{pontos}): ",
        1,
        pontos
    )
    credito = usar / taxas[modal_escolhido]
    usuario["pontos"] -= usar
    salvar_usuarios()
    print(f"Crédito gerado: R$ {credito:.2f}")


#funcao feita para consultar o saldo do usuario, o mesmo pede o usuario e email para realizar o cadastro, print mostrando o nome inserido pelo e usuario e sua quantidade de pontos. E exibe seu historico de resgate atraves da estrutura for 
def consultar_saldo():
    email = input("Seu email: ").strip().lower()
    usuario = buscar_usuario(email)
    if not usuario:
        print("Usuário não encontrado.")
        return
    print(f"\nNome: {usuario['nome']}")
    print(f"Pontos: {usuario['pontos']}")
    print("\nHistórico:")
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
            case _:
                print("Opção inválida.")


#serve para sempre carregar o menu e o cadastro dos usuarios 

carregar_usuarios()
menu()

#Metas de melhorias do progama 
# - Melhorar sistema de cadastro ao usuario ou remover o mesmo 
# - focar mais na conversao de passgens 
# - integrar com o sistema de front-end 
# - limitar quantidade de postagens 
