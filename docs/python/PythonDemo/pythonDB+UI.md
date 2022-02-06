## Create the database
```
# sqlite3 sqlite.db
sqlite> .database
main: /opt/projects/myPython/pythonDB+UI/sqlite.db
sqlite> create table employee (
id integer primary key autoincrement,
code varchar(100),
name varchar(200)
);
sqlite> .tables
employee
sqlite> select * from employee;
23|E01|Ying
24|E02|Wang
25|E03|Zhang
sqlite> 
```

## Model folder
File `config.ini` is to set up configuration of Sqlite database
```
[DB_SECTION]
user=root
password=
database=/opt/projects/myPython/pythonDB+UI/sqlite.db
```
File `employee.py` is to define class `Employee`
```
class Employee(object):
    def __init__(self, code, name, *, salary=0.0, **kwargs):
        self.code = code
        self.name = name
        self.salary = salary
        self.details = kwargs
        print(kwargs)
```
File `databaseSqlite.py` is to define database connection and CRUD.   
File `application.py` is the entry of the web application. Run below command to start the service at http://127.0.0.1:9000/   
```
python3 application.py
```
## Home foder
File `controller.py` is to about logic of each pages based on templates
```
# Initialize home page
@get('/')
def index():
    return {
        '__template__': 'employee_list.html'
    }


# Show the list in home page
@get('/services/employees')  #  Row29 in employee_list.html
def get_employees():
    employees = Database.query()
    return dict(employees=employees)


# Define the new page ADD after clicking button ADD
@get('/ui/employees/add')
def ui_add_employee():
    return {
        '__template__': 'add_edit_employee.html',
        'id': '',
        'action': '/service/employees'
    }


# Define the logic of SAVE button in the ADD page
@post('/service/employees')
def add_employee(*, code, name):
    employee = Employee(code, name)
    Database.save(employee)


# Define the new page EDIT after clicking EDIT button in the homepage
@get('/ui/employees/edit')
def ui_edit_employee(*, id):
    return {
        '__template__': 'add_edit_employee.html',
        'id': id,
        'action': '/services/employees/%s' % id
    }


# Define what will be shown in the EDIT page
@get('/services/employees/{id}')
def edit_employee(*, id):
    employee = Database.query_by_id(id)
    print(employee)
    return dict(id=employee[0], code=employee[1], name=employee[2])


# Define function of SAVE button in the EDIT page
@post('/services/employees/{id}')
def save_change(*, id, code, name):
    employee = Employee(code, name)
    employee.id = id
    Database.update(employee)


# Define the function of DELETE button in the homepage
@post('/services/employees/{id}/delete')  # Row18 in employee_list.html
def delete_employee(*, id):
    Database.delete(id)
```

## Template folder
Define templates






