from django.db import models


# Create your models here.
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=8, decimal_places=3, default=0.0)
