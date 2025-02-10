import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_historical_data(ticker, period='1y'):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            raise ValueError("No data found for this ticker")
            
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        return {
            'dates': df['Date'].tolist(),
            'open': df['Open'].round(2).tolist(),
            'high': df['High'].round(2).tolist(),
            'low': df['Low'].round(2).tolist(),
            'close': df['Close'].round(2).tolist(),
            'volume': df['Volume'].astype(int).tolist()
        }
    except Exception as e:
        raise RuntimeError(f"Data loading failed: {str(e)}")

def fetch_realtime_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d', interval='1m')
        if data.empty:
            return {"error": "No real-time data available"}
            
        latest = data.iloc[-1]
        return {
            'timestamp': datetime.now().isoformat(),
            'price': round(latest['Close'], 2),
            'open': round(latest['Open'], 2),
            'high': round(latest['High'], 2),
            'low': round(latest['Low'], 2),
            'volume': int(latest['Volume'])
        }
    except Exception as e:
        raise RuntimeError(f"Realtime price fetch failed: {str(e)}")