from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from schools.models import Subject, Department, StudentClass,SchoolLevel, Course, CourseSubject
from django.utils.functional import SimpleLazyObject
import logging

from django.core.handlers.wsgi import WSGIRequest
from threading import current_thread

stdlogger = logging.getLogger(__name__)

def get_current_request():
    return SimpleLazyObject(lambda: get_current_request_actual())

def get_current_request_actual():
    request = None

    if isinstance(getattr(current_thread(), 'request', None), WSGIRequest):
        request = current_thread()
        print(request)
    return request

@receiver(pre_delete, sender = 'schools.Department')
def deleting_student(sender, **kwargs):
    request = get_current_request()
    print(request.user)
    if request == None and not request.user.is_authenticated:
        print("Start pre_save Item in signals.py under items app")
        print("sender %s" % (sender))
        print("kwargs %s" % str(kwargs['instance'].name))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
