from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from models.golf_courses import Golf_Courses

courses = Blueprint('courses', __name__)

@courses.route('/courses',methods=['GET','POST'])
@login_required
def render_courses():
    courses = Golf_Courses.objects()
    return render_template('courses.html', name=current_user.name,courses=courses, panel="Course")