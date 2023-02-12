from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

if __name__ == '__main__':
    print("Automação google")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# url = "https://www.b3.com.br/pt_br"
# driver.get(url)


#-------FLUXO DE GET DADOS------------
#1 - [x] abri o site
#2 - [ ] mudar a visualização para 100
#3 - [ ] ler a tabela
#4 - [ ] avançar todas as paginas
#5 - [ ] trocar para outra categoria
#6 - [ ]  vler todas as tabelas dessa outra categoria


#-------PROCESSAMENTO DE DADOS------------

# 1 abrir o site.
url = "https://www.etf.com/etfanalytics/etf-finder"
driver.get(url)

logs = driver.get_log("browser")
for log_entry in logs:
    print(log_entry)

# #2 mudar a visualização para 100.
# driver.find_element("xpath", )



