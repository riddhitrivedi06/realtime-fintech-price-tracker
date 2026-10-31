import yfinance as yf
import pandas as pd

def fetch_market_data(ticker_symbol, period="1mo", interval="1d"):
    """
    Fetches historical and live market data for a given stock or crypto ticker
    using Yahoo Finance.
    
    Parameters:
    - ticker_symbol (str): e.g., 'AAPL', 'BTC-USD', 'NVDA'
    - period (str): Data timeframe ('1d', '5d', '1mo', '6mo', '1y')
    - interval (str): Data frequency ('1m', '5m', '1h', '1d')
    """
    try:
        # Fetching data from Yahoo Finance
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return None
            
        # Clean columns: reset index so Date/Datetime becomes a regular column
        df.reset_index(inplace=True)
        
        # Ensure standard column naming
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

# Quick test if run directly
if __name__ == "__main__":
    print("Testing data fetcher for Apple (AAPL)...")
    sample_data = fetch_market_data("AAPL", period="5d", interval="1d")
    print(sample_data.head())