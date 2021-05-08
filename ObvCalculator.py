import pandas as pd
import numpy as np
from technical_indicators_lib import OBV

obv = OBV()
columns = ["open","high","low","close","volume"]

class ObvCalculator:

    def test(self):
        df = pd.read_csv("test_data.csv")

        # Method 1: get the data by sending a dataframe
        df = obv.get_value_df(df)


        # Method 2: get the data by sending series values
        # obv_values = obv.get_value_list(df["close"], df["volume"])

        print(df)

    def currentObv(self, data):
        df = pd.DataFrame(data, columns=columns)
        obvDf = obv.get_value_df(df)
        return obvDf.loc[obvDf.index[-1], "OBV"]
