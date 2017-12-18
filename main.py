from Watch.Bitrex_acquisition import Bittrex_acquisition
from Watch.Bitrex_acquisition import Bittrex_acquisition
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze

market = "USDT-BTC"
tickInterval = "oneMin"
filename = "Data_Bitrex/data_min.csv"
bitrex = Bittrex_acquisition(filename, market, tickInterval)

macd_analyze = MACD_Analyze(bitrex.get_dataframe())
macd_analyze.perform()
