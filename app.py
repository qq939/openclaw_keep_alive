from flask import Flask, jsonify

app = Flask(__name__)
# Status is kept in memory. Resets to "on" on restart.
status = "on"

@app.route('/', methods=['GET'])
def home():
    return f"Keep-Alive Control Center is running.<br>Current Status: <b>{status.upper()}</b><br><br>Actions:<br>- <a href='/on'>Turn ON</a><br>- <a href='/off'>Turn OFF</a><br>- <a href='/status'>View Raw Status</a>"

@app.route('/status', methods=['GET'])
def get_status():
    return status

@app.route('/on', methods=['GET', 'POST'])
def turn_on():
    global status
    status = "on"
    return "Keep-Alive is ON. <br><a href='/'>Go back</a>"

@app.route('/off', methods=['GET', 'POST'])
def turn_off():
    global status
    status = "off"
    return "Keep-Alive is OFF. <br><a href='/'>Go back</a>"

@app.route('/toggle', methods=['GET', 'POST'])
def toggle():
    global status
    status = "off" if status == "on" else "on"
    return f"Keep-Alive is {status.upper()}. <br><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079)
