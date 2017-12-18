# 1 : achat
# 0 : rien
# -1 : vente
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze

class Model_test:
    def __init__(self, serve):
        self.serve = serve

    def perform(self, dataframe):
        macd_analyze = MACD_Analyze(dataframe)
        signals_macd = macd_analyze.perform()

        if signals_macd[-1] == 1:
            self.serve.buy()
        elif signals_macd[-1] == -1:
            self.serve.sell()
        else:
            print("rien")

