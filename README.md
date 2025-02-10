
---

# Esse é um script em python destinado ao download automático de arquivos PDF


1. Coloque o endereço do caminho onde os arquivos serão baixados na linha 16 (multi) ou linha 14 (mono).

2. Coloque o link do site na linha 109 (multi) ou linha 98 (mono).

- Mono: Versão do código mais simples e sequencial, baixa 1 arquivo por vez.

Lento, mas usa pouca rede e o risco de bloqueio é pequeno.

- Multi: Usa ThreadPoolExecutor permitindo download's paralelos em páginas paralelas. Busca diferentes páginas ao mesmo tempo.

Bem mais rápido, mas usa mais rede e processamento, tendo risco de bloqueio (falha de download) maior.

---
---
---

> **Como funciona**: O script acessa a página e busca *no corpo principal da página* links de PDF's. 
> Caso não ache, acessa links que estejam *no corpo principal da página* em busca de links de PDF's.
>
> Após achar um link de PDF, ele cria uma pasta raiz do endereço principal fornecido e cria sub-pastas de acordo com os links de pdf que ele vai encontrando.
>
> **Ele não cria pastas vazias.**

---
---
---

> Se estiver lento ou se o servidor estiver bloqueando conexões por excesso de requisições,
> Altere o número de threads:
> ~~~python
> ( max_workers=? )
> ~~~
> Ou altere o número de atraso:
> ~~~python
> ( time.sleep(?) )
> ~~~

---
---
---

# Como usar

Após configurar o diretório e o link na aba indicada:

1. Instale os requirements
**pip install -r requirements.txt**
2. Execute o script
**python multi.py**
3. Caso precise interromper
**Ctrl + C**

---
---
---

# Crie o ambiente virtual

> ```bash
> python -m venv .venv
> source .venv/bin/activate  # Linux/macOS
> .venv\Scripts\activate      # Windows
> pip install -r requirements.txt
>

---

## Créditos
---

██████╗░███████╗██████╗░██████╗░░█████╗░░█████╗░███╗░░░███╗██████╗░░█████╗░
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗░████║██╔══██╗██╔══██╗
██████╔╝█████╗░░██║░░██║██████╔╝██║░░██║███████║██╔████╔██║██║░░██║██║░░╚═╝
██╔═══╝░██╔══╝░░██║░░██║██╔══██╗██║░░██║██╔══██║██║╚██╔╝██║██║░░██║██║░░██╗
██║░░░░░███████╗██████╔╝██║░░██║╚█████╔╝██║░░██║██║░╚═╝░██║██████╔╝╚█████╔╝
╚═╝░░░░░╚══════╝╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░░╚════╝░

Copyright (C) 2025 by PedroAMDC