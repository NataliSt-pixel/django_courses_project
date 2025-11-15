from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def clean(self):
        if self.students.count() >= getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20):
            raise ValidationError('Превышено максимальное количество студентов на курсе')


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name