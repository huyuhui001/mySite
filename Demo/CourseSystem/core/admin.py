#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Admin Views
#

from interface import admin_interface


# Admin register
def register():
    while True:
        username = input("Please enter username:").strip()
        password = input("Please enter password:").strip()
        re_password = input("Please enter password again:").strip()

        if password == re_password:
            # Call interface to register user
            flag, msg = admin_interface.admin_register_interface(username, password)

            if flag:  # If user created successfully
                print(msg)
                break
            else:  # If user exists, print error info
                print(msg)
        
        else:
            print("Password inconsistent, please re-enter your password.")


# Admin login
def login():
    pass


# Admin add school
def add_school():
    pass


# Admin add course
def add_course():
    pass


# Admin add teacher
def add_teacher():
    pass


# Menu dictionary
menu_dict = {
    '1': register,
    '2': login,
    '3': add_school,
    '4': add_course,
    '5': add_teacher
}


# Admin view function
def admin_view():
    while True:
        print('''
        ======Welcome to Course System======
        1. Register
        2. Login
        3. Add School
        4. Add Course
        5. Add Teacher
        ====================================
        ''')

        choice = input("Please enter your selection (1/2/3...):").strip()

        if choice == 'q':
            break

        if choice not in menu_dict:
            print("Invalid selection, please select menu again")
            continue

        menu_dict.get(choice)()
