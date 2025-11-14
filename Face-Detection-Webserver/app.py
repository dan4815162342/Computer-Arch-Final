from flask import Flask, Response, render_template_string, request, jsonify
import time
import threading

app = Flask(__name__)


# Global variable to hold the most recent frame from the Jetson.

latest_frame = None
frame_lock = threading.Lock()


#Simple HTML template for the browser.
HTML_TEMPLATE = """
<html>
<head>
    <title>Jetson Face Detection Stream</title>
</head>
<body style="background-color: #333; color: white; font-family: sans-serif;">
    <h1>Jetson Face Detection</h1>
    <img src="{{ url_for('video_feed') }}" width="640" height="480">
</body>
</html>
"""

# For Vieing HTML_TEMPLATE on browser.
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Receive data from the Jetson
@app.route('/data', methods=['POST'])
def receive_data():
    global latest_frame, frame_lock
    if request.data:
        # Get the raw JPEG bytes from the Jetson
        image_bytes = request.data
        with frame_lock:
            latest_frame = image_bytes
            
        return "OK", 200
    return "Invalid request", 400

# Send lastest frame to HTML
def video_generator():
    global latest_frame, frame_lock
    
    while True:
        with frame_lock:
            # Wait if no frame
            if latest_frame is None:
                time.sleep(0.1)
                continue
            # Grab the latest frame
            frame = latest_frame
        
        # Send the frame as a "multipart" response.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the Flask web server on port 5000
    app.run(host='0.0.0.0', port=5000)