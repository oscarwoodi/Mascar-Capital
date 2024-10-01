import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_strategy(df, profit_df=None):
    """
    Plot asset prices with markers for position changes and background shading 
    indicating long/short positions. Optionally plot the profit over time.

    Args:
        prices_df (pd.DataFrame): DataFrame containing the asset prices with a 'Close' column.
        positions_df (pd.DataFrame): DataFrame containing the position sizes where negative 
                                     values represent short positions and positive represent long.
        profit_df (pd.DataFrame or pd.Series, optional): DataFrame or Series containing profit over time.
    """
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Set the background color for the plot
    fig.set_facecolor('black')
    ax1.set_facecolor('black')

    # Plot asset prices
    ax1.plot(df['close'], label='Asset Price', color='lime', lw=2)

    # Get the positions
    positions = df['position_size']

    # Get indices where the position changes
    changes = positions.diff().ne(0)  # True where there is a change in position
    indices = positions[changes].index

    # Iterate over the indices to place markers and shading
    for i in range(len(positions) - 1):

        # CODE FOR BACKGROUND LONG/SHORT INDICATION
        #if positions.iloc[i] > 0:
            #ax1.axvspan(df.index[i], df.index[i + 1], color='green', alpha=0.2)  # Green shaded area for long positions
        #elif positions.iloc[i] < 0:
            #ax1.axvspan(df.index[i], df.index[i + 1], color='red', alpha=0.2)  # Red shaded area for short positions
            
        # Plot markers for position changes
        if changes.iloc[i]:
            if positions.diff().iloc[i] > 0:
                ax1.plot(df.index[i], df['close'].iloc[i], '^', color='green', markersize=8, label='Buy' if i == indices[0] else "")  # Green for buy
            elif positions.diff().iloc[i] < 0:
                ax1.plot(df.index[i], df['close'].iloc[i], 'v', color='red', markersize=8, label='Sell' if i == indices[0] else "")  # Red for sell


    # Add second axis to show the position size over time
    ax2 = ax1.twinx()
    ax2.plot(df['position_size'], color='white', lw=3, label='Position Size', alpha=0.4)
    ax2.set_ylabel('Position Size', color='white')

    # Set title, labels, and grid
    ax1.set_title("Asset Prices with Position Changes", fontsize=20, color='#00FF00', fontweight='bold')
    ax1.set_xlabel("Date", fontsize=12, color='#00FF00')
    ax1.set_ylabel("Price", fontsize=12, color='#00FF00')

    # Change x and y ticks color
    ax1.tick_params(axis='x', colors='#00FF00')
    ax1.tick_params(axis='y', colors='#00FF00')
    ax2.tick_params(axis='y', colors='white')

    # Add grid with green lines
    ax1.grid(color='#004400', linestyle='--', linewidth=0.5)
    
    # Formatting the date on the x-axis for better visibility
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    plt.grid(True)
    plt.tight_layout()

    # Plot the profit on a separate plot if provided
    if profit_df is not None:
        fig, ax3 = plt.subplots(figsize=(14, 5))

        # Set the background color for the plot
        fig.set_facecolor('black')
        ax3.set_facecolor('black')

        ax3.plot(profit_df, color='yellow', lw=2, label='Profit')
        # Set title, labels, and grid
        ax3.set_title('Profit Over Time', fontsize=20, color='#00FF00', fontweight='bold')
        ax3.set_ylabel("Cumulative Profit", fontsize=12, color='#00FF00')
        ax3.set_xlabel("Date", fontsize=12, color='#00FF00')
        
        # Change x and y ticks color to green
        ax3.tick_params(axis='x', colors='#00FF00')
        ax3.tick_params(axis='y', colors='#00FF00')

        # Formatting the date on the x-axis for better visibility
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator())
        fig.autofmt_xdate()

        plt.grid(True)
        plt.tight_layout()

    plt.show()
