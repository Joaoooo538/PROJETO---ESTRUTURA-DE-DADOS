class Livro:
    def __init__(self, titulo, autor, codigo, genero):
        self.titulo = titulo
        self.genero = genero
        self.autor = autor
        self.codigo = codigo
        self.emprestado = False
