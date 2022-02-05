from django.contrib import admin
from employee.models import Employee


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'salary']  # 对于model里面的定义
    search_fields = ['code', 'name']
    list_filter = ['id']


admin.site.register(Employee, EmployeeAdmin)
