from Watch.Bitrex_acquisition import Bittrex_acquisition
from Compute.Model_macd_rsi import Model_macd_rsi
from Serve.Serve_test import Serve_test
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze
from Compute.Indicator_analyze.RSI_Analyze import RSI_Analyze


market = "USDT-BTC"
tickInterval = "oneMin"
filename = "../Data_Bitrex/data_min.csv"

"La classe utilisé pour l'acquisition des données"
acquisition = Bittrex_acquisition(filename, market, tickInterval)

serve = Serve_test()

dataframe = acquisition.get_dataframe()

memory_filename = "Memory/memory_macd_rsi_simulation.txt"

macd_analyze = MACD_Analyze(dataframe)
macd = macd_analyze.perform()
rsi_analyze = RSI_Analyze(dataframe)
rsi = rsi_analyze.perform()

last_trade = -1
euro = 100
bitcoin = 0

for i in range(10000, dataframe.__len__()):
    # On cherche à acheter
    if last_trade == -1:
        if rsi[i] == -1:
            rate = dataframe['close'][i]
            bitcoin = euro / rate
            euro = 0
            last_trade = 1
            line = "buy, rate : " + rate.__str__()
            print(line)

    # On cherche à vendre

    if last_trade == 1:
        if macd[i] == -1 and rsi[i] == 1:
            rate = dataframe['close'][i]
            euro = bitcoin*rate
            bitcoin = 0
            last_trade = -1
            line = "sell, rate : " + rate.__str__()

            print(line)

print(euro)
print(bitcoin)
euro = euro + bitcoin*dataframe['close'][-1]
line = " euro : "+euro.__str__()
print(line)



# for i in range(100, dataframe.__len__()):
#    model = Model_macd_rsi(serve, memory_filename)
#    model.perform(dataframe[i:])
#    print(dataframe[i:])
