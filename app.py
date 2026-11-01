import subprocess
import json
from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Biến lưu trữ dữ liệu cảm biến nhận từ ESP32 qua MQTT
sensor_data = {
    "heart_rate": 72,
    "location": "Phòng tập",
    "is_fallen": False
}

# Biến trạng thái điều khiển từ web
virtual_state = False

TUNNEL_ID = "a892db59-043d-4fc1-afd7-aa9fe6907fc2"
PORT = 8080

# Cấu hình MQTT Broker trên Raspberry Pi
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/sensors"  # Topic mà ESP32 sẽ publish dữ liệu lên

def on_connect(client, userdata, flags, rc):
    print(f"✅ Đã kết nối MQTT Broker, mã phản hồi: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global sensor_data
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        sensor_data.update(data)
        print(f"📥 Nhận dữ liệu MQTT từ ESP32: {sensor_data}")
    except Exception as e:
        print(f"❌ Lỗi xử lý bản tin MQTT: {e}")

# Khởi tạo MQTT Client chạy ngầm
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start() # Chạy vòng lặp nhận tin nhắn ngầm
except Exception as e:
    print(f"⚠️ Không thể kết nối MQTT Broker: {e}")

@app.route('/')
def index():
    return render_template('index.html')

# 1. API cung cấp dữ liệu cảm biến cho trang web đọc định kỳ
@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify({
        'sensor': sensor_data,
        'device_state': virtual_state
    })

# 2. API nhận lệnh điều khiển từ web và in log ra Terminal Raspberry Pi
@app.route('/toggle', methods=['POST'])
def toggle_state():
    global virtual_state
    virtual_state = not virtual_state
    
    if virtual_state:
        print("🟢 [WEB ACTION] Thiết bị đã được BẬT (ON)")
    else:
        print("🔴 [WEB ACTION] Thiết bị đã bị TẮT (OFF)")
        
    return jsonify({'state': virtual_state})

if __name__ == '__main__':
    print("🌐 Đang khởi chạy Cloudflare Tunnel...")
    tunnel_process = subprocess.Popen(
        ["cloudflared", "tunnel", "run", "--url", f"http://localhost:{PORT}", TUNNEL_ID]
    )

    print(f"🚀 Flask Web Server đang chạy tại cổng {PORT}...")
    try:
        app.run(host='0.0.0.0', port=PORT, debug=False)
    finally:
        tunnel_process.terminate()
        mqtt_client.loop_stop()
