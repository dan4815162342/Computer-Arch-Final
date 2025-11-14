from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    """
    Receives data from the Jetson client and prints it to the pod's log.
    """
    if request.data:
        # Get the raw data and decode it as a string
        data_str = request.data.decode('utf-8')
        
        # Print a message confirming data receieved
        print(f"--- Data Received from Jetson ---")
        print(data_str)
        print(f"-----------------------------------")
        
        # Send response back to Jetson
        return "OK", 200
    
    # else return error
    return "Invalid request. Please send data via POST.", 400

@app.route('/')
def hello():
    # Simple Test to see if server is up and running 
    return "Hello World! This is the Simple Heterogeneous Edge-Cluster Test."

if __name__ == '__main__':
    # Port must match yaml file
    app.run(host='0.0.0.0', port=5000)