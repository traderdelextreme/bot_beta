import pandas
import time
from Acquisition.Bitrex_acquisition import Bittrex_acquisition


market = "USDT-BTC"
tickInterval = "oneMin"
filename = "Data_Bitrex/data_min.csv"
bitrex = Bittrex_acquisition(filename, market, tickInterval)

#df = bitrex.init()
bitrex.update()

#while True:
    #time.sleep(60)
    #bitrex.update()