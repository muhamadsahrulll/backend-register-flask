from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from email_validator import validate_email, EmailNotValidError
from config import Config
from utils.email_sender import send_email
import re

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
mysql = MySQL(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    address = data.get("address", "").strip()

    # Validasi kosong
    if not name or not email or not address:
        return jsonify({"error": "Semua field wajib diisi"}), 400

    # Validasi panjang dan karakter
    if len(name) > 100 or not re.match(r"^[a-zA-Z\s.'-]+$", name):
        return jsonify({"error": "Nama tidak valid"}), 400
    if len(address) > 200:
        return jsonify({"error": "Alamat terlalu panjang"}), 400

    # Validasi email format
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({"error": "Email tidak valid"}), 400

    # Simpan ke database
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO registrations (name, email, address) VALUES (%s, %s, %s)",
            (name, email, address),
        )
        mysql.connection.commit()
        cursor.close()

        # Kirim email
        send_email(email, name)

        return jsonify({"message": "Registrasi berhasil"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/registrations", methods=["GET"])
def get_registrations():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, name, email, address FROM registrations")
    rows = cursor.fetchall()
    cursor.close()
    data = [
        {"id": row[0], "name": row[1], "email": row[2], "address": row[3]}
        for row in rows
    ]
    return jsonify(data)

@app.route('/')
def home():
    return 'Hello, Flask!'

if __name__ == "__main__":
    app.run(debug=True)
