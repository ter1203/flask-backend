from flask import Flask
app = Flask(__name__)

@app.route('/')
async def hello_world():
    return 'Hi, This is a tradeshop!'
