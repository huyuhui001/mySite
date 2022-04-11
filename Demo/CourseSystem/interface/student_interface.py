#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Student interface
#

from db import models

# Register Interface
def student_register_interface(username, password):
    # Call classmethod Student.get() to get filename with full path
    student_obj = models.Student.get(username)
    
    # if student_obj is not None, return error
    if student_obj:
        return False, "Student already exists!"

    # if student_obj is None, register new user by creating instance of the class
    student_obj = models.Student(username, password)

    # Save object
    student_obj.save()

    # Return successful information
    return True, "Student created!"


# Student choose and register new school
def student_choose_school_interface(school_name, created_by):
    # Check if school is already registered by the student
    student_obj = models.Student.get(created_by)
    
    if student_obj.school_name:
        return False, "You already registered this school!"
    
    student_obj.add_school(school_name)

    return True, f"You registered school {school_name} successfully"



# Student get registered course list
def student_get_course_interface(student_name):
    # Get current student object
    student_obj = models.Student.get(student_name)
    school_name = student_obj.school_name

    if not school_name:
        return False, "No registered school. Please register school first!"
    
    school_obj = models.School.get(school_name)
    
    course_list = school_obj.course_list

    if not course_list:
        return False, "No courses under the school. Please register course first!"

    return True, course_list




# Student register new course provided by a school
def student_register_course_interface(course_name, student_name):
    # Check if student exists
    student_obj = models.Student.get(student_name)

    if course_name in student_obj.course_list:
        return False, "The course was already registered!"

    student_obj.register_course(course_name)

    return True, f"Course {course_name} was registered successfully!"




def check_score_interface(student_name):
    # Check if student exists
    student_obj = models.Student.get(student_name)

    # Check if student already has score
    if student_obj.score_dict:
        return student_obj.score_dict



