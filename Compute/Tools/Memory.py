

class Memory:
    """
    Cette classe permet de sauvegarder les ordres en cours,
    et d'abstraire l'accès à cette mémoire
    elle consiste en un tableau de string, la dernière case correspond à la dernière mémoire
    sauvegardé.
    Le traitement du string et laissé à la discrétion du model
    """

    def __init__(self):
        self.tab = []

    def add(self, line):
        self.tab.append(line)
        #print(line)

    def read(self, index):
        #print(self.tab[index])
        return self.tab[index]