import json

ARQUIVO = "usuarios.json"

usuarios = [
    {"nome": "Ana Silva", "email": "ana.silva@exemplo.com", "pontos": 0, "historico": []}
]
taxas = {"energia": 0.05, "metro": 10, "trem": 10, "onibus": 8}
postagens = {"foto": 5, "video": 15, "story": 3, "reels": 20}


def salvar_usuarios():
    """Persiste usuários no JSON.

    Não recebe parâmetros. Retorna ``True`` se gravar os dados e ``False`` em
    caso de erro de arquivo ou de serialização.
    """
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except (OSError, TypeError) as erro:
        print(f"Erro ao salvar os usuários: {erro}")
        return False
    else:
        return True
    finally:
        # O bloco with fecha o arquivo mesmo se ocorrer uma exceção.
        pass


def carregar_usuarios():
    """Carrega os usuários do JSON ou cria o arquivo se ele não existir.

    Não recebe parâmetros nem retorna valor; atualiza a lista global
    ``usuarios``.
    """
    global usuarios
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        salvar_usuarios()


def buscar_usuario(email):
    """Busca um usuário pelo e-mail, ignorando letras maiúsculas.

    Args:
        email (str): E-mail a pesquisar.

    Returns:
        dict | None: Usuário encontrado ou ``None``.
    """
    for usuario in usuarios:
        if usuario["email"].lower() == email.lower():
            return usuario
    return None


def validar_email(email):
    """Valida se um e-mail possui usuário, @ e domínio com ponto.

    Args:
        email (str): E-mail a validar.

    Returns:
        bool: ``True`` se for válido; caso contrário, ``False``.
    """
    if "@" not in email:
        return False
    nome, *dominios = email.split("@")
    return len(dominios) == 1 and bool(nome) and "." in dominios[0]


def validar_nome(nome):
    """Valida um nome composto somente por letras e espaços.

    Args:
        nome (str): Nome a validar.

    Returns:
        bool: ``True`` se for válido; caso contrário, ``False``.
    """
    return bool(nome) and all(parte.isalpha() for parte in nome.split())


def escolher_numero(msg, minimo, maximo):
    """Solicita um número inteiro dentro de um intervalo.

    Args:
        msg (str): Mensagem exibida ao usuário.
        minimo (int): Menor valor aceito.
        maximo (int): Maior valor aceito.

    Returns:
        int: Número válido informado.
    """
    while True:
        try:
            valor = int(input(msg))
            if minimo <= valor <= maximo:
                return valor
            print("Número inválido.")
        except ValueError:
            print("Digite apenas números.")


def cadastrar_usuario():
    """Cadastra um usuário com nome e e-mail válidos.

    Não recebe parâmetros nem retorna valor. Solicita dados no terminal e
    persiste o novo usuário no JSON.
    """
    print("\n--- Cadastrar usuário ---")
    try:
        nome = input("Nome: ").strip().title()
        if not validar_nome(nome):
            raise ValueError("Nome inválido. Use somente letras e espaços.")
        email = input("E-mail: ").strip().lower()
        if not validar_email(email):
            raise ValueError("E-mail inválido.")
        if buscar_usuario(email):
            raise ValueError("E-mail já cadastrado.")

        usuarios.append({"nome": nome, "email": email, "pontos": 0, "historico": []})
        if not salvar_usuarios():
            usuarios.pop()
            raise OSError("Não foi possível gravar o cadastro no arquivo.")
    except ValueError as erro:
        print(f"Erro no cadastro: {erro}")
    except OSError as erro:
        print(f"Erro no cadastro: {erro}")
    except Exception as erro:
        print(f"Erro inesperado no cadastro: {erro}")
    else:
        print("Usuário cadastrado com sucesso!")
    finally:
        print("Tentativa de cadastro finalizada.")


def listar_usuarios():
    """Exibe todos os usuários cadastrados.

    Não recebe parâmetros nem retorna valor.
    """
    print("\n--- Usuários cadastrados ---")
    if not usuarios:
        print("Não há usuários cadastrados.")
        return
    for indice, usuario in enumerate(usuarios, 1):
        print(f"{indice} - {usuario['nome']} | {usuario['email']} | {usuario['pontos']} pontos")


