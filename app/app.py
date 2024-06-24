# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for
from app import app, db, login_manager
from datetime import datetime, timedelta

# Define routes for blueprints
from controllers.dashboard import dashboard
from controllers.courses import courses
from controllers.auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(courses)
app.register_blueprint(auth)

from models.users import User
from models.forms import dtForm
from models.golf_courses import Golf_Courses
from models.booking import Booking
from models.hole import Hole
import csv, io, json

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
    

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route("/makeBooking", methods=['GET','POST'])
@login_required  
def makeBooking():

    form = dtForm()
    course = request.args.get('course')
    current_course = Golf_Courses.objects(course=course).first()

    if request.method == 'POST': 
        teetime = request.form.get('tee_time')
        if form.validate():
            print("passed")
            teetime = datetime.strptime(teetime, '%Y-%m-%dT%H:%M')
            teetime = datetime.strftime(teetime,'%d/%m/%Y %I:%M:%S %p')
            current_course.teetime.append(teetime)
            current_course.save()
            return redirect(url_for('courses.render_courses'))
        else:
            print('failed')
            course = request.form.get('course')
            current_course = Golf_Courses.objects(course=course).first()
    return render_template('makeBooking.html',form=form, name=current_user.name,current_course=current_course, panel=course)


@app.route("/upload", methods=['GET','POST'])
@login_required   
def upload():
    # if the user just key in the /upload in the address
    if request.method == 'GET':
        if current_user.email != 'admin@abc.com':
            return render_template('401.html',name=current_user.name, panel='Unauthorised')
        else:
            return render_template("upload.html", name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        
        type = request.form.get('filetype')
        file = request.files.get('file')
        data = file.read().decode('utf-8')
        dict_reader = list(csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"'))
        file.close()
        
        if type == 'opt_C':
            for item in dict_reader:
                course=item['course']
                index=json.loads(item['index'])
                par=json.loads(item['par'])
                dist=json.loads(item['dist'])
                img_url=item['image_url']
                description=item['description']
                # modified to create hole object first, before creating course object
                hole_obj_list = []
                for i in range(len(index)):
                    hole = Hole(index=index[i],par=par[i],dist=dist[i])
                    hole_obj_list.append(hole)
                
                a_course = Golf_Courses(course=course,holes=hole_obj_list, img_url=img_url, description=description).save()

            # original code below
            '''       
            if type == 'opt_C':
                for item in dict_reader:
                    course=item['course']
                    index=json.loads(item['index'])
                    par=json.loads(item['par'])
                    dist=json.loads(item['dist'])
                    img_url=item['image_url']
                    description=item['description']
                    a_course = Golf_Courses(course=course,index=index, par=par, dist=dist, img_url=img_url, description=description).save()
            '''
        elif type =='opt_B':
            for item in dict_reader:
                teetime = json.loads(item['check_in_time']) 
                # no square bracket needed yet, check if booking exists

                user = item['user']
                course = item['course_name'] 
                user_in_Booking = User.objects(email=user).first()
                golf_course = Golf_Courses.objects(course=course).first()
                if not golf_course or not user_in_Booking:
                    print('Something is wrong')
                else:
                    # You need to find Booking in mongodb for the course and the current user and if can find
                    # you need to append to the teetime
                    bookings = Booking.objects()
                    for b in bookings:
                        # check whther b.course has the matching course_name and for b.user has the matching email
                        if b.course.course == course and b.user.email == user:
                            print('found past booking')
                            b.teetime.append(teetime)
                            b.save()
                            break  
                    else:
                        Booking(course=golf_course, user=user_in_Booking, teetime=[teetime]).save()
                    
                
        
        return render_template("upload.html", name=current_user.name, panel="Upload")

