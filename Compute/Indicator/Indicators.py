import pandas as pd
"""
On va placer ici les indicateurs boursiers
"""

def ema(df, n):
    """
    :param df: données OCHL
    :param n: période de calcul
    :type arg1: DataFrame
    :type arg1: int
    :return: données OCHL + Moyenne mobile
    :rtype: DataFrame
    """
    price = df['C']
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    ema = pd.Series(price.ewm(span=n, min_periods=n).mean(), name='EMA_{}'.format(n))
    df = df.join(ema)
    return df

