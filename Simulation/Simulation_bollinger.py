from Watch.Bitrex_acquisition import Bittrex_acquisition
from Serve.Serve_test2 import Serve_test2
from Compute.Model_bollinger import Model_bollinger
from Compute.Tools.Memory import Memory


market = "USDT-BTC"
tickInterval = "fiveMin"
filename = "../Data_Bitrex/data_five_min.csv"

"La classe utilisé pour l'acquisition des données"
acquisition = Bittrex_acquisition(
    filename, market, tickInterval)
acquisition.update()

dataframe = acquisition.get_dataframe()



parameter_offset = 0
parameter_stoploss  = 0
best_bilan = 0

for j in range(0,20):
    offset = j*0.005
    for f in range(0,20):
        stoploss = f*0.005

        memory = Memory()
        memory.add("{}")
        serve = Serve_test2()
        model = Model_bollinger(serve, memory, offset, stoploss)

        print("offset : " + offset.__str__()+" stoploss : " + stoploss.__str__())
        for i in range(4894, 5470):
            model.perform(dataframe[i - 100:i])
        bilan = serve.bilan()
        if bilan > best_bilan:
            parameter_offset = offset
            parameter_stoploss = stoploss
            best_bilan = bilan



