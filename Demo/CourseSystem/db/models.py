#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Define all classed in models
#

from db import db_handler


# Base class
# save() and get() are needed by all other classes
class Base:
    # Save data to file
    def save(self):
        # Pass instance object (self) to db_handler.save_data function 
        db_handler.save_data(self)
    
    # Get data from file
    @classmethod
    def get(cls, usr):
        # The obj received from db_handler.get_data would be an obj or None
        obj = db_handler.get_data(cls, usr)
        return obj


class Admin(Base):
    def __init__(self, usr, pwd):        
        self.usr = usr  # Username
        self.pwd = pwd  # Password
       
    # Add new school
    def add_school(self, school_name, school_addr):
        school_obj = School(school_name, school_addr)
        school_obj.save()
    
    # Add new course
    def add_course(self, school_obj, course_name):
        # Create Course instance
        course_obj = Course(course_name)
        course_obj.save()
        
        # Get School object, add course to course list
        school_obj.course_list.append(course_name)

        # Update school object
        school_obj.save()

    
    # Add new teacher
    def add_teacher(self, teacher_name, teacher_pwd):
        teacher_obj = Teacher(teacher_name, teacher_pwd)
        teacher_obj.save()


class School(Base):
    def __init__(self, school_name, school_addr):
        self.usr = school_name  # School name (It's hardcode here because obj.usr in db_handler)
        self.addr = school_addr  # School address
        self.course_list = []  # Course list. Multple courses each school
    


class Course(Base):
    def __init__(self, course_name):
        self.usr = course_name  # School name (It's hardcode here because obj.usr in db_handler)
        self.student_list = []  # Student list. Multiple students each course



class Teacher(Base):
    def __init__(self, teacher_name, teacher_pwd):
        self.usr = teacher_name  # Teacher's name
        self.pwd = teacher_pwd  # Teacher's password
        self.course_list_assigned=[]  # Course list assigned to teacher



class Student(Base):
    pass



