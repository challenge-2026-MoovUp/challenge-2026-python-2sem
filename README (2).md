# MOOV-UP — SoulUp

> Sistema de conversão de pontos (ganhos por postagens em redes sociais e, futuramente, por economia registrada em contas de energia elétrica) em passagens de transporte público.

## 👥 Integrantes

- Juan Souza Marques — RM573469
- Matheus Matsushita de Souza — RM570017
- Lucas Leite Carlos — RM571985
- Pedro Amaro Pires — RM570636


## 📑 Sumário

1. [Tema Geral](#-tema-geral)
2. [Solução Proposta](#-solução-proposta)
3. [Aderência ao Tema](#-aderência-ao-tema)
4. [Explicação do Código-Fonte](#-explicação-do-código-fonte)
5. [Casos de Execução](#-casos-de-execução)
6. [Como Executar](#-como-executar)

## 🎯 Tema Geral

Este projeto nasce de um *challenge* proposto pela SoulUp aos alunos da FIAP: desenvolver uma solução em Python para um sistema de conversão de pontos que a empresa já possui atualmente com base em contas de luz. O desafio consiste em ampliar esse sistema, permitindo que os pontos acumulados pelos usuários sejam também convertidos em passagens de transporte público (metrô, trem e ônibus), com uma taxa de conversão de **1 ponto = R$ 0,09**.

## 💡 Solução Proposta

O sistema desenvolvido em **Python** para o *challenge* permite que o usuário:

- Se cadastre na plataforma (CRUD completo de usuários, persistido em JSON);
- Ganhe pontos ao registrar postagens em redes sociais (foto, vídeo, story ou reels), cada uma com uma pontuação diferente;
- Converta os pontos acumulados em crédito para passagens de metrô, trem ou ônibus;
- Consulte, a qualquer momento, seu saldo de pontos e o histórico de movimentações.

Todos os dados são persistidos em um arquivo `usuarios.json`, carregado automaticamente ao iniciar o sistema.

## ✅ Aderência ao Tema

O código desenvolvido atende diretamente ao desafio proposto pela SoulUp por estender a lógica original de conversão de pontos — hoje restrita à economia registrada em contas de luz — para um novo eixo de recompensa: o engajamento do usuário em redes sociais, através da função registrar_postagem(), que converte fotos, vídeos, stories e reels em pontos.

Esses pontos, independentemente de sua origem, são armazenados em um saldo único por usuário (usuarios["pontos"]), o que já deixa o sistema preparado para futuramente somar também os pontos gerados pela economia de energia (representada no dicionário taxas["energia"]), unificando as duas fontes propostas pela SoulUp em uma única "moeda" de pontos.

A principal aderência ao tema, no entanto, está na função converter_passagem(), que transforma esse saldo acumulado em crédito real para transporte público (metrô, trem ou ônibus), seguindo a taxa de conversão de 1 ponto = R$ 0,09 definida no desafio. Dessa forma, a solução não apenas mantém a essência do sistema já existente da SoulUp, como amplia seu impacto: o usuário passa a ser recompensado tanto por hábitos sustentáveis (economia de energia) quanto por engajamento digital, podendo usar essa recompensa para se locomover de forma mais barata e incentivada, o que reforça a mobilidade sustentável proposta no desafio.

## 🧩 Explicação do Código-Fonte

O sistema está implementado em um único arquivo (`main.py`), organizado nas seguintes seções:

```
📄 main.py
├── Dados globais       # usuarios, taxas, postagens
├── Persistência        # salvar_usuarios, carregar_usuarios
├── Buscas e validações # buscar_usuario, validar_email, validar_nome, escolher_numero
├── CRUD de usuários    # cadastrar_usuario, listar_usuarios, consultar_usuario,
│                       # editar_usuario, excluir_usuario, menu_usuarios
├── Regras de negócio   # registrar_postagem, converter_passagem, consultar_saldo
└── menu()              # Menu principal da aplicação
```

**Dados globais**
- `usuarios`: lista de dicionários com `nome`, `email`, `pontos` e `historico` de cada usuário, pré-carregada com um usuário de exemplo (Ana Silva).
- `taxas`: dicionário com o valor de conversão de pontos por modal (`metro`: 10 pts, `trem`: 10 pts, `onibus`: 8 pts) e por energia (`energia`: 0.05).
- `postagens`: dicionário com a pontuação concedida por tipo de postagem (`foto`: 5, `video`: 15, `story`: 3, `reels`: 20).

**Persistência**
- `salvar_usuarios()`: grava a lista `usuarios` no arquivo `usuarios.json`, tratando erros de escrita/serialização (`OSError`, `TypeError`) e retornando `True`/`False` conforme o sucesso da operação.
- `carregar_usuarios()`: lê o JSON ao iniciar o programa; se o arquivo não existir ou estiver corrompido, cria um novo a partir da lista padrão.

**Buscas e validações**
- `buscar_usuario(email)`: procura um usuário pelo e-mail (case-insensitive).
- `validar_email(email)` / `validar_nome(nome)`: validam formato de e-mail (usuário, `@` e domínio com ponto) e nome (apenas letras e espaços).
- `escolher_numero(msg, minimo, maximo)`: solicita repetidamente um número inteiro dentro de um intervalo válido, tratando entradas não numéricas.

**CRUD de usuários** (`menu_usuarios`)
- `cadastrar_usuario()`: valida nome/e-mail, impede e-mails duplicados e persiste o novo usuário, com `try/except/else/finally` para desfazer o cadastro em caso de falha ao salvar.
- `listar_usuarios()`, `consultar_usuario()`: exibem os usuários cadastrados e os dados de um usuário específico.
- `editar_usuario()`: permite alterar nome e/ou e-mail, validando os novos dados e revertendo a alteração caso a gravação no JSON falhe.
- `excluir_usuario()`: remove um usuário após confirmação, restaurando o registro caso a gravação falhe.

**Regras de negócio**
- `registrar_postagem()`: soma pontos ao usuário conforme o tipo e a quantidade de postagens informadas, e registra o ganho no histórico.
- `converter_passagem()`: converte uma quantidade de pontos escolhida pelo usuário em crédito de transporte, de acordo com a taxa do modal selecionado.
- `consultar_saldo()`: exibe o saldo atual de pontos e todo o histórico de movimentações do usuário.

**Menu principal**
- `menu()`: laço principal que direciona para o submenu de usuários, registro de postagens, conversão de passagens e consulta de saldo, até que o usuário escolha sair.

## ▶️ Casos de Execução

**Caso 1 — Cadastro de usuário**
```
Entrada:
  Nome: Joao Pedro
  E-mail: joao.pedro@exemplo.com

Saída esperada:
  Usuário cadastrado com sucesso!
  Tentativa de cadastro finalizada.
```

**Caso 2 — Registro de postagem e acúmulo de pontos**
```
Entrada:
  Seu e-mail: joao.pedro@exemplo.com
  Tipo de postagem: [2] video (+15 pts)
  Quantidade: 3

Saída esperada:
  Você ganhou 45 pontos!
```

**Caso 3 — Conversão de pontos em passagem**
```
Entrada:
  Seu e-mail: joao.pedro@exemplo.com
  Tipo de transporte: [1] metro (10 pts = R$ 1,00)
  Quantos pontos deseja converter? (1-45): 30

Saída esperada:
  Crédito gerado: R$ 3.00
```

**Caso 4 — Consulta de saldo e histórico**
```
Entrada:
  Seu e-mail: joao.pedro@exemplo.com

Saída esperada:
  Nome: Joao Pedro
  Pontos: 15

  Histórico:
  - 3x video (+45 pts)
```

## ⚙️ Como Executar

```bash
python moovup.py
```

Pré-requisitos: Python 3.x instalado. Nenhuma biblioteca externa é necessária (apenas o módulo `json`, nativo do Python). Ao rodar pela primeira vez, o arquivo `usuarios.json` é criado automaticamente.
