#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import configparser
import sqlite3
from model.employee import Employee


class Database(object):
    @classmethod
    def create_connection(cls):
        config_parser = configparser.ConfigParser()
        config_parser.read('model/config.ini')
        db = config_parser.get('DB_SECTION', 'database')
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        return conn

    @classmethod
    def query(cls):
        sql_select = "select * from employee"
        conn = Database.create_connection()
        cur = conn.cursor()
        cur.execute(sql_select)
        result_set = cur.fetchall()
        cur.close()
        conn.close()
        return result_set

    @classmethod
    def query_by_id(cls, id):
        sql_select_by_id = "select * from employee where id=?"
        conn = Database.create_connection()
        cur = conn.cursor()
        cur.execute(sql_select_by_id, [id])
        result_set = cur.fetchall()
        cur.close()
        conn.close()
        if len(result_set) == 0:
            return None
        else:
            return result_set[0]  # 假设返回一个值

    @classmethod
    def save(cls, emp):
        sql_insert = "insert into employee (code, name) values (?, ?)"
        conn = Database.create_connection()
        cur = conn.cursor()
        cur.execute(sql_insert, (emp.code, emp.name))
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def update(cls, emp):
        sql_update = 'update employee set code=?, name=? where id=?'
        conn = Database.create_connection()
        cur = conn.cursor()
        cur.execute(sql_update, (emp.code, emp.name, emp.id))
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def delete(cls, id):
        sql_delete = 'delete from employee where id=?'
        conn = Database.create_connection()
        cur = conn.cursor()
        cur.execute(sql_delete, [id])
        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    # Query
    # Database.create_connection()
    # print(Database.query())
    # Query by ID
    print(Database.query_by_id(22))

    # Save
    # employee = Employee("E01", "Jason")
    # employee = Employee("E02", "Jack")
    # Database.save(employee)

    # # Update
    # employee = Employee('Exx', 'Will')
    # employee.id = 22  # feature column，按需要灵活添加
    # Database.update(employee)

    print(Database.delete('22'))
    # print(Database.query())
