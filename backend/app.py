from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import logging
import time
import json
from utils.data_loader import fetch_historical_data, fetch_realtime_price
from models.model import predict_price
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": Config.VERSION,
        "environment": "development"
    })

@app.route('/api/historical', methods=['GET'])
def get_historical_data():
    ticker = request.args.get('ticker', 'AAPL')
    period = request.args.get('period', '1y')
    
    if not ticker.isalpha():
        return jsonify({"error": "Invalid ticker symbol"}), 400
    
    try:
        data = fetch_historical_data(ticker, period)
        return jsonify({
            "ticker": ticker.upper(),
            "period": period,
            "data": data
        })
    except Exception as e:
        logger.error(f"Historical data error: {str(e)}")
        return jsonify({"error": "Failed to fetch historical data"}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        ticker = data.get('ticker', 'AAPL')
        days = int(data.get('days', 7))
        
        if days < 1 or days > 30:
            return jsonify({"error": "Days must be between 1 and 30"}), 400
            
        prediction = predict_price(ticker, days)
        return jsonify({
            "ticker": ticker.upper(),
            "prediction": prediction,
            "unit": "USD"
        })
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Prediction failed"}), 500

@app.route('/api/realtime', methods=['GET'])
def realtime_stream():
    ticker = request.args.get('ticker', 'AAPL')
    
    def generate():
        while True:
            try:
                price_data = fetch_realtime_price(ticker)
                yield f"data: {json.dumps(price_data)}\n\n"
                time.sleep(60)  # Update every 60 seconds
            except Exception as e:
                logger.error(f"Realtime stream error: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                time.sleep(10)
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)