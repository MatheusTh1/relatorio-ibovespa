import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import win32com.client as win32

minhas_acoes = ["MGLU3.SA"]
codigos_de_negociacao = ["^BVSP", "BRL=X"]

hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days = 365)
dados_mercado = yf.download(codigos_de_negociacao,um_ano_atras,hoje)
periodo = um_ano_atras.date() - hoje.date()

if __name__ == '__main__':
    print("Abaixo consta a cotação em um periodo de ", periodo)
print(dados_mercado)