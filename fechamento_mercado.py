import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import pandas as pd

url = "http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/"
ret = requests.get(url)
soup = bs(ret.text)

data = soup.find("span", {"id": "x-data-pregao"})

caminho_chrome_driver = r"chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(caminho_chrome_driver)
driver.get(url)
soup = bs(driver.page_source, "html.parser")

data_pregao = soup.find("span", {"id": "x-data-pregao"}).text
status_pregao = soup.find("span", {"id": "x-status-pregao"}).text

volume = soup.find("span", {"id": "x-volume-pregao"}).text
negocios = int(soup.find("span", {"id": "x-qtd-pregao"}).text.replace(".", ""))
print(
    f"Data: {data_pregao} \nStatus pregão: {status_pregao}, com total de {negocios} negócios, com volume total de {volume}"
)

iframe_path = soup.find("div", {"id": "tradingview-widget-acoes"})
iframe_path


def get_variation(idx):
    url2 = f"https://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/{idx}"
    driver.get(url2)
    soup2 = bs(driver.page_source)
    s2json = json.loads(soup2.text)

    status = s2json["BizSts"]["cd"]
    data_hora = s2json["Msg"]["dtTm"]

    if status == "OK":
        print(f"Maiores altas do {idx}:")
        for item in s2json["SctyHghstIncrLst"]:
            ativo = item["symb"]
            descricao = item["desc"]
            preco_atual = item["SctyQtn"]["curPrc"]
            variacao_perc = item["SctyQtn"]["prcFlcn"]
            print(
                f"{ativo} - Preço atual: {preco_atual} - Variação percentual {round(variacao_perc,2)}%"
            )
        print(f"Maiores baixas do {idx}:")
        for item in s2json["SctyHghstDrpLst"]:
            ativo = item["symb"]
            descricao = item["desc"]
            preco_atual = item["SctyQtn"]["curPrc"]
            variacao_perc = item["SctyQtn"]["prcFlcn"]
            print(
                f"{ativo} - Preço atual: {preco_atual} - Variação percentual {round(variacao_perc,2)}%"
            )


indexes = ["ibov", "ifix", "smll"]
for item in indexes:
    get_variation(item)

driver.close()
