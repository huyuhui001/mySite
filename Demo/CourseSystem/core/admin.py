#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Admin Views
#

from interface import admin_interface
from interface import common_interface
from lib import common


# Record active users' status
user_info = {
    'user': None
}


# Admin register
def register():
    while True:
        username = input("Please enter username:").strip()
        password = input("Please enter password:").strip()
        re_password = input("Please enter password again:").strip()
        
        # Call Admin interface to register user
        if password == re_password:
        
            flag, msg = admin_interface.admin_register_interface(username, password)

            if flag:
                # Print logon successful info
                print(msg)
                break
            else:
                # Print logon failed info
                print(msg)
        
        else:
            print("Password inconsistent, please re-enter your password.")


# Admin login
def login():
    while True:
        username = input("Please enter username:").strip()
        password = input("Please enter password:").strip()
        
        # Call Admin interface to login
        flag, msg = admin_interface.admin_login_interface(username, password)

        if flag:  # If logon successfully
            # Record user status
            user_info['user'] = username
            # Print logon successful info
            print(msg)
            break
        else:
            # Print logon failed info
            print(msg)



# Admin add school
@common.auth('admin')
def add_school():
    while True:
        # Get school name and address
        school_name = input("Please enter school name:").strip()
        school_addr = input("Plaese enter school address:").strip()

        # Call interface to save school info
        flag, msg = admin_interface.admin_add_school_interface(school_name, school_addr, user_info.get('user'))

        if flag:
            # Print successful info
            print(msg)
            break
        else:
            # Print failed info
            print(msg)



# Admin add course
@common.auth('admin')
def add_course():
    while True:
        # Call interface to get all schools
        flag, school_list_or_msg = common_interface.get_all_schools_interface()

        if not flag:
            print(school_list_or_msg)
            break
        
        # Generate list for schools
        for index, school_name in enumerate(school_list_or_msg):
            print(f'NO. {index}  School Name {school_name}')

        # Get user input
        choice = input("Please select school index:").strip()

        # Check if input is a mumeric
        if not choice.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice = int(choice)

        # Check if input is out of the index of school list
        if choice not in range(len(school_list_or_msg)):
            print("Incorrect index!")
            continue

        # Finalize user selected school
        school_name = school_list_or_msg[choice]

        # Get input of new course to be created in current selected school
        course_name = input("Please input course name:")

        # Call interface to save course info
        flag, msg = admin_interface.admin_add_course_interface(school_name, course_name, user_info.get('user'))

        if flag:
            # Print successful info
            print(msg)
            break
        else:
            # Print failed info
            print(msg)


# Admin add teacher
@common.auth('admin')
def add_teacher():
    while True:
        # Get teacher's name
        teacher_name = input("Please input teacher's name:").strip()
        
        # Call teacher interface
        flag, msg = admin_interface.admin_add_teacher_interface(teacher_name, user_info.get('user'))

        if flag:
            # Print successful info
            print(msg)
            break
        else:
            # Print failed info
            print(msg)




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
        =============Admin Menu=============
        1. Register
        2. Login
        3. Add School
        4. Add Course
        5. Add Teacher
        q. Return
        ====================================
        ''')

        choice = input("Please enter your selection (1/2/3...):").strip()

        if choice == 'q':
            break

        if choice not in menu_dict:
            print("Invalid selection, please select menu again")
            continue

        menu_dict.get(choice)()
