#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Student interface
#

from db import models

# Register Interface
def teacher_register_interface(username, password):
    # Call classmethod Student.get() to get filename with full path
    teacher_obj = models.Teacher.get(username)
    
    # if student_obj is not None, return error
    if teacher_obj:
        return False, "Teacher already exists!"

    # if student_obj is None, register new user by creating instance of the class
    teacher_obj = models.Teacher(username, password)

    # Save object
    teacher_obj.save()

    # Return successful information
    return True, "Teacher created!"


# Check assigned course interface
def teacher_check_assigned_course(teacher_name):
    # Get teacher's object
    teacher_obj = models.Teacher.get(teacher_name)

    # Get assigned course list
    course_list = teacher_obj.course_list_assigned

    if not course_list:
        return False, "No courses assigned to current teacher."
        
    return True, course_list


# Teacher assign course interface
def teacher_assign_course_interface(course_name, teacher_name):
    # Get teacher object
    teacher_obj = models.Teacher.get(teacher_name)

    # Get current assigned courses
    # course_list = teacher_obj.course_list_assigned
    course_list = teacher_obj.check_assigned_course()

    if course_name in course_list:
        return False, "Course was already assigned"
    
    teacher_obj.assign_course(course_name)
    
    return True, "Course was assigned successfully!"


# Check registered studender of a course
def check_registered_student_of_course(course_name, teacher_name):
    # Get teacher object
    teacher_obj = models.Teacher.get(teacher_name)
    
    # Get assigned student
    student_list = teacher_obj.get_registered_student(course_name)

    # Check if registered student under the course
    if not student_list:
        return False, "No registered student under current course!"
    
    return True, student_list



def update_score_interface(course_name, student_name, score, teacher_name):
    # Get teacher object
    teacher_obj = models.Teacher.get(teacher_name)
    # Update score
    teacher_obj.change_score(course_name, student_name, score)

    return True, "Score was updated successfully!"

