import secrets
import string 

def gerar_senha(tamanho: int = 12)-> str:
    
    caracteres = string.ascii_letters + string.digits;
    senha_gerada = ''.join(secrets.choice(caracteres) for i in range(tamanho))
    return senha_gerada

if __name__ == '__main__':
    
    try:
        texto_digitado = input("Digite o tamanho da senha: ")
        tamanho_desejado = int(texto_digitado)
        nova_senha = gerar_senha(tamanho_desejado)
        print(f"Senha gerada: {nova_senha}")

    except ValueError:
        print("Por favor, digite um número inteiro válido.")
