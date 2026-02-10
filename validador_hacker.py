import re
import sys
from colorama import init, Fore, Style

# Inicializa o colorama para funcionar no Windows e Linux
init(autoreset=True)

def exibir_banner():
    """
    Exibe o banner ASCII no estilo Hacker.
    """
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
    ____ _       __ ____     _____  ______ ______ _   __ ____   ______
   / __ \ |     / // __ \   / ___/ / ____// ____// | / // __ \ / ____/
  / /_/ / | /| / // / / /   \__ \ / __/  / /    /  |/ // / / // __/   
 / ____/| |/ |/ // /_/ /   ___/ // /___ / /___ / /|  // /_/ // /___   
/_/     |__/|__/ /_____/   /____//_____/ \____//_/ |_/ \____//_____/   
                                                                       
{Fore.CYAN}--- SECURITY PASSWORD ANALYZER v1.0 ---
    """
    print(banner)

def analisar_senha(senha):
    """
    Analisa a força da senha baseada em 4 critérios principais.
    Retorna uma lista de feedbacks e a pontuação final.
    """
    pontos = 0
    feedback = []
    
    # 1. Verificação de Comprimento
    if len(senha) >= 8:
        pontos += 25
        feedback.append(f"{Fore.GREEN}[+] Comprimento adequado (8+ caracteres)")
    else:
        feedback.append(f"{Fore.RED}[-] Muito curta (mínimo 8 caracteres)")

    # 2. Verificação de Letras Maiúsculas e Minúsculas
    # O regex [a-z] procura minúsculas e [A-Z] procura maiúsculas
    if re.search(r"[a-z]", senha) and re.search(r"[A-Z]", senha):
        pontos += 25
        feedback.append(f"{Fore.GREEN}[+] Contém letras maiúsculas e minúsculas")
    else:
        feedback.append(f"{Fore.RED}[-] Misture letras maiúsculas e minúsculas")

    # 3. Verificação de Números
    # O regex \d procura por qualquer dígito de 0 a 9
    if re.search(r"\d", senha):
        pontos += 25
        feedback.append(f"{Fore.GREEN}[+] Contém números")
    else:
        feedback.append(f"{Fore.RED}[-] Adicione pelo menos um número")

    # 4. Verificação de Caracteres Especiais
    # O regex procura por símbolos comuns de segurança
    if re.search(r"[@#$!%*?&]", senha):
        pontos += 25
        feedback.append(f"{Fore.GREEN}[+] Contém caracteres especiais (@,#,$,etc)")
    else:
        feedback.append(f"{Fore.RED}[-] Use caracteres especiais para maior segurança")

    return pontos, feedback

def main():
    exibir_banner()
    
    # Solicita a senha ao usuário
    # Em um cenário real, usaríamos getpass.getpass() para ocultar a digitação
    senha = input(f"{Fore.WHITE}Digite a senha para análise: {Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Iniciando varredura de segurança...\n")
    
    pontuacao, resultados = analisar_senha(senha)
    
    # Exibe os resultados da análise
    for item in resultados:
        print(item)
    
    # Resultado Final e Nota
    print(f"\n{'='*40}")
    cor_final = Fore.GREEN if pontuacao >= 75 else (Fore.YELLOW if pontuacao >= 50 else Fore.RED)
    
    print(f"NOTA DE SEGURANÇA: {cor_final}{pontuacao}%")
    
    if pontuacao == 100:
        print(f"{Fore.GREEN}{Style.BRIGHT}STATUS: SENHA HACKER-PROOF! (FORTE)")
    elif pontuacao >= 50:
        print(f"{Fore.YELLOW}STATUS: SENHA MODERADA - PODE SER MELHORADA.")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}STATUS: SENHA VULNERÁVEL! (FRACA)")
    print(f"{Fore.WHITE}{'='*40}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Sessão encerrada pelo usuário.")
        sys.exit()
