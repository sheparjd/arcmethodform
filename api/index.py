from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# Import your cleanup and database logic here

app = Flask(__name__)
CORS(app) # Keeps CORS active for your backend routing

@app.route('/api/submit', methods=['POST'])
def handle_form():
    # 1. Grab data from request.form or request.json
    # 2. Run data cleanup
    # 3. Post to Neon Database
    return jsonify({"status": "success", "message": "Data processed"})

# Vercel needs this line to find the application instance
app = app
