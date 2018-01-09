class Serve_test2:
    """
    Simple print pour un signal d'achat ou de vente
    """
    def __init__(self):
        self.achat = 0
        self.vente = 0
        self.btc = 0
        self.euros = 20000
        self.last_buy = 0

    def buy(self, rate, volume):
        self.achat = self.achat + rate*volume
        print("achat, rate : " + rate.__str__() + ", volume : " + volume.__str__())
        self.btc = self.btc + volume
        self.euros = self.euros - volume*rate
        self.last_buy = rate

    def sell(self, rate, volume):
        self.vente = self.vente + rate*volume
        print("vente, rate : " + rate.__str__() + ", volume : " + volume.__str__())
        self.btc = self.btc - volume
        self.euros = self.euros + volume*rate

        marge = rate - self.last_buy
        print("marge : " + marge.__str__())

    def bilan(self):
        print("euros")
        print(self.euros)
        print("btc")
        print(self.btc)
        print("total : ")
        total  = self.euros + self.btc*self.last_buy
        print(total)
        return total