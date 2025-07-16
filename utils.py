import os
import platform

def menu_principal():
    clear_console()
    print("="*35)
    print("     SISTEMA DE BIBLIOTECA")
    print("="*35)
    print("1. Cadastrar Livro")
    print("2. Cadastrar Usuário")
    print("3. Emprestar Livro")
    print("4. Devolver Livro")
    print("5. Buscar Livro")
    print("6. Relatório de Empréstimos")
    print("0. Sair")
    print("="*35)

    opcao = input("Escolha uma opção: ").strip()
    return opcao

def clear_console():

    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pausar():

    input("\nPressione Enter para continuar...")
