# Sistema bancário com operações: sacar, depositar, visualizar extrato e gerenciar contas
saldo = float(300)
LIMITE_DIARIO = 3
contagem_saques = 0
LIMITE_SAQUES = 500
saque_extrato = {}
deposito_extrato = {}
contagem_p_saque = 1
contagem_p_deposito = 1
usuarios = []
contas = []
numero_sequencial_conta = 1
usuario_logado = ""
cpf_logado = ""

print("""
        BEM VINDO
           AO
      SANTANDER DIO      
""")

def saque(*, saldo, saque_extrato, LIMITE_DIARIO, numero_saques, LIMITE_SAQUES):
    valor = float(input(f"""
    ===== SAQUE =====
    
    Saldo da conta:
    R${saldo:.2f}
                
    Digite o valor desejado para saque: """))
    
    if numero_saques < LIMITE_DIARIO and valor <= saldo:
        if valor <= LIMITE_SAQUES:
            numero_saques += 1
            saldo -= valor
            saque_extrato[numero_saques] = valor
            print(f"Saldo atual: R${saldo:.2f}")
        else:
            print("Valor acima do limite por saque (R$ 500).")
    else:
        print("Limite diário de saques atingido ou saldo insuficiente.")
    return saldo, saque_extrato, numero_saques

def deposito(saldo, deposito_extrato, /, contagem_p_deposito):
    valor_deposito = float(input("Digite o valor do depósito: "))
    saldo += valor_deposito
    deposito_extrato[contagem_p_deposito] = valor_deposito
    contagem_p_deposito += 1
    print(f"Saldo disponível: R${saldo:.2f}")
    return saldo, deposito_extrato, contagem_p_deposito

def extrato(saldo, /, saque_extrato, deposito_extrato):
    opcao = int(input("""
    ======== Extrato ========
          
    1 - Saques
    2 - Depósito
    0 - SAIR
      
    (Digite o número da opção desejada)
      
    =========================  
          """))
    if opcao == 1:
        if not saque_extrato:
            print("Nenhum saque foi realizado")
        for numero, saque in saque_extrato.items():
            print(f"- {numero:.2f} - SACOU R${saque:.2f}")
    elif opcao == 2:
        if not deposito_extrato:
            print("Nenhum depósito foi realizado")
        for numero, deposito in deposito_extrato.items():
            print(f"- {numero} - DEPOSITOU R${deposito:.2f}")
    elif opcao == 0:
        return
    else:
        print("Valor inválido, tente novamente")
    print(f"\nSaldo disponivel: R${saldo:.2f} ")

def listar_minhas_contas(cpf_usuario):
    contas_do_usuario = [conta for conta in contas if conta["usuario"] == cpf_usuario]
    
    if not contas_do_usuario:
        print("\nNenhuma conta encontrada em seu nome.")
    else:
        print("\n=== SUAS CONTAS ===")
        for conta in contas_do_usuario:
            print(f"""
            Agência: {conta['fixo_agencia']}
            Número: {conta['numero_conta']}
            Titular: {conta['usuario']}
            """)

