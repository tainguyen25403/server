from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import hashlib  # Thêm thư viện để băm mật khẩu

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"
PASSWORD = """I don't wanna be needing your love
I just wanna be deep in your love"""

# Băm mật khẩu có xuống dòng
PASSWORD_HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"submissions": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/submit', methods=['POST'])
def submit_data():
    received_data = request.get_json()
    if not received_data:
        return jsonify({"error": "No data received"}), 400

    # Thêm timestamp (ngày giờ hiện tại)
    received_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Lưu vào danh sách lịch sử
    current_data = load_data()
    current_data["submissions"].append(received_data)
    save_data(current_data)

    print(f"New submission added: {received_data}")
    return jsonify({"message": "Success", "updated_data": current_data}), 200

@app.route('/data', methods=['GET'])
def get_data():
    data = load_data()  # Đọc dữ liệu từ file data.json
    return jsonify(data), 200

@app.route('/validate', methods=['POST'])
def validate_password():
    data = request.get_json()
    if not data or "password" not in data:
        return jsonify({"valid": False, "error": "No password provided"}), 400

    received_password_hash = data["password"]
    
    # Kiểm tra hash của mật khẩu nhập vào có khớp với PASSWORD_HASH không
    if received_password_hash == PASSWORD_HASH:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False}), 401  # Unauthorized

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
