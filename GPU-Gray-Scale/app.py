from flask import Flask, request, jsonify

app = Flask(__name__)

# This app will store the last message it received
last_message = "No data received yet."

# This route receives data from the Jetson
@app.route('/data', methods=['POST'])
def receive_data():
    global last_message
    if request.data:
        data_str = request.data.decode('utf-8')
        
        # Store the received data
        last_message = data_str
        
        # Print to the log for debugging
        print(f"--- Grayscale Demo Data Received ---")
        print(data_str)
        print(f"------------------------------------")
        
        return "OK", 200
    
    return "Invalid request. Please send data via POST.", 400

# This route lets you see the last message in your browser
@app.route('/')
def hello():
    global last_message
    return jsonify({
        "message": "Hello from the Grayscale Receiver!",
        "last_data_received": last_message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)