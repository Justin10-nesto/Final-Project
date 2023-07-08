
from django.urls import path, include
from . import api
urlpatterns = [
    
    path('ShowUserApi', api.ShowUserApi, name ='ShowUserApi' ),
    path('GettingSubject/<int:id>/', api.GettingSubject, name="GettingSubject"),
    path('tutorialTrackingApi/<str:tuid>/<str:time>/<str:full_length>', api.tracking, name="tutorialTrackingApi"),
    path('generatingQuestions', api.generatingQuestions, name = 'generatingQuestions'),
    path('ExamNotification', api.ExamNotification, name = 'ExamNotification'),
    path('generatingExams', api.generatingExams, name = 'generatingExams'),
    path('StudentPromotin', api.StudentPromotin, name = 'StudentPromotin'),
    path('GettingTutorialBsedOnUser', api.GettingTutorialBsedOnUser, name = 'GettingTutorialBsedOnUser'),
    path('UpdateQuestionGeneratedCheckBox/<int:id>', api.UpdateQuestionGeneratedCheckBox, name='UpdateQuestionGeneratedCheckBox'),
]
