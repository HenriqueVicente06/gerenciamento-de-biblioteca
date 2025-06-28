from dataclasses import dataclass
from typing import List

@dataclass
class Livro:
    codigo: str
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str
    quantidade_total: int
    quantidade_disponivel: int

@dataclass
class Usuario:
    id_usuario: str
    nome: str
    tipo: str

@dataclass
class Emprestimo:
    id_usuario: str
    codigo_livro: str
    dia_emprestimo: int
    dia_devolucao_prevista: int
    status: str
    dia_devolucao_efetiva: int = 0
    multa: float = 0.0

livros, usuarios, emprestimos = [], [], []
dia_atual_sistema = 1
VALOR_MULTA_POR_DIA = 1.0

def entrada(prompt, tipo=str, erro="Entrada inválida", validacao=None):
    while True:
        try:
            v = tipo(input(prompt).strip())
            if not v or (validacao and not validacao(v)):
                print(erro)
            else:
                return v
        except:
            print(erro)

def buscar(lista, chave, campo):
    return next((x for x in lista if getattr(x, campo) == chave), None)

def cadastrar_livro():
    print("\n--- Cadastro de Livro ---")
    while True:
        codigo = entrada("Código único: ")
        if not buscar(livros, codigo, 'codigo'):
            break
        print("Código já existe.")
    qt = entrada("Qtd total: ", int, "Qtd inválida", lambda x: x >= 0)
    novo = Livro(
        codigo,
        entrada("Título: "),
        entrada("Autor: "),
        entrada("Ano: ", int, "Ano inválido", lambda x: x > 0),
        entrada("Gênero: "),
        qt,
        qt
    )
    livros.append(novo)
    print(f"Livro '{novo.titulo}' cadastrado com sucesso.")

def listar_livros():
    print("\n--- Lista de Livros ---")
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    for l in livros:
        print(f"{l.codigo} | {l.titulo} | {l.autor} | {l.ano_publicacao} | {l.genero} | Tot: {l.quantidade_total} | Disp: {l.quantidade_disponivel}")

def buscar_livro():
    termo = input("Digite código, título ou autor: ").strip().lower()
    encontrados = [l for l in livros if termo in l.codigo.lower() or termo in l.titulo.lower() or termo in l.autor.lower()]
    if not encontrados:
        print("Nenhum livro encontrado.")
        return
    for l in encontrados:
        print(f"{l.codigo} | {l.titulo} | {l.autor} | Ano: {l.ano_publicacao} | Disp: {l.quantidade_disponivel}")

def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    while True:
        id_u = entrada("ID único: ")
        if not buscar(usuarios, id_u, 'id_usuario'):
            break
        print("ID já existe.")
    usuarios.append(
        Usuario(
            id_u,
            entrada("Nome: "),
            entrada("Tipo (aluno/professor): ", str, "Tipo inválido", lambda x: x in ["aluno", "professor"])
        )
    )
    print("Usuário cadastrado.")

def listar_usuarios():
    print("\n--- Lista de Usuários ---")
    if not usuarios:
        print("Nenhum usuário.")
        return
    for u in usuarios:
        print(f"{u.id_usuario} | {u.nome} | {u.tipo}")

def emprestar():
    global dia_atual_sistema
    print("\n--- Empréstimo ---")
    id_u = entrada("ID Usuário: ")
    cod = entrada("Código do Livro: ")
    u = buscar(usuarios, id_u, 'id_usuario')
    l = buscar(livros, cod, 'codigo')
    if not u or not l:
        print("Usuário ou livro não encontrado.")
        return
    if l.quantidade_disponivel < 1:
        print("Livro indisponível.")
        return
    prazo = 7 if u.tipo == "aluno" else 10
    l.quantidade_disponivel -= 1
    emprestimos.append(
        Emprestimo(id_u, cod, dia_atual_sistema, dia_atual_sistema + prazo, "ativo")
    )
    print(f"Livro '{l.titulo}' emprestado a {u.nome}. Devolução até dia {dia_atual_sistema + prazo}.")

def devolver():
    global dia_atual_sistema
    print("\n--- Devolução ---")
    id_u = entrada("ID Usuário: ")
    cod = entrada("Código Livro: ")
    emp = next((e for e in emprestimos if e.id_usuario == id_u and e.codigo_livro == cod and e.status == "ativo"), None)
    if not emp:
        print("Empréstimo não encontrado.")
        return
    l = buscar(livros, cod, 'codigo')
    emp.dia_devolucao_efetiva = dia_atual_sistema
    emp.status = "devolvido"
    l.quantidade_disponivel += 1
    atraso = max(0, emp.dia_devolucao_efetiva - emp.dia_devolucao_prevista)
    emp.multa = atraso * VALOR_MULTA_POR_DIA
    print(f"Devolvido. {'Multa: R$'+str(emp.multa) if atraso else 'Sem multa.'}")

