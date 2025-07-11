from livro import Livro
from usuario import Usuario
from emprestimo import Emprestimo

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []

    def cadastrar_livro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        codigo = input("Código: ")
        self.livros.append(Livro(titulo, autor, codigo))
        print("Livro cadastrado com sucesso.")

    def cadastrar_usuario(self):
        nome = input("Nome do usuário: ")
        user_id = input("ID do usuário: ")
        self.usuarios.append(Usuario(nome, user_id))
        print("Usuário cadastrado com sucesso.")

    def emprestar_livro(self):
        codigo = input("Código do livro: ")
        user_id = input("ID do usuário: ")
        for livro in self.livros:
            if livro.codigo == codigo and not livro.emprestado:
                for usuario in self.usuarios:
                    if usuario.user_id == user_id:
                        livro.emprestado = True
                        self.emprestimos.append(Emprestimo(livro, usuario))
                        print("Empréstimo realizado com sucesso.")
                        return
        print("Livro indisponível ou usuário não encontrado.")

    def devolver_livro(self):
        codigo = input("Código do livro: ")
        for emprestimo in self.emprestimos:
            if emprestimo.livro.codigo == codigo:
                emprestimo.livro.emprestado = False
                self.emprestimos.remove(emprestimo)
                print("Livro devolvido com sucesso.")
                return
        print("Empréstimo não encontrado.")

    def buscar_livro(self):
        termo = input("Digite o título ou autor: ").lower()
        encontrados = [l for l in self.livros if termo in l.titulo.lower() or termo in l.autor.lower()]
        if encontrados:
            for l in encontrados:
                status = "Emprestado" if l.emprestado else "Disponível"
                print(f"{l.codigo} - {l.titulo} ({l.autor}) - {status}")
        else:
            print("Nenhum livro encontrado.")

    def relatorio_emprestimos(self):
        if not self.emprestimos:
            print("Nenhum livro emprestado.")
            return
        for emp in self.emprestimos:
            print(f"{emp.livro.titulo} ({emp.livro.codigo}) emprestado por {emp.usuario.nome} ({emp.usuario.user_id})")
