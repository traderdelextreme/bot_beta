import pandas as pd
from ..Tools import Tools

class MACD_Analyze:
    """
    Permet de calculer le macd sur les données et de renvoyer un tableau de (-1,0,1) (vente, rien, achat)

    """
    def __init__(self, dataFrame):
        self.df = dataFrame
        self.short_avg = 12
        self.long_avg = 26
        self.signal = 9

    def get_signals(self, macd, ema_signal):
        """
        Donne un tableau de signaux (-1,0,1) =(vente, rien, achat)
        en fonction de la stratégie du macd

        achat : le macd passe au-dessus de la ligne de signal
        :param macd:
        :param ema_signal:
        :return: tableau de signaux
        """
        signals_trade = []
        signal_repeat = 0
        signals_trade.append(0)
        for i in range(1, macd.__len__()):
            if macd[i-1] > ema_signal[i-1] and macd[i] < ema_signal[i]:
                signal_repeat = 5
                signals_trade.append(-1)
            elif macd[i-1] < ema_signal[i-1] and macd[i] > ema_signal[i]:
                signal_repeat = 5
                signals_trade.append(1)
            else:
                if signal_repeat > 0 :
                    signal_repeat = signal_repeat - 1
                    signals_trade.append(signals_trade[-1])
                else:
                    signals_trade.append(0)
        return signals_trade

    def perform(self):
        ema_short = pd.Series(Tools.ema(self.df, self.short_avg, 'C')['EMA_{}'.format(self.short_avg)], name='ema_short')
        ema_long = pd.Series(Tools.ema(self.df, self.long_avg, 'C')['EMA_{}'.format(self.long_avg)], name='ema_long')
        self.df = self.df.join(ema_short)
        self.df = self.df.join(ema_long)
        macd_values = self.df['ema_short'] - self.df['ema_long']
        macd = pd.Series(macd_values, name='macd')
        self.df = self.df.join(macd)

        ema_signal = pd.Series(Tools.ema(self.df, self.signal, 'macd')['EMA_{}'.format(self.signal)], name='ema_signal')
        self.df = self.df.join(ema_signal)


        signals_trade = pd.Series(self.get_signals(self.df['macd'],self.df['ema_signal']), name='signals_trade', index=self.df.index.values)
        self.df = self.df.join(signals_trade)
        return self.df['signals_trade']