def relatorios():
    print("\n--- Relatórios ---")
    ativos = [e for e in emprestimos if e.status == "ativo"]
    if not ativos:
        print("Nenhum empréstimo ativo.")
    else:
        print("\nEmpréstimos Ativos:")
        for e in ativos:
            l = buscar(livros, e.codigo_livro, 'codigo')
            u = buscar(usuarios, e.id_usuario, 'id_usuario')
            print(f"{l.titulo} | {u.nome} | Previsão: {e.dia_devolucao_prevista}")
    atrasados = [e for e in ativos if e.dia_devolucao_prevista < dia_atual_sistema]
    if atrasados:
        print("\nAtrasos:")
        for e in atrasados:
            l = buscar(livros, e.codigo_livro, 'codigo')
            u = buscar(usuarios, e.id_usuario, 'id_usuario')
            dias_atraso = dia_atual_sistema - e.dia_devolucao_prevista
            print(f"{l.titulo} | {u.nome} | Previsão: {e.dia_devolucao_prevista} | Atraso: {dias_atraso} dias")

# Variável global (ou gerenciada de forma acessível)
# dia_atual_sistema = 1 # Definida no início do programa principal

def menu_gerenciar_tempo(dia_sistema_atual_param): # Exemplo recebendo e retornando
    """Gerencia a passagem do tempo no sistema."""
    # Se dia_atual_sistema for global, use: global dia_atual_sistema
    # Neste exemplo, passamos como parâmetro e retornamos o valor modificado.
    
    while True:
        print("\\n--- Gerenciar Tempo ---")
        print(f"Dia Atual do Sistema: {dia_sistema_atual_param}")
        print("1. Avançar 1 dia")
        print("2. Avançar 7 dias (1 semana)")
        print("3. Avançar N dias")
        print("4. Consultar dia atual")
        print("5. Voltar ao Menu Principal")
        
        opcao_tempo = input("Escolha uma opção: ")

        if opcao_tempo == '1':
            dia_sistema_atual_param += 1
            print(f"Sistema avançou para o dia: {dia_sistema_atual_param}")
        elif opcao_tempo == '2':
            dia_sistema_atual_param += 7
            print(f"Sistema avançou 7 dias. Novo dia: {dia_sistema_atual_param}")
        elif opcao_tempo == '3':
            try:
                n_dias = int(input("Quantos dias deseja avançar? "))
                if n_dias > 0:
                    dia_sistema_atual_param += n_dias
                    print(f"Sistema avançou {n_dias} dias. Novo dia: {dia_sistema_atual_param}")
                else:
                    print("Por favor, insira um número positivo de dias.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        elif opcao_tempo == '4':
            print(f"O dia atual do sistema é: {dia_sistema_atual_param}")
        elif opcao_tempo == '5':
            print("Retornando ao Menu Principal...")
            break # Sai do loop do menu_gerenciar_tempo
        else:
            print("Opção inválida. Tente novamente.")
    return dia_sistema_atual_param # Retorna o dia atualizado

# No loop principal do seu programa, quando a opção "Gerenciar Tempo" for escolhida:
# dia_atual_sistema = menu_gerenciar_tempo(dia_atual_sistema)


def main():
    global dia_atual_sistema
    while True:
        print("\n=== Menu Principal ===")
        print(" 1.Livros\n 2.Usuários\n 3.Empréstimo\n 4.Devolução\n 5.Relatórios\n 6.Tempo\n 7.Sair")
        m = input("Opção: ")
        match m:
            case '1':
                while True:
                    print("==Livros==\n1.Cadastrar\n2.Listar\n3.Buscar\n4.Voltar")
                    op = input("Opção: ")
                    if op == '1': cadastrar_livro()
                    elif op == '2': listar_livros()
                    elif op == '3': buscar_livro()
                    elif op == '4': break
            case '2':
                while True:
                    print("==Usuário==\n1.Cadastrar\n2.Listar\n3.Voltar")
                    op = input("Opção: ")
                    if op == '1': cadastrar_usuario()
                    elif op == '2': listar_usuarios()
                    elif op == '3': break
            case '3':
                emprestar()
            case '4':
                devolver()
            case '5':
                relatorios()
            case '6':
                dia_atual_sistema = menu_gerenciar_tempo(dia_atual_sistema)
            case '7':
                print("Encerrando..."); break
            case _:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
