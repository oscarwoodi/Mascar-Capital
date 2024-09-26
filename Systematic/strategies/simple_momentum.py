## Example signals generator file. Strategy is not tested and should not be used for real trading. 

import pandas as pd
import numpy as np

def simple_momentum(df, CAPITAL):
    """
    input: 
        data: a dict of dataframes.
            Example:
                data = DataFrame(open, close, high, low, volume)
                All DataFrames are: (Time_Open(index), markets...) 
    output:
        desired_positions = { date: DateTime, DateFrame}
        desired_position = desired_position_normalized * capital

    """

    df['R'] = df['Close'].pct_change()
    R = df['R']
    signal = np.sign(R.rolling(10, min_periods=10).mean())
    final_positions_usd = CAPITAL * signal
    return final_positions_usd

