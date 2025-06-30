import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base de busca para imóveis em Goiânia
base_url = "https://www.zapimoveis.com.br/venda/imoveis/go+goiania/?pagina={}"

# Lista para armazenar os dados dos imóveis
dados_imoveis = []
num_paginas = 3  # Você pode aumentar esse número se quiser mais resultados

for pagina in range(1, num_paginas + 1):
    url = base_url.format(pagina)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro na página {pagina}: código {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    imoveis = soup.find_all('div', class_='simple-card__box')

    for imovel in imoveis:
        tipo = imovel.find('h2', class_='simple-card__title')
        preco = imovel.find('p', class_='simple-card__price')
        detalhes = imovel.find_all('li', class_='feature__item')
        link = imovel.find('a', class_='simple-card__link')

        tipo_imovel = tipo.text.strip() if tipo else ""
        preco_imovel = preco.text.strip() if preco else ""
        url_imovel = "https://www.zapimoveis.com.br" + link['href'] if link else ""

        quartos = banheiros = vagas = ""

        for item in detalhes:
            texto = item.text.strip().lower()
            if "quarto" in texto:
                quartos = texto
            elif "banheiro" in texto:
                banheiros = texto
            elif "vaga" in texto:
                vagas = texto

        dados_imoveis.append({
            "Tipo": tipo_imovel,
            "Preço": preco_imovel,
            "Quartos": quartos,
            "Banheiros": banheiros,
            "Vagas": vagas,
            "Link": url_imovel
        })

# Exporta os dados para Excel
df = pd.DataFrame(dados_imoveis)
df.to_excel("imoveis_goiania.xlsx", index=False)

print("✅ Planilha gerada com sucesso: imoveis_goiania.xlsx")
