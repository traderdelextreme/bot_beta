# bot_beta
bot de trading : 

https://medium.com/la-baleine/concevoir-un-bot-de-trading-partie-1-bdcfbf29eb7f

https://medium.com/la-baleine/concevoir-un-bot-de-trading-partie-2-b84fcbe672f7

https://medium.com/la-baleine/concevoir-un-bot-de-trading-partie-3-aa7e5d8dcaa8


Prérequis pour le projet : 

pip3 install pandas 

pip3 install python-bittrex

Dossier :
- Watch : requetage et nettoyage des données
input : paramètre, bourse, currency
output : dataframe pandas

On place ici les classes qui vont récupérer les données de place boursière,
la sortie est une dataframe de pandas indexé par des date

Exemple : kraken...
(Pour l'instant : Bitrex implémenté)

- Compute : analyse des données
input : dataframe pandas
output : envoie un ordre grace à serve

On place les modèles utilisés pour donner un ordre d'achat ou de vente, les models utilisent les indicateurs

Exemple : Big Data, détection de patern, macd+mm200, macd+rsi ...
(Pour l'instant : Modèle simple achat et vente avec la statégie du macd)

   - Indicator : indicateur boursiers utilisés dans les models
input : dataframe pandas
output : tableau de (-1,0,1) (vente, rien, achat)
   Exemple : RSI, macd zerolag, pattern, divergence ...
    (Pour l'instant : macd)

- Serve : passage d'ordre et gestion des fonds
Contient la fonction buy() et send()
(Pour l'instant : Simple print d'achat et de vente)

Exemple : Envoie de mail, achat direct sur la plateforme




