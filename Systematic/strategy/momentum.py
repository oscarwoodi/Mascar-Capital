## Example signals generator file. Strategy is not tested and should not be used for real trading. 

import pandas as pd
import numpy as np

def simple_momentum_vix(df, CAPITAL, LAYERS, WINDOW):
    """
    input: 
        data: a dict of dataframes.
            Example:
                data = DataFrame(open, close, high, low, volume)
                All DataFrames are: (Time_Open(index), markets...) 
        CAPITAL: maximum amount of capital to deploy
        WINDOW: window used in determining momentum
        LAYERS: number of equal sized trades to make before reaching capital limit
    output:
        desired_positions = { date: DateTime, DateFrame}
        desired_position = desired_position_normalized * capital

    """

    # Get trades
    df['R'] = df['Close'].pct_change()
    R = df['R']
    signal_buy = np.sign(R.rolling(WINDOW).mean())

    final_positions_usd = CAPITAL/LAYERS * signal_buy
    final_positions_usd = final_positions_usd.fillna(0)

    # Pre allocate
    total_pos = 0
    pos = np.zeros(len(final_positions_usd))

    for i, trade in enumerate(final_positions_usd): 
        if trade < 0: 
            total_pos = 0
        if (abs(total_pos + trade) <= CAPITAL) and ((total_pos + trade) >= 0) : 
            total_pos += trade
        else: 
            None
        pos[i] = total_pos

    final_positions_usd.loc[:] = pos
    
    return final_positions_usd

