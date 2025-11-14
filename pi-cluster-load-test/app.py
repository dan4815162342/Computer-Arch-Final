from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    # A simple, fast response for the load test
    return "Hello from the Pi Load Test Server!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)