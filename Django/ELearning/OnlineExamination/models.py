from django.db import models
from OnlineLearning.models import Student,Topic
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass, UserLog
import datetime
from django.utils import timezone

class Grade(models.Model):
    name = models.CharField(max_length=100)
    lower_marks = models.BigIntegerField()
    upper_marks = models.BigIntegerField()
    weight = models.BigIntegerField(null=True)
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grade"
        db_table = "Grade"

class Division(models.Model):
    name = models.CharField(max_length=100)
    lower_point = models.BigIntegerField()
    upper_point = models.BigIntegerField()
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Division"
        db_table = "Division"

class GPAClasses(models.Model):
    name = models.CharField(max_length=100)
    lower_gpa = models.BigIntegerField()
    upper_gpa = models.BigIntegerField()
    description = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "GPA Class"
        db_table = "GPA Class"

class ExamType(models.Model):
    name = models.CharField(max_length=100)
    weight_annual = models.BigIntegerField(null=True)
    weight_final = models.BigIntegerField(null=True)
    is_final = models.BooleanField(default=False)
    studentClass = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Examn Type"
        db_table = "Examn Type"

class QuestionsType(models.Model):
    name = models.CharField(max_length=100)
    number_of_questions = models.BigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Questions Type"
        db_table = "Questions Type"

class ExamFormat(models.Model):
    section = models.CharField(max_length=100)
    weight = models.BigIntegerField()
    number_of_questions = models.BigIntegerField()
    exam_type = models.ForeignKey(ExamType, on_delete = models.CASCADE)
    type_questions = models.ForeignKey(QuestionsType, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    exam_type =models.ForeignKey(ExamType, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section

    @property
    def gettingMarks(self):
        perQuestion = self.weight/self.number_of_questions
        return perQuestion

    class Meta:
        verbose_name = "Examination Format"
        db_table = "Examination Format"

class Generated_exam(models.Model):
    question = models.TextField()
    answers = models.TextField()
    examination_identity = models.BigIntegerField(default=0)
    is_generated = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    exam_format = models.ForeignKey(ExamFormat, on_delete = models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    @property
    def status(self):
        current_time = datetime.datetime.now()
        exam_date = self.date_created
        ending_validity = datetime.datetime(exam_date.year, exam_date.month, exam_date.day, exam_date.hour +5, exam_date.minute, exam_date.second)

        if (current_time > ending_validity):
            return 'Invalid'

        else:
            return 'Valid'

    class Meta:
        verbose_name = "Examination Generated"
        db_table = "Examination Generated"
        ordering = ['-date_created']

class StudentExam(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    marks = models.BigIntegerField(null=True)
    is_submitted = models.BigIntegerField(default=0)
    date_of_exam = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    is_notified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_result_generated = models.BooleanField(default=False)
    examination_identity = models.BigIntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete = models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    exam = models.ForeignKey(ExamType, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name + ' '+ self.subject.subject_name + ' ' +self.status

    @property
    def getting_fully_endtime(self):
        exam_date = self.date_of_exam
        end_exam = datetime.datetime(exam_date.year, exam_date.month, exam_date.day, self.end_time.hour, self.end_time.minute, self.end_time.second)
        return end_exam

    @property
    def status(self):
        current_time = datetime.datetime.now()
        exam_date = self.date_of_exam
        preparing_exam = datetime.datetime.combine(exam_date, self.start_time) - datetime.timedelta(minutes=30)
        start_exam = datetime.datetime(exam_date.year, exam_date.month, exam_date.day, self.start_time.hour, self.start_time.minute, self.start_time.second)
        end_exam = datetime.datetime(exam_date.year, exam_date.month, exam_date.day, self.end_time.hour, self.end_time.minute, self.end_time.second)

        if (preparing_exam > current_time):
            return 'PENDING'

        elif (start_exam > current_time) and  (preparing_exam < current_time):
            return 'INITIAL PREPARATION'

        elif (end_exam > current_time) and  (start_exam < current_time):
            return 'EXAM CONTINUE'

        elif current_time >end_exam:
            return 'EXAM END'
        else:
            return ''

    class Meta:
        verbose_name = "Student Exam"
        db_table = "Student Exam"

class StudentAnswer(models.Model):
    user_answers = models.TextField()
    marks_scored = models.BigIntegerField(default=0)
    is_marked_byML = models.BooleanField(default=False)
    is_verified_teacher = models.BooleanField(default=False)
    studentExam = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    generated_question = models.ForeignKey(Generated_exam, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Student Answer"
        db_table = "Student Answer"

class StudentResult(models.Model):
    point = models.BigIntegerField(null=True)
    grade = models.CharField(max_length=100)
    average = models.BigIntegerField(null=True)
    division =models.CharField(max_length=100)
    exam = models.ForeignKey(StudentExam, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name + " " + self.status

    class Meta:
        verbose_name = "Student Result"
        db_table = "Student Result"

class ExaminationDump(models.Model):
    questions =models.TextField(null=True)
    answers = models.TextField()
    # complexety_level = models.CharField(max_length=355)
    is_generated_Model = models.BooleanField(default=True)
    questionType = models.ForeignKey(QuestionsType, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Examination Dump  Questions"
        db_table = "Examination Dump  Questions"

