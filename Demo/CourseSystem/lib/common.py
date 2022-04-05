#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Common method
#

# Decorator for role-based authorization validation
def auth(role):
    from core import admin, student, teacher
    # role: admin, teacher, student
    # logon validation
    def logon_auth(func):
        def inner(*args, **kwargs):
            if role == 'admin':
                # Check if the dictionary user_info['user'] returns None (no admin user)
                if admin.user_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    admin.login()
            elif role == 'student':
                if student.user_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    student.login()
            elif role == 'teacher':
                if teacher.user_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    teacher.login()
            else:
                print("No view authorized")
        
        return inner    
    return logon_auth











