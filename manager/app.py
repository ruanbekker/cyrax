import os
import requests
import subprocess
import socket
import randomname
import docker
from flask import Flask, request, jsonify

client = docker.from_env()

domain = "127.0.0.1.nip.io"

def find_open_port():
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    return port

def generate_name():
    name = randomname.generate('v/corporate', 'adj/colors', ('n/geography', 'n/coding'))
    return name

def fetch_compose_file(stack_name, compose_url):
    os.mkdir(f'/src/stacks/{stack_name}')
    fetch = requests.get(compose_url)
    if fetch.status_code == 200:
        with open(f'/src/stacks/{stack_name}/docker-compose.yml', 'wb') as f:
            f.write(fetch.content)
        response = True
    else:
        response = False
    return response

def compose_ps(stack_name):
    open_port = find_open_port()
    subdomain = stack_name
    os.environ["LOCAL_PORT"] = str(open_port)
    os.environ["APPNAME"] = str(subdomain)
    os.environ["FQDN"] = f"{subdomain}.{domain}"
    dc = subprocess.run(['which', 'docker-compose'], capture_output=True)
    docker_compose_binary = dc.stdout.decode('utf-8').rstrip('\n')
    cwd = os.getcwd()
    os.chdir(f'/src/stacks/{stack_name}')
    with open('docker-compose.yml', 'r') as composefile:
        filedata = composefile.read()
    filedata = filedata.replace('__APPNAME__', stack_name)
    with open('docker-compose.yml', 'w') as composefile:
        composefile.write(filedata)
    cmds = subprocess.run([
        f'{docker_compose_binary}',
        '-f', 'docker-compose.yml',
        'up', '-d', '--remove-orphans'
    ], capture_output=True)
    response = cmds.stdout.decode('utf-8')
    os.chdir(cwd)
    print(response)
    application_status = {"app_url": f"http://{subdomain}.{domain}"}
    #application_status = {"app_url": f"http://{local_ip}:{open_port}"}
    return jsonify(application_status)

def list_containers():
    containers = []
    for ctr in client.containers.list():
        if 'cyrax' not in ctr.name:
            containers.append(ctr.name)
    return {'containers': containers}

def remove_containers(stack_name):
    cwd = os.getcwd()
    os.chdir(f'/src/stacks/{stack_name}')
    cmds = subprocess.run([
        'docker-compose', 'down', '--remove-orphans'
    ], capture_output=True)
    os.chdir(cwd)
    message = {"message": f"{stack_name} removed"}
    return message

app = Flask(__name__)

@app.route('/deploy')
def deploy_app():
    args = request.args
    compose = args['compose']
    stack_name = generate_name()
    fetch = fetch_compose_file(stack_name, compose)
    if fetch:
        res = compose_ps(stack_name)
    else:
        res = "error"
    return res

@app.route('/list')
def list_running_containers():
    running_containers = list_containers()
    return jsonify(running_containers)

@app.route('/delete')
def delete_containers():
    args = request.args
    stack_name = args['stack']
    response = remove_containers(stack_name)
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health_check():
    cmds = subprocess.run([
        f'docker',
        'version'
    ], capture_output=True)
    response = cmds.stdout.decode('utf-8')
    message = {"message": "ok"}
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
