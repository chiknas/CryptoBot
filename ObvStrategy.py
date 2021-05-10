import pandas as pd
import numpy as np
from technical_indicators_lib import OBV

obv = OBV()
columns = ["open","high","low","close","volume"]

class ObvStrategy:

    def test(self):
        df = pd.read_csv("test_data.csv")
        df = df.iloc[::-1]
        length = len(df.index) - 1

        for x in range(1, length - 50, 1):
            currentDf = df.iloc[x:x + 50]
            result = self.whatShouldIDo(currentDf)
            if result == 1:
                print("BUY")
            elif result == -1:
                print("SELL")


        # Method 1: get the data by sending a dataframe
        # df = obv.get_value_df(df)


        # Method 2: get the data by sending series values
        # obv_values = obv.get_value_list(df["close"], df["volume"])

        # print(df)

    def getPercentageChange(self, previous, current):
        try:
            return ((current - previous) / previous) * 100.0
        except ZeroDivisionError:
            return 0

    def whatShouldIDo(self, data):
        df = pd.DataFrame(data, columns=columns)
        obvDf = obv.get_value_df(df)

        pricePercentageChange = self.getPercentageChange(df.iloc[0]["close"], df.iloc[-1]["close"])
        obvPercentageChange = self.getPercentageChange(obvDf.loc[obvDf.index[0], "OBV"], obvDf.loc[obvDf.index[-1], "OBV"])

        if pricePercentageChange < 0.5 and obvPercentageChange >= 1000:
            print('Price changed: ', pricePercentageChange, '%', '  ', 'OBV changed: ', obvPercentageChange, '%')
            return 1
        elif obvPercentageChange <= -400:
            print('Price changed: ', pricePercentageChange, '%', '  ', 'OBV changed: ', obvPercentageChange, '%')
            return -1
        return 0
        
