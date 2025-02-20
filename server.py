from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
