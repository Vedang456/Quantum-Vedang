from flask import Flask, request, jsonify
import sys
import os
import numpy as np
from functools import wraps
import time
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from api.quantum_intelligence import QuantumIntelligenceAPI
import multiprocessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
quantum_api = None

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def get_api():
    global quantum_api
    if quantum_api is None:
        try:
            quantum_api = QuantumIntelligenceAPI(security_level='high')
        except Exception as e:
            logger.error(f"Error initializing API: {str(e)}")
            raise
    return quantum_api

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key required'}), 401
            
        api = get_api()
        if not api.verify_token(api_key):
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 401
            
        return f(*args, **kwargs)
    return decorated

@app.route('/api/auth', methods=['POST'])
@limiter.limit("10 per minute")
def authenticate():
    try:
        api_key = request.json.get('api_key')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key required'}), 400
            
        api = get_api()
        token = api.authenticate(api_key)
        
        return jsonify({
            'status': 'success',
            'token': token
        })
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/process-signal', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def process_signal():
    try:
        data = np.array(request.json['signal_data'])
        api = get_api()
        result = api.process_signal(data)
        return jsonify({'status': 'success', 'result': result})  # Return full result
    except Exception as e:
        logger.error(f"Process signal error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/detect-anomalies', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def detect_anomalies():
    try:
        data = np.array(request.json['data'])
        threshold = request.json.get('threshold', 0.8)
        api = get_api()
        result = api.detect_anomalies(data, threshold)
        return jsonify({
            'status': 'success',
            'result': {
                'anomalies': result['anomalies'],
                'confidence': result['confidence'],
                'threshold': result['threshold']
            }
        })
    except Exception as e:
        logger.error(f"Detect anomalies error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/encrypt', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def encrypt_data():
    try:
        data = request.json['data']
        api = get_api()
        encrypted = api.encrypt_data(data)
        return jsonify({
            'status': 'success',
            'encrypted_data': encrypted.decode('utf-8')
        })
    except Exception as e:
        logger.error(f"Encrypt data error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/quantum-intelligence', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def quantum_intelligence_endpoint():
    try:
        api = get_api()
        start_time = time.time()
        
        data = request.json.get('data_stream', [])
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
        data_stream = np.array(data, dtype=np.float32)
        result = api.process_signal(data_stream)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'processing_time': time.time() - start_time
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/metrics', methods=['GET'])
@limiter.limit("10 per minute")
@require_api_key
def get_metrics():
    try:
        api = get_api()
        return jsonify({
            'status': 'success',
            'metrics': api.get_metrics()
        })
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    try:
        multiprocessing.freeze_support()
        logger.info("Starting Quantum Intelligence API server...")
        app.run(host='0.0.0.0', port=7777, ssl_context='adhoc')
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")