### Initialize the project and get `manage.py` file as starting point
```
# cd /opt/projects/myPython
# django-admin startproject pythonDjango
```

### Initialize employee model
```
# python3 manage.py startapp employee
```

### Register your model by add admin.py in folder employee
```
from django.contrib import admin
from employee.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'salary']  # 对于model里面的定义
    search_fields = ['code', 'name']
    list_filter = ['id']

admin.site.register(Employee, EmployeeAdmin)
```
### Configure the app
```
from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employee'
```

### Deploy the change and start the server
```
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver
```
### Validate the service is up (no content here!)
http://127.0.0.1:8000/


### Create super user
```
# python3 manage.py createsuperuser
Username (leave blank to use 'i310913'): root
Email address: aa@bb.cn
Password: root
Password (again): root
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```
### Validate the admin service. Add records in Employee, also available for delete and update
http://127.0.0.1:8000/admin

Validate 3 records added via admin page in Sqlite database
```
# /opt/projects/myPython/pythonDjango/sqlite-utils tables db.sqlite3
[{"table": "django_migrations"},
 {"table": "sqlite_sequence"},
 {"table": "auth_group_permissions"},
 {"table": "auth_user_groups"},
 {"table": "auth_user_user_permissions"},
 {"table": "django_admin_log"},
 {"table": "django_content_type"},
 {"table": "auth_permission"},
 {"table": "auth_group"},
 {"table": "auth_user"},
 {"table": "django_session"},
 {"table": "employee_employee"}]
```
Query table employee, and see 3 records below. 
```
# sqlite-utils db.sqlite3 "select * from employee_employee"
[{"id": 1, "code": "E01", "name": "James", "salary": 0},
 {"id": 2, "code": "E02", "name": "Jim", "salary": 0},
 {"id": 3, "code": "E03", "name": "Jason", "salary": 120.5}]

 ```
 
 
 
 
