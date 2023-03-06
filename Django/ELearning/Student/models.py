from django.db import models
from schools.models import Subject, Course, Department, SchoolLevel, StudentClass
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User
from datetime import datetime, timedelta

class DefaultUsers(models.Model):
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school_selected = models.TextField()
    course = models.TextField()
    type = models.CharField(max_length=255)   
    location = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DefaultUsers'
    

class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE) 
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField(null=True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class QuestionType(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.ForeignKey(QuestionType, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class AssigmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weight = models.BigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Assigment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    task = models.TextField(null=True)
    date = models.DateField()
    time = models.TimeField()
    Weight = models.IntegerField()
    file = models.FileField(upload_to='Assigments', null=True)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    type = models.ForeignKey(AssigmentType, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True)
    file = models.FileField(upload_to='Books')
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    file = models.FileField(upload_to='Tutorials')
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class StudentGroupType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'StudentGroupType'
    
    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    token = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to='Groups', null=True)
    type_group = models.ForeignKey(StudentGroupType, on_delete= models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class  StudentGroupManyToMany(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE)
    user_isaccept = models.CharField(max_length=50, default='Accepted')

class AssigmentSubmission(models.Model):
    doc = models.FileField(upload_to='Submited Assigments', null=True)
    marks = models.IntegerField(default=0)
    is_group = models.BooleanField(default=False)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    assigniment = models.ForeignKey(Assigment, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def status(self):
        # deadline = datetime.date(self.assigniment.date) + datetime.time(self.assigniment.time)
        deadline = datetime.strptime('1/1/2024', '%d/%m/%Y')
        current_time = datetime.now()
        difference = deadline - current_time
        int_delta = (difference.days*24*60*60)+difference.seconds
        
        if int_delta >0:
            return 'submission'
        else:
            return 'Late submission'
 
class AnnouncimentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Announciment(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    is_opened = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    announcimentType = models.ForeignKey(AnnouncimentType, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
        

class Student(models.Model):
    name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50)
    index_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, null=True)
    school = models.CharField(max_length=255)
    photo = models.FileField(upload_to='Photos', null = True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    classCurrent = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    anaunciment =  models.ForeignKey(Announciment, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name + ' '+ self.subject.name

class StudentClassManyToMany(models.Model):
    classCurrent = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student.name

class GroupWorkDivision(models.Model):
    work_description = models.TextField()
    task = models.TextField()
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class StudentGroupManyToMany(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE, null=True)
    work = models.ForeignKey(GroupWorkDivision, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student.name
    
class GroupDiscussionReply(models.Model):
    message = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class GroupDiscussionsMessage(models.Model):
    message = models.CharField(max_length=255)
    is_replay = models.BooleanField(default=False)
    reply = models.ForeignKey(GroupDiscussionReply, on_delete= models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class GroupPost(models.Model):
    message = models.TextField()
    has_topic = models.BooleanField()
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, null=True)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class GroupPostComent(models.Model):
    message = models.CharField(max_length=255)
    post = models.ForeignKey(GroupPost, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class GroupPostLike(models.Model):
    likes = models.BooleanField()
    message_liked = models.ForeignKey(GroupPost, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

