# 1 : achat
# 0 : rien
# -1 : vente
from Compute.Indicator_analyze.MACD_Analyze import MACD_Analyze
from Compute.Indicator_analyze.RSI_Analyze import RSI_Analyze

class Model_macd_rsi:
    #TODO : memory filename à changer en memory descriptor
    def __init__(self, serve, memory_filename):
        self.serve = serve
        self.memory_filename = memory_filename

        # On regarde le dernier trade que l'on a effectué, si c'est une vente on peut de nouveau acheter
        try:
            with open(self.memory_filename, "r") as memory:
                self.last_trade = int(memory.readlines()[-1])
            memory.close()

        except:
            self.last_trade = -1

    def perform(self, dataframe):
        macd_analyze = MACD_Analyze(dataframe)
        macd = macd_analyze.perform()
        rsi_analyze = RSI_Analyze(dataframe)
        rsi = rsi_analyze.perform()

        # On cherche à acheter
        if self.last_trade == -1:
            if macd[-1] == 1 and (rsi[-1] == 1 or rsi[-1] == -1):
                with open(self.memory_filename, "a") as memory:
                    line = "1\n"
                    memory.writelines(line)
                memory.close()
                self.serve.buy()

        # On cherche à vendre

        if self.last_trade == 1:
            if macd[-1] == -1:
                with open(self.memory_filename, "a") as memory:
                    line = "-1\n"
                    memory.writelines(line)
                memory.close()
                self.serve.sell()







