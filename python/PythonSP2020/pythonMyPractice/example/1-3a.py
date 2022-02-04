#!/usr/bin/env python 
# -*- coding:utf-8 -*-

"""
工作任务
(1) 编写程序实现使用文件系统管理数据的功能。
(2) 职员对象具有编号、姓名、年龄等属性，假设已知职员信息为：
    （'201901','tom','17'）、,('201902','jack','18')、('201901','alice','19')
(3) 编写职员管理类 staff_manager，能够录入职员信息，并将每个职员的信息存入staff.txt文件，保存在python工作目录下。
(4) 职员管理类具有增加职员(input_staff)、按编号查询职员(get_staff)、统计职员人数(count_staff)等功能。
(5) 程序的完成界面如下：
输入职员编号：001
输入职员姓名：tom
输入职员年龄：17
总共有4位同仁
请输入要查询的职员编号：001
001

tom

17
"""
class staff_manager():
    def input_staff(self, staffs):

    def count_staff(self):
        pass
    def get_staff(self, staffnum):
        pass

stm = staff_manager()
stm.input_staff(staff_list)
stm.count_staff()
staff_id = input('input id: ')
stm.get_staff(staff_id)





















"""
import os

staff_number = input('input staff number: ')
staff_name = input('input staff name: ')
staff_age = input('input staff age: ')
staff_list = [staff_number, staff_name, staff_age]


class staff_manager():
    def input_staff(self, staffs):
        self.staffs = staffs
        staff_file = 'staff.txt'
        if os.path.exists(staff_file):
            with open(staff_file, 'a+') as file1:
                file1.write(staffs[0] + '\n' + staffs[1] + '\n' + staffs[2] + '\n')
                file1.write('*' * 20 + '\n')
        else:
            print("file does not exist")

    def count_staff(self):
        cnt = 0
        staff_file = 'staff.txt'
        if os.path.exists(staff_file):
            with open(staff_file, 'r+') as file1:
                for line in file1:
                    if line == '*' * 20 + '\n':
                        cnt += 1
        else:
            print("file does not exist")
        print("total staffs " + str(cnt))

    def get_staff(self, staff_no):
        staff_n = str(staff_no) + '\n'
        staff_file = 'staff.txt'
        if os.path.exists(staff_file):
            with open(staff_file, 'r+') as file1:
                for line in file1:
                    if line == staff_n:
                        print(line)
                        print(file1.readline())
                        print(file1.readline())
        else:
            print("file does not exist")


stm = staff_manager()
stm.input_staff(staff_list)
stm.count_staff()

staff_num = input("staff no: ")
stm.get_staff(staff_num)

*************************************************************
import os

staff_number = input("staff no:")
staff_name = input("staff name: ")
staff_age = input("staff age: ")
staff_list = [staff_number, staff_name, staff_age]


class Staff_Manager:
    def input_staff(self, staffs):
        self.staffs = staff_list
        staff_file_name = "staff.txt"

        if os.path.exists(staff_file_name):
            with open(staff_file_name, 'a') as file1:
                file1.write(staffs[0] + '\n' + staffs[1] + '\n' + staffs[2] + '\n')
                file1.write('-' * 20 + '\n')
        else:
            print("file does not exist")

    def get_staff(self, staff_number):
        staff_file_name = "staff.txt"
        staff_no = str(staff_number) + '\n'

        if os.path.exists(staff_file_name):
            with open(staff_file_name, 'r') as file1:
                for each_line in file1:
                    if each_line == staff_no:
                        print(each_line)
                        print(file1.readline())
                        print(file1.readline())
        else:
            print("file does not exist")

    def count_staff(self):
        cnt = 0
        staff_file_name = "staff.txt"

        if os.path.exists(staff_file_name):
            with open(staff_file_name, 'r') as file1:
                for each_line in file1:
                    if each_line == '-' * 20 + '\n':
                        cnt += 1
        else:
            print("file does not exist")

        print("total staff: " + str(cnt) + '\n')


stm = Staff_Manager()
stm.input_staff(staff_list)
stm.count_staff()

staff_num = input("input staff number: ")
stm.get_staff(staff_num)
"""
