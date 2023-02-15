from django.db import models
from schools.models import Subject, Department, SchoolLevel, StudentClass

from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User

class DefaultUsers(models.Model):
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school_selected = models.TextField()
    course = models.TextField()
    type = models.CharField(max_length=255)   
    location = models.CharField(max_length=255)


    class Meta:
        db_table = 'DefaultUsers'
        

class NotesFiles(models.Model):
    title_of_documment = models.CharField(max_length=50)
    type_of_the_book = models.CharField(max_length=50)
    documment = models.FileField(upload_to=None )
    
    def __str__(self):
        return self.title_of_documment
 
class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField(null=True)
    
    def __str__(self):
        return self.title
    

class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class QuestionType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.ForeignKey(QuestionType, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class AssigmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weight = models.BigIntegerField()
    
    def __str__(self):
        return self.name
    
class Assigment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    task = models.TextField(null=True)
    date = models.DateField()
    time = models.TimeField()
    Weight = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    type = models.ForeignKey(AssigmentType, on_delete= models.CASCADE)

    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True)
    file = models.FileField()
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)


class StudentGroupType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'StudentGroupType'
        

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    type = models.ForeignKey(StudentGroupType, on_delete= models.CASCADE)
    assignent = models.ForeignKey(Assigment, on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete= models.CASCADE, null =True)
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50)
    index_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    classCurrent = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    def __str__(self):
        return self.name

