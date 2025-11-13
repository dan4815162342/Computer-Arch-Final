from flask import Flask, request

app = Flask(__name__)

# This is the endpoint that the Jetson's script will send data to.
@app.route('/data', methods=['POST'])
def receive_data():
    """
    Receives data from the Jetson client and prints it to the pod's log.
    """
    if request.data:
        # Get the raw data and decode it as a string
        data_str = request.data.decode('utf-8')
        
        # Print a clear message to the pod's log for debugging
        print(f"--- Data Received from Jetson ---")
        print(data_str)
        print(f"-----------------------------------")
        
        # Send a success response back to the Jetson
        return "OK", 200
    
    # If something else (like a GET request) hits this, send an error
    return "Invalid request. Please send data via POST.", 400

@app.route('/')
def hello():
    """
    A simple "hello" route so you can check if the server is running
    by visiting it in your browser.
    """
    return "Hello from the Pi K3s Receiver! I'm ready for data."

if __name__ == '__main__':
    # We run on port 5000 because that's what the 
    # cpu-frontend-github.yaml file's containerPort is set to.
    app.run(host='0.0.0.0', port=5000)