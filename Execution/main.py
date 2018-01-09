from Watch.Bitrex_acquisition import Bittrex_acquisition
from Watch.Bitrex_acquisition import Bittrex_acquisition
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze
from Compute.Model_macd_rsi import Model_macd_rsi
from Serve.Serve_test import Serve_test
import time
from stockstats import StockDataFrame
import pandas as pd

market = "USDT-BTC"
tickInterval = "oneMin"
filename = "Data_Bitrex/data_min.csv"

"La classe utilisé pour l'acquisition des données"
acquisition = Bittrex_acquisition(filename, market, tickInterval)

"La classe utilisé par le model, pour donner ses ordres d'achat ou de vente"
server = Serve_test()

# Fichier de mémoire de trade
memory_filename = "Memory/memory_macd_rsi_simulation.txt"

"Model d'achat ou de vente"
model = Model_macd_rsi(server, memory_filename)


"Boucle mise à jour des données, et lancement du model de trade, toutes les minutes"
while(True):
    acquisition.update()
    model.perform(acquisition.get_dataframe())
    time.sleep(60)

# df = pd.read_csv('Data_Bitrex/data_min.csv')
# #print(df.columns)
# df.rename(columns = {'C': 'Close', 'H':'High', 'L':'Low', 'V':'Volume', 'O':'Open'}, inplace = True)
# #print(df)
# stock = StockDataFrame.retype(df)
#
# #print(stock)
# stock = stock['macd']
#
#
# #ema = stock['macd_5_ema']
# #stock.set_index('macd')
# stock = StockDataFrame.retype(stock.to_frame('macd'))
# print(stock)
# stock = stock['macd_5_ema']
# print(stock[-1])
# #print(stock['macd'])
# #stock = stock.get(stock, stock['close'],12)
# #print(stock)