def consultar_usuario():
    """Exibe os dados de um usuário encontrado pelo e-mail.

    Não recebe parâmetros nem retorna valor; solicita o e-mail no terminal.
    """
    email = input("E-mail do usuário: ").strip()
    usuario = buscar_usuario(email)
    if not usuario:
        print("Usuário não encontrado.")
        return
    print(f"Nome: {usuario['nome']}")
    print(f"E-mail: {usuario['email']}")
    print(f"Pontos: {usuario['pontos']}")


def editar_usuario():
    """Altera nome e/ou e-mail de um usuário.

    Não recebe parâmetros nem retorna valor. Valida os dados e persiste a
    alteração no arquivo JSON.
    """
    print("\n--- Editar usuário ---")
    try:
        usuario = buscar_usuario(input("E-mail atual: ").strip())
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        novo_nome = input(f"Novo nome [{usuario['nome']}]: ").strip()
        novo_email = input(f"Novo e-mail [{usuario['email']}]: ").strip().lower()
        if novo_nome and not validar_nome(novo_nome):
            raise ValueError("Nome inválido. Use somente letras e espaços.")
        if novo_email and not validar_email(novo_email):
            raise ValueError("E-mail inválido. Nenhuma alteração foi salva.")
        if novo_email:
            outro_usuario = buscar_usuario(novo_email)
            if outro_usuario and outro_usuario is not usuario:
                raise ValueError("E-mail já cadastrado. Nenhuma alteração foi salva.")

        dados_anteriores = usuario.copy()
        if novo_nome:
            usuario["nome"] = novo_nome.title()
        if novo_email:
            usuario["email"] = novo_email
        if not salvar_usuarios():
            usuario.update(dados_anteriores)
            raise OSError("Não foi possível gravar a alteração no arquivo.")
    except ValueError as erro:
        print(f"Erro na alteração: {erro}")
    except OSError as erro:
        print(f"Erro na alteração: {erro}")
    except Exception as erro:
        print(f"Erro inesperado na alteração: {erro}")
    else:
        print("Usuário atualizado com sucesso!")
    finally:
        print("Tentativa de alteração finalizada.")


def excluir_usuario():
    """Exclui um usuário após confirmação.

    Não recebe parâmetros nem retorna valor. Solicita e-mail e confirmação no
    terminal e persiste a exclusão no arquivo JSON.
    """
    print("\n--- Excluir usuário ---")
    try:
        usuario = buscar_usuario(input("E-mail do usuário: ").strip())
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        if input(f"Excluir {usuario['nome']}? (S/N): ").strip().upper() != "S":
            print("Exclusão cancelada.")
            return

        indice = usuarios.index(usuario)
        usuarios.remove(usuario)
        if not salvar_usuarios():
            usuarios.insert(indice, usuario)
            raise OSError("Não foi possível gravar a exclusão no arquivo.")
    except ValueError as erro:
        print(f"Erro na exclusão: {erro}")
    except OSError as erro:
        print(f"Erro na exclusão: {erro}")
    except Exception as erro:
        print(f"Erro inesperado na exclusão: {erro}")
    else:
        print("Usuário excluído com sucesso!")
    finally:
        print("Tentativa de exclusão finalizada.")


def menu_usuarios():
    """Exibe e controla o submenu das operações CRUD de usuários.

    Não recebe parâmetros nem retorna valor.
    """
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
    """Registra postagens e adiciona seus pontos ao usuário.

    Não recebe parâmetros nem retorna valor. Solicita e-mail, tipo e quantidade,
    atualiza saldo e histórico e salva os dados.
    """
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
    """Converte pontos de um usuário em crédito de transporte.

    Não recebe parâmetros nem retorna valor. Solicita e-mail, modal e pontos,
    atualiza o saldo e exibe o crédito gerado.
    """
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
    """Exibe saldo e histórico de movimentações do usuário.

    Não recebe parâmetros nem retorna valor; solicita o e-mail no terminal.
    """
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
    """Exibe e controla o menu principal da aplicação.

    Não recebe parâmetros nem retorna valor.
    """
    while True:
        print("\n===== MOVE-UP =====")
        print("1 - Configurações de usuário")
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


carregar_usuarios()
menu()
