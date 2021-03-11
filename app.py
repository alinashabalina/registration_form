from db import User
from flask import Flask, request, send_from_directory
from flask.json import jsonify

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('formpage.html')

@app.route('/register/', methods = ['POST'])
def register():
    ui = User()
    default_password = ui.register(request.get_json()['name'], request.get_json()['surname'], request.get_json()['email'])
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


@app.route('/login/', methods = ['POST'])
def signin():
    ui = User()
    check = ui.signin(request.get_json()['email'], request.get_json()['password'])
    return {
        'code': 200,
        'user_id': check
    }
    

@app.route('/recover/', methods = ['POST'])
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
    