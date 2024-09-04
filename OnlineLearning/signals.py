from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save, post_delete, post_migrate
from django.utils.functional import SimpleLazyObject
from OnlineLearning.models import Student,DefaultUsers,StudentSubject, Book, Assigment, AssigmentType, Topic
from schools.models import Subject, Department, StudentClass,SchoolLevel, Course, CourseSubject
from django.contrib.auth.models import User

@receiver(post_migrate, sender = User)
def registeringDumyData(sender, **kwargs):
    print('migration done sucessfully')

@receiver(post_save, sender='OnlineLearning.StudentSubject')
def moduleregistration(sender, **kwargs):
    email = [kwargs['instance'].student.user.email]
    header = 'Account Creation'
    message = f'dear user_info.name,\n cogratulation you subject registration is done sucessfully'
    email_from = settings.EMAIL_HOST_USER
    send_mail(header, message, email_from, email)

@receiver(post_save, sender='OnlineLearning.Student')
def studentregistration(sender, **kwargs):

    email_reciver = [kwargs['instance'].user.email]
    header = 'Account Creation'
    user_info = kwargs['instance']
    message = f'dear {user_info.name},\n congratulations, your account is sucessfully created'
    email_from = settings.EMAIL_HOST_USER
    send_mail(header, message, email_from, email_reciver)
