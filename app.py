# app.py
import sys
sys.dont_write_bytecode = True

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import json
import os
from detect import detect_phishing
from whitelist import Whitelist
import nltk

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

app = Flask(__name__)
CORS(app)
app.json_encoder = NumpyEncoder

# Update model path to use absolute path
model_path = os.path.join(os.path.dirname(__file__), 'phishing.pkl')
model = pickle.load(open(model_path, 'rb'))

whitelist = Whitelist()

# Download necessary NLTK data files
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

@app.route("/api/check_url", methods=["POST", "GET"])
def check_url():
    try:
        if request.method == "GET":
            url = request.args.get('url')
        else:
            data = request.get_json(force=True)
            url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Check whitelist first
        if whitelist.is_whitelisted(url):
            print(f"\n------------------------")
            print(f"URL {url} found in whitelist")
            print("------------------------\n")
            return jsonify({
                "url": url,
                "prediction": "good",
                "is_phishing": False,
                "confidence": 100.0,
                "whitelisted": True
            })

        # Get prediction and probabilities
        prediction = model.predict([url])[0]
        probabilities = model.predict_proba([url])[0]
        
        # Calculate confidence based on prediction
        confidence = float(probabilities[1] * 100) if prediction == 'bad' else float(probabilities[0] * 100)
        
        response = {
            "url": url,
            "prediction": prediction,
            "is_phishing": prediction == 'bad',
            "confidence": round(confidence, 2),  # Round to 2 decimal places
            "whitelisted": False
        }
        
        # Enhanced logging
        print(f"\n------------------------")
        print(f"URL checked: {url}")
        print(f"Prediction: [{prediction}]")
        print(f"Confidence: {confidence:.2f}%")
        print(f"Probabilities - Safe: {probabilities[0]:.2%}, Phishing: {probabilities[1]:.2%}")
        print(f"Is Phishing: {response['is_phishing']}")
        print("------------------------\n")
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/whitelist", methods=["POST"])
def add_to_whitelist():
    try:
        data = request.get_json(force=True)
        url = data.get("url")
        temporary = data.get("temporary", False)
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
            
        success = whitelist.add_url(url, temporary=temporary)
        return jsonify({
            "success": success,
            "message": "URL added to whitelist" if success else "URL already whitelisted",
            "temporary": temporary
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
