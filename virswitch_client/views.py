from flask import render_template, request, redirect, url_for
from virswitch_client import app, comm, models

active_u = ''
admin = False
vms = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_vm', methods=["POST", "GET"])
def start_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        print(vm)
        msg_id = "start"
        msg = [msg_id, vm, '']
        msg_back = comm.msg(msg)
        print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('vmachines.html', v_list=vms_list)


@app.route('/stop_vm', methods=["POST", "GET"])
def stop_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        print(vm)
        msg_id = "stop"
        msg = [msg_id, vm, '']
        msg_back = comm.msg(msg)
        print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('vmachines.html', v_list=vms_list)


@app.route('/restart_vm', methods=["POST", "GET"])
def restart_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        print(vm)
        msg_id = "restart"
        msg = [msg_id, vm, '']
        msg_back = comm.msg(msg)
        print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('vmachines.html', v_list=vms_list)


@app.route('/kill_vm', methods=["POST", "GET"])
def kill_vm():
    if request.method == "POST":
        vm = request.args.get('vm')
        print(vm)
        msg_id = "kill"
        msg = [msg_id, vm, '']
        msg_back = comm.msg(msg)
        print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('vmachines.html', v_list=vms_list)


@app.route('/vmachines', methods=["POST", "GET"])
def vmachines():
    global active_u
    global admin
    global vms

    if request.method == "POST":
        msg_id = "v_list"
        msg = [msg_id, active_u, active_u]
        msg_back = comm.msg(msg)
        print(type(msg_back))
        vms_list = comm.admin_check(admin, msg_back, vms)
        return render_template('vmachines.html', v_list=vms_list)
    return render_template('vmachines.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    global active_u
    global admin
    global vms

    if request.method == "POST":
        msg_id = "user_check"
        log = request.form["login_"]
        pas = request.form["pass_"]
        msg = [msg_id, log, pas]
        msg_back = comm.msg(msg)
        print(msg_back)
        if msg_back[0] == 'password_ok':
            active_u = msg_back[1]
            admin = msg_back[3]
            vms = msg_back[4]
            print(msg_back)

            return redirect(url_for('vmachines'))
        elif comm.msg(msg)[0] == 'password_wrong':
            return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/users', methods=["POST", "GET"])
def users():
    if request.method == "POST":
        msg_id = "get_user_list"
        msg = [msg_id, '', '']
        u_back = comm.msg(msg)
        u_list = u_back.items()
        return render_template('users.html', u_list=u_list)
    return render_template('users.html')


@app.route('/logs', methods=["POST", "GET"])
def logs():
    if request.method == "POST":
        msg_id = "get_logs"
        msg = [msg_id, '', '']
        msg_back = comm.msg(msg)
        print(type(msg_back))
        logs = msg_back
        return render_template('logs.html', logs=logs)
    return render_template('logs.html')


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
    return dict(
        name=active_u,
        admin=admin)

