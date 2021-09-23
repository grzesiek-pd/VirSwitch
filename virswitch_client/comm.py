from virswitch_client import app
import socket as sock

from virswitch_client.encrypt import Crypt


@app.route('/msg')
def msg(msg_to_send):
    # host = '192.168.122.11'
    host = '192.168.0.77'
    # host = '192.168.81.131'
    # host = '127.0.0.1'
    port = 3333
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect((host, port))

    pack_to_send = Crypt.encrypt(msg_to_send)
    client_socket.send(pack_to_send)

    # send pack view
    # print(f'-------------------')
    # print(f'przygotowana paczka -> {type(msg_to_send)}--{msg_to_send}')
    # print(f'zakodowana paczka -> {type(pack_to_send)}--{pack_to_send}')

    msg_back = client_socket.recv(8000)
    msg_get_back = Crypt.decrypt(msg_back)

    # received pack view
    # print(f'-------------------')
    # print(f'otrzymana paczka -> {type(msg_back)}--{msg_back}')
    # print(f'rozkodowana paczka -> {type(msg_get_back)}--{msg_get_back}')

    if msg_get_back == 'error':
        print('error!')

    elif msg_get_back in range(32000):
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
        # print('short msg ->', msg_get_back)
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
