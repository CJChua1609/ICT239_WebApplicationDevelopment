from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

from models.golf_courses import Golf_Courses
from models.users import User
from models.booking import Booking
from models.hole import Hole

import csv
import io


dashboard = Blueprint('dashboard', __name__)

   
@dashboard.route("/chart", methods=['GET','POST'])
@login_required
def chart():
    # this segment is to filter the bookings that the current user have
    courses = []
    bookings = Booking.objects()
    
    for b in bookings:
        buser = b.user

        if buser == current_user:
            cname = b.course.course
            courses.append(cname)
            

    if request.method == "GET":
        return render_template("chart.html", courses=courses)
        
    if request.method =="POST":
        # get selected course from dropdown menu
        coursename = request.args.get('a', 0)
        
        # define to get corresponding booking object document
        user = User.objects(email=current_user.email).first()
        course = Golf_Courses.objects(course=coursename).first()

        for item in bookings:
            if item.user == user and item.course == course:
                # calculate holes duration
                hole_obj_list = course.holes
                distlist = []
                for h in hole_obj_list:
                    d = h.dist

                    if d <= 100:
                        distlist.append(60)
                    elif d <= 200:
                        distlist.append(120)
                    elif d <= 300:
                        distlist.append(180)
                    elif d <= 400:
                        distlist.append(240)
                    elif d <= 500:
                        distlist.append(300)
                    elif d > 500:
                        distlist.append(360)
                
                holes_duration = []
                accumulated_duration = [0]

                for i,t in enumerate(hole_obj_list):
                    par = t.par
                    index = t.index
                    
                    if index <= 6:
                        holes_duration.append(par*180 + distlist[i])
                    elif index <= 12:
                        holes_duration.append(par*150 + distlist[i])
                    elif index <= 18:
                        holes_duration.append(par*120 + distlist[i])
                    

                for i, t in enumerate(holes_duration):
                    accumulated_duration.append(accumulated_duration[i] + t)

                # get teetime from booking doc
                teetime = item.teetime
                charts = {}
                hole_labels = [f'Hole {i}' for i in range(1, len(accumulated_duration))] 
                hole_labels.insert(0, 'Tee Time')

                for i,t in enumerate(teetime):
                    tee_time_date = datetime.strptime(t, '%d/%m/%Y %I:%M:%S %p')
                    hole_start_time = []
                    

                    for t in accumulated_duration:
                        hole_start_time.append(tee_time_date + timedelta(seconds = t))

                    charts[f'Flight {i+1}'] =  hole_start_time
                      
                             
        return jsonify({'charts': charts, 'labels': hole_labels})
                        
            