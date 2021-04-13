from virswitch_client import app
import socket as sock
import pickle
from cryptography.fernet import Fernet


@app.route('/msg')
def msg(msg_to_send):
    key = b'8tnFL71voDHkQ3V7XySswRC2ZHOIfB7lDt11n4OieQQ='
    host = '192.168.81.131'
    port = 3333
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect((host, port))

    b_msg = pickle.dumps(msg_to_send)

    binary_msg = str(msg_to_send).encode()
    encoded_msg = Fernet(key).encrypt(binary_msg)

    # print(b_msg)
    # print(encoded_msg)

    client_socket.send(encoded_msg)

    msg_get_back = pickle.loads(client_socket.recv(8000))

    if msg_get_back == 'error':
        print('error!')

    elif msg_get_back in range(100):
        parts = msg_get_back
        print('parts =', msg_get_back)
        msg_str = ''

        part = client_socket.recv(32000).decode("utf-8")
        # for i in range(parts + 1):
        msg_str = msg_str.join(part)
        print(f'part -> ', part)
        print('all --> ', msg_str)
        # msg = eval(msg_str)
        # print('all eval --> ', msg)

        msg = ['string too long!!!\n', 'string too long!!!\n', 'string too long!!!\n']

        # data = []
        # while True:
        #     part = client_socket.recv(16000)
        #     if not part:
        #         break
        #     data.append(part)
        # data_arr = pickle.loads(b"".join(data))
        # print(type(data_arr), data_arr)
        # msg = data_arr.decode()
        # print(type(msg), msg)

        print('long msg ->', msg)
        return msg
    else:
        print('short msg ->', msg_get_back)
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
