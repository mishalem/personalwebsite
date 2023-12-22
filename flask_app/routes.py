# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, flash
from flask import jsonify, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from .utils.blockchain.blockchain import Block, Blockchain
from werkzeug.utils import secure_filename
from pprint import pprint
import os
import json
import random
import functools
import base64
import imghdr
from jinja2 import Undefined
from . import socketio
db = database()


UPLOAD_FOLDER = "flask_app/static/main/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    # db.reversibleEncrypt("decrypt", session['email'])
    return db.reversibleEncrypt("decrypt", session['email']) if 'email' in session else 'Unknown'


@app.route('/login')
def login():
    return render_template('login.html', user=getUser())

@app.route('/signup')
def signup():
    return render_template('signup.html', user=getUser())

@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    my_dict = db.authenticate(form_fields['email'], form_fields['password'])
    if my_dict['success'] == 1:
        session['email'] = db.reversibleEncrypt("encrypt", form_fields['email'])
        status = {'status' :'1'}
        return json.dumps(status)
    else:
        status = {'status' :'0'}
        return json.dumps(status)


@app.route('/process_signup', methods = ["POST","GET"])
def process_signup():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    my_dict = db.authenticate(form_fields['email'], form_fields['password'])
    if my_dict['success'] == 1:
        status = {'status' :'0'}
        return json.dumps(status)
    db.createUser(form_fields['email'], form_fields['password'], 'guest', balance=100)
    status = {'status' :'1'}
    return json.dumps(status)


#######################################################################################
# MARKETPLACE RELATED
#######################################################################################
@app.route('/marketplace')
@login_required
def marketplace():
    return render_template('marketplace.html', user=getUser())

@app.route('/sellerpage')
@login_required
def sellerpage():
    nft_dict = db.getNFT()
    for key in nft_dict.keys():
        nft_dict[key]['image'] = nft_dict[key]['image'].decode('utf-8')
    return render_template('sellerpage.html', user=getUser(), nft_data = nft_dict, balance = db.getBalance(getUser()))

@app.route('/buyerpage')
@login_required
def buyerpage():
    nft_dict = db.getNFT()
    for key in nft_dict.keys():
        nft_dict[key]['image'] = nft_dict[key]['image'].decode('utf-8')
    return render_template('buyerpage.html', user=getUser(), nft_data = nft_dict, balance = db.getBalance(getUser()))


@app.route('/adminpage')
@login_required
def adminpage():
    nft_dict = db.getNFT()
    transactions = {}
    for key in nft_dict.keys():
        nft_dict[key]['image'] = nft_dict[key]['image'].decode('utf-8')
        transactions[key] = db.getTransactions(str(key))
    print(transactions)
    return render_template('adminpage.html', user=getUser(), nft_data = nft_dict, transactions = transactions)



@app.route('/process_nft', methods = ["POST","GET"])
@login_required
def process_nft():
    x = random.choice(['NFT01.jpg','NFT02.jpeg','NFT03.jpg', 'NFT04.png'])
    my_str = 'flask_app/static/main/images/' + x
    with open(my_str,  'rb') as file:
        image_data = file.read()
    data = base64.b64encode(image_data)
    data = data.decode('utf-8')
    description = request.form.get('description')
    token = request.form.get('token')
    db.createNFT(description=description, token=token, image=data, owner=getUser())
    return json.dumps({'status' :'1'}) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}



@app.route('/upload_nft', methods = ["POST","GET"])
@login_required
def upload_nft():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return json.dumps({'status' :'0'}) 
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return json.dumps({'status' :'0'}) 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    my_str = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(my_str,  'rb') as file:
        image_data = file.read()
    data = base64.b64encode(image_data)
    data = data.decode('utf-8')
    description = request.form.get('description')
    token = request.form.get('token')
    db.createNFT(description=description, token=token, image=data, owner=getUser())
    return json.dumps({'status' :'1'}) 

@app.route('/update_nft_description', methods=['POST'])
@login_required
def update_nft_description():
    nft_id = request.form.get('nft_id')
    description = request.form.get('description')
    db.update_nft_description(nft_id, description)
    status = {'status' :'1'}
    return json.dumps(status)

@app.route('/update_nft_token', methods=['POST'])
@login_required
def update_nft_token():
    nft_id = request.form.get('nft_id')
    token = request.form.get('token')
    db.update_nft_token(nft_id, token)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/process_transaction', methods=['POST'])
@login_required
def process_transaction():
    buyer = request.form.get('buyer')
    nft_id = request.form.get('nft_id')
    token = request.form.get('token')
    db.completeTransaction(nft_id, buyer, token)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/show_nft', methods=["POST"])
@login_required
def show_nft():
    nft_id = request.form.get('nft_id')
    nft_id = str(nft_id)
    print(nft_id)
    return json.dumps(db.getTransactions(nft_id))


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    if getUser() == 'owner@email.com':
        # this line and lines similar to it were provided by the professor
        emit('status', {'msg': getUser() + ' has joined the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
       emit('status', {'msg': getUser() + ' has joined the room.', 'style': 'width: 100%;color:gray;text-align: left'}, room='main') 



@socketio.on('disconnect', namespace='/chat')
def left():
    leave_room('main')
    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
       emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:gray;text-align: left'}, room='main') 
    return render_template('home.html')

@socketio.on('message', namespace='/chat')
def message(message):
    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ': ' + message['message']['message'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('status', {'msg': getUser() + ': ' + message['message']['message'], 'style': 'width: 100%;color:grey;text-align: left'}, room='main')

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
    print(db.query('SELECT * FROM users'))
    x = random.choice(['I won my first chess championship at the age of 12.','I have had the pleasure of meeting individuals from over 15 different countries.'])
    return render_template('home.html', user=getUser(), fun_fact = x)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    return render_template('resume.html', resume_data = resume_data, user=getUser())

@app.route('/projects')
def projects():
    return render_template('projects.html', user=getUser())


@app.route('/piano')
def piano():
    return render_template('piano.html', user=getUser())

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', user=getUser())

@app.route('/processfeedback', methods=['POST'])
def userFeedback():
    my_list = []
    my_dict = request.form.to_dict()
    for key,val in my_dict.items():
        my_list.append(val)
    db.insertRows('feedback.sql', "random", my_list)
    feedbackData = db.getFeedbackData()
    return render_template('processfeedback.html', feedbackData=feedbackData)


@app.route('/editResume')
@login_required
def edit_Resume():
    resume_data = db.getResumeData()
    return render_template('editResume.html', resume_data = resume_data, user=getUser())



@app.route('/update_institution', methods=['POST'])
def update_institution():
    inst_id = request.form.get('inst_id')

    name = request.form.get('name')
    department = request.form.get('department')
    address = request.form.get('address')
    city = request.form.get('city')
    db.update_institution(inst_id,name, department, address, city)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/update_name', methods=['POST'])
def update_name():
    inst_id = request.form.get('inst_id')
    name = request.form.get('name')
    db.update_name(inst_id, name)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/update_department', methods=['POST'])
def update_department():
    inst_id = request.form.get('inst_id')
    department = request.form.get('department')
    db.update_department(inst_id, department)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/update_address', methods=['POST'])
def update_address():
    inst_id = request.form.get('inst_id')
    address = request.form.get('address')
    db.update_address(inst_id, address)
    status = {'status' :'1'}
    return json.dumps(status)

@app.route('/update_city', methods=['POST'])
def update_city():
    inst_id = request.form.get('inst_id')
    city = request.form.get('city')
    db.update_city(inst_id, city)
    status = {'status' :'1'}
    return json.dumps(status)



@app.route('/update_title', methods=['POST'])
def update_title():
    pos_id = request.form.get('pos_id')
    title = request.form.get('title')
    db.update_title(pos_id, title)
    status = {'status' :'1'}
    return json.dumps(status)



@app.route('/update_start_date', methods=['POST'])
def update_start_date():
    pos_id = request.form.get('pos_id')
    start_date = request.form.get('start_date')
    db.update_start_date(pos_id, start_date)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/update_end_date', methods=['POST'])
def update_end_date():
    pos_id = request.form.get('pos_id')
    end_date = request.form.get('end_date')
    db.update_end_date(pos_id, end_date)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/update_skills', methods=['POST'])
def update_skills():
    skill_id = request.form.get('skill_id')
    name = request.form.get('skills')
    db.update_skills(skill_id, name)
    status = {'status' :'1'}
    return json.dumps(status)



@app.route('/update_expname', methods=['POST'])
def update_expname():
    exp_id = request.form.get('exp_id')
    expname = request.form.get('expname')
    db.update_expname(exp_id, expname)
    status = {'status' :'1'}
    return json.dumps(status)



@app.route('/update_description', methods=['POST'])
def update_description():
    exp_id = request.form.get('exp_id')
    description = request.form.get('description')
    print(description)
    db.update_description(exp_id, description)
    status = {'status' :'1'}
    return json.dumps(status)


@app.route('/add_entry', methods=['POST'])
def add_entry():
    institution = request.form.get('institution')
    department = request.form.get('department')
    address = request.form.get('address')
    city = request.form.get('city')
    position = request.form.get('position')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    position_name = request.form.get('position_name')
    position_description = request.form.get('position_description')
    skill = request.form.get('skill')
    db.add_entry(institution, department, address, city, position, start_date, end_date, position_name, position_description, skill)
    return render_template("resume.html",  resume_data = db.getResumeData(), user = getUser())