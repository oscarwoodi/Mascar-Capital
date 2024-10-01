import pandas as pd

def calculate_profit(df):
    """
    Calculate profit over time based on asset prices and position sizes.

    Args:
        prices_df (pd.DataFrame): DataFrame containing the asset prices with a 'Close' column
            and position sizes in 'position' column where negative values represent short positions
            and positive represent long.

    Returns:
        pd.Series: A pandas Series representing the cumulative profit over time.
    """
    # Initialize the profit series
    profit = pd.Series(index=df.index, data=0.0)
    
    # Track the current position and the entry price
    current_position = 0
    entry_price = 0.0
    accumulated_profit = 0.0
    
    for i in range(1, len(df)):
        position_size = df['position_size'].iloc[i]
        price = df['close'].iloc[i]
        
        # Check if the position has changed
        if position_size != current_position:
            # Calculate the profit for the change in position
            if current_position != 0:
                profit_from_trade = (price - entry_price) * current_position
                accumulated_profit += profit_from_trade

            # Update the entry price and current position
            entry_price = price
            current_position = position_size

        # Update the accumulated profit at each time step
        profit.iloc[i] = accumulated_profit
    
    return profit