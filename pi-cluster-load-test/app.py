from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    # Simple Test to see if Webserver is working
    return "Hello World! This is the Server Load Test"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)