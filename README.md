# DataStalker 🕵️‍♂️

DataStalker é uma ferramenta de OSINT (Open Source Intelligence) para Termux, projetada para fazer uma "varredura profunda" na internet em busca de informações associadas a um nome de usuário do Roblox ou TikTok.

Ela automatiza o processo de "doxxing" legal, encontrando apenas o que já está disponível publicamente, mas que seria difícil de encontrar manualmente.

## ✨ Como Funciona?

A ferramenta não hackeia nada. Ela age como um detetive digital incansável, realizando as seguintes ações:

1.  **Verificação de Plataformas**: Confirma a existência de perfis no Roblox e TikTok.
2.  **Google Dorking Avançado**: Utiliza consultas de busca especiais (`dorks`) para encontrar o nome de usuário em sites de vazamento de texto (como Pastebin), fóruns e em discussões onde dados como IPs, e-mails ou nomes reais podem ter sido expostos.
3.  **Análise de Snippets**: Analisa os resultados da busca em busca de palavras-chave sensíveis (como "ip", "password", "leak", "dox") e destaca os links mais promissores.
4.  **Relatório Consolidado**: Apresenta todos os achados em um relatório final, fácil de ler.

## 🚀 Instalação (Termux)

A instalação é projetada para ser rápida e fácil.

```bash
# 1. Atualize o Termux e instale o Git
pkg update -y && pkg upgrade -y
pkg install git -y

# 2. Clone o repositório do DataStalker
git clone https://github.com/dqrkveil01/Data-Stalker/

# 3. Entre no diretório da ferramenta
cd data-stalker

# 4. Execute o script de instalação para preparar o ambiente
bash install.sh
```

## ⚙️ Como Usar

Com tudo instalado, iniciar o DataStalker é simples:

```bash
python stalker.py
```

Você será recebido por um menu principal:

- **`[1] Iniciar Varredura por Username`**: A função principal. Ela pedirá o nome de usuário do alvo e começará a caçada.
- **`[2] Sobre`**: Informações sobre a ferramenta.
- **`[3] Sair`**: Fecha o programa.
