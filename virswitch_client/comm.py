from virswitch_client import app
import socket as sock
import pickle


@app.route('/msg')
def msg(msg_to_send):
    host = '192.168.0.64'
    port = 3333
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect((host, port))

    print(msg_to_send)
    b_msg = pickle.dumps(msg_to_send)
    print(b_msg)
    client_socket.send(b_msg)

    msg_get_back = pickle.loads(client_socket.recv(32767))

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
