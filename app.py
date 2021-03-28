from db import User, System
import os
from flask import Flask, request, send_from_directory
from flask.json import jsonify
from werkzeug.utils import secure_filename
 
app = Flask(__name__, static_url_path='')

app.config['MAX_CONTENT_PATH'] = 100




@app.route('/')
def root():
    return app.send_static_file('formpage.html')

@app.route('/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory('photos', filename)

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


@app.route('/gallery', methods = ['GET'])
def show_page_gallery():
    return app.send_static_file('gallery.html')


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

@app.route('/buylikes/', methods = ['POST'])
def likes_purchase():
    ui = User()
    purchase = ui.likes_purchase(request.get_json()['user_id'],request.get_json()['number'])
    if purchase != None:
        return {
            'code': 200,
            'user_id': purchase.user_id,
            'likes_balance': purchase.likes,
            'total_payments': purchase.payments
        }
    else:
        return {
            'code': 400,
            'reason': 'Something went wrong. Please try again later'
        }


@app.route('/userinfo', methods = ['POST'])
def get_user_info():
    ui = User()
    info = ui.get_user_info(request.get_json()['user_id'])
    if info != None:
        return {
            'code': 200,
            'user_id': info.user_id,
            'likes_balance': info.likes,
            'total_payments': info.payments,
            'total_likes': info.liked_photos
        }
    else:
        return {
            'code': 400,
            'reason': 'Something went wrong. Please try again later'
        }


@app.route('/like', methods = ['POST'])
def like_a_photo():
    ui = User()
    like = ui.like_a_photo(request.get_json()['user_id'], request.get_json()['photo_id'])
    if like != None:
        return {
            'code': 200,
            'user_id': like['user_info']['user_id'],
            'liked_photos': like['photo']['total_likes']
        }
    else: 
        return {
            'code': 400,
            'reason':'Something went wrong. Please try again later'
        }


@app.route('/int_update_likes', methods = ['POST'])
def update_likes():
    ui = System()
    update = ui.likes_updated()
    return {
        'code': 200
    }


@app.route('/int_gallery', methods = ['POST'])
def update_gallery():
    ui = System()
    render = ui.render_photos()
    return {
        'code': 200,
        '0': render[0],
        '1': render[1],
        '2': render[2],
        '3': render[3],
        '4': render[4],
        '5': render[5]
    }


@app.route('/uploader', methods = ['POST'])
def upload_file():
   f = request.files['photo']
   name = secure_filename(f.filename)
   os.makedirs('photos', exist_ok=True)
   f.save(os.path.join('photos', secure_filename(f.filename)))
   ui = User()
   save = ui.upload_photos(request.form['user_id'], request.form['description'], name)
   if save != None:
       return 'OK'
   else:
       return 'Something went wrong'


