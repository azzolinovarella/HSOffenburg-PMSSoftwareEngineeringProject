from flask import Flask, request, jsonify
from werkzeug import exceptions
from .user_files.user import User
from .admin_files.admin import Admin

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'This is working!! Options\n' \
           '/add_user --> POST\n' \
           '/edit_password --> PUT\n' \
           '/add_service --> PUT\n' \
           '/edit_service --> PUT\n' \
           '/del_service --> DELETE\n' \
           '/check_user --> GET\n' \
           '/del_user --> DELETE\n' \
           '/admin_options --> PUT\n' \
           '/admin_edit --> PUT'


@app.route('/add_user', methods=['POST'])
def add_user():
    """This function is used to add user to our system, but NOT their services."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            return jsonify(Process='Invalid', Process_Message='This user already exists.')
        if validator == 'invalid':
            return jsonify(Process='Invalid', Process_Message='This user email is invalid.')
        resp = User.create_user(user_email, user_password)
        if isinstance(resp, User):
            new_user = resp
            user_list.append(new_user)
            User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
            return jsonify(Process='Valid', Process_Message=f'User {user_email} created successfully!')
        return jsonify(Process='Invalid', Process_Message='Invalid password.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/edit_password', methods=['PUT'])
def edit_password():
    """This function is used to edit the user's password of the system."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']
        user_new_password = req_data['user_new_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].change_user_password(user_password, user_new_password)
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/add_service', methods=['PUT'])
def add_service():
    """This function is used to add a service for the given user."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']
        service_name = req_data['service_name']
        service_password = req_data['service_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].create_service(user_password, service_name, service_password)
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/edit_service', methods=['PUT'])  # TIRAR CONFIRMAÇÃO DE SENHA! DESNECESSARIO
def edit_service():
    """This function is used to edit the password of a certain user's service."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']
        service_name = req_data['service_name']
        service_new_password = req_data['service_new_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].change_service(user_password, service_name, service_new_password)
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/del_service', methods=['DELETE'])
def del_service():
    """This function is used to delete a given user's service."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']
        service_name = req_data['service_name']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].delete_service(user_password, service_name)
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/check_user', methods=['GET'])
def check_user():
    """This function is used to check the user data."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].get_user_data(user_password)
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/del_user', methods=['DELETE'])
def del_user():
    """This function is used to delete all user data from our system."""

    try:
        req_data = request.get_json()
        user_email = req_data['user_email']
        user_password = req_data['user_password']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if validator == 'exists':
            if user_list[pos].active is True:
                resp = user_list[pos].delete_user(user_password)
                if resp[0] == 'Valid':
                    del user_list[pos]
                User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                return jsonify(Process=resp[0], Process_Message=resp[1])
            else:
                return jsonify(Process='Invalid', Process_Message='Your account was deactivated because of many tries to'
                                                                  'access/modify it.Enter in contact with an ADM to '
                                                                  'reactivate it.')
        return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/admin_options', methods=['PUT'])
def admin_options():
    """This function is special for administrator utilization only.
    In this function, the admin can select between:
    - Activate/deactivate an user;
    - Delete an user;
    - Reset randomly the user's password (for allow him to switch it latter);
    """

    try:
        req_data = request.get_json()
        admin_login = req_data['admin_login']
        admin_pw1 = req_data['admin_pw1']
        admin_pw2 = req_data['admin_pw2']
        admin_opt = req_data['admin_opt']
        user_email = req_data['user_email']

        email_list, user_list = User.get_emails_and_users('software_engineering_project/json_files/UserData.json')
        validator, pos = User.check_email(user_email, email_list)  # Get the email list, and the position

        if Admin.admin_checker(admin_login, admin_pw1, admin_pw2,
                               'software_engineering_project/json_files/AdminEspecifications.json'):
            if validator == 'exists':
                if admin_opt == 'ACT':
                    resp = Admin.activate(user_list[pos])
                    User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                    return jsonify(Process=resp[0], Process_Message=resp[1])
                elif admin_opt == 'DEACT':
                    resp = Admin.deactivate(user_list[pos])
                    User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                    return jsonify(Process=resp[0], Process_Message=resp[1])
                elif admin_opt == 'DEL':
                    resp = Admin.delete(user_list[pos])
                    del user_list[pos]
                    User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                    return jsonify(Process=resp[0], Process_Message=resp[1])
                elif admin_opt == 'RANDPAS':
                    resp = Admin.random_password(user_list[pos])
                    User.user_to_json(user_list, 'software_engineering_project/json_files/UserData.json')
                    return jsonify(Process=resp[0], Process_Message=resp[1])
                return jsonify(Process='Invalid', Process_Message='Invalid option.')
            return jsonify(Process='Invalid', Process_Message='This user do not exists or it is invalid.')
        return jsonify(Process='Invalid', Process_Message='Wrong admin validation!')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')


@app.route('/admin_edit', methods=['PUT'])
def admin_edit():
    """This function allows the admin to change its passwords and login."""

    try:
        req_data = request.get_json()
        admin_login = req_data['admin_login']
        admin_pw1 = req_data['admin_pw1']
        admin_pw2 = req_data['admin_pw2']
        admin_new_login = req_data['admin_new_login']
        admin_new_pw1 = req_data['admin_new_pw1']
        admin_new_pw2 = req_data['admin_new_pw2']

        if Admin.admin_checker(admin_login, admin_pw1, admin_pw2,
                               'software_engineering_project/json_files/AdminEspecifications.json'):
            Admin.edit_admin_data(admin_new_login, admin_new_pw1, admin_new_pw2,
                                  'software_engineering_project/json_files/AdminEspecifications.json')
            return jsonify(Process='Valid', Process_Message='Admin data changed successfully!')
        return jsonify(Process='Invalid', Process_Message='Wrong admin validation!')
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')

# admin_edit_password_rules??


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.102')  # The user should type the machine ID here
