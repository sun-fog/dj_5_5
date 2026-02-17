# models.py
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)  # Вместо TextField()
    birth_date = models.DateField(null=True)


class Course(models.Model):
    name = models.CharField(max_length=100)  # Вместо TextField()
    students = models.ManyToManyField(Student, blank=True)

