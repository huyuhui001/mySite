#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Main View for all roles
#

from core import admin
from core import student
from core import teacher

# Menu Dictionary
menu_dict = {
    '1': admin.admin_view,
    '2': student.student_view,
    '3': teacher.teacher_view
}


def run():
    while True:
        print('''
        ======Welcome to Course System======
        1. Admin Menu
        2. Student Menu
        3. Teacher Menu
        q. Exit
        ====================================
        ''')

        choice = input("Please enter your selection (1/2/3):").strip()

        if choice == 'q':
            break

        if choice not in menu_dict:
            print("Invalid selection, please select menu again")
            continue

        menu_dict.get(choice)()
