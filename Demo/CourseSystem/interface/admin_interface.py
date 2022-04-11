#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Admin interface
#

from db import models


# Register Interface
# Call methods defined in models.py
def admin_register_interface(username, password):
    # Call classmethod Admin.get() to get filename with full path
    admin_obj = models.Admin.get(username)
    
    # if admin_obj is not None, return error
    if admin_obj:
        return False, "User exists!"

    # if admin_obj is None, register new user by creating instance of the class
    admin_obj = models.Admin(username, password)

    # Save object
    admin_obj.save()

    # Return successful information
    return True, "User created!"




# Login Interface
# def admin_login_interface(username, password):
#     # Check if user exists
#     admin_obj = models.Admin.get(username)

#     # If user does not exist, return error info
#     if not admin_obj:
#         return False, "User does not exist!"

#     # If user exists, validate password
#     if password == admin_obj.pwd:
#         return True, "Login successfully!"
#     else:
#         return False, "Password error!"




# Add school Interface
def admin_add_school_interface(school_name, school_addr, created_by):
    # Check if school exists
    school_obj = models.School.get(school_name)

    # If exists, return false with info
    if school_obj:
        return False, "School Exists!"
    
    # If not exist, add new school by admin (admin obj)
    admin_obj = models.Admin.get(created_by)
    admin_obj.add_school(school_name, school_addr)

    return True, f'School [{school_name}] was created successfully'




# Add course
def admin_add_course_interface(school_name, course_name, created_by):
    # Get course list
    school_obj = models.School.get(school_name)

    # Check if course exists
    if course_name in school_obj.course_list:
        return False, "Course exists!"
    
    # Add new course (by admin)
    admin_obj = models.Admin.get(created_by)
    admin_obj.add_course(school_obj, course_name)

    return True, f"Course {course_name} was created successfully and bound to school {school_name}"



# Add teacher
def admin_add_teacher_interface(teacher_name, created_by, teacher_pwd='123'):
    # Get teacher list
    teacher_obj = models.Teacher.get(teacher_name)

    # Check if teacher exists
    if teacher_obj:
        return False, "Teacher exists"

    # Add new teacher (by admin)
    admin_obj = models.Admin.get(created_by)
    admin_obj.add_teacher(teacher_name, teacher_pwd)

    return True, f"Teacher {teacher_name} was created successfully"






