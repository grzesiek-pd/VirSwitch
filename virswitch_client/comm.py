from virswitch_client import app
from flask import Blueprint, request, render_template, url_for
import socket as sock
import pickle


comm_blueprint = Blueprint('comm_blueprint', __name__)


@app.route('/msg')
def msg(msg_to_send):
    host = '192.168.0.64'
    port = 4444
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(pickle.dumps(msg_to_send))
    msg_get_back = pickle.loads(client_socket.recv(50000))

    print("msg_get_back=", msg_get_back, type(msg_get_back))
    return msg_get_back


@app.route('/admin_check')
def admin_check(admin, msg_back, vms):

    if admin:
        vms_list = msg_back
        return vms_list
    else:
        vms_list = []
        for line in msg_back:
            if line[0] in vms:
                vms_list.append(line)
        return vms_list
