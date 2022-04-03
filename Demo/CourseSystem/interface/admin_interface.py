#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Admin interface
#

from db import models

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


