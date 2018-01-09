import pandas as pd
from stockstats import StockDataFrame

class MACD_Analyze:
    """
    Permet de calculer le macd sur les données et de renvoyer un tableau de (-1,0,1) (vente, rien, achat)

    """
    def __init__(self, dataFrame):
        self.df = dataFrame
        self.short_avg = 12
        self.long_avg = 26
        self.signal = 9
        "Repition du signal, après le vrai signal"
        self.repetition_signal = 5


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
                signal_repeat = self.repetition_signal
                signals_trade.append(-1)
            elif macd[i-1] < ema_signal[i-1] and macd[i] > ema_signal[i]:
                signal_repeat = self.repetition_signal
                signals_trade.append(1)
            else:
                if signal_repeat > 0 :
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

        series_macd = sdf['macd']
        sdf_macd = StockDataFrame.retype(series_macd.to_frame('macd'))

        series_ema_signal_macd = sdf_macd['macd_5_ema']

        indicators = series_macd.join(series_ema_signal_macd)

        return indicators

    def perform(self):
        sdf = StockDataFrame.retype(self.df)

        series_macd = sdf['macd']
        sdf_macd = StockDataFrame.retype(series_macd.to_frame('macd'))

        series_ema_signal_macd = sdf_macd['macd_5_ema']
        sdf_ema_signal_macd = StockDataFrame.retype(series_ema_signal_macd.to_frame('ema_signal_macd'))

        signals_trade = pd.Series(self.get_signals(sdf_macd['macd'],sdf_ema_signal_macd['ema_signal_macd']), name='signals_trade', index=self.df.index.values)

        return signals_trade

