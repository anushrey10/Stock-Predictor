from datetime import timedelta
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from utils.data_loader import fetch_historical_data

def predict_price(ticker, forecast_days=7):
    try:
        # Fetch and prepare data
        data = fetch_historical_data(ticker, '5y')
        df = pd.DataFrame(data)
        
        # Create features
        close_prices = df['close']
        dates = pd.to_datetime(df['dates'])
        
        # Feature engineering
        df['day'] = dates.dt.dayofweek
        df['month'] = dates.dt.month
        df['sma_7'] = close_prices.rolling(7).mean()
        df['sma_30'] = close_prices.rolling(30).mean()
        df = df.dropna()
        
        # Prepare data for model
        X = df[['day', 'month', 'sma_7', 'sma_30']]
        y = df['close']
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate future dates
        last_date = dates.iloc[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days+1)]
        
        # Predict future prices
        predictions = []
        current_features = X.iloc[-1].values.reshape(1, -1)
        
        for _ in range(forecast_days):
            pred = model.predict(current_features)[0]
            predictions.append(round(pred, 2))
            
            # Update features for next prediction
            current_features[0][2] = (current_features[0][2] * 6 + pred) / 7  # Update SMA_7
            current_features[0][3] = (current_features[0][3] * 29 + pred) / 30  # Update SMA_30
        
        return {
            "dates": [d.strftime('%Y-%m-%d') for d in future_dates],
            "predictions": predictions
        }
        
    except Exception as e:
        raise RuntimeError(f"Prediction error: {str(e)}")