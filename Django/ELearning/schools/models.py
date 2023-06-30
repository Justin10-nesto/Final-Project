from django.db import models
from django.contrib.auth.models import User
# from django_tenants.models import TenantMixin, DomainMixin

# class School(TenantMixin):
#     school_name = models.CharField(max_length=100)
#     schoo_logo    =  models.CharField(max_length=100)
#     school_level = models.CharField(max_length=100)
#     school_adress = models.CharField(max_length=100)
#     head_of_school = models.TextField()
#     is_active = models.BooleanField(default=True)
#     created_on = models.DateField(auto_now_add=True)

#     # default true, schema will be automatically created and synced when it is saved
#     auto_create_schema = True
#     auto_drop_schema = True

# class Domain(DomainMixin):
#     pass

class UserLog(models.Model):
    task = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Log"
        verbose_name_plural = "User Logs"
        db_table = "User Log"

    def __str__(self):
        return self.task

class Department(models.Model):
    name = models.CharField(max_length=100)
    department_Hod = models.CharField(max_length=100)
    start_date= models.DateField()

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = "Department"

    def __str__(self):
        return self.name

class Subject(models.Model):
    subject_code = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50, unique = True)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)

    def __str__(self):
        return self.subject_name

    class Meta:
        db_table = "Subject"
        permissions = (('register_subject','Can perform subject registeration'),('can_drop_subject','Can drop subject'))

class SchoolLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "SchoolLevel"


class StudentClass(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    def get_final_class(self):
        if self.name == 'Form Four' or self.name == 'Form Six':
            return True
        else:
            return False

    def get_national_test_class(self):
        if self.name == 'Form Two':
            return True
        else:
            return False

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        db_table = "Class"

class SubjectClass(models.Model):
    studentClass = models.ForeignKey(StudentClass, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)

    def __str__(self):
        return self.studentClass.name + " " + self.subject.subject_name

    class Meta:
        verbose_name = "Subject Class"
        db_table = "Subject Class"


class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete= models.CASCADE, null =True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        db_table = "Course"
        permissions = (('enroll_course','Can enroll course'),('drop_subject','Can drop Course'))

class SubjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SubjectCategory"
        verbose_name_plural = "SubjectCategories"
        db_table = "Subject Category"

class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    studentClass = models.ForeignKey(StudentClass, on_delete = models.CASCADE)

    def __str__(self):
        return self.course.name + ' '+ self.subject.name

    class Meta:
        verbose_name = "CourseSubject"
        db_table = "Course Subject"
