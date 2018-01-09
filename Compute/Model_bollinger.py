from stockstats import StockDataFrame
from Compute.Indicator_analyze.Bollinger_Analyze import Bollinger_Analyze
import json

FOLLODOWN = 'followdown'
FOLLOWUP = 'followup'
RATE = 'rate'
OFFSET = 'offset'
VOLUME = 'volume'
TARGET = 'target'
BUY = 'buy'
SELL = 'sell'
STOPLOSS = 'stoploss'


class Model_bollinger:
    def __init__(self, serve, memory, offset=0.01, stoploss=0.05):
        self.memory = memory
        self.serve = serve
        self.offset = offset
        self.volume = 1
        self.stoploss = stoploss

    def perform(self, dataframe):
        memory = json.loads(self.memory.read(-1))

        bollinger = Bollinger_Analyze(dataframe)
        signal_bollinger = bollinger.perform()
        rate_current = dataframe['close'][-1]

        #print('signal bollinger : ' + signal_bollinger[-1].__str__())
        #print('rate current : ' + rate_current.__str__())

        #print(memory)

        # On cherche un signal de vente
        if memory.keys().__contains__(BUY):
            rate_stoploss = memory[BUY][STOPLOSS]

            # On vérifie le stoploss
            if rate_current < rate_stoploss:
                self.serve.sell(rate_current, self.volume)
                sell = {}
                sell[RATE] = rate_current
                sell[VOLUME] = self.volume

                order = {}
                order[SELL] = sell

                line = json.dumps(order)
                self.memory.add(line)
                print("stoploss!!!!!!!!!")

            # On a le signal de vente
            elif signal_bollinger[-1] == -1:
                followup = {}
                followup[RATE] = rate_current
                followup[OFFSET] = self.offset
                followup[VOLUME] = self.volume
                followup[STOPLOSS] = memory[BUY][STOPLOSS]
                followup[TARGET] = rate_current*(1-self.offset)

                order = {}
                order[FOLLOWUP] = followup

                line = json.dumps(order)
                self.memory.add(line)

        # On suit la courbe pour acheter
        elif memory.keys().__contains__(FOLLODOWN):
            rate_min = memory[FOLLODOWN][RATE]
            rate_target = memory[FOLLODOWN][TARGET]

            # La courbe continue de descendre on met a jour le rate_min
            if rate_current < rate_min:
                followdown = {}
                followdown[RATE] = rate_current
                followdown[OFFSET] = self.offset
                followdown[VOLUME] = self.volume
                target = rate_current*(1+self.offset)
                followdown[TARGET] = target

                order = {}
                order[FOLLODOWN] = followdown

                line = json.dumps(order)
                self.memory.add(line)
            else:
                # On a depasse l'offset, on doit acheter
                if rate_current > rate_target:
                    # On achete
                    self.serve.buy(rate_current, self.volume)
                    buy = {}
                    buy[RATE] = rate_current
                    buy[VOLUME] = self.volume

                    # On place le stoploss
                    buy[STOPLOSS] = rate_current*(1-self.stoploss)

                    order = {}
                    order[BUY] = buy

                    line = json.dumps(order)
                    self.memory.add(line)
                # On a pas depasse l'offset, on ne fait rien
                else:
                    None


        # On suit la courbe pour vendre, on verifie le stoploss
        elif memory.keys().__contains__(FOLLOWUP):
            rate_max = memory[FOLLOWUP][RATE]
            rate_target = memory[FOLLOWUP][TARGET]
            rate_stoploss = memory[FOLLOWUP][STOPLOSS]

            # On vérifie le stop loss
            if rate_current < rate_stoploss:
                self.serve.sell(rate_current, self.volume)
                sell = {}
                sell[RATE] = rate_current
                sell[VOLUME] = self.volume

                order = {}
                order[SELL] = sell

                line = json.dumps(order)
                self.memory.add(line)
                print("stoploss!!!!!!!!!")

            # On est en-dessous de l'offset on vend
            elif rate_current < rate_target:
                self.serve.sell(rate_current, self.volume)
                sell = {}
                sell[RATE] = rate_current
                sell[VOLUME] = self.volume

                order = {}
                order[SELL] = sell

                line = json.dumps(order)
                self.memory.add(line)

            # On met à jour le rate_max
            elif rate_current > rate_max:
                followup = {}
                followup[RATE] = rate_current
                followup[OFFSET] = self.offset
                followup[VOLUME] = self.volume
                followup[STOPLOSS] = rate_stoploss
                followup[TARGET] = rate_max*(1-self.offset)


                order = {}
                order[FOLLOWUP] = followup

                line = json.dumps(order)
                self.memory.add(line)

            # On ne fait rien
            else:
                None

        # On cherche un signal d'achat
        else:

            # Signal d'achat
            if signal_bollinger[-1] == 1:
                followdown = {}
                followdown[RATE] = rate_current
                followdown[OFFSET] = self.offset
                followdown[VOLUME] = self.volume
                target = rate_current*(1+self.offset)
                followdown[TARGET] = target

                stoploss = {}
                stoploss[RATE] = self.stoploss
                stoploss[VOLUME] = self.volume

                order = {}
                order[FOLLODOWN] = followdown

                line = json.dumps(order)
                self.memory.add(line)