def cadastro(*, usuarios):
    while True:
        nome = input("Nome: ")
        if all(not texto.isalpha() for texto in nome.split()):
            print("Utilize apenas letras, TENTE NOVAMENTE")
        else:
            break

    while True:
        data = input("Data de nascimento ex(dd/mm/aaaa): ")
        if len(data) <= 8 and not data.isdigit():
            print("Inválido, TENTE NOVAMENTE(apenas numeros)")
        else:
            break

    while True:
        cpf = input("CPF: ")
        if not cpf.isdigit():
            print("Inválido, TENTE NOVAMENTE (apenas numeros)")
        elif any(u["cpf"] == cpf for u in usuarios):
            print("Esse CPF já está cadastrado. Tente outro.")
        else:
            break
     
    endereco = []
    while True:
        rua = input("Rua: ")
        if all(not texto.isalpha() for texto in rua.split()):
            print("Utilize apenas letras, TENTE NOVAMENTE")
        else:
            endereco.append(rua)
            break
    
    while True:
        numero = input("Numero: ")
        if not numero.isdigit():
                print("Utilize apenas números, TENTE NOVAMENTE")
        else:
            endereco.append(numero)
            break

    while True:
        bairro = input("Bairro: ")
        if all(not texto.isalpha() for texto in bairro.split()):
            print("Utilize apenas letras, TENTE NOVAMENTE")
        else:
            endereco.append(bairro)
            break

    while True:
        cidade = input("Cidade: ")
        if all(not texto.isalpha() for texto in cidade.split()):
            print("Utilize apenas letras, TENTE NOVAMENTE")
        else:
            endereco.append(cidade)
            break

    while True:
        uf = input("UF: ")
        if not uf.isalpha():
            print("Utilize apenas letras, TENTE NOVAMENTE")
        else:
            endereco.append(uf)
            break

    while True:
        cep = input("CEP: ")
        if not cep.isdigit():
            print("Utilize apenas números, TENTE NOVAMENTE")
        else:
            break
    
    usuario = {
        "nome": nome,
        "data": data,
        "cpf": cpf,
        "endereco": endereco
    }
    
    usuarios.append(usuario)
    return usuarios

def login(lista_usuarios):
    global usuario_logado, cpf_logado
    cpf = input("Digite seu CPF: ")
    
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            print(f"Bem-vindo, {usuario['nome']}!")
            usuario_logado = usuario["nome"]
            cpf_logado = usuario["cpf"]
            conta_corrente(usuario_logado=usuario_logado, contas=contas)
            return
    print("CPF não cadastrado.")

def conta_corrente(*, usuario_logado, contas):
    global numero_sequencial_conta, cpf_logado
    
    while True:    
        print("""
    ======== CONTA ========
    1 - Criar conta
    2 - Listar Minhas Contas
    0 - SAIR
        """)
        opcao = input("Opção:")
        if opcao == "1":
            fixo_agencia = "0001"
            numero_conta = numero_sequencial_conta
            numero_sequencial_conta += 1
            
            conta = {
                "fixo_agencia": fixo_agencia,
                "numero_conta": numero_conta,
                "usuario": cpf_logado
            }
            print(f"""
                  Conta cadastrada com Sucesso
                  {conta}
                  """)
            contas.append(conta)
        elif opcao == "2":
            listar_minhas_contas(cpf_logado)
        elif opcao == "0":
            break

def operacoes():
    global saldo, saque_extrato, contagem_saques, deposito_extrato, contagem_p_deposito, cpf_logado
    
    while True:
        print("""
    ======== MENU ========
    1 - Sacar
    2 - Depositar
    3 - Extrato
    4 - Minhas Contas
    0 - SAIR
        """)
        opcao = input("Opção: ")
        
        if opcao == "1":
            if saldo == 0:
                print("Não é possível sacar. Saldo: R$ 0.00")
            else:
                saldo, saque_extrato, contagem_saques = saque(
                    saldo=saldo,
                    saque_extrato=saque_extrato,
                    LIMITE_DIARIO=LIMITE_DIARIO,
                    numero_saques=contagem_saques,
                    LIMITE_SAQUES=LIMITE_SAQUES
                )
        elif opcao == "2":
            saldo, deposito_extrato, contagem_p_deposito = deposito(
                saldo, deposito_extrato, contagem_p_deposito
            )
        elif opcao == "3":
            extrato(saldo, saque_extrato=saque_extrato, deposito_extrato=deposito_extrato)
        elif opcao == "4":
            listar_minhas_contas(cpf_logado)
        elif opcao == "0":
            print("\nObrigado por usar o Santander DIO. Volte sempre!")
            break
        else:
            print("\nOpção inválida! Por favor, escolha uma opção de 1 a 4")

def main():
    global saldo, saque_extrato, contagem_saques, contagem_p_deposito, deposito_extrato, usuarios

    while True:
        print("""
    ======== MENU PRINCIPAL ========
    1 - Cadastro
    2 - Login
    0 - SAIR
        """)
        opcao = input("Opção: ")
        if opcao == "1":
           usuarios = cadastro(usuarios=usuarios)
        elif opcao == "2":
            login(usuarios)
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

main()