from flask import Flask, jsonify, make_response
import os

app = Flask(__name__)

STATUS_DIR = os.path.join(os.path.dirname(__file__), "..", "status")

def read_status(key):
    f = os.path.join(STATUS_DIR, f"{key}.txt")
    if os.path.exists(f):
        return open(f).read().strip()
    return "on"

def write_status(key, value):
    f = os.path.join(STATUS_DIR, f"{key}.txt")
    open(f, "w").write(value)

HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Keep-Alive 控制中心</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 { text-align: center; margin-bottom: 30px; font-size: 28px; letter-spacing: 2px; }
        .card {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card.master { border: 2px solid #00d26a; }
        .info h2 { font-size: 20px; margin-bottom: 5px; }
        .info p { font-size: 14px; opacity: 0.7; }
        .switch { position: relative; width: 70px; height: 34px; }
        .switch input { display: none; }
        .slider {
            position: absolute; cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #ff4757; transition: .4s; border-radius: 34px;
        }
        .slider:before {
            position: absolute; content: "";
            height: 26px; width: 26px;
            left: 4px; bottom: 4px;
            background: white; transition: .4s; border-radius: 50%;
        }
        input:checked + .slider { background: #00d26a; }
        input:checked + .slider:before { transform: translateX(36px); }
        .status { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; animation: pulse 2s infinite; }
        .dot.on { background: #00d26a; box-shadow: 0 0 10px #00d26a; }
        .dot.off { background: #ff4757; box-shadow: 0 0 10px #ff4757; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .links { text-align: center; margin-top: 30px; display: flex; justify-content: center; gap: 15px; }
        .links a { color: #8aaae5; text-decoration: none; font-size: 14px; padding: 8px 16px; border-radius: 8px; background: rgba(138,170,229,0.1); }
    </style>
    <script>
        function toggle(k) { fetch('/'+k+'/toggle').then(()=>location.reload()); }
    </script>
</head>
<body>
    <div class="container">
        <h1>🤖 Keep-Alive 控制中心</h1>
        CNT_CARDS
        <div class="links"><a href="/status">📊 状态</a></div>
    </div>
</body>
</html>
"""

def get_status(key):
    s = read_status(key)
    return ("ON" if s == "on" else "OFF", "on" if s == "on" else "off", "checked" if s == "on" else "")

def make_card(key, title, icon, desc, is_master=False):
    txt, dot, chk = get_status(key)
    cls = " master" if is_master else ""
    return f'''<div class="card{cls}">
        <div class="info"><h2>{icon} {title}</h2><p>{desc}</p></div>
        <div style="text-align:right">
            <div class="status"><span class="dot {dot}"></span><span>{txt}</span></div>
            <label class="switch"><input type="checkbox" {chk} onchange="toggle('{key}')"><span class="slider"></span></label>
        </div>
    </div>'''

@app.route('/')
def home():
    cards = make_card("total", "控制中心", "🎛️", "全局启停", True)
    cards += make_card("openclaw", "OpenClaw Gateway", "🐝", "Node.js AI Agent")
    cards += make_card("comfy", "ComfyUI", "🎨", "Python AI绘画")
    return HTML.replace("CNT_CARDS", cards)

@app.route('/status')
def status():
    return jsonify({"total": read_status("total"), "openclaw": read_status("openclaw"), "comfy": read_status("comfy")})

@app.route('/<key>/toggle')
def toggle(key):
    cur = read_status(key)
    write_status(key, "off" if cur == "on" else "on")
    return f"{key} is {'OFF' if cur == 'on' else 'ON'} <a href='/'>返回</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079)