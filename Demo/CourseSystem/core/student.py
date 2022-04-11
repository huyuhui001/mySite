#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Student Views
#


from lib import common
from interface import student_interface
from interface import common_interface

# Record active users' status
user_info = {
    'user': None
}


# Student register
def register():
    while True:
        username = input("Please enter username:")
        password = input("Please enter password:")
        re_password = input("Please re-enter password:")

        if password == re_password:
            flag, msg = student_interface.student_register_interface(username, password)
        
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print("Password inconsistent, please re-enter your password.")



# Student login
def login():
    while True:
        username = input("Please enter username:").strip()
        password = input("Please enter password:").strip()
        
        # Call Admin interface to login
        flag, msg = common_interface.login_interface(username, password, usr_type='student')

        if flag:  # If logon successfully
            # Record user status
            user_info['user'] = username
            # Print logon successful info
            print(msg)
            break
        else:
            # Print logon failed info
            print(msg)



# Student register school
@common.auth('student')
def choose_school():
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
        # course_name = input("Please input course name:")

        # Call interface to save course info
        flag, msg = student_interface.student_choose_school_interface(school_name, user_info.get('user'))

        if flag:
            # Print successful info
            print(msg)
            break
        else:
            # Print failed info
            print(msg)



# Student register course
@common.auth('student')
def register_course():
    while True:
        # Get registered course list
        flag, course_list = student_interface.student_get_course_interface(user_info.get('user'))

        # If course exists
        if not flag:
            print(course_list)
            break
        
        # Generate list for courses
        for index, course_name in enumerate(course_list):
            print(f'NO. {index}  Course Name {course_name}')

        # Get user input
        choice = input("Please select course index:").strip()

        # Check if input is a mumeric
        if not choice.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice = int(choice)

        # Check if input is out of the index of course list
        if choice not in range(len(course_list)):
            print("Incorrect index!")
            continue

        # Finalize user selected course
        course_name = course_list[choice]

        # Call interface
        flag, msg = student_interface.student_register_course_interface(course_name, user_info.get('user'))

        if flag:
            # Print successful info
            print(msg)
            break
        else:
            # Print failed info
            print(msg)




# Student check score
@common.auth('student')
def check_score():
    # Get student's score
    score_dict = student_interface.check_score_interface(user_info.get('user'))

    if not score_dict:
        print("No score found, you may register a course first!")

    print(score_dict)


# Student pay training fee
@common.auth('student')
def training_fee():
    pass


# Menu dictionary
menu_dict = {
    '1': register,
    '2': login,
    '3': choose_school,
    '4': register_course,
    '5': check_score,
    '6': training_fee
}


# Student view function
def student_view():
    while True:
        print('''
        ============Student Menu============
        1. Register
        2. Login
        3. Choose School
        4. Register Course
        5. Check Score
        6. Training Fee
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
