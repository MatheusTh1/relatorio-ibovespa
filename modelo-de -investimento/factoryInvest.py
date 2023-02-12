import yfinance as yf
import pandas as pd
# import quantstats as qs

if __name__ == '__main__':
    print("Factory Investments")

        #-----------LENDO OS DADOS DA PLANILHA------------
composicao_historica = pd.read_excel(r"C:\Development\Python Projects\ibov_materials\composicao_ibov.xlsx")
lista_acoes = pd.read_excel(r"C:\Development\Python Projects\ibov_materials\composicao_ibov.xlsx", sheet_name = "lista_acoes")
# print(composicao_historica)


        # -----------PUXAR AS COTACOES DE TODAS AS ACOES------------
dados_cotacoes = (yf.download(lista_acoes["tickers"].to_list(),
                             start = "2015-06-30", end = "2022-12-31")["Adj Close"])

    #defininindo o indice em data e ordendando
dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)
dados_cotacoes = dados_cotacoes.sort_index()


    #calculando o retorno, retirando todos as cotaçoes vazias, porém esta estipulando que todos os elementos da linha seja vazio e retirando a ultima linha tb
retorno_6_meses = (dados_cotacoes.resample("M").last().pct_change(periods = 6).dropna(axis = 0, how = "all").drop("2022-12-31"))
print(retorno_6_meses)


    #retirando empresas que não estava na ibov em tal epoca

for data in retorno_6_meses.index:
    for empresas in retorno_6_meses.columns:

            #realizando a condicional e retirando o .sa do nome da empresa do get do yfinance
            if empresas.replace(".SA", "") not in composicao_historica.loc[:, data].to_list():
                retorno_6_meses.loc[data, empresas] = pd.NA


