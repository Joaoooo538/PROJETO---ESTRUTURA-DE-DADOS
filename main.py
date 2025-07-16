from biblioteca import Biblioteca
from utils import menu_principal

def main():
    biblioteca = Biblioteca()

    try:
        while True:
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
            elif opcao == "0":
                biblioteca.salvar_dados()
                print("Salvando Dados...")
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida.")
    except KeyboardInterrupt:
        print("Programa interrompido manualmente. Salvando Dados...")
        biblioteca.salvar_dados()
if __name__ == "__main__":
    main()
