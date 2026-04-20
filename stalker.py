import os
import sys
import time
import requests
from bs4 import BeautifulSoup
import json
import random

# --- Classe de Cores e Estilos ---
class Cores:
    RESET = '\033[0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    BOLD = '\033[1m'

# --- Banner da Ferramenta ---
def banner():
    os.system('clear')
    print(f"""{Cores.RED}{Cores.BOLD}
 ____        _        _   _            _
|  _ \  __ _| |_ __ _| | | | __ _  ___| | _____ _ __
| | | |/ _` | __/ _` | |_| |/ _` |/ __| |/ / _ \ '__|
| |_| | (_| | || (_| |  _  | (_| | (__|   <  __/ |
|____/ \__,_|\__\__,_|_| |_|\__,_|\___|_|\_\___|_|
   {Cores.YELLOW}-> O Caçador de Informações Implacável <-{Cores.RESET}
    """)

# --- Função de Animação de Carregamento ---
def loading_animation(text):
    print(f"{Cores.CYAN}[~] {text}{Cores.RESET}", end="")
    chars = ["/", "-", "\\", "|"]
    for _ in range(15):
        for char in chars:
            sys.stdout.write(f'\b{Cores.YELLOW}{char}{Cores.RESET}')
            sys.stdout.flush()
            time.sleep(0.1)
    print("\b ")

# --- Função Principal de Busca ---
def search_engine_deep_dive(username):
    banner()
    print(f"{Cores.MAGENTA}Iniciando varredura profunda para o alvo: {Cores.BOLD}{username}{Cores.RESET}\n")
    
    # Dorks: Consultas avançadas para motores de busca
    dorks = [
        f'"{username}" site:pastebin.com',
        f'"{username}" "password"',
        f'"{username}" "email"',
        f'"{username}" "ip address"',
        f'"{username}" "real name"',
        f'"{username}" site:facebook.com',
        f'"{username}" site:twitter.com',
        f'"{username}" site:instagram.com',
        f'"{username}" "phone number"',
        f'"{username}" filetype:sql "password"',
        f'intext:"{username}" "last seen ip"',
    ]
    
    found_data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 1. Busca no Roblox
    loading_animation("Verificando perfil no Roblox...")
    try:
        roblox_url = f"https://www.roblox.com/users/profile?username={username}"
        # A API oficial é mais confiável para ID
        api_url = f"https://api.roblox.com/users/get-by-username?username={username}"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200 and 'Id' in response.json():
            user_info = response.json()
            user_id = user_info['Id']
            print(f"{Cores.GREEN}[+] Perfil Roblox Encontrado!{Cores.RESET}")
            print(f"  -> {Cores.CYAN}Username:{Cores.RESET} {user_info['Username']}")
            print(f"  -> {Cores.CYAN}User ID:{Cores.RESET} {user_id}")
            print(f"  -> {Cores.CYAN}Link do Perfil:{Cores.RESET} https://www.roblox.com/users/{user_id}/profile\n")
            found_data['Roblox_Profile'] = f"https://www.roblox.com/users/{user_id}/profile"
        else:
            print(f"{Cores.RED}[-] Perfil Roblox não encontrado publicamente.{Cores.RESET}\n")
    except Exception as e:
        print(f"{Cores.RED}[-] Erro ao buscar no Roblox: {e}{Cores.RESET}\n")

    # 2. Busca no TikTok
    loading_animation("Verificando perfil no TikTok...")
    tiktok_url = f"https://www.tiktok.com/@{username}"
    try:
        response = requests.get(tiktok_url, headers=headers, timeout=10, allow_redirects=True)
        # Se a URL final não for a página inicial, o perfil existe
        if response.status_code == 200 and "tiktok.com/@" in response.url:
             print(f"{Cores.GREEN}[+] Perfil TikTok Encontrado!{Cores.RESET}")
             print(f"  -> {Cores.CYAN}Link do Perfil:{Cores.RESET} {response.url}\n")
             found_data['TikTok_Profile'] = response.url
        else:
             print(f"{Cores.RED}[-] Perfil TikTok não encontrado.{Cores.RESET}\n")
    except Exception as e:
        print(f"{Cores.RED}[-] Erro ao buscar no TikTok: {e}{Cores.RESET}\n")
        
    # 3. Mergulho profundo com Dorks no Google
    loading_animation("Iniciando busca profunda na web (dorks)...")
    print("\n")
    google_search_url = "https://www.google.com/search?q="
    total_dorks = len(dorks)
    
    for i, dork in enumerate(dorks):
        print(f"{Cores.YELLOW}[{i+1}/{total_dorks}] Buscando por: {Cores.CYAN}{dork}{Cores.RESET}")
        try:
            response = requests.get(google_search_url + dork, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Procura por links ou texto relevante nos resultados
            search_results = soup.find_all('div', class_='g')
            if not search_results: # Tenta outra classe se a primeira falhar
                 search_results = soup.find_all('div', class_='tF2Cxc')

            found_something = False
            for result in search_results:
                title_tag = result.find('h3')
                link_tag = result.find('a')
                snippet_tag = result.find('div', class_='VwiC3b') # Classe do snippet
                
                title = title_tag.get_text() if title_tag else "N/A"
                link = link_tag['href'] if link_tag else "N/A"
                snippet = snippet_tag.get_text() if snippet_tag else ""
                
                #
                # ESTA É A PARTE CRÍTICA - análise de palavras-chave
                #
                keywords = ["ip", "password", "email", "phone", "address", "dox", "leak", "nome", "pai", "mae", "endereço"]
                
                # Verifica se o snippet ou o título contêm palavras-chave sensíveis
                if any(keyword in snippet.lower() for keyword in keywords) or any(keyword in title.lower() for keyword in keywords):
                    print(f"  {Cores.RED}{Cores.BOLD}>> POSSÍVEL DADO SENSÍVEL ENCONTRADO <<{Cores.RESET}")
                    print(f"     {Cores.CYAN}Título:{Cores.RESET} {title}")
                    print(f"     {Cores.CYAN}Link:{Cores.RESET} {link}")
                    print(f"     {Cores.CYAN}Snippet:{Cores.RESET} {snippet[:150]}...") # Exibe um trecho
                    found_something = True
                    # Melhoria: Adicionar automaticamente aos dados encontrados
                    if 'possible_leaks' not in found_data: found_data['possible_leaks'] = []
                    found_data['possible_leaks'].append(link)

            if not found_something:
                print(f"  -> Nenhum resultado imediato para esta busca.\n")
            else:
                print("") # Espaçamento
                
            time.sleep(random.uniform(2, 5)) # Pausa para evitar bloqueio do Google

        except Exception as e:
            print(f"{Cores.RED}[-] Erro na busca: {e}{Cores.RESET}\n")

    # 4. Relatório Final
    print(f"\n{Cores.GREEN}================== RELATÓRIO FINAL =================={Cores.RESET}")
    if not found_data:
        print(f"{Cores.YELLOW}A busca foi concluída, mas nenhum dado concreto foi encontrado publicamente.{Cores.RESET}")
        print(f"{Cores.YELLOW}Isto pode significar que o alvo tem boa segurança digital.{Cores.RESET}")
    else:
        for key, value in found_data.items():
            if isinstance(value, list):
                print(f"{Cores.GREEN}[+] {key.replace('_', ' ').title()}:{Cores.RESET}")
                for item in value:
                    print(f"  -> {Cores.CYAN}{item}{Cores.RESET}")
            else:
                print(f"{Cores.GREEN}[+] {key.replace('_', ' ').title()}:{Cores.RESET} {Cores.CYAN}{value}{Cores.RESET}")
    print(f"{Cores.GREEN}======================================================={Cores.RESET}")
    input("\nPressione Enter para voltar ao menu...")

# --- Menu Principal ---
def main_menu():
    while True:
        banner()
        print(f"{Cores.CYAN}   [1] Iniciar Varredura por Username{Cores.RESET}")
        print(f"{Cores.CYAN}   [2] Sobre{Cores.RESET}")
        print(f"{Cores.CYAN}   [3] Sair{Cores.RESET}\n")
        
        choice = input(f"{Cores.YELLOW}   Escolha uma opção > {Cores.RESET}")
        
        if choice == '1':
            username = input(f"\n{Cores.YELLOW}[?] Digite o username do Roblox/TikTok do alvo: {Cores.CYAN}")
            if username:
                search_engine_deep_dive(username)
            else:
                print(f"{Cores.RED}[!] Username não pode ser vazio.{Cores.RESET}")
                time.sleep(1)
        elif choice == '2':
            banner()
            print(f"""
    {Cores.BOLD}{Cores.MAGENTA}DataStalker v1.0{Cores.RESET}
    
    Esta ferramenta realiza uma investigação de código aberto
    (OSINT) para encontrar dados publicamente disponíveis
    associados a um nome de usuário.
    
    Ela vasculha perfis conhecidos e usa técnicas de busca
    avançada para encontrar informações vazadas em pastes,
    fóruns e bancos de dados públicos.
    
    {Cores.CYAN}Autor: [Seu Nickname]{Cores.RESET}
    {Cores.CYAN}GitHub: [Link do seu GitHub]{Cores.RESET}
            """)
            input("\nPressione Enter para voltar ao menu...")
        elif choice == '3':
            print(f"\n{Cores.YELLOW}Encerrando...{Cores.RESET}")
            sys.exit(0)
        else:
            print(f"\n{Cores.RED}[!] Opção inválida, tente novamente.{Cores.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
