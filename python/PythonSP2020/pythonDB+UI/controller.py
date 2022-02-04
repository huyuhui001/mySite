#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# http://127.0.0.1:9000/

from webhandler import get, post
from model.employee import Employee
from model.databaseSqlite import Database


# 首页模板模板定义
@get('/')
def index():
    return {
        '__template__': 'employee_list.html'
    }


# 首页显示逻辑
@get('/services/employees')  # 对应 employee_list.html 第29行
def get_employees():
    employees = Database.query()
    return dict(employees=employees)


# ADD按钮跳转页面定义
@get('/ui/employees/add')
def ui_add_employee():
    return {
        '__template__': 'add_edit_employee.html',
        'id': '',
        'action': '/service/employees'
    }


# ADD页面的SAVE逻辑
@post('/service/employees')
def add_employee(*, code, name):
    employee = Employee(code, name)
    Database.save(employee)


# 首页行记录中的修改按钮跳转页面定义
@get('/ui/employees/edit')  # 对应employee_list.html第14行
def ui_edit_employee(*, id):
    return {
        '__template__': 'add_edit_employee.html',
        'id': id,
        'action': '/services/employees/%s' % id
    }


# 修改页面显示
@get('/services/employees/{id}')
def edit_employee(*, id):
    employee = Database.query_by_id(id)
    print(employee)
    return dict(id=employee[0], code=employee[1], name=employee[2])


# 修改页面SAVE逻辑
@post('/services/employees/{id}')
def save_change(*, id, code, name):
    employee = Employee(code, name)
    employee.id = id
    Database.update(employee)


# 删除按钮逻辑
@post('/services/employees/{id}/delete')  # 对应employee_list.html第18行
def delete_employee(*, id):
    Database.delete(id)
