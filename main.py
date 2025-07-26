import os
import pickle  # Importado diretamente aqui, pois é usado no main

from biblioteca import Biblioteca
from utils import menu_principal

# Define o nome do arquivo onde os dados da biblioteca serão salvos
ARQUIVO_DADOS = 'dados_biblioteca.pkl'


def limpar_tela():
    """Limpa o terminal, compatível com Windows, macOS e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    biblioteca = None

    # Tenta carregar os dados da biblioteca ao iniciar
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
        # Limpa a tela antes de exibir o menu ou qualquer output da ação
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
            # Salva os dados da biblioteca antes de sair
            try:
                with open(ARQUIVO_DADOS, 'wb') as f:
                    pickle.dump(biblioteca, f)
                print("Dados da biblioteca salvos com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar os dados da biblioteca: {e}")
            break
        else:
            print("Opção inválida.")

        # Pausa para o usuário ver a mensagem antes da tela ser limpa novamente
        if opcao != "0":  # Não precisa pausar se for sair
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()