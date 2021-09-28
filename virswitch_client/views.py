from flask import render_template, request, redirect, url_for, session
from virswitch_client import app, comm
import hashlib

active_u = ''
names = []
admin = False
vms = []


@app.route('/')
def index():
    ip = comm.read_ip()
    print(f'ip = {ip}')
    if ip == 'wrong_ip':
        return render_template('bad_config.html')
    else:
        return render_template('index.html')


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
        if msg_back[0] == 'password_ok':
            session['username'] = msg_back[1]
            active_u = session['username']
            if msg_back[3] == 'yes':
                admin = True
            else:
                admin = False
            vms = msg_back[4].split(',')

            return redirect(url_for('vmachines'))
        elif comm.msg(msg)[0] == 'password_wrong':
            return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/bad_config', methods=["POST", "GET"])
def bad_config():
    return render_template('bad_config.html')


@app.route('/start_vm', methods=["POST", "GET"])
def start_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        msg_id = "start"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/stop_vm', methods=["POST", "GET"])
def stop_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        msg_id = "stop"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/restart_vm', methods=["POST", "GET"])
def restart_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        msg_id = "restart"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/kill_vm', methods=["POST", "GET"])
def kill_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        msg_id = "kill"
        msg = [msg_id, active_u, vm, '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        host_info = comm.msg(["host_memory", active_u, '', ''])
        return render_template('vmachines.html', v_list=vms_list, host_info=host_info, active_u=active_u)


@app.route('/change_cpus', methods=["POST", "GET"])
def change_cpus():
    if request.method == "POST":
        vm = request.args.get('vm')
        new_cpus = request.form.get("new_cpus")
        msg_id = "new_cpus"
        msg = [msg_id, active_u, vm, new_cpus]
        msg_back = comm.msg(msg)
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
        msg_back = comm.msg(msg)
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
        msg_back = comm.msg(msg)
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
    host_info = comm.msg(["host_memory", active_u, '', ''])
    msg_id = "v_list"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
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


@app.route('/users', methods=["POST", "GET"])
def users():
    msg_id = "get_user_list"
    msg = [msg_id, '', '', '']
    u_list = comm.msg(msg)
    msg_id = "v_list"
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    vms_list = comm.admin_check(admin, msg_back, vms)
    return render_template('users.html', u_list=u_list, v_list=vms_list, active_u=active_u)


@app.route('/vm_users', methods=["POST", "GET"])
def vm_users():
    vm_selected = request.args.get('vm')
    msg_id = "get_user_list"
    msg = [msg_id, '', '', '']
    u_list = comm.msg(msg)

    vm_users_set = set()
    all_users_list = []

    for user in u_list:
        if user[1] == 'no':
            all_users_list.append(user[0])
        user_vms_list = user[2].split(',')
        if vm_selected in user_vms_list:
            vm_users_set.add(user[0])
    return render_template('vm_users.html', u_list=u_list, vm=vm_selected, vm_users_set=vm_users_set, all_users_list=all_users_list)


@app.route('/add_user_to_vm', methods=["POST", "GET"])
def add_user_to_vm():
    vm_selected = request.form.get('vm')
    vm_user = request.form.get('user_add')
    action = 'add'
    msg_id = "update_user_vm_list"
    msg = [msg_id, vm_user, vm_selected, action]
    u_list = comm.msg(msg)
    return redirect(f'/vm_users?vm={vm_selected}')


@app.route('/remove_user_from_vm', methods=["POST", "GET"])
def remove_user_from_vm():
    vm_selected = request.form.get('vm')
    vm_user = request.form.get('user_remove')
    action = 'remove'
    msg_id = "update_user_vm_list"
    msg = [msg_id, vm_user, vm_selected, action]
    u_list = comm.msg(msg)
    return redirect(f'/vm_users?vm={vm_selected}')


@app.route('/add_user', methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        login = request.form.get('login_')
        pas = request.form.get("pass_")
        password = hashlib.md5(pas.encode()).hexdigest()
        vm_list = request.form.getlist("vm_")
        vms = ",".join(vm_list)
        is_admin = request.form.get("is_admin")

        msg_id = "get_user_list"
        msg = [msg_id, '', '', '']
        u_list = comm.msg(msg)
        for user in u_list:
            if login == user[0]:
                return render_template('user_exists.html', login=login)

        msg_id = "add_user"
        msg = [msg_id, login, [password, is_admin, vms], '']
        u_list = comm.msg(msg)
        msg_id = "v_list"
        msg = [msg_id, active_u, '', '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('users.html', u_list=u_list, v_list=vms_list)


@app.route('/add_vm_user', methods=["POST", "GET"])
def add_vm_user():
    if request.method == "POST":
        vm = request.args.get("vm")
        login = request.form.get('login_')
        pas = request.form.get("pass_")
        password = hashlib.md5(pas.encode()).hexdigest()
        vms = "-"
        is_admin = 'no'

        msg_id = "get_user_list"
        msg = [msg_id, '', '', '']
        u_list = comm.msg(msg)
        for user in u_list:
            if login == user[0]:
                return render_template('user_exists.html', login=login)

        msg_id = "add_user"
        msg = [msg_id, login, [password, is_admin, vms], '']
        u_list = comm.msg(msg)
        return redirect(f'/vm_users?vm={vm}')


@app.route('/delete_user', methods=["POST", "GET"])
def delete_user():
    if request.method == "POST":
        login = request.form.get('login_confirm')
        msg_id = "delete_user"
        msg = [msg_id, login, '', '']
        u_list = comm.msg(msg)
        msg_id = "v_list"
        msg = [msg_id, active_u, '', '']
        msg_back = comm.msg(msg)
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('users.html', u_list=u_list, v_list=vms_list)


@app.route('/logs', methods=["POST", "GET"])
def logs():
    msg_id = "get_logs"
    try:
        current_page = int(request.args.get('page'))
    except TypeError:
        current_page = 1
    msg = [msg_id, '', current_page, '']
    msg_back = comm.msg(msg)
    logs_pack = msg_back
    prev = logs_pack.get('prev')
    next = logs_pack.get('next')
    current_page = logs_pack.get('current')
    logs = logs_pack.get('log_pack')
    return render_template('logs.html', logs=logs, current_page=current_page, prev=prev, next=next)


@app.route('/reset_logs', methods=["POST", "GET"])
def reset_logs():
    msg_id = "reset_logs"
    active_u = '+++'
    print(active_u)
    active_u = session['username']
    print(active_u)
    msg = [msg_id, active_u, '', '']
    msg_back = comm.msg(msg)
    logs = msg_back
    return render_template('logs.html', logs=logs)


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
        return redirect('/vmachines')


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

