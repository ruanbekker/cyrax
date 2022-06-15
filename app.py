import os
import requests
import subprocess
import socket
from flask import Flask, request, jsonify

def find_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    local_ip_address = s.getsockname()[0]
    return local_ip_address

def find_open_port():
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    return port

def fetch_compose_file(compose_url):
    fetch = requests.get(compose_url)
    if fetch.status_code == 200:
        with open('docker-compose.yml', 'wb') as f:
            f.write(fetch.content)
        response = True
    else:
        response = False
    return response

def compose_ps():
    open_port = find_open_port()
    os.environ["LOCAL_PORT"] = str(open_port)
    dc = subprocess.run(['which', 'docker-compose'], capture_output=True)
    docker_compose_binary = dc.stdout.decode('utf-8').rstrip('\n')
    cmds = subprocess.run([
        f'{docker_compose_binary}',
        '-f', 'docker-compose.yml',
        'up', '-d', '--remove-orphans'
    ], capture_output=True)
    response = cmds.stdout.decode('utf-8')
    print(response)
    local_ip = find_local_ip()
    application_status = {"app_url": f"http://{local_ip}:{open_port}"}
    return jsonify(application_status)

app = Flask(__name__)

@app.route('/deploy')
def deploy_app():
    args = request.args
    compose = args['compose']
    fetch = fetch_compose_file(compose)
    if fetch:
        res = compose_ps()
    else:
        res = "error"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8232)
