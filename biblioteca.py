from livro import Livro
from usuario import Usuario
from emprestimo import Emprestimo
import json

class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []
        self.carregar_dados()

    def cadastrar_livro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        codigo = input("Código: ")

        if codigo in self.livros:
            print("esse livro já está cadastrado.")
            return

        self.livros[codigo] = Livro(titulo, autor, codigo)
        print("Livro cadastrado com sucesso.")

    def cadastrar_usuario(self):
        nome = input("Nome do usuário: ")
        user_id = input("ID do usuário: ")
        self.usuarios[user_id]= Usuario(nome, user_id)
        print("Usuário cadastrado com sucesso.")

    def emprestar_livro(self):
        codigo = input("Código do livro: ")
        user_id = input("ID do usuário: ")

        livro = self.livros.get(codigo)
        usuario = self.usuarios.get(user_id)

        if livro and usuario and not livro.emprestado:
            livro.emprestado = True
            self.emprestimos.append(Emprestimo(livro, usuario))
            print("Empréstimo realizado com sucesso.")
        else:
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
        encontrados = [l for l in self.livros.values() if termo in l.titulo.lower() or termo in l.autor.lower()]
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



    #BLOCO DE SERIALIZAÇÃO
    def salvar_dados(self, arquivos_usuarios="usuarios.json",arquivos_livros="livros.json", arquivos_emprestimos="emprestimos.json"):

        with open(arquivos_usuarios, "w") as f:
            json.dump({uid: vars(usuario) for uid, usuario in self.usuarios.items()}, f, indent=4)

        with open(arquivos_livros, "w") as f:
            json.dump({codigo: vars(livro) for codigo, livro in self.livros.items()}, f, indent=4)

        with open(arquivos_emprestimos, "w") as f:
            json.dump(
                [
                    {
                        "codigo_livro": emp.livro.codigo,
                        "id_usuario": emp.usuario.user_id

                    }
                    for emp in self.emprestimos
                ],
                f,
                indent=4
            )

    def carregar_dados(self, arquivo_usuarios="usuarios.json", arquivos_livros="livros.json"):
        try:
            with open(arquivo_usuarios, "r") as f:
                usuarios_data = json.load(f)
                self.usuarios = {
                    uid: Usuario(**dados) for uid, dados in usuarios_data.items()
                }
                print("Usuários serializados com sucesso.")
        except FileNotFoundError:
            print("Não foi possível serializar. Carregando lista de usuários vazia.")
            self.usuarios = {}


        try:
            with open(arquivos_livros) as f:
                livros_data = json.load(f)
                self.livros={
                    codigo: Livro(**dados) for codigo, dados in livros_data.items()
                }
                print("Livros serializados com sucesso.")
        except FileNotFoundError:
            print("Não foi possível serializar. Carregando lista de livros vazia.")
            self.livros = {}

        try:
            with open("emprestimos.json", "r") as f:
                emprestimos_data = json.load(f)
                self.emprestimos = []

                for emp in emprestimos_data:
                    livro = self.livros.get(emp["codigo_livro"])
                    usuario = self.usuarios.get(emp["id_usuario"])
                    if livro and usuario:
                        livro.emprestado = True
                        self.emprestimos.append(Emprestimo(livro, usuario))
                print("Empréstimos carregados com sucesso.")

        except FileNotFoundError:
            print("Não foi possível carregar os empréstimos.")
            self.emprestimos = []
