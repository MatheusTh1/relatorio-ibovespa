import pandas as pd
import datetime
import win32com.client as win32
import yfinance as yf
from matplotlib import pyplot as plt

# import matplotlib.pyplot as plt
# import matplotlib.style as style

if __name__ == '__main__':
    print("Relatorio mercado financeiro!")

#-----------------BUSCANDO OS DADOS E SENTANDO--------
minhas_acoes = ["MGLU3.SA"]

# Definindo quais ativos vou pegar as cotações do yahoo
codigos_de_negociacao = ["^BVSP", "BRL=X"]

# Pegando a data de hoje
hoje = datetime.datetime.now()

# pegando um perido de 1 ano a partir de hoje
um_ano_atras = hoje - datetime.timedelta(days=365)

# Baixando os dados do yahoo conforme parametros acima
dados_mercado = yf.download(codigos_de_negociacao, um_ano_atras, hoje)
periodo = um_ano_atras.date() - hoje.date()


#-------------MANIPULANDO OS DADOS-------------

# Renomeando os nomes das tabelas
dados_fechamento = dados_mercado['Adj Close']
dados_fechamento.columns = ["dolar", "ibovespa"]

# Excluindo dados onde está vazio e pegando os 3 primeiros dados
exclua_dados_faltante = dados_fechamento.dropna()
primeiros_50_dados = exclua_dados_faltante.head(20)

print("Abaixo consta a cotação em um periodo de", periodo)
print(primeiros_50_dados)

# Pegando e exibindos os dados por ano e por mes e por dia
dados_anuais = dados_fechamento.resample("y").last()
dados_mensais = dados_fechamento.resample("M").last()

retorno_anual = dados_anuais.pct_change().dropna()
retorno_mensal = dados_mensais.pct_change().dropna()
retorno_diario = dados_fechamento.pct_change().dropna()

print("Dados anuais", retorno_anual)
print("Dados mensais", retorno_mensal)
print("Dados diarios", retorno_diario)


#--------------LOCALIZANDO DADOS DENTRO DE UM DATAFRAME---------------------#

# loc -> referencia elementos a partir pelo nome
retorno_fev_17_2022 = retorno_diario.loc["2022-02-17", "ibovespa"]
print(retorno_fev_17_2022)

# iloc -> faz o mesmo mas por uma matriz, como se fosse o procv do excel
retorno_fev_17_2022 = retorno_diario.iloc[2, 1]
print(retorno_fev_17_2022)

# Pegando sempre o fechamento diariamente
retorno_diario_ibov = retorno_diario.iloc[-1, 1]
print("Fechamento do ultimo dia do ibov", retorno_diario_ibov)

# Transformando em %
retorno_diario_ibov_em_perct = round((retorno_diario_ibov * 100), 2)
print(retorno_diario_ibov_em_perct, "%")


#--------------------GERANDO O GRAFICO-------------------#

plt.style.use("cyberpunk")
# Definindo que o eixo vertical será os dados do ibov e os index as datas
dados_fechamento.plot(y = "ibovespa", use_index = True, legend = False)
plt.title("Ibovespa")

plt.savefig("ibovespa.png", dpi = 300)
plt.show()


#--------------------ENVIANDO OS DADOS POR EMAIL-------------------#

# Logando no outlook
outlook = win32.Dispatch("outlook.application")

email = outlook.CreateItem(0)

email.To = "matheushenriquesilva.th@gmail.com"
email.Subject = "Relatório Diário Ibov"
nome = "Matheus Henrique"

# Criando uma string personalizada com quebra de linhas
email.Body = f''' Olá {nome}, o fechamento do Ibov foi de {retorno_diario_ibov_em_perct}.

Obrigado!
'''

# Anexando arquivo e enviando o email
anexo_ibov = r"C:\Development\Python Projects\ibov-fechamento-relatorio\ibov\ibovespa.png"

email.Attachments.Add(anexo_ibov)

email.Send()