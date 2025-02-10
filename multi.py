import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import concurrent.futures

# Função para limpar nomes de arquivos e pastas
def limpar_nome(nome):
    caracteres_invalidos = '<>:"/\\|?*'  # Caracteres proibidos em nomes de arquivos/pastas
    nome = ''.join(c if c not in caracteres_invalidos else '_' for c in nome)
    nome = nome.replace("\n", "_").replace("\r", "_").strip()
    return nome[:100]  # Limita a 100 caracteres para evitar erros com nomes longos

# Função principal para buscar e baixar PDFs
def baixar_pdfs(url, pasta_destino=r"CAMINHO DO ARQUIVO AQUI", visitados=None, pasta_principal=None, executor=None): 
    if visitados is None:
        visitados = set()
    
    if url in visitados:
        print(f"Página já visitada: {url}. Pulando...")
        return
    
    visitados.add(url)
    
    try:
        response = requests.get(url, timeout=30)
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
    
    corpo_principal = soup.find("main") or soup.find("div", class_="content") or soup.body
    links = corpo_principal.find_all("a", href=True) if corpo_principal else []
    
    pdfs_encontrados = False
    arquivos_para_baixar = []
    
    for link in links:
        href = link["href"].strip()
        if href.endswith(".pdf"):
            pdfs_encontrados = True
            pdf_url = urljoin(url, href)
            nome_arquivo = limpar_nome(href.split("/")[-1])
            arquivos_para_baixar.append((pdf_url, os.path.join(pasta_principal, nome_arquivo)))
    
    if pdfs_encontrados:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(baixar_arquivo, pdf_url, caminho_arquivo): pdf_url for pdf_url, caminho_arquivo in arquivos_para_baixar}
            for future in concurrent.futures.as_completed(futures):
                future.result()
    else:
        print("Nenhum PDF encontrado. Buscando em links internos...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for link in links:
                href = link["href"].strip()
                if not href.endswith(".pdf") and not href.startswith("#"):
                    sub_url = urljoin(url, href)
                    nome_subpasta = limpar_nome(link.text.strip().replace(" ", "_")) or "Subpagina"
                    pasta_sub = os.path.join(pasta_principal, nome_subpasta)
                    print(f"Acessando: {sub_url} e salvando em {pasta_sub}")
                    futures.append(executor.submit(baixar_pdfs, sub_url, pasta_destino, visitados, pasta_sub, executor))
            for future in concurrent.futures.as_completed(futures):
                future.result()

# Função para baixar um arquivo PDF com suporte a retomada
def baixar_arquivo(url, caminho):
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            headers = {}
            if os.path.exists(caminho):
                tamanho_baixado = os.path.getsize(caminho)
                headers['Range'] = f'bytes={tamanho_baixado}-'
            else:
                tamanho_baixado = 0
            
            response = requests.get(url, stream=True, timeout=30, headers=headers)
            if response.status_code in [200, 206]:
                modo_abertura = "ab" if tamanho_baixado else "wb"
                with open(caminho, modo_abertura) as f:
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
        time.sleep(5)
    print(f"Falha ao baixar {url} após {tentativas} tentativas.")

if __name__ == "__main__":
    url_pagina = "LINK DA PÁGINA AQUI"
    baixar_pdfs(url_pagina)
