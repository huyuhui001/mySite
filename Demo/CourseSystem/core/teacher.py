#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Teacher Views
#

from lib import common
from interface import common_interface
from interface import teacher_interface

# Record active users' status
user_info = {
    'user': None
}


# Teacher register
def register():
    while True:
        username = input("Please enter username:")
        password = input("Please enter password:")
        re_password = input("Please re-enter password:")

        if password == re_password:
            flag, msg = teacher_interface.teacher_register_interface(username, password)
        
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print("Password inconsistent, please re-enter your password.")


# Teacher login
def login():
    while True:
        username = input("Please enter username:").strip()
        password = input("Please enter password:").strip()
        
        # Call Admin interface to login
        flag, msg = common_interface.login_interface(username, password, usr_type='teacher')

        if flag:  # If logon successfully
            # Record user status
            user_info['user'] = username
            # Print logon successful info
            print(msg)
            break
        else:
            # Print logon failed info
            print(msg)


# Teacher check courses assigned to them
@common.auth('teacher')
def check_assigned_course():
    flag, course_list = teacher_interface.teacher_check_assigned_course(user_info.get('user'))

    if flag:
        # Print successful info
        print(course_list)
    else:
        # Print failed info
        print(course_list)



# Teacher assign course to themselves
@common.auth('teacher')
def assign_course():
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

        # Get courses from school
        flag2, course_list_or_msg = common_interface.get_courses_from_school_interface(school_name)

        if not flag2:
            # Print successful info
            print(course_list_or_msg)
            break

        # Generate list for courses
        for index2, course_name in enumerate(course_list_or_msg):
            print(f'NO. {index2}  Course Name {course_name}')

        # Get user input
        choice2 = input("Please select course index:").strip()

        # Check if input is a mumeric
        if not choice2.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice2 = int(choice2)

        # Check if input is out of the index of school list
        if choice2 not in range(len(course_list_or_msg)):
            print("Incorrect index!")
            continue

        # Finalize user selected school
        course_name = course_list_or_msg[choice2]

        # Add course to teacher's object
        flag3, msg3 = teacher_interface.teacher_assign_course_interface(course_name, user_info.get('user'))

        if flag3:
            # Print successful info
            print(msg3)
            break
        else:
            # Print failed info
            print(msg3)



# Teacher check registered student of a course
@common.auth('teacher')
def check_registered_student_of_course():
    while True:
        # Get teacher assigned courses
        flag, course_list = teacher_interface.teacher_check_assigned_course(user_info.get('user'))
    
        if not flag:
            print(course_list)
            break

        for index, course_name in enumerate(course_list):
            print(f'NO. {index}  Course Name {course_name}')

        # Get user input
        choice = input("Please select course index:").strip()

        # Check if input is a mumeric
        if not choice.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice = int(choice)

        # Check if input is out of the index of school list
        if choice not in range(len(course_list)):
            print("Incorrect index!")
            continue

        # Get assigned course name
        course_name = course_list[choice]

        # Get registered students under the course
        flag2, student_list = teacher_interface.check_registered_student_of_course(course_name, user_info.get('user'))

        if flag2:
            print(student_list)
            break
        else:
            print(student_list)
            break




# Teacher update students' score
@common.auth('teacher')
def update_student_score():
    while True:
        # Get teacher assigned courses
        flag, course_list = teacher_interface.teacher_check_assigned_course(user_info.get('user'))
    
        if not flag:
            print(course_list)
            break

        for index, course_name in enumerate(course_list):
            print(f'NO. {index}  Course Name {course_name}')

        # Get user input
        choice = input("Please select course index:").strip()

        # Check if input is a mumeric
        if not choice.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice = int(choice)

        # Check if input is out of the index of school list
        if choice not in range(len(course_list)):
            print("Incorrect index!")
            continue

        # Get assigned course name
        course_name = course_list[choice]

        # Get registered students under the course
        flag2, student_list = teacher_interface.check_registered_student_of_course(course_name, user_info.get('user'))

        if not flag2:
            print(student_list)
            break

        # Print all students for teacher's selection
        for index2, student_name in enumerate(student_list):
            print(f'NO. {index2}  Student Name {student_name}')

        # Get user input
        choice2 = input("Please select student index:").strip()

        # Check if input is a mumeric
        if not choice2.isdigit():
            print("Please input a nummeric.")
            continue
        
        choice2 = int(choice2)

        # Check if input is out of the index of school list
        if choice2 not in range(len(student_list)):
            print("Incorrect index!")
            continue

        # Get assigned course name
        student_name = student_list[choice2]

        # Get input of new score
        score = input("Please enter new score:").strip()
        
        if not score.isdigit():
            continue
        
        score = int(score)

        # Call teacher interface to update score
        flag3, msg3 = teacher_interface.update_score_interface(course_name, student_name, score, user_info.get('user'))

        if flag3:
            print(msg3)
            break




# Menu dictionary
menu_dict = {
    '1': login,
    '2': check_assigned_course,
    '3': assign_course,
    '4': check_registered_student_of_course,
    '5': update_student_score
}


def teacher_view():
    while True:
        print('''
        ============Teacher Menu============
        1. Login
        2. Check Assigned Courses
        3. Assign Course
        4. Check Registered Student of Course
        5. Update Student Scores
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
