import pandas as pd
from stockstats import StockDataFrame

class Bollinger_Analyze:
    def __init__(self, dataframe):
        self.df = dataframe
        self.repetition_signal = 0

    def get_signals(self, close, boll_ub, boll_lb):
        """
                Donne un tableau de signaux (-1,0,1) =(vente, rien, achat)
                en fonction de la stratégie du bollinger, -1 lorsque le cours touche
                la bande supérieur, 1 lorsque le cours touche la bande supérieur

                :param close:
                :param boll_ub: borne superieur
                :param boll_lb: borne inférieur
                :return: tableau de signaux
                """

        signals_trade = []
        signal_repeat = 0

        for i in range(0, close.__len__()):
            if close[i] > boll_ub[i]:
                signal_repeat = self.repetition_signal
                signals_trade.append(-1)
            elif close[i] < boll_lb[i]:
                signal_repeat = self.repetition_signal
                signals_trade.append(1)
            else:
                if signal_repeat > 0:
                    signal_repeat = signal_repeat - 1
                    signals_trade.append(signals_trade[-1])
                else:
                    signals_trade.append(0)

        return signals_trade


    def get_indicator(self):
        """
        Renvoie les valeurs de cet indicateur
        :return:
        """
        sdf = StockDataFrame.retype(self.df)
        boll_ub = sdf['boll_ub'].to_frame('boll_ub')
        boll_lb = sdf['boll_lb'].to_frame('boll_lb')

        indicators = boll_ub.join(boll_lb)

        return indicators

    def perform(self):
        sdf = StockDataFrame.retype(self.df)

        boll_ub = sdf['boll_ub']
        boll_lb = sdf['boll_lb']
        close = sdf['close']

        signals_trade = pd.Series(self.get_signals(close, boll_ub, boll_lb), name='signals_trade', index=self.df.index.values)

        return signals_trade


