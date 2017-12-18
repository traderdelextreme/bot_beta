from Watch.Bitrex_acquisition import Bittrex_acquisition
from Watch.Bitrex_acquisition import Bittrex_acquisition
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze
from Compute.Model_test import Model_test
from Serve.Serve_test import Serve_test
import time


market = "USDT-BTC"
tickInterval = "oneMin"
filename = "Data_Bitrex/data_min.csv"

"La classe utilisé pour l'acquisition des données"
acquisition = Bittrex_acquisition(filename, market, tickInterval)

"La classe utilisé par le model, pour donner ses ordres d'achat ou de vente"
server = Serve_test()

"Model d'achat ou de vente"
model = Model_test(server)


"Boucle mise à jour des données, et lancement du model de trade, toutes les minutes"
while(True):
    acquisition.update()
    model.perform(acquisition.get_dataframe())
    time.sleep(60)


