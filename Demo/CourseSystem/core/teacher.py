#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Teacher Views
#

from lib import common


# Record active users' status
user_info = {
    'user': None
}


# Teacher register
def register():
    pass


# Teacher login
def login():
    pass


# Teacher check courses assigned to them
@common.auth('teacher')
def check_assigned_course():
    pass


# Teacher assign course to themselves
@common.auth('teacher')
def assign_course():
    pass


# Teacher check registered student of a course
@common.auth('teacher')
def check_registered_student_of_course():
    pass


# Teacher update students' score
@common.auth('teacher')
def update_student_score():
    pass


# Menu dictionary
menu_dict = {
    '1': login,
    '2': check_assigned_course,
    '3': assign_course,
    '4': check_registered_student_of_course,
    '5': update_student_score
}

# Menu Dictionary
menu_dict = {'1': '', '2': '', '3': ''}


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