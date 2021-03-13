from db import User
from flask import Flask, request, send_from_directory
from flask.json import jsonify

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('formpage.html')


@app.route('/login', methods=['GET'])
def show_page_login():
    return app.send_static_file('loginpage.html')


@app.route('/area/<user_id>', methods=['GET'])
def show_page_area(user_id):
    return app.send_static_file('personalmain.html')


@app.route('/password', methods=['GET'])
def show_page_password():
    return app.send_static_file('passwordrecovery.html')


@app.route('/recover/<link_id>', methods=['GET'])
def show_page_recover(link_id):
    return app.send_static_file('recovery_field.html')


@app.route('/register/', methods=['POST'])
def register():
    ui = User()
    default_password = ui.register(request.get_json()['name'], request.get_json()[
                                   'surname'], request.get_json()['email'])
    if default_password != None:
        return {
            'code': 200,
            'default_password': default_password
        }
    else:
        return {
            'code': 400,
            'reason': 'The user with the email '+request.get_json()['email']+' already exists'
        }


@app.route('/login/', methods=['POST'])
def signin():
    ui = User()
    check = ui.signin(request.get_json()[
                      'email'], request.get_json()['password'])
    if check != None:
        return {
            'code': 200,
            'user_id': check
        }
    else:
        return {
            'code': 400,
            'reason': 'Either the password or the email is not correct. Please try again'
        }


@app.route('/recover/', methods=['POST'])
def recover_password():
    ui = User()
    process = ui.recover_password(request.get_json()['email'])
    if process != None:
        return {
            'code': 200,
            'link': process
        }
    else:
        return {
            'code': 200,
            'reason': 'If you are registered you will receive your link to the email you have entered'
        }


@app.route('/setapassword/', methods=['POST'])
def generate_password():
    ui = User()
    new_password = ui.generate_password(request.get_json()['link_id'])
    if new_password != None:
        return {
            'code': 200,
            'new_password': new_password
        }
    else:
        return {
            'code': 400,
            'reason': 'Your unique link seems to have expired. Please try again'
        }
