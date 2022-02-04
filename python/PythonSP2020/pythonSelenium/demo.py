#!/usr/bin/env python 
# -*- coding:utf-8 -*-


'''
To complete below demo, the demo Django need to be started first.
Command to start the service /opt/projects/myPython/pythonDjango/python manage.py runserver

If any codes were changed, need executed below two commands before starting the server.
/opt/projects/myPython/pythonDjango/python manage.py makemigrations
/opt/projects/myPython/pythonDjango/python manage.py migrate

'''


from selenium import webdriver


class SeleniumDemo(object):
    def __init__(self):
        self.url_login = 'http://127.0.0.1:8000/admin/login/?next=/admin/'
        self.url_add_employee = 'http://127.0.0.1:8000/admin/employee/employee/add/'

        self.browser = webdriver.Chrome()
        # self.browser.maximize_window()

    def login(self):
        self.browser.get(self.url_login)
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        btn_save = self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')
        username.send_keys('root')
        password.send_keys('root')
        btn_save.click()

    def add_employee(self):
        click_add = self.browser.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr/td[1]/a')
        click_add.click()

        if self.browser.current_url != self.url_add_employee:
            self.browser.get(self.url_add_employee)

        code = self.browser.find_element_by_name('code')
        name = self.browser.find_element_by_name('name')
        salary = self.browser.find_element_by_name('salary')
        btn_save = self.browser.find_element_by_xpath('//*[@id="employee_form"]/div/div/input[1]')

        code.send_keys('E10')
        name.send_keys(('BBB'))
        salary.send_keys('1000')

        btn_save.click()

    def edit_employee(self):
        # After CREATE operation, stay on current page, and complete below EDIT operation
        click_edit = self.browser.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th')
        click_edit.click()

        code = self.browser.find_element_by_name('code')
        name = self.browser.find_element_by_name('name')
        salary = self.browser.find_element_by_xpath('//*[@id="id_salary"]')
        btn_save = self.browser.find_element_by_xpath('//*[@id="employee_form"]/div/div/input[1]')

        code.clear()
        code.send_keys('E10-update')
        name.clear()
        name.send_keys('BBB-Update')
        salary.clear()
        salary.send_keys('9999')

        btn_save.click()

    def delete_employee(self):
        # After EDIT operation, stay on current page, select top record and delete it.
        # Select the top record
        click_select = self.browser.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th')
        click_select.click()
        # Click DELETE button
        btn_delete = self.browser.find_element_by_xpath('//*[@id="employee_form"]/div/div/p/a')
        btn_delete.click()
        # Confirm the deletion
        btn_confirm = self.browser.find_element_by_xpath('//*[@id="content"]/form/div/input[2]')
        btn_confirm.click()

        ''' Instructor's code
        check_box_xpath = '//*[@id="result_list"]/tbody/tr/td[1]/input'
        check_box = self.browser.find_element_by_xpath(check_box_xpath)
        check_box.click()
        select_xpath = '//*[@id="changelist-form"]/div[1]/label/select'
        select = self.browser.find_element_by_xpath(select_xpath)
        select.click()
        if select.is_displayed():
            delete_selected_xpath = '//*[@id="changelist-form"]/div[1]/label/select/option[2]'
            delete_selected = self.browser.find_element_by_xpath(delete_selected_xpath)
            delete_selected.click()
        btn_go_xpath = '//*[@id="changelist-form"]/div[1]/button'
        btn_go = self.browser.find_element_by_xpath(btn_go_xpath)
        btn_go.click()
        btn_sure_xpath = '//*[@id="content"]/form/div/input[4]'
        btn_sure = self.browser.find_element_by_xpath(btn_sure_xpath)
        btn_sure.click()
        '''

if __name__ == '__main__':
    sd = SeleniumDemo()
    sd.login()
    sd.add_employee()
    sd.edit_employee()
    sd.delete_employee()
