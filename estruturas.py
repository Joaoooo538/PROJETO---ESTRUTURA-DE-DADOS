class NoArvore:
    
    def __init__(self, livro):
        
        self.livro = livro
        
        self.esquerda = None
        
        self.direita = None

class ArvoreLivros:
    
    def __init__(self):
        
        self.raiz = None

    def inserir(self, livro):
        
        self.raiz = self._inserir_recursivo(self.raiz, livro)

    def _inserir_recursivo(self, no, livro):
        
        if not no:
            
            return NoArvore(livro)
        
        if livro.titulo < no.livro.titulo:
            
            no.esquerda = self._inserir_recursivo(no.esquerda, livro)
            
        else:
            
            no.direita = self._inserir_recursivo(no.direita, livro)
            
        return no

class NoGenero:
    
    def __init__(self, genero):
        
        self.genero = genero
        
        self.arvore = ArvoreLivros()
        
        self.proximo = None