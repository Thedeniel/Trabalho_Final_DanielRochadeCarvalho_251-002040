from collections import deque

ARQUIVO = "dados_sistema.txt"

# Estruturas em memória. O sistema sempre começa vazio.
leitores = []          # Lista: cadastro de leitores
reservas = deque()     # Fila: quem espera por um livro (entra no fim, sai do início)
devolvidos = []        # Pilha: o topo é o último elemento da lista
acervo = {}            # Árvore: dicionários aninhados, cada chave é uma área


# ---------------------------------------------------------------
# Entrada de dados
# ---------------------------------------------------------------

def ler_texto(mensagem):
    # O pipe é o separador do arquivo, então não pode aparecer dentro de um campo
    while True:
        texto = input(mensagem).strip().replace("|", "-")
        if texto:
            return texto
        print("Esse campo não pode ficar vazio.")


def ler_inteiro(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        return None


def nome_do_leitor(matricula):
    leitor = buscar_leitor(matricula)
    if leitor is None:
        return "(leitor removido)"
    return leitor["nome"]


# ---------------------------------------------------------------
# LISTA - leitores
# ---------------------------------------------------------------

def buscar_leitor(matricula):
    for leitor in leitores:
        if leitor["matricula"] == matricula:
            return leitor
    return None


def cadastrar_leitor():
    matricula = ler_texto("Matrícula: ")
    if buscar_leitor(matricula) is not None:
        print("Já existe um leitor com essa matrícula.")
        return
    nome = ler_texto("Nome: ")
    curso = ler_texto("Curso ou vínculo: ")
    leitores.append({"matricula": matricula, "nome": nome, "curso": curso})
    print("Leitor cadastrado.")


def listar_leitores():
    if not leitores:
        print("Nenhum leitor cadastrado.")
        return
    for i, leitor in enumerate(leitores, start=1):
        print(f"{i}. [{leitor['matricula']}] {leitor['nome']} - {leitor['curso']}")


def atualizar_leitor():
    leitor = buscar_leitor(ler_texto("Matrícula do leitor: "))
    if leitor is None:
        print("Leitor não encontrado.")
        return
    print("Deixe em branco o que não quiser mudar.")
    novo_nome = input(f"Nome ({leitor['nome']}): ").strip().replace("|", "-")
    novo_curso = input(f"Curso ({leitor['curso']}): ").strip().replace("|", "-")
    if novo_nome:
        leitor["nome"] = novo_nome
    if novo_curso:
        leitor["curso"] = novo_curso
    print("Cadastro atualizado.")


def remover_leitor():
    matricula = ler_texto("Matrícula do leitor a remover: ")
    leitor = buscar_leitor(matricula)
    if leitor is None:
        print("Leitor não encontrado.")
        return
    # Quem ainda está na fila não pode sumir, senão a reserva fica sem dono
    for reserva in reservas:
        if reserva["matricula"] == matricula:
            print("Esse leitor ainda tem reserva na fila. Atenda ou ajuste a reserva antes.")
            return
    leitores.remove(leitor)
    print("Leitor removido.")


def menu_leitores():
    while True:
        print("\n--- Leitores ---")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Atualizar")
        print("4. Remover")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadastrar_leitor()
        elif opcao == "2":
            listar_leitores()
        elif opcao == "3":
            atualizar_leitor()
        elif opcao == "4":
            remover_leitor()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# FILA - reservas de exemplares
# ---------------------------------------------------------------

def reservar_livro():
    matricula = ler_texto("Matrícula do leitor: ")
    if buscar_leitor(matricula) is None:
        print("Leitor não cadastrado.")
        return
    titulo = ler_texto("Título do livro: ")
    for reserva in reservas:
        if reserva["matricula"] == matricula and reserva["titulo"].lower() == titulo.lower():
            print("Esse leitor já está na fila desse livro.")
            return
    reservas.append({"matricula": matricula, "titulo": titulo})  # sempre no fim
    print(f"Reserva feita. Posição na fila: {len(reservas)}")


def listar_reservas():
    if not reservas:
        print("Fila de reservas vazia.")
        return
    for posicao, reserva in enumerate(reservas, start=1):
        print(f"{posicao}. {reserva['titulo']} - {nome_do_leitor(reserva['matricula'])} ({reserva['matricula']})")


def atender_reserva():
    if not reservas:
        print("Não há reservas para atender.")
        return
    reserva = reservas.popleft()  # só quem está há mais tempo sai
    print(f"Atendido: {reserva['titulo']} para {nome_do_leitor(reserva['matricula'])}.")


def corrigir_reserva():
    if not reservas:
        print("Fila de reservas vazia.")
        return
    listar_reservas()
    posicao = ler_inteiro("Posição da reserva: ")
    if posicao is None or posicao < 1 or posicao > len(reservas):
        print("Posição inválida.")
        return
    novo_titulo = ler_texto("Novo título: ")
    # Só troca o título, a ordem da fila continua a mesma
    reservas[posicao - 1]["titulo"] = novo_titulo
    print("Reserva corrigida.")


def menu_reservas():
    while True:
        print("\n--- Fila de reservas ---")
        print("1. Reservar livro (entrar no fim da fila)")
        print("2. Listar fila")
        print("3. Atender próxima reserva")
        print("4. Corrigir título de uma reserva")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            reservar_livro()
        elif opcao == "2":
            listar_reservas()
        elif opcao == "3":
            atender_reserva()
        elif opcao == "4":
            corrigir_reserva()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# PILHA - livros devolvidos aguardando a estante
# ---------------------------------------------------------------

def registrar_devolucao():
    matricula = ler_texto("Matrícula de quem devolveu: ")
    if buscar_leitor(matricula) is None:
        print("Leitor não cadastrado.")
        return
    titulo = ler_texto("Título do livro: ")
    devolvidos.append({"titulo": titulo, "matricula": matricula})  # vai para o topo
    print("Livro colocado no topo da pilha.")


def ver_topo():
    if not devolvidos:
        print("Pilha vazia.")
        return
    livro = devolvidos[-1]
    print(f"Topo: {livro['titulo']} (devolvido por {nome_do_leitor(livro['matricula'])})")


def listar_devolvidos():
    if not devolvidos:
        print("Pilha vazia.")
        return
    print("(do topo para a base)")
    for i, livro in enumerate(reversed(devolvidos), start=1):
        print(f"{i}. {livro['titulo']} - {nome_do_leitor(livro['matricula'])}")


def corrigir_topo():
    if not devolvidos:
        print("Pilha vazia.")
        return
    # Numa pilha só se mexe no topo, então a correção também é só nele
    print(f"Título atual do topo: {devolvidos[-1]['titulo']}")
    devolvidos[-1]["titulo"] = ler_texto("Título correto: ")
    print("Topo corrigido.")


def guardar_na_estante():
    if not devolvidos:
        print("Não há livros para guardar.")
        return
    livro = devolvidos.pop()  # tira sempre o último que entrou
    print(f"Pode levar para a estante: {livro['titulo']}")


def menu_devolvidos():
    while True:
        print("\n--- Pilha de devolvidos ---")
        print("1. Registrar devolução")
        print("2. Ver topo")
        print("3. Listar pilha")
        print("4. Corrigir título do topo")
        print("5. Guardar livro do topo na estante")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            registrar_devolucao()
        elif opcao == "2":
            ver_topo()
        elif opcao == "3":
            listar_devolvidos()
        elif opcao == "4":
            corrigir_topo()
        elif opcao == "5":
            guardar_na_estante()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# ÁRVORE - acervo por áreas do conhecimento
# ---------------------------------------------------------------

def pedir_caminho(mensagem):
    # Caminho digitado assim: Ciências Exatas/Computação/Algoritmos
    texto = input(mensagem).replace("|", "-")
    return [parte.strip() for parte in texto.split("/") if parte.strip()]


def localizar_pai(partes):
    # Devolve o dicionário que contém o último nome do caminho, ou None se não existir
    if not partes:
        return None
    no = acervo
    for parte in partes[:-1]:
        if parte not in no:
            return None
        no = no[parte]
    if partes[-1] not in no:
        return None
    return no


def contar_nos(no):
    total = 0
    for filhos in no.values():
        total += 1 + contar_nos(filhos)
    return total


def inserir_area():
    partes = pedir_caminho("Caminho completo (use / entre os níveis): ")
    if not partes:
        print("Caminho vazio.")
        return
    no = acervo
    criadas = 0
    for parte in partes:
        if parte not in no:
            no[parte] = {}
            criadas += 1
        no = no[parte]
    if criadas == 0:
        print("Esse caminho já existia.")
    else:
        print(f"{criadas} área(s) nova(s) criada(s).")


def mostrar_arvore(no, nivel=0):
    for nome in sorted(no):
        print("    " * nivel + "- " + nome)
        mostrar_arvore(no[nome], nivel + 1)


def listar_acervo():
    if not acervo:
        print("Acervo vazio.")
        return
    mostrar_arvore(acervo)


def achar_caminhos(no, nome, trilha, achados):
    for chave, filhos in no.items():
        atual = trilha + [chave]
        if chave.lower() == nome.lower():
            achados.append(" / ".join(atual))
        achar_caminhos(filhos, nome, atual, achados)


def buscar_area():
    nome = ler_texto("Nome da área: ")
    achados = []
    achar_caminhos(acervo, nome, [], achados)
    if not achados:
        print("Nenhuma área com esse nome.")
        return
    for caminho in achados:
        print(caminho)


def renomear_area():
    partes = pedir_caminho("Caminho da área a renomear: ")
    pai = localizar_pai(partes)
    if pai is None:
        print("Caminho não encontrado.")
        return
    novo = ler_texto("Novo nome: ").replace("/", "-")
    if novo in pai:
        print("Já existe uma área com esse nome nesse nível.")
        return
    pai[novo] = pai.pop(partes[-1])
    print("Área renomeada.")


def remover_area():
    partes = pedir_caminho("Caminho da área a remover: ")
    pai = localizar_pai(partes)
    if pai is None:
        print("Caminho não encontrado.")
        return
    filhas = contar_nos(pai[partes[-1]])
    if filhas > 0:
        resposta = input(f"Isso também apaga {filhas} subárea(s). Continuar? (s/n): ").strip().lower()
        if resposta != "s":
            print("Cancelado.")
            return
    del pai[partes[-1]]
    print("Área removida.")


def menu_acervo():
    while True:
        print("\n--- Acervo (áreas do conhecimento) ---")
        print("1. Inserir área")
        print("2. Listar acervo")
        print("3. Buscar área pelo nome")
        print("4. Renomear área")
        print("5. Remover área")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            inserir_area()
        elif opcao == "2":
            listar_acervo()
        elif opcao == "3":
            buscar_area()
        elif opcao == "4":
            renomear_area()
        elif opcao == "5":
            remover_area()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# Persistência em dados_sistema.txt
# ---------------------------------------------------------------

def caminhos_das_folhas(no, prefixo=()):
    # Só as folhas vão para o arquivo; os nós do meio são recriados no carregamento
    caminhos = []
    for nome, filhos in no.items():
        atual = prefixo + (nome,)
        if filhos:
            caminhos.extend(caminhos_das_folhas(filhos, atual))
        else:
            caminhos.append(atual)
    return caminhos


def salvar_dados():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arq:
            for l in leitores:
                arq.write(f"LISTA|{l['matricula']}|{l['nome']}|{l['curso']}\n")
            for r in reservas:  # do início para o fim da fila
                arq.write(f"FILA|{r['matricula']}|{r['titulo']}\n")
            for d in devolvidos:  # da base para o topo, para recarregar na mesma ordem
                arq.write(f"PILHA|{d['titulo']}|{d['matricula']}\n")
            for caminho in caminhos_das_folhas(acervo):
                arq.write("ARVORE|" + "|".join(caminho) + "\n")
    except OSError as erro:
        print(f"Não consegui salvar: {erro}")
        return
    print(f"Dados salvos em {ARQUIVO}.")


def carregar_dados():
    # Monta tudo em variáveis temporárias; só troca a memória se o arquivo abrir
    novos_leitores = []
    novas_reservas = []
    novos_devolvidos = []
    nova_arvore = {}
    ignoradas = 0

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arq:
            linhas = arq.read().splitlines()
    except FileNotFoundError:
        print("Ainda não existe arquivo salvo.")
        return
    except OSError as erro:
        print(f"Não consegui ler o arquivo: {erro}")
        return

    for linha in linhas:
        if not linha.strip():
            continue
        campos = linha.split("|")
        tipo = campos[0]
        if tipo == "LISTA" and len(campos) == 4:
            novos_leitores.append({"matricula": campos[1], "nome": campos[2], "curso": campos[3]})
        elif tipo == "FILA" and len(campos) == 3:
            novas_reservas.append({"matricula": campos[1], "titulo": campos[2]})
        elif tipo == "PILHA" and len(campos) == 3:
            novos_devolvidos.append({"titulo": campos[1], "matricula": campos[2]})
        elif tipo == "ARVORE" and len(campos) >= 2:
            no = nova_arvore
            for parte in campos[1:]:
                no = no.setdefault(parte, {})
        else:
            ignoradas += 1

    leitores.clear()
    leitores.extend(novos_leitores)
    reservas.clear()
    reservas.extend(novas_reservas)
    devolvidos.clear()
    devolvidos.extend(novos_devolvidos)
    acervo.clear()
    acervo.update(nova_arvore)

    print(f"Carregado: {len(leitores)} leitor(es), {len(reservas)} reserva(s), "
          f"{len(devolvidos)} livro(s) na pilha.")
    if ignoradas:
        print(f"{ignoradas} linha(s) fora do padrão foram ignoradas.")


# ---------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------

def main():
    while True:
        print("\n===== BIBLIOTECA =====")
        print("1. Leitores (lista)")
        print("2. Reservas (fila)")
        print("3. Devolvidos (pilha)")
        print("4. Acervo (árvore)")
        print("5. Salvar dados")
        print("6. Carregar dados")
        print("0. Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            menu_leitores()
        elif opcao == "2":
            menu_reservas()
        elif opcao == "3":
            menu_devolvidos()
        elif opcao == "4":
            menu_acervo()
        elif opcao == "5":
            salvar_dados()
        elif opcao == "6":
            carregar_dados()
        elif opcao == "0":
            if input("Salvar antes de sair? (s/n): ").strip().lower() == "s":
                salvar_dados()
            print("Até logo.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
