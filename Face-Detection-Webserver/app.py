from flask import Flask, Response, render_template_string, request, jsonify
import time
import threading

app = Flask(__name__)

# --- Global variable to store the latest frame ---
# We'll use a lock to make sure this is thread-safe
latest_frame = None
frame_lock = threading.Lock()

# --- HTML Page Template ---
# This is the webpage you will visit. It has an <img> tag
# that points to our /video_feed route.
HTML_TEMPLATE = """
<html>
<head>
    <title>Jetson Face Detection Stream</title>
</head>
<body style="background-color: #333; color: white; font-family: sans-serif;">
    <h1>Jetson Face Detection (Live Stream)</h1>
    <p>This stream is being processed on the Jetson, sent to the Pi K3s Cluster, and streamed to your browser.</p>
    <img src="{{ url_for('video_feed') }}" width="640" height="480">
</body>
</html>
"""

# --- Route 1: The Web Page ---
@app.route('/')
def index():
    # This renders the HTML page
    return render_template_string(HTML_TEMPLATE)

# --- Route 2: The Upload Route (for the Jetson) ---
@app.route('/data', methods=['POST'])
def receive_data():
    global latest_frame, frame_lock
    if request.data:
        # Get the raw JPEG bytes
        image_bytes = request.data
        
        # Safely update the global frame
        with frame_lock:
            latest_frame = image_bytes
            
        return "OK", 200
    return "Invalid request", 400

# --- Route 3: The Video Feed (for the Browser) ---
def video_generator():
    global latest_frame, frame_lock
    
    while True:
        with frame_lock:
            if latest_frame is None:
                # If no frame yet, wait
                time.sleep(0.1)
                continue
            
            # Copy the frame so we can release the lock
            frame = latest_frame
        
        # Yield the frame in the multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # This returns the generator function as a streaming response
    return Response(video_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)