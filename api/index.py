import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def clean_input(text):
    """Basic structural text trimming and cleaning."""
    if not text:
        return ""
    return str(text).strip()

def clean_phone(phone_str):
    """Extracts exactly the digits out of the incoming phone format string."""
    if not phone_str:
        return ""
    return re.sub(r'\D', '', str(phone_str))

@app.route('/api/submit', methods=['POST', 'OPTIONS'])
def handle_form():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing payload data"}), 400

        # Data Sanitization and Normalization
        first_name = clean_input(data.get('first_name'))
        last_name = clean_input(data.get('last_name'))
        email = clean_input(data.get('email')).lower()
        phone = clean_phone(data.get('phone'))
        concern = clean_input(data.get('concern'))

        # Field Validation
        if not all([first_name, last_name, email, phone, concern]):
            return jsonify({"error": "All fields are required and must contain content."}), 400

        # Database Insertion
        # Vercel retrieves the Connection String securely from environment variables
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            return jsonify({"error": "Database environment link missing."}), 500

        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        insert_query = """
            INSERT INTO website_leads (first_name, last_name, email, phone, concern)
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (first_name, last_name, email, phone, concern))
        conn.commit()
        
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Lead written successfully."}), 201

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Expose backend application instance
app = app
