from Watch.Bitrex_acquisition import Bittrex_acquisition
from Serve.Serve_test import Serve_test
from Compute.Model_bollinger import Model_bollinger
from Compute.Indicator_analyze.Bollinger_Analyze import Bollinger_Analyze

market = "USDT-BTC"
tickInterval = "oneMin"
filename = "../Data_Bitrex/data_min.csv"

"La classe utilisé pour l'acquisition des données"
acquisition = Bittrex_acquisition(filename, market, tickInterval)

serve = Serve_test()

dataframe = acquisition.get_dataframe()

model = Model_bollinger(serve, None)

bollinger = Bollinger_Analyze(dataframe[-100:])
print(bollinger.perform())

print(bollinger.get_indicator())