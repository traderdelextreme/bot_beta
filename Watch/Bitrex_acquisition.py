import pandas as pd
from bittrex import Bittrex
import json

class Bittrex_acquisition:
    """
    Cette classe permet de maintenir à jour la base de données des prix de la crypto-currencie voulue
    On accède à cette base par cette classe.

    Mise en forme :

    dataFrame (index : date, column: BV, C, H, L, O, T, V)
    """
    def __init__(self, file_path, market="USDT-BTC", tickInterval="oneMin"):
        """
        Chargement ou création de la base de donnée

        :param file_path: fichier où socker la base de donnée
        :param market: marché de la base de donnée, par défault : USDT-BTC
        :param tickInterval: interval de temps entre deux valeurs demandées à l'API bittrex
        avec ces valeurs possibles : oneMin, fiveMin, hour, thirtyMin,Day
        """
        self.bittrex = Bittrex(None, None, api_version='v2.0')
        self.file_path = file_path
        self.market = market
        self.tickInterval = tickInterval

        try:
            with open(file_path, "r") as file:
                self.data = pd.read_csv(file)

            format = '%Y-%m-%d %H:%M:%S'
            self.data['date'] = pd.to_datetime(self.data['date'], format=format)
            self.data = self.data.set_index(pd.DatetimeIndex(self.data['date']))
            del self.data['date']
            print("[+] Valeurs chargées")
        except:
            self.data = None
            print("[-] Valeurs non chargées")
            self.init()

    def request(self):
        """
        Envoie une requète des prix du marché défini à l'API bitcoin
        :return:
        """
        return self.bittrex.get_candles(self.market, self.tickInterval)

    def init(self):
        """
        Initialisation de la base de donnée, on enregistre toutes les valeurs données par l'API bittrex
        Les données sont mise en forme
        :return: Boolean suivant la bonne exécution de l'initialisation
        """
        request = self.request()
        data = request['result']
        string_data = data.__str__()
        string_data = string_data.replace("\'", "\"")
        try:
            df = pd.read_json(string_data, orient="records")
        except:
            print("[-] Erreur initialisation")
            return False
        format = '%Y-%m-%d %H:%M:%S'
        df['date'] = pd.to_datetime(df['T'], format=format)
        df = df.set_index(pd.DatetimeIndex(df['date']))
        del df['date']
        del df['T']
        self.data = df
        print("[+] Données initialisées")
        self.save()
        return True

    def get_dataframe(self):
        """
        Renvoie les données

        :return: dataFrame (index : date, BV, C, H, L, O, T, V)
        """
        return self.data

    def update(self):
        """
        Mets à jour la base de données avec l'API bittrex
        :return: Boolean
        """
        request = self.request()
        data_temp = request['result']
        string_data = data_temp.__str__()
        string_data = string_data.replace("\'", "\"")
        try:
            data_temp = pd.read_json(string_data, orient="records")
        except:
            return False
        format = '%Y-%m-%d %H:%M:%S'
        data_temp['date'] = pd.to_datetime(data_temp['T'], format=format)
        data_temp = data_temp.set_index(pd.DatetimeIndex(data_temp['date']))
        del data_temp['date']
        del data_temp['T']

        data = self.data
        data = data.iloc[-1:]

        last_date_save = data.index.values[0]

        data_to_add = data_temp.iloc[-1:]
        start_date_of_data_to_add_first = data_to_add.index.values[0]

        if start_date_of_data_to_add_first != last_date_save: # les valeurs sont déjà à jour
            for i in range(2, data_temp.index.values.__len__()):
                data_to_add = data_temp.iloc[-i:]
                start_date_of_data_to_add = data_to_add.index.values[0]

                if last_date_save == start_date_of_data_to_add:
                    data_to_add = data_temp.iloc[(-i+1):]
                    print(data_to_add)
                    break
            self.data = self.data.append(data_to_add)
            print("[+] Données mise à jour")
            self.save()
        else:
            print("[+] Données déjà mise à jour")

        return True

    def save(self):
        """
        Sauvegarde les données sous forme de csv
        """
        self.data.to_csv(self.file_path)
        print("[+] Données sauvegardées")



