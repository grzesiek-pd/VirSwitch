from flask import redirect
from virswitch_client import app
import socket as sock
import os
import re

from virswitch_client.encrypt import Crypt


def read_ip():
    ip = []
    try:
        f = open('ip_config.txt', 'r', encoding='utf-8')
        o = f.read()
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", o)
    except FileNotFoundError:
        print(f'file ip_config.txt not found!')
        f_create = open('ip_config.txt', 'w+', encoding='utf-8')
        f_create.write('your_server_ip_here')

    if len(ip) == 1:
        host = ip[0]
        print(f'host = ({type(host)})<>{host}<>')
    else:
        print(f'wrong ip address')
        host = 'wrong_ip'

    try:
        port = 3333
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        if result == 0:
            print(f'Connect {host} / {port}')
        else:
            host = 'wrong_ip'
            print(f'No connect to {host} / {port}')
    except:
        pass
    return host

    # try:
    #     # rel_path = "virswitch_client/ip_config.txt"
    #     # script_dir = os.path.dirname(__file__)
    #     # file_path = os.path.join(script_dir, rel_path)
    #     # print(file_path)
    #     # f = open('ip_config.txt', 'a+', encoding='utf-8')
    #     f = open('ip_config.txt', 'r', encoding='utf-8')
    #     # f = open(f'{file_path}', 'r', encoding='utf-8')
    #     ip = f.readline()
    #     print(f'ip =  {ip}')
    #     return ip
    # except IOError as err:
    #     print('No ip_config file!')
    #     print(f'Error: {err}')


@app.route('/msg')
def msg(msg_to_send):
    host = read_ip()

    print(f'host = {host}')
    # host = '192.168.0.77'
    # host = '192.168.122.11'
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

    else:
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
