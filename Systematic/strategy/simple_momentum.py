## Example signals generator file. Strategy is not tested and should not be used for real trading. 

import pandas as pd
import numpy as np

def simple_momentum_1(df, CAPITAL, WINDOW):
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

    cap = CAPITAL / 4
    
    # Get trades
    df['R'] = df['Close'].pct_change()
    R = df['R']
    signal = np.sign(R.rolling(10, min_periods=10).mean())
    final_positions_usd = CAPITAL/10 * signal
    final_positions_usd = final_positions_usd.fillna(0)

    # Pre allocate
    total_pos = 0
    pos = np.zeros(len(final_positions_usd))

    for i, trade in enumerate(final_positions_usd): 
        if abs(total_pos + trade) <= cap: 
            total_pos += trade
        else: 
            None
        pos[i] = total_pos

    final_positions_usd.loc[:] = pos
    
    return final_positions_usd

