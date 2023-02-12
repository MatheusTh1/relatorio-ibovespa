import yfinance as yf
import pandas as pd
import quantstats as qs

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
# print(retorno_6_meses)


    #retirando empresas que não estava na ibov em tal epoca

for data in retorno_6_meses.index:
    for empresas in retorno_6_meses.columns:

            #realizando a condicional e retirando o .sa do nome da empresa do get do yfinance
            if empresas.replace(".SA", "") not in composicao_historica.loc[:, data].to_list():
                retorno_6_meses.loc[data, empresas] = pd.NA

    #manipular os dados, criar as matrizes com função lambdam e gerar um rankig para controlar a carteira

ranking = retorno_6_meses.rank(axis = 1, ascending = False)
quantidade_de_acoes = 10

    # applymap - se for menor que 11 passa o 1 senão 0 para qualificar as 10 melhores empresas do periodo
carteira = ranking.applymap(lambda x: 1 if x <= quantidade_de_acoes else 0)
# print(carteira)


            #------------FILTRANDO A MELHOR CARTEIRA------------
retorno_mensal = dados_cotacoes.resample("M").last().pct_change(periods = 1)

retorno_mensal = retorno_mensal.drop(retorno_mensal.index[:7], axis = 0)

retorno_mensal.index = carteira.index

#cruzar matrizes

retorno_modelo = (retorno_mensal * carteira).sum(axis = 1)/quantidade_de_acoes

print(retorno_modelo)


#------------------Inserindo grafico---

qs.extend_pandas()

retorno_modelo.plot_monthly_heatmap()

#-------------Calcular com Ibov-----

ibovespa = yf.download("^BVSP", start= "2015-12-30", end="2022-12-31")["Adj Close"]

ibovespa = ibovespa.resample("M").last().pct_change().dropna()

print(ibovespa)


#-------------Comparar o modeldo contra o ibovespa----------
retorno_acumulado_modelo = (1+retorno_modelo).cumprod() - 1
retorno_acumulado_ibov = (1+ibovespa).cumprod() - 1

retorno_acumulado_modelo.plot_monthly_heatmap()
retorno_acumulado_ibov.plot_monthly_heatmap()


#--------------como verificar mes a mes o rentabilidade do modelo x ibov--
ganhos_modelos = retorno_modelo - ibovespa
ganhos_modelos.plot_monthly_heatmap()
