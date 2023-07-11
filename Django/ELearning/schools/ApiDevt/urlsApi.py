
from django.urls import path, include
from . import api
urlpatterns = [
    
    path('ShowUserApi', api.ShowUserApi, name ='ShowUserApi' ),
    path('GettingSubject/<int:id>/', api.GettingSubject, name="GettingSubject"),
    path('studentAnalysisByExam/<int:id>/', api.studentAnalysisByExam, name="studentAnalysisByExam"),
    path('tutorialTrackingApi/<str:tuid>/<str:time>/<str:full_length>', api.tracking, name="tutorialTrackingApi"),
    path('generatingQuestions', api.generatingQuestions, name = 'generatingQuestions'),
    path('ExamNotification', api.ExamNotification, name = 'ExamNotification'),
    path('generatingExams', api.generatingExams, name = 'generatingExams'),
    path('StudentPromotin', api.StudentPromotin, name = 'StudentPromotin'),
    path('GettingTutorialBsedOnUser', api.GettingTutorialBsedOnUser, name = 'GettingTutorialBsedOnUser'),
    path('training_model_marks_prediction', api.training_model_marks_prediction, name = 'training_model_marks_prediction'),
    path('UpdateQuestionGeneratedCheckBox/<int:id>', api.UpdateQuestionGeneratedCheckBox, name='UpdateQuestionGeneratedCheckBox'),

]
