from flask import Flask

app = Flask(__name__)

# Just testing things out and making sure they work
@app.route('/')
def hello():
    return 'Hello, World!'
