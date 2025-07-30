import os
import pickle 
from biblioteca import Biblioteca
from utils import menu_principal
ARQUIVO_DADOS = 'dados_biblioteca.pkl'


def limpar_tela():
    """Limpa o terminal, compatível com Windows, macOS e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    biblioteca = None
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'rb') as f:
                biblioteca = pickle.load(f)
            print("Dados da biblioteca carregados com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar os dados da biblioteca: {e}. Iniciando com uma biblioteca vazia.")
            biblioteca = Biblioteca()
    else:
        print("Arquivo de dados da biblioteca não encontrado. Iniciando com uma nova biblioteca.")
        biblioteca = Biblioteca()

    while True:
        limpar_tela()

        opcao = menu_principal()
        if opcao == "1":
            biblioteca.cadastrar_livro()
        elif opcao == "2":
            biblioteca.cadastrar_usuario()
        elif opcao == "3":
            biblioteca.emprestar_livro()
        elif opcao == "4":
            biblioteca.devolver_livro()
        elif opcao == "5":
            biblioteca.buscar_livro()
        elif opcao == "6":
            biblioteca.relatorio_emprestimos()
        elif opcao == "7":
            biblioteca.visualizar_livros()
        elif opcao == "8":
            biblioteca.visualizar_usuarios()
        elif opcao == "0":
            print("Encerrando o sistema...")
          
            try:
                with open(ARQUIVO_DADOS, 'wb') as f:
                    pickle.dump(biblioteca, f)
                print("Dados da biblioteca salvos com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar os dados da biblioteca: {e}")
            break
        else:
            print("Opção inválida.")

       
        if opcao != "0": 
            
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()