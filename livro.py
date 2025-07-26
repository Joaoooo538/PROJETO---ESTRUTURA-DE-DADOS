class Livro:
    def __init__(self, titulo, autor, codigo, genero, quantidade_total=1):
        self.titulo = titulo
        self.genero = genero
        self.autor = autor
        self.codigo = codigo
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = quantidade_total
        # 'emprestado' indica se há ALGUMA cópia emprestada
        self.emprestado = False if quantidade_total > 0 else True
        self.historico_emprestimos = [] # Adicionado para registrar quem pegou emprestado