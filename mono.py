import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def limpar_nome(nome):
    # Remove caracteres inválidos para nomes de pastas no Windows
    caracteres_invalidos = '<>:"/\\|?*'
    for c in caracteres_invalidos:
        nome = nome.replace(c, "_")
    return nome.strip()

def baixar_pdfs(url, pasta_destino=r"CAMINHO DO ARQUIVO AQUI", visitados=None, pasta_principal=None):
    if visitados is None:
        visitados = set()
    
    if url in visitados:
        print(f"Página já visitada: {url}. Pulando...")
        return
    
    visitados.add(url)
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Erro ao acessar a página.")
            return
    except requests.exceptions.Timeout:
        print(f"Timeout ao tentar acessar {url}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    titulo_pagina = limpar_nome(soup.title.string.strip().replace(" ", "_")) if soup.title else "PDFs_Baixados"
    
    if pasta_principal is None:
        pasta_principal = os.path.join(pasta_destino, titulo_pagina)
    os.makedirs(pasta_principal, exist_ok=True)
    
    # Considera apenas os links dentro do corpo principal da página
    corpo_principal = soup.find("main") or soup.find("div", class_="content") or soup.body
    links = corpo_principal.find_all("a", href=True) if corpo_principal else []
    
    pdfs_encontrados = False
    arquivos_para_baixar = []
    
    for link in links:
        href = link["href"]
        if href.endswith(".pdf"):
            pdfs_encontrados = True
            pdf_url = urljoin(url, href)
            nome_arquivo = href.split("/")[-1]
            arquivos_para_baixar.append((pdf_url, nome_arquivo))
    
    if pdfs_encontrados:
        for pdf_url, nome_arquivo in arquivos_para_baixar:
            caminho_arquivo = os.path.join(pasta_principal, nome_arquivo)
            if not os.path.exists(caminho_arquivo):  # Evita baixar o mesmo arquivo mais de uma vez
                baixar_arquivo(pdf_url, caminho_arquivo)
                print(f"Baixado: {caminho_arquivo}")
            else:
                print(f"Arquivo já existe: {caminho_arquivo}")
    else:
        print("Nenhum PDF encontrado. Buscando em links internos...")
        for link in links:
            href = link["href"]
            if not href.endswith(".pdf") and not href.startswith("#") and href.startswith("http"):
                sub_url = urljoin(url, href)
                nome_subpasta = limpar_nome(link.text.strip().replace(" ", "_")) or "Subpagina"
                pasta_sub = os.path.join(pasta_principal, nome_subpasta)
                print(f"Acessando: {sub_url} e salvando em {pasta_sub}")
                baixar_pdfs(sub_url, pasta_destino, visitados, pasta_sub)

def baixar_arquivo(url, caminho):
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(caminho, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Baixado: {caminho}")
                return
            else:
                print(f"Erro ao baixar {url}. Código: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Timeout ao tentar acessar {url}. Tentativa {tentativa + 1} de {tentativas}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
        time.sleep(5)  # Aguarda 5 segundos antes de tentar de novo
    print(f"Falha ao baixar {url} após {tentativas} tentativas.")

if __name__ == "__main__":
    url_pagina = "LINK DA PÁGINA AQUI"
    baixar_pdfs(url_pagina)
