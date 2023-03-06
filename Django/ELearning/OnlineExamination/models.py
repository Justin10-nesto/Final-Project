from django.db import models
from Student.models import Student,Topic
from schools.models import Department, Subject, SchoolLevel, StudentClass, CourseSubject

# Create your models here.
class Grade(models.Model):
    name = models.CharField(max_length=100)
    lower_marks = models.BigIntegerField()
    upper_marks = models.BigIntegerField()
    weight = models.BigIntegerField(null=True)
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)

class Division(models.Model):
    name = models.CharField(max_length=100)
    lower_point = models.BigIntegerField()
    upper_point = models.BigIntegerField()
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)

class GPAClasses(models.Model):
    name = models.CharField(max_length=100)
    lower_gpa = models.BigIntegerField()
    upper_gpa = models.BigIntegerField()
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)
    
class ExamType(models.Model):
    name = models.CharField(max_length=100)
    weight_annual = models.BigIntegerField(null=True)
    weight_final = models.BigIntegerField(null=True)
    studentClass = models.ForeignKey(StudentClass, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)
    
class QuestionsType(models.Model):
    name = models.CharField(max_length=100)
    number_of_questions = models.BigIntegerField()
    weight = models.BigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    
class ExamFormat(models.Model):
    section = models.CharField(max_length=100)
    weight = models.BigIntegerField()
    number_of_questions = models.BigIntegerField()
    exam_type = models.ForeignKey(ExamType, on_delete = models.CASCADE)    
    type_questions = models.ForeignKey(QuestionsType, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
class Exam(models.Model):
    name = models.CharField(max_length=100)
    weight_annual = models.BigIntegerField(null=True)
    weight_Final = models.BigIntegerField(null=True)
    exam_type = models.ForeignKey(ExamType, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)

class StudentExam(models.Model):
    name = models.CharField(max_length=100)
    weight_annual = models.BigIntegerField(null=True)
    marks = models.BigIntegerField(null=True)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete = models.CASCADE)    
    student = models.ForeignKey(Student, on_delete = models.CASCADE)    
    exam = models.ForeignKey(Exam, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)

class StudentResult(models.Model):
    status = models.CharField(max_length=100)
    point = models.BigIntegerField(null=True)
    points = models.ForeignKey(Division, on_delete = models.CASCADE)    
    exam = models.ForeignKey(StudentExam, on_delete = models.CASCADE)    
    student = models.ForeignKey(Student, on_delete = models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)
