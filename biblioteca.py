from livro import Livro
from usuario import Usuario
from emprestimo import Emprestimo
from estruturas import NoArvore, ArvoreLivros, NoGenero
import datetime  # Importação adicionada


class Biblioteca:
    def __init__(self):
        self.generos = None  # Lista encadeada de NoGenero
        self.livros_por_codigo = {}  # Dicionário para acesso rápido por código
        self.usuarios = []  # Lista de objetos Usuario (CORREÇÃO: inicializada aqui)
        self.emprestimos = []  # Lista de objetos Emprestimo (CORREÇÃO: inicializada aqui)

        self.generos_padrao = [
            "Aventura", "Romance", "Ficção Científica", "Terror", "Drama",
            "Comédia", "Fantasia", "Suspense", "Biografia", "História"
        ]

        for genero in self.generos_padrao:
            self._adicionar_genero(genero)

    def _adicionar_genero(self, genero_nome):
        novo_genero = NoGenero(genero_nome)
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

        genero_escolhido = ""
        if escolha == len(generos_lista) + 1:
            genero_escolhido = input("Digite o novo gênero: ")
            self._adicionar_genero(genero_escolhido)
        else:
            genero_escolhido = generos_lista[escolha - 1]

        titulo = input("Título: ")
        autor = input("Autor: ")
        codigo = input("Código: ")

        if codigo in self.livros_por_codigo:
            print("Já existe um livro com esse código. Adicionando uma nova cópia.")
            # Se o livro já existe, apenas aumenta a quantidade disponível
            self.livros_por_codigo[codigo].quantidade_total += 1
            self.livros_por_codigo[codigo].quantidade_disponivel += 1
            print(
                f"Quantidade total de cópias para '{titulo}' agora é: {self.livros_por_codigo[codigo].quantidade_total}")
            return

        try:
            quantidade = int(input("Quantidade de cópias a cadastrar: "))
            if quantidade <= 0:
                print("A quantidade deve ser um número positivo.")
                return
        except ValueError:
            print("Entrada inválida para quantidade.")
            return

        novo_livro = Livro(titulo, autor, codigo, genero_escolhido, quantidade)
        self.livros_por_codigo[codigo] = novo_livro

        # Adiciona o livro à árvore do gênero correspondente
        atual = self.generos
        while atual is not None:
            if atual.genero == genero_escolhido:
                atual.arvore.inserir(novo_livro)
                print("Livro cadastrado com sucesso.")
                return
            atual = atual.proximo

    def cadastrar_usuario(self):
        nome = input("Nome do usuário: ")
        user_id = input("ID do usuário: ")
        # Verifica se o ID do usuário já existe
        if any(u.user_id == user_id for u in self.usuarios):
            print("Já existe um usuário com esse ID.")
            return
        self.usuarios.append(Usuario(nome, user_id))
        print("Usuário cadastrado com sucesso.")

    def emprestar_livro(self):
        codigo = input("Código do livro: ")
        user_id = input("ID do usuário: ")

        livro = self.livros_por_codigo.get(codigo)
        if not livro:
            print("Livro não encontrado.")
            return

        if livro.quantidade_disponivel <= 0:
            print(f"Todas as cópias de '{livro.titulo}' estão emprestadas.")
            return

        usuario_encontrado = None
        for usuario in self.usuarios:
            if usuario.user_id == user_id:
                usuario_encontrado = usuario
                break

        if not usuario_encontrado:
            print("Usuário não encontrado.")
            return

        # Realiza o empréstimo
        livro.quantidade_disponivel -= 1
        if livro.quantidade_disponivel < livro.quantidade_total:
            livro.emprestado = True  # Marca como emprestado se houver alguma cópia fora

        # Adiciona ao histórico do livro
        livro.historico_emprestimos.append({"user_id": user_id, "data_emprestimo": datetime.date.today().isoformat()})

        novo_emprestimo = Emprestimo(livro, usuario_encontrado)
        self.emprestimos.append(novo_emprestimo)
        print(f"Empréstimo de '{livro.titulo}' para '{usuario_encontrado.nome}' realizado com sucesso.")

    def devolver_livro(self):
        codigo = input("Código do livro: ")
        user_id = input("ID do usuário que devolve: ")  # Pede o ID do usuário para melhor controle

        livro = self.livros_por_codigo.get(codigo)
        if not livro:
            print("Livro não encontrado.")
            return

        # Verifica se o livro foi realmente emprestado para este usuário
        emprestimo_encontrado = None
        for emp in self.emprestimos:
            if emp.livro.codigo == codigo and emp.usuario.user_id == user_id:
                emprestimo_encontrado = emp
                break

        if not emprestimo_encontrado:
            print("Empréstimo não encontrado para este livro e usuário.")
            return

        livro.quantidade_disponivel += 1
        if livro.quantidade_disponivel == livro.quantidade_total:
            livro.emprestado = False  # Marca como não emprestado se todas as cópias voltaram

        self.emprestimos.remove(emprestimo_encontrado)
        print(f"Livro '{livro.titulo}' devolvido por '{user_id}' com sucesso.")

    def buscar_livro(self):
        termo = input("Digite o título ou autor: ").lower()
        encontrados = []

        atual_genero = self.generos
        while atual_genero:
            # Função auxiliar para buscar na árvore de um gênero
            def _buscar_na_arvore(no):
                if not no:
                    return
                # Percurso in-order para manter a ordem alfabética ao listar
                _buscar_na_arvore(no.esquerda)
                livro = no.livro
                if termo in livro.titulo.lower() or termo in livro.autor.lower():
                    encontrados.append(livro)
                _buscar_na_arvore(no.direita)

            _buscar_na_arvore(atual_genero.arvore.raiz)
            atual_genero = atual_genero.proximo

        if encontrados:
            print("\n--- Livros Encontrados ---")
            for l in encontrados:
                status = "Disponível" if l.quantidade_disponivel > 0 else "Emprestado (Todas as cópias)"
                print(f"Código: {l.codigo} - Título: {l.titulo} ({l.autor})")
                print(f"  Gênero: {l.genero} - Status: {status}")
                print(f"  Cópias disponíveis: {l.quantidade_disponivel}/{l.quantidade_total}")
                if l.historico_emprestimos:
                    print("  Histórico de Empréstimos (últimos):")
                    # Mostra os 3 últimos empréstimos para não lotar a tela
                    for hist in l.historico_emprestimos[-3:]:
                        print(f"    - Usuário ID: {hist['user_id']} em {hist['data_emprestimo']}")
                print("-" * 30)
        else:
            print("Nenhum livro encontrado.")

    def relatorio_emprestimos(self):
        if not self.emprestimos:
            print("Nenhum livro emprestado no momento.")
            return
        print("\n--- Relatório de Empréstimos Ativos ---")
        for emp in self.emprestimos:
            print(f"Livro: {emp.livro.titulo} (Cód: {emp.livro.codigo})")
            print(f"  Emprestado para: {emp.usuario.nome} (ID: {emp.usuario.user_id})")
            print("-" * 30)

    def visualizar_livros(self):
        """Lista todos os livros na biblioteca, organizados por gênero."""
        if self.generos is None:
            print("Nenhum livro cadastrado ainda.")
            return

        print("\n--- Todos os Livros na Biblioteca ---")
        atual_genero = self.generos
        while atual_genero:
            print(f"\n===== Gênero: {atual_genero.genero} =====")
            if atual_genero.arvore.raiz is None:
                print("  Nenhum livro neste gênero.")
            else:
                # Percurso in-order na árvore para listar em ordem alfabética por título
                def _percorrer_arvore(no):
                    if no is not None:
                        _percorrer_arvore(no.esquerda)
                        livro = no.livro
                        status = "Disponível" if livro.quantidade_disponivel > 0 else "Emprestado (Todas as cópias)"
                        print(f"  Cód: {livro.codigo} - Título: {livro.titulo} ({livro.autor})")
                        print(f"    Status: {status} | Cópias: {livro.quantidade_disponivel}/{livro.quantidade_total}")
                        if livro.historico_emprestimos:
                            print("    Histórico de Empréstimos (últimos):")
                            for hist in livro.historico_emprestimos[-2:]:  # Mostra os 2 últimos
                                print(f"      - Usuário ID: {hist['user_id']} em {hist['data_emprestimo']}")
                        _percorrer_arvore(no.direita)

                _percorrer_arvore(atual_genero.arvore.raiz)
            atual_genero = atual_genero.proximo
        print("\n--- Fim da Lista de Livros ---")

    def visualizar_usuarios(self):
        """Lista todos os usuários cadastrados."""
        if not self.usuarios:
            print("Nenhum usuário cadastrado ainda.")
            return
        print("\n--- Todos os Usuários Cadastrados ---")
        for usuario in self.usuarios:
            print(f"Nome: {usuario.nome} - ID: {usuario.user_id}")
        print("\n--- Fim da Lista de Usuários ---")