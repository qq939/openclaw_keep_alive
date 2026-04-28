from flask import Flask, jsonify, make_response
app = Flask(__name__)

status = {"openclaw": "on", "comfyui": "on"}

HTML_TEMPLATE = """
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
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
            letter-spacing: 2px;
        }
        .service-card {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .service-info h2 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        .service-info p {
            font-size: 14px;
            opacity: 0.7;
        }
        .toggle-btn {
            position: relative;
            width: 80px;
            height: 40px;
            background: #333;
            border-radius: 20px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .toggle-btn.active { background: #00d26a; }
        .toggle-btn.inactive { background: #ff4757; }
        .toggle-btn a {
            display: block;
            width: 100%;
            height: 100%;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        .dot.on { background: #00d26a; box-shadow: 0 0 10px #00d26a; }
        .dot.off { background: #ff4757; box-shadow: 0 0 10px #ff4757; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .links {
            text-align: center;
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        .links a {
            color: #8aaae5;
            text-decoration: none;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 8px;
            background: rgba(138, 170, 229, 0.1);
            transition: all 0.3s;
        }
        .links a:hover {
            background: rgba(138, 170, 229, 0.2);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Keep-Alive 控制中心</h1>
        
        <div class="service-card">
            <div class="service-info">
                <h2>🐝 OpenClaw Gateway</h2>
                <p>Node.js AI Agent Gateway</p>
            </div>
            <div style="text-align: right;">
                <div class="status-indicator">
                    <span class="dot {{ 'on' if status.openclaw == 'on' else 'off' }}"></span>
                    <span>{{ 'ON' if status.openclaw == 'on' else 'OFF' }}</span>
                </div>
                <div style="margin-top: 10px;">
                    <a href="/openclaw/toggle" class="toggle-btn {{ 'active' if status.openclaw == 'on' else 'inactive' }}"></a>
                </div>
            </div>
        </div>
        
        <div class="service-card">
            <div class="service-info">
                <h2>🎨 ComfyUI</h2>
                <p>Python AI Image Generation</p>
            </div>
            <div style="text-align: right;">
                <div class="status-indicator">
                    <span class="dot {{ 'on' if status.comfyui == 'on' else 'off' }}"></span>
                    <span>{{ 'ON' if status.comfyui == 'on' else 'OFF' }}</span>
                </div>
                <div style="margin-top: 10px;">
                    <a href="/comfyui/toggle" class="toggle-btn {{ 'active' if status.comfyui == 'on' else 'inactive' }}"></a>
                </div>
            </div>
        </div>
        
        <div class="links">
            <a href="/status">📊 状态 API</a>
            <a href="https://github.com/qq939/openclaw_keep_alive" target="_blank">📚 文档</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    rendered = HTML_TEMPLATE.replace('{{ \'on\' if status.openclaw == \'on\' else \'off\' }}', 'on' if status['openclaw'] == 'on' else 'off')
    rendered = rendered.replace('{{ \'active\' if status.openclaw == \'on\' else \'inactive\' }}', 'active' if status['openclaw'] == 'on' else 'inactive')
    rendered = rendered.replace('{{ status.openclaw }}', status['openclaw'])
    rendered = rendered.replace('{{ \'on\' if status.comfyui == \'on\' else \'off\' }}', 'on' if status['comfyui'] == 'on' else 'off')
    rendered = rendered.replace('{{ \'active\' if status.comfyui == \'on\' else \'inactive\' }}', 'active' if status['comfyui'] == 'on' else 'inactive')
    rendered = rendered.replace('{{ status.comfyui }}', status['comfyui'])
    response = make_response(rendered)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(status)

@app.route('/openclaw/on', methods=['GET', 'POST'])
def openclaw_on():
    status['openclaw'] = 'on'
    return make_response(f"OpenClaw Keep-Alive is ON. <br><a href='/'>Go back</a>")

@app.route('/openclaw/off', methods=['GET', 'POST'])
def openclaw_off():
    status['openclaw'] = 'off'
    return make_response(f"OpenClaw Keep-Alive is OFF. <br><a href='/'>Go back</a>")

@app.route('/openclaw/toggle', methods=['GET', 'POST'])
def openclaw_toggle():
    status['openclaw'] = 'off' if status['openclaw'] == 'on' else 'on'
    return make_response(f"OpenClaw Keep-Alive is {status['openclaw'].upper()}. <br><a href='/'>Go back</a>")

@app.route('/comfyui/on', methods=['GET', 'POST'])
def comfyui_on():
    status['comfyui'] = 'on'
    return make_response(f"ComfyUI Keep-Alive is ON. <br><a href='/'>Go back</a>")

@app.route('/comfyui/off', methods=['GET', 'POST'])
def comfyui_off():
    status['comfyui'] = 'off'
    return make_response(f"ComfyUI Keep-Alive is OFF. <br><a href='/'>Go back</a>")

@app.route('/comfyui/toggle', methods=['GET', 'POST'])
def comfyui_toggle():
    status['comfyui'] = 'off' if status['comfyui'] == 'on' else 'on'
    return make_response(f"ComfyUI Keep-Alive is {status['comfyui'].upper()}. <br><a href='/'>Go back</a>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079)