from livro import Livro

from usuario import Usuario

from emprestimo import Emprestimo

from estruturas import NoArvore, ArvoreLivros, NoGenero

class Biblioteca:
    
    def __init__(self):
        
        self.generos = None
        
        self.livros_por_codigo = {}
        
        self.generos_padrao = [
            "Aventura", "Romance", "Ficção Científica", "Terror", "Drama",
            "Comédia", "Fantasia", "Suspense", "Biografia", "História"
        ]
        
        for genero in self.generos_padrao:
            
            self._adicionar_genero(genero)

    def _adicionar_genero(self, genero):
        
        novo_genero = NoGenero(genero)
        
        if self.generos is None:
            
            self.generos = novo_genero
            
        else:
            
            atual = self.generos
            
            while atual.proximo is not None:
                
                atual = atual.proximo
                
            atual.proximo = novo_genero

    def cadastrar_livro(self):
        
        print("Selecione o gênero do livro:")
        
        generos_lista = []
        
        atual = self.generos
        
        i = 1
        
        while atual is not None:
            
            print(f"{i}. {atual.genero}")
            
            generos_lista.append(atual.genero)
            
            atual = atual.proximo
            
            i += 1
            
        print(f"{i}. Outro (Cadastrar novo gênero)")

        try:
            escolha = int(input("Digite o número correspondente: "))
            
        except ValueError:
            
            print("Entrada inválida.")
            
            return

        if escolha < 1 or escolha > len(generos_lista) + 1:
            
            print("Opção inválida.")
            
            return

        if escolha == len(generos_lista) + 1:
            
            genero = input("Digite o novo gênero: ")
            
            self._adicionar_genero(genero)
            
        else:
            
            genero = generos_lista[escolha - 1]

        titulo = input("Título: ")
        autor = input("Autor: ")
        codigo = input("Código: ")

        if codigo in self.livros_por_codigo:
            
            print("Já existe um livro com esse código.")
            
            return

        novo_livro = Livro(titulo, autor, codigo, genero)
        
        self.livros_por_codigo[codigo] = novo_livro

        atual = self.generos
        
        while atual is not None:
            
            if atual.genero == genero:
                
                atual.arvore.inserir(novo_livro)
                
                print("Livro cadastrado com sucesso.")
                
                return
            
            atual = atual.proximo



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
