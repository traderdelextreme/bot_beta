import pandas as pd
from stockstats import StockDataFrame

class RSI_Analyze:
    """
    Permet de calculer le RSI, renvoie
    -1: rsi plus petit que la borne basse,
    0 : rsi entre les deux bornes
    1 : rsi plus grand que la borne superieur
    """
    def __init__(self, dataFrame):
        self.df = dataFrame
        self.period = 12
        self.borne_sup = 65
        self.borne_inf = 15

    def get_signals(self, rsi):
        signal_trade = []
        for value in rsi:
            if value <= self.borne_inf:
                signal_trade.append(-1)
            elif value >= self.borne_sup:
                signal_trade.append(1)
            else:
                signal_trade.append(0)
        return signal_trade

    def perform(self):
        sdf = StockDataFrame.retype(self.df)
        series_rsi = sdf['rsi_{}'.format(self.period)]

        signals_trade = pd.Series(self.get_signals(series_rsi), name='signals_trade', index=self.df.index.values)

        return signals_trade

