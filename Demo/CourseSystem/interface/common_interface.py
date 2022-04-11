#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Common Interface
#

import os
from conf import settings
from db import models


# Login for all roles
def login_interface(usr, pwd, usr_type):
    # Check role
    if usr_type == 'admin':
        obj = models.Admin.get(usr)
    elif usr_type == 'student':
        obj = models.Student.get(usr)
    elif usr_type == 'teacher':
        obj = models.Teacher.get(usr)
    else:
        return False, "Incorrect role, please input role:"
    
    # Check if user exists.
    if obj:
        if pwd == obj.pwd:
            return True, "Logon successfully!"
        else:
            return False, "Logon failed, incorrect password!"
    else:
        return False, "User does not exist!"



# Get schools for all roles
def get_all_schools_interface():
    # Get path of saving school info
    school_dir = os.path.join(
        settings.DB_PATH, 'School'
    )

    # Check if school exists
    if not os.path.exists(school_dir):
        return False, "School does not exist, please contact with Admin"
    
    # If school exists, get school info
    school_list = os.listdir(school_dir)
    
    return True, school_list




# Get courses from school for all roles
def get_courses_from_school_interface(school_name):
    # Get current school object
    school_obj = models.School.get(school_name)

    # Get courses list
    course_list = school_obj.course_list

    if not course_list:
        return False, "No courses from current school!"
    
    return True, course_list
