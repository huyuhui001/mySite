#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Student Views
#


# Student register
def register():
    pass


# Student login
def login():
    pass


# Student choose school
def choose_school():
    pass


# Student register course
def register_course():
    pass


# Student check score
def check_score():
    pass


# Student pay training fee
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
        ======Welcome to Course System======
        1. Register
        2. Login
        3. Choose School
        4. Register Course
        5. Check Score
        6. Training Fee
        ====================================
        ''')

        choice = input("Please enter your selection (1/2/3...):").strip()

        if choice == 'q':
            break

        if choice not in menu_dict:
            print("Invalid selection, please select menu again")
            continue

        menu_dict.get(choice)()
