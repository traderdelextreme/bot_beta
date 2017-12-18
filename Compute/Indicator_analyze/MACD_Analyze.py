import pandas as pd
from ..Indicator import Indicators

class MACD_Analyze:
    """
    Permet d'analyser l'indicateur et de renvoyer un tableau de (-1,0,1) (vente, rien, achat)
    """
    def __init__(self, dataFrame):
        self.df = dataFrame
        self.short_avg = 10
        self.long_avg = 26
        self.signal = 9


    def perform(self):
        ema_short = pd.Series(Indicators.ema(self.df, self.short_avg, 'C')['EMA_{}'.format(self.short_avg)], name='ema_short')
        ema_long = pd.Series(Indicators.ema(self.df, self.long_avg,'C')['EMA_{}'.format(self.long_avg)], name='ema_long')
        self.df = self.df.join(ema_short)
        self.df = self.df.join(ema_long)
        macd_values = self.df['ema_short'] - self.df['ema_long']
        macd = pd.Series(macd_values, name='macd')
        self.df = self.df.join(macd)
        print(self.df)


