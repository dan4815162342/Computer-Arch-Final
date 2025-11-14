from flask import Flask, request, jsonify
import os
import time 

app = Flask(__name__)

# Save path for image from jetson 
SAVE_PATH = "/app/storage" 

# This route receives data from the Jetson
@app.route('/data', methods=['POST'])
def receive_data():
    if request.data:
        try:
            # Create unique filename using the current time
            filename = f"received_image_{int(time.time())}.jpg"
            filepath = os.path.join(SAVE_PATH, filename)
            
            # Get the raw bytes and write them to the file
            with open(filepath, "wb") as f:
                f.write(request.data)
            
            # Debugging
            print(f"--- Image Received from Jetson ---")
            print(f"Saved to: {filepath}")
            print(f"----------------------------------")
            
            return "OK", 200
        except Exception as e:
            print(f"Error saving file: {e}")
            return "Error saving file", 500
    
    return "Invalid request. Please send data via POST.", 400

# This route lets you see the list of saved files
@app.route('/')
def hello():
    try:
        # Look inside our storage folder
        files = os.listdir(SAVE_PATH)
    except Exception as e:
        files = [f"Error reading storage: {e}"]
        
    return jsonify({
        "message": "Hello from the Pi File Receiver!",
        "storage_path": SAVE_PATH,
        "files_in_storage": files
    })

if __name__ == '__main__':
    # Ensure the storage directory exists inside the container
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    app.run(host='0.0.0.0', port=5000)