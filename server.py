from flask import Flask,session,render_template,flash,request,redirect,url_for,jsonify,send_from_directory,send_file,Response
from flask_socketio import SocketIO,emit,join_room
from werkzeug.utils import secure_filename
import pandas as pd
import os,time

from datetime import timedelta,datetime

# from Data_Models.connect_db import *
import sqlite3
conn = sqlite3.connect("database.db",check_same_thread=False)
c=conn.cursor()

from Data_Models.College import *
from Data_Models.User import *
from Data_Models.Class import *
from Data_Models.Assignment import *
from Data_Models.Chat import *
from Data_Models.Announcements import *

import re

app = Flask(__name__,template_folder="./template")
# allowed_extensions=['txt', 'csv', 'ppt', 'pptx' , 'doc','docx','mp3','mp4']
app.config['UPLOAD_FOLDER'] = '.\\uploads'
app.secret_key = "(*&$^JSDHDjdffjjfp;pwwdm&)%$(&)$"
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=150)
socketio=SocketIO(app)

#printdb
# for i in ['college','class','assignment','urc','ura','cra','chat','clrch','user','announcements']:
# 	c.execute("select * from "+i)
# 	print(i.upper(),c.fetchall(),sep="::::  ",end="\n\n")

def check_session():
	if 'user' in session:
		return True
	return False
	


@app.route('/')
def home():
    if 'user' in session:
        return redirect('/Class')
    return redirect(url_for('login'))

@app.route('/login')
def login():
    # print(session)
    if 'user' in session:
        return redirect('/Class')

    return render_template('login.html')

@app.route('/loginrequest',methods=["POST"])
def loginrequest():
	u_name = request.form.get("username")
	passw = request.form.get("password")
	print("loginReq-",u_name,passw)
	u=user.user_validation(c,u_name,passw)
	if u==False:
		
		flash('Invalid Credentials')
		return redirect(url_for('login'))

	session['user'] = u
	session.permanent=True
	print(session)
	# occ=user.get_occ(c,u_name)
	# print(occ)
	# return ]redirect('/Class?occ='+occ)
	return redirect('/Class')

@app.route('/register')
def register():
	# return render_template('user_reg.html',colleges=colg_name.keys())
	# clgs = colleges.keys()
	clg_list=college.collegelist(c)

	return render_template('register.html', clgs=clg_list)

@app.route('/create_id',methods=["POST"])
def create_id():
	l=[]
	# clg_id email name passw occ roll
	
	
	l.append(request.form.get("user_data1").split("(")[1][:-1])
	for i in range(2,7):
		l.append(request.form.get("user_data"+str(i)))
	print(l)
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", l[1]):
		flash("Enter a valid email")
		return redirect('/register')
	else:
		if not (user.check_avl(c,l[1])):
			flash("Already Registered")
			return redirect('/register')
		else:
			u=user(l[1],l[0],l[2],l[3],l[4],l[5])
			u.add(c)
			conn.commit()
	return redirect('/login')

@app.route('/Class')
def Classs():
	if not check_session(): return redirect(url_for('login'))

	occ=session['user']['occ']
	# print(dir(Class))
	classes=Class.allclasses(c,session['user']['user_id'])
	name=session['user']['name']
	roll=session['user']['roll']
	username=session['user']['user_id']
	clg_name=college.getCollegeName(c,session['user']['clg_id'])
	teachers=getTeachers()
	if occ=='teacher':
		return render_template('teacher.html',classes=classes,username=username,teacher=name,clg_name=clg_name)
	else:
		return render_template('student.html',classes=classes,username=username,name=name,roll=roll,clg_name=clg_name,teachers=teachers)

@app.route('/check_classavail',methods=["POST"])
def check_classavail():
	cl_id=request.form.get("cls_id")
	cls_id=session['user']['clg_id']+'_'+cl_id
	res=Class.check_classavail(c,cls_id)
	return res


@app.route('/add_class',methods=["POST"])
def add_class():
	if not check_session(): return redirect(url_for('login'))

	cls_id=request.form.get("cls_code")
	desc=request.form.get("desc")
	# print(cls_id,desc)
	clg_id=session['user']['clg_id']
	user_id=session['user']['user_id']
	if Class.alreadyJoined(c,user_id,clg_id+'_'+cls_id):
		if session['user']['occ']=='teacher':
			flash("You already created this class")
		else:
			flash("Already enrolled in this class")
	
	elif session['user']['occ']=='teacher':	
		res=Class.check_classavail(c,clg_id+'_'+cls_id)
		if res=='In_use':
			flash("Class Id already in use")
			return redirect('/Class')
		C=Class(cls_id=clg_id+'_'+cls_id,desc=desc,creator=session['user']['name'],c_id=session['user']['user_id'])
		C.add(c,session['user']['user_id'])
	else:
		if not Class.add_userclass(c,session['user']['user_id'],clg_id+'_'+cls_id):
			flash("No Such Class")
	conn.commit()
	return redirect('/Class')

@app.route('/class_list')
def class_list():

	ls=Class.class_list(c,session['user']['clg_id'])
	return '<sep>'.join(ls)

@app.route('/deleteClass',methods=["POST"])
def deleteClass():
	if not check_session(): return redirect(url_for('login'))

	cls_id=request.form.get("cls_id")
	Class.delete(c,session['user']['clg_id']+'_'+cls_id,session['user']['user_id'])
	conn.commit()
	return redirect('/Class')

@app.route('/removeClass',methods=["POST"])
def removeClass():
	if not check_session(): return redirect(url_for('login'))

	cls_id=request.form.get("cls_id")
	Class.remove(c,session['user']['clg_id']+'_'+cls_id,session['user']['user_id'])
	conn.commit()
	return redirect('/Class')


@app.route('/createAss',methods=["POST"])
def createAss():
	if not check_session(): return redirect(url_for('login'))

	cls_id=request.form.get("cls_id")
	ass_name=request.form.get("name")
	ass_desc=request.form.get("desc")
	ass_date=request.form.get("date")
	ass_id=session['user']['clg_id']+'_'+cls_id+'_'+str(time.time())
	clg_id=session['user']['clg_id']
	a=assignment(ass_id,clg_id+'_'+cls_id,ass_name,ass_date,ass_desc)
	a.add(c)
	conn.commit()
	return redirect('/Class')

@app.route('/viewAss')
def viewAss():
	if not check_session(): return redirect(url_for('login'))

	cls_id=request.args.get("cls_id")
	u_name=session['user']['user_id']
	clg_id=session['user']['clg_id']
	assignmentsDict=assignment.allass(c,u_name,clg_id+'_'+cls_id)

	teacher,desc=Class.getteacher_desc(c,clg_id+'_'+cls_id)

	return render_template('assignments.html',cls_id=cls_id,assignments=assignmentsDict,
							username=session['user']['user_id'],clg_id=clg_id,
							teacher=teacher,occ=session['user']['occ'],name=session['user']['name'],
							desc=desc)

@app.route('/submitAss',methods=["POST"])
def submitAss():
	if not check_session(): return redirect(url_for('login'))

	file=request.files['file']
	ass_id=request.form.get("ass_id")
	user_id=session['user']['user_id']
	print("upload req Received ",file.filename,ass_id)
	print(ass_id)
	filename=""
	if file.filename!='':
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#check file name
		# filename	
		print('uploaded')
		assignment.add_userass(c,user_id,ass_id,str(datetime.now()),file.filename)
		conn.commit()
		flash("Assignment Submitted")
	# return url_for('send',data="",file=file_name)
	return redirect(url_for("viewAss",cls_id=ass_id.split("_")[-2]))

@app.route('/submissions')
def submissions():
	ass_id=request.args.get("ass_id")
	data=assignment.getSubmissions(c,ass_id)
	ass_detail=assignment.getAssDetail(c,ass_id)
	print(data,ass_detail,sep="\n")
	c_id=ass_detail['cls_id'].split("_")[1]
	return render_template("submissions.html",submissions=data,ass=ass_detail,occ=session['user']['occ'],c_id=c_id)

@app.route("/deluserAss",methods=["POST"])
def deluserAss():

	if not check_session(): return redirect(url_for('login'))
	ass_id=request.form.get("ass_id")
	user_id=request.form.get("user_id")
	print(ass_id,user_id)
	assignment.removeUserAss(c,ass_id,user_id)
	conn.commit()
	return redirect(url_for('submissions',ass_id=ass_id))

@app.route('/removeAss',methods=["POST"])
def removeAss():

	if not check_session(): return redirect(url_for('login'))
	# cls_id=request.form.get("cls_id")
	ass_id=request.form.get("ass_id")
	assignment.remove(c,ass_id)
	conn.commit()
	return redirect('/Class')


@app.route('/chats')
def chats():
	if not check_session(): return redirect(url_for('login'))
	cls_id=session['user']['clg_id']+"_"+request.args.get("cls_id")
	classes=Class.allclasses(c,None,cls_id)
	posts=chat.getChats(c,cls_id)
	allowed=chat.isAllowed(c,session['user']['user_id'],cls_id)
	studs,num=Class.getAllStuds(c,cls_id)
	announce=announcements.getAnnouncements(c,cls_id)
	print(studs,posts)
	return render_template("chat.html",num=num,cls=classes,posts=posts,studs=studs,allowed=allowed,occ=session['user']['occ'],user_id=session['user']['user_id']
		,name=session['user']['name'],announce=reversed(announce))

@socketio.on("delChat")
def delChat(chat_id):
	if session['user']['occ']=='teacher':
		chat.delChat(c,chat_id)
		conn.commit()
		emit("delliveChat",chat_id,room=session['room'])

@socketio.on("connect")
def connect():
    print("client wants to connect")
    # emit("status", { "data": "Connected. Hello!" })

@socketio.on('join')
def on_join(data):
    room = data
    
    # check if current user has subscribed to the class/ else dont join
    
    join_room(room)
    session['room']=room
    # emit('msg',data + ' has entered the room.', room=room)

@socketio.on('send')
def send(file,data):
	# print("\n\nXXXXrecei: ",str(data),str(file),sep="_")
	time = ":".join(str(datetime.now()).split(':')[:-1])
	usr = session['user']['user_id']
	occ = session['user']['occ']
	clg_cls_id = session['user']['clg_id']+"_"+session['room']
	chat_id = clg_cls_id+"_"+str(datetime.now())
	new_chat = chat(clg_cls_id,usr,chat_id,time,data,file)
	img = True if file.split('.')[-1] in ['jpg','png','jpeg'] else False
	new_chat.add(c)
	conn.commit() 
	reply={'cls_id':clg_cls_id,'user_id':usr,'chat_id':chat_id,
			'time':time,'text':data,'file':file,'occ':occ,'img':img,'name':session['user']['name']}
	emit("reply",reply,room=session['room'])

@socketio.on('send_Announce')
def send_Announce(file,data):
	clg_cls_id = session['user']['clg_id']+"_"+session['room']
	ann_id=clg_cls_id+"_"+str(datetime.now())
	new_announce=announcements(clg_cls_id,ann_id,data,file)
	new_announce.add(c)
	conn.commit()
	announce={'cls_id':clg_cls_id,'ann_id':ann_id,'data':data,'file':file}
	emit("announce",announce,room=session['room'])


@socketio.on('changePrivilage')
def changePrivilage(d,cls_id):
	print(d)
	for user_id,check in d.items():
		Class.changePrivilage(c,user_id,session['user']['clg_id']+"_"+cls_id,check)
		conn.commit()
	emit('updatePrivilage',d,room=session['room'])
	

@app.route('/upload',methods=['POST'])
def upload():
	# changes required for file
	if not check_session(): return redirect(url_for('login'))

	file=request.files['file']
	print("upload req Received",file.filename)
	filename=""
	if file.filename!='':
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#check file name
		# filename	
		print('uploaded')
	# return url_for('send',data="",file=file_name)
	return "ok"

@app.route("/retrieve_file",methods=['GET'])
def retrieve_file():
	if not check_session(): return redirect(url_for('login'))

	filename = request.args.get("file_name")
	print(filename)
	print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename),as_attachment=True,attachment_filename=filename)




def getTeachers():
	teachers = user.getTeachers(c,session['user']['clg_id'])
	ls=[]
	for t in teachers:
		d={}
		d['name']=t['name']
		d['user_id']=t['user_id']
		d['classes']=getTeacherClasses(t['user_id'])
		ls.append(d)
	print(ls)
	return ls

def getTeacherClasses(uid):

	classes=Class.getTeacherClasses(c,uid)
	return classes

@app.route("/logout")
def logout():
    if not check_session(): return redirect(url_for('login'))
    session.pop('user')
    return redirect('/')

# app.run(threaded=True, port=5000)

socketio.run(app)