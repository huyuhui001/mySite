#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Define all classed in models
#

from db import db_handler


class Admin():
    def __init__(self, usr, pwd):
        self.usr = usr
        self.pwd = pwd
    
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


class Student():
    pass


class Teacher():
    pass


class School():
    pass


class Course():
    pass
