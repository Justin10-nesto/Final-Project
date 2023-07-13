from django.db import models
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass, UserLog
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User
import datetime
from dateutil.relativedelta import relativedelta

class DefaultUsers(models.Model):
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    school_selected = models.TextField()
    course = models.TextField()
    type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    level = models.ForeignKey(SchoolLevel, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Default Users"
        db_table = "Default Users"

class OtpCode(models.Model):
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_status(self):
        date = datetime.datetime(self.date_created.year, self.date_created.month, self.date_created.day, self.date_created.hour +3, self.date_created.minute, self.date_created.second)

        if date > self.date_created:
            return 'Valid'
        else:
            return 'Invalid'

    class Meta:
        verbose_name = "OtpCode"
        db_table = "OtpCode"

class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    subject = models.ForeignKey(SubjectClass, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Topic"
        db_table = "Topic"

class Notes(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField(null=True)
    is_questions_exacted = models.BooleanField(default=False)
    file = models.FileField(upload_to='Notes', null = True)
    html = models.FileField(upload_to='NotesHtml', null = True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes"
        db_table = "Notes"

class QuestionType(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Question Type"
        db_table = "Question Type"

class Question(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.ForeignKey(QuestionType, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Question"
        db_table = "Question"


class Status(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
        db_table = "Status"

class AssigmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weight = models.BigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Assigment Type"
        db_table = "Assigment Type"

class Assigment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    task = models.TextField(null=True)
    date = models.DateField()
    time = models.TimeField()
    Weight = models.IntegerField()
    is_questions_exacted = models.BooleanField(default=False)
    file = models.FileField(upload_to='Assigments', null=True)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    type = models.ForeignKey(AssigmentType, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    @property
    def status(self):
        deadline = self.date
        # deadline = datetime.strptime('1/1/2024', '%d/%m/%Y')
        deadline_time = self.time
        deadline_complete = datetime.datetime(deadline.year, deadline.month, deadline.day, deadline_time.hour, deadline_time.minute, deadline_time.second)
        previous_complete = datetime.datetime(deadline.year, deadline.month, deadline.day+3, deadline_time.hour, deadline_time.minute, deadline_time.second)
        current_time = datetime.datetime.now()

        if deadline_complete >= current_time:
            return 'submission'
        elif previous_complete <= deadline_complete:
            return 'Late submission'
        else:
            return 'Previous assigments'

    class Meta:
        verbose_name = "Assigment"
        db_table = "Assigment"

class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True)
    file = models.FileField(upload_to='Books')
    is_questions_exacted = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Book"
        db_table = "Book"
        permissions = (('can_download','Can download book'),('can_share_book','Can share book'))

class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    file = models.FileField(upload_to='Tutorials')
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tutorial"
        db_table = "Tutorial"

class StudentGroupType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student Group Type"
        db_table = "Student Group Type"


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    token = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to='Groups', null=True)
    type_group = models.ForeignKey(StudentGroupType, on_delete= models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student Group"
        permissions = (('can_view_description','can view group description'),('can_hide_description','can hide group description'))
        db_table = "Student Group"

class  StudentGroupManyToMany(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE)
    user_isaccept = models.CharField(max_length=50, default='Accepted')

    def __str__(self):
        return self.user.first_name + ' ' + self.group.name

    class Meta:
        default_permissions = ('add',)
        permissions = (('can_join_group','can join to the group'),('can_left_group','can left from the group'), ('can_add_group_members','can add group members'), ('can_remove_group_members','can remove group members'))
        db_table = "Group Members"

class AssigmentSubmission(models.Model):
    doc = models.FileField(upload_to='Submited Assigments', null=True)
    parlagrims = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    remark = models.CharField(max_length=255, null=True)
    is_group = models.BooleanField(default=False)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    assigniment = models.ForeignKey(Assigment, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.first_name + " " + self.assigniment.name

    @property
    def status(self):
        deadline = self.assigniment.date
        # deadline = datetime.strptime('1/1/2024', '%d/%m/%Y')
        deadline_time = self.assigniment.time
        deadline_complete = datetime.datetime(deadline.year, deadline.month, deadline.day, deadline_time.hour, deadline_time.minute, deadline_time.second)
        previous_complete = datetime.datetime(deadline.year, deadline.month, deadline.day+5, deadline_time.hour, deadline_time.minute, deadline_time.second)
        current_time = datetime.datetime.now()

        if deadline_complete >= current_time:
            return 'submission'
        elif previous_complete >= deadline_complete:
            return 'Late submission'
        else:
            return 'Previous assigments'

    class Meta:
        verbose_name = "Assigment Submission"
        default_permissions = ()
        permissions = (('can_submit_assigment','can can submit assigment'),('can_view_submitted_assigment','can view submitted assigment'), ('can_resubmit_assigment','can resubmit assigment'), ('can_assign_marks','can assign marks and give comment to the assigment'))
        db_table = "Assigment Submission"

class AnnouncimentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Announciment Type"
        db_table = "Announciment Type"

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
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Announciment"
        db_table = "Announciment"


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
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def admision_time_status(self):
        current_time = datetime.datetime.now()
        next_month = self.date_updated + relativedelta(month=1)
        next_moth_promotion = datetime.datetime(next_month.year, next_month.month, next_month.day, next_month.hour, next_month.minute, next_month.second)
        if next_moth_promotion < current_time:
            return 'NEW'
        else:
            return 'OLD'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        db_table = "Student"

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    classCurrent = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name + ' '+ self.subject.subject_name

    class Meta:
        verbose_name = "Student Subject"
        default_permissions = ()
        permissions = (('can_register_subject','can register subject'),('can_deregister_subject','can deregister from a given subject subject'), ('can_remove_student_from_given_subject','can remove student from given subject'), ('can_add_studen_to_given_subject','can_add_studen_to_given_subject'))
        db_table = "Student Subject"

class StudentClassManyToMany(models.Model):
    classCurrent = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name

    class Meta:
        db_table = "Student Class"
        default_permissions = ()
        permissions = (('can_promote_student','can promote student'),('can_update_student_current_status','can update student current status'), ('can_track_and_evaluate_students','can track and evaluate students'))


class GroupWork(models.Model):
    work_description = models.TextField()

    class Meta:
        verbose_name = "Group Work"
        verbose_name_plural = "Group pWorks"
        db_table = "Group Work"

    def __str__(self):
        return self.name

class GroupWorkDivision(models.Model):
    task = models.TextField()
    comment = models.TextField(null=True)
    presentation_date = models.DateTimeField()
    is_presented = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete= models.CASCADE, null=True)
    work = models.ForeignKey(GroupWork, on_delete= models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete = models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.work_description

    class Meta:
        verbose_name = "Group Work Division"
        db_table = "Group Work Division"

class StudentGroupManyToMany(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name

    class Meta:
        default_permissions = ('add',)
        permissions = (('can_join_group','can join to the group'),('can_left_group','can left from the group'), ('can_add_group_members','can add group members'), ('can_remove_group_members','can remove group members'))
        db_table = "Group Members"


class StudentTask(models.Model):
    is_presented = models.BooleanField(default=False)
    groupStudent = models.ForeignKey(StudentGroupManyToMany, on_delete = models.CASCADE)
    work = models.ForeignKey(GroupWorkDivision, on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.groupStudent.student.name

    class Meta:
        db_table = "Group and Student Task"

class GroupDiscussionReply(models.Model):
    message = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Group Discussion Reply"
        verbose_name_plural = "Group Discussion Replies"
        db_table = "Group Discussion Reply"

class GroupDiscussionsMessage(models.Model):
    message = models.CharField(max_length=255)
    is_replay = models.BooleanField(default=False)
    reply = models.ForeignKey(GroupDiscussionReply, on_delete= models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Group Discussions Message"
        db_table = "Group Discussions Message"


class GroupPost(models.Model):
    message = models.TextField()
    has_topic = models.BooleanField()
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, null=True)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Group Post"
        db_table = "Group Post"


class GroupPostComent(models.Model):
    message = models.CharField(max_length=255)
    post = models.ForeignKey(GroupPost, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Group Post Coment"
        db_table = "Group Post Coment"


class GroupPostLike(models.Model):
    likes = models.FloatField()
    message_liked = models.ForeignKey(GroupPost, on_delete= models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.message_liked.message +' ' + self.sender.first_name

    class Meta:
        verbose_name = "Group Post Like"
        db_table = "Group Post Like"

class TutorialTimeTacking(models.Model):
    time = models.FloatField()
    full_length = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def video_is_completed(self):
        if self.full_length == self.time:
            return True
        else:
            return False

    @property
    def video_complition_percentage(self):
        percentage = (self.time/self.full_length)*100
        return percentage

    def __str__(self):
        return self.user.first_name

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    school = models.CharField(max_length=255)
    photo = models.FileField(upload_to='Photos', null = True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null=True, blank=True)
    anaunciment =  models.ForeignKey(Announciment, on_delete= models.CASCADE, null=True, blank=True)
    classSubject = models.ManyToManyField(SubjectClass)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name