import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    """
    Calculates technical indicators such as SMA (Simple Moving Average) 
    and RSI (Relative Strength Index) on the stock/crypto dataframe.
    
    Parameters:
    - df (pd.DataFrame): Dataframe containing 'Close' prices.
    
    Returns:
    - pd.DataFrame: Dataframe with added indicator columns.
    """
    if df is None or df.empty:
        return None
        
    df = df.copy()
    
    # 1. Calculate Simple Moving Averages (SMA)
    # Short-term trend (10 periods) and Medium-term trend (20 periods)
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # 2. Calculate Relative Strength Index (RSI - 14 periods)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    # Avoid division by zero
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 3. Calculate Daily Returns (%)
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    return df

# Quick test if run directly
if __name__ == "__main__":
    from data_fetcher import fetch_market_data
    
    print("Testing technical analytics on AAPL...")
    raw_df = fetch_market_data("AAPL", period="2mo", interval="1d")
    analyzed_df = calculate_technical_indicators(raw_df)
    
    print(analyzed_df[['Date', 'Close', 'SMA_10', 'SMA_20', 'RSI']].tail())