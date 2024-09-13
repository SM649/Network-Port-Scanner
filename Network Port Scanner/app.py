from flask import Flask, jsonify, request, render_template
import socket
import re       

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_port', methods=['POST'])
def scan_port():
    data = request.json
    ip = data['ip']
    port = data['port']
    status = scan_single_port(ip, port)
    return jsonify({'port': port, 'status': status})

def is_valid_ip(ip):
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return pattern.match(ip) is not None

def scan_single_port(ip, port):
    ip = ip.strip()
    if not is_valid_ip(ip):
        return "Error: Invalid IP address"
    
    if not (1 <= port <= 65535):
        return "Error: Invalid port number"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            return "Open" if result == 0 else "Closed"
    except socket.timeout:
        return "Error: Connection timed out"
    except socket.gaierror:
        return "Error: Invalid IP address"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
