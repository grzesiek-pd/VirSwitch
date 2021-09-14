from flask import render_template, request, redirect, url_for
from virswitch_client import app, comm
import hashlib

active_u = ''
names = []
admin = False
vms = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_vm', methods=["POST", "GET"])
def start_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        # print(vm)
        msg_id = "start"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/stop_vm', methods=["POST", "GET"])
def stop_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        # print(vm)
        msg_id = "stop"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/restart_vm', methods=["POST", "GET"])
def restart_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        # print(vm)
        msg_id = "restart"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/kill_vm', methods=["POST", "GET"])
def kill_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        # print(vm)
        msg_id = "kill"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/change_memory', methods=["POST", "GET"])
def change_memory():
    if request.method == "POST":
        vm = request.args.get('vm')
        new_memory = request.form.get("new_memory")
        msg_id = "new_memory"
        msg = [msg_id, active_u, vm, new_memory]
        # print(msg)
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/change_max_memory', methods=["POST", "GET"])
def change_max_memory():
    if request.method == "POST":
        vm = request.args.get('vm')
        new_max_memory = request.form.get("new_max_memory")
        msg_id = "new_max_memory"
        msg = [msg_id, active_u, vm, new_max_memory]
        # print(msg)
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/vmachines', methods=["POST", "GET"])
def vmachines():
    global active_u
    global admin
    global vms

    msg_id = "get_user_list"
    msg = [msg_id, '', '', '']
    u_list = comm.msg(msg)
    print(f'{type(u_list)}--{u_list}')
    host_info = comm.msg(["host_memory", active_u, '', ''])
    msg_id = "v_list"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    # print(type(msg_back))
    vms_list = comm.admin_check(admin, msg_back, vms)
    for line in vms_list:
        vm_users_list = []
        for user in u_list:
            vm_user = user[2].split(",")
            if line[0] in vm_user:
                vm_users_list.append(user[0])
        vm_users = ", ".join(vm_users_list)
        line.append(vm_users)
    return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/login', methods=["POST", "GET"])
def login():
    global active_u
    global admin
    global vms

    if request.method == "POST":
        msg_id = "user_check"
        log = request.form["login_"]
        pas = request.form["pass_"]
        password = hashlib.md5(pas.encode()).hexdigest()
        msg = [msg_id, log, pas, password]
        msg_back = comm.msg(msg)
        # print(msg_back)
        if msg_back[0] == 'password_ok':
            active_u = msg_back[1]
            if msg_back[3] == 'yes':
                admin = True
            else:
                admin = False
            vms = msg_back[4].split(',')
            # print(msg_back)
            # print(active_u, admin, vms)

            return redirect(url_for('vmachines'))
        elif comm.msg(msg)[0] == 'password_wrong':
            return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/users', methods=["POST", "GET"])
def users():
    msg_id = "get_user_list"
    msg = [msg_id, '', '', '']
    u_list = comm.msg(msg)
    msg_id = "v_list"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    # print(type(msg_back))
    vms_list = comm.admin_check(admin, msg_back, vms)
    return render_template('users.html', u_list=u_list, v_list=vms_list)


@app.route('/vm_users', methods=["POST", "GET"])
def vm_users():
    msg_id = "get_user_list"
    msg = [msg_id, '', '', '']
    u_list = comm.msg(msg)
    msg_id = "v_list"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    # print(type(msg_back))
    vms_list = comm.admin_check(admin, msg_back, vms)
    return render_template('vm_users.html', u_list=u_list, v_list=vms_list)


@app.route('/add_user', methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        login = request.form.get('login_')
        pas = request.form.get("pass_")
        password = hashlib.md5(pas.encode()).hexdigest()
        vm_list = request.form.getlist("vm_")
        vms = ",".join(vm_list)
        is_admin = request.form.get("is_admin")
        msg_id = "add_user"
        msg = [msg_id, login, [password, is_admin, vms], '']
        # print(msg)
        u_list = comm.msg(msg)
        msg_id = "v_list"
        msg = [msg_id, active_u, '', '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('users.html', u_list=u_list, v_list=vms_list)


@app.route('/delete_user', methods=["POST", "GET"])
def delete_user():
    if request.method == "POST":
        login = request.form.get('login_confirm')
        msg_id = "delete_user"
        msg = [msg_id, login, '', '']
        # print(msg)
        u_list = comm.msg(msg)
        msg_id = "v_list"
        msg = [msg_id, active_u, '', '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('users.html', u_list=u_list, v_list=vms_list)


@app.route('/logs', methods=["POST", "GET"])
def logs():

    msg_id = "get_logs"
    msg = [msg_id, '', '', '']
    msg_back = comm.msg(msg)
    # print(type(msg_back))
    logs = msg_back
    return render_template('logs.html', logs=logs)


@app.route('/reset_logs', methods=["POST", "GET"])
def reset_logs():
    msg_id = "reset_logs"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    # print(type(msg_back))
    logs = msg_back
    return render_template('logs.html', logs=logs)


@app.route('/vm_details', methods=["POST", "GET"])
def vm_details():
    if request.method == "POST":
        vm = request.args.get('vm')
        msg_id = "get_vm_details"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        # print(type(msg_back))
        vm_details = msg_back
    # vm_details = "xxxxxxxxxxxxxx"
    return render_template('vm_details.html', vm_details=vm_details)
    # return render_template('vm_details.html')


@app.route('/update_description', methods=["POST", "GET"])
def update_description():
    if request.method == "POST":
        vm = request.form.get('vmName')
        vm_ip = request.form.get("vmIp")
        vm_pass = request.form.get("vmPass")

        msg_id = "update_description"
        description = {
            "ip": vm_ip,
            "pass": vm_pass
        }
        msg = [msg_id, active_u, vm, description]
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(400)
def request_error(error):
    return render_template('errors/400.html')


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html')


@app.errorhandler(405)
def method_error(error):
    return render_template('errors/405.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html')


@app.context_processor
def inject_variables():
    return dict(active_u=active_u, admin=admin, names=names)

