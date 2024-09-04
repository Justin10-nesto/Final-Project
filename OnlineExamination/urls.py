
from django.urls import path, include
from . import views
urlpatterns = [

    path('studentVerification', views.studentVerification, name = 'studentVerification'),
    path('gradeList', views.gradeList, name = 'gradeList'),
    path('gradeAdd', views.gradeAdd, name ='gradeAdd'),
    path('gradeEdit/<str:id>', views.gradeEdit, name ='gradeEdit'),
    path('gradeDelete/<str:id>', views.gradeDelete, name ='gradeDelete'),

    path('divisionList', views.divisionList, name = 'divisionList'),
    path('divisionAdd', views.divisionAdd, name ='divisionAdd'),
    path('divisionEdit/<str:id>', views.divisionEdit, name ='divisionEdit'),
    path('divisionDelete/<str:id>', views.divisionDelete, name ='divisionDelete'),

    path('examTypeList', views.examTypeList, name = 'examTypeList'),
    path('examTypeAdd', views.examTypeAdd, name ='examTypeAdd'),
    path('examTypeEdit/<str:id>', views.examTypeEdit, name ='examTypeEdit'),
    path('examTypeDelete/<str:id>', views.examTypeDelete, name ='examTypeDelete'),

    path('QuestionsTypeList', views.QuestionsTypeList, name = 'QuestionsTypeList'),
    path('QuestionsTypeAdd', views.QuestionsTypeAdd, name ='QuestionsTypeAdd'),
    path('QuestionsTypeEdit/<str:id>', views.QuestionsTypeEdit, name ='QuestionsTypeEdit'),
    path('QuestionsTypeDelete/<str:id>', views.QuestionsTypeDelete, name ='QuestionsTypeDelete'),

    path('examFormatList', views.examFormatList, name = 'examFormatList'),
    path('examFormatAdd', views.examFormatAdd, name ='examFormatAdd'),
    path('examFormatEdit/<str:id>', views.examFormatEdit, name ='examFormatEdit'),
    path('examFormatDelete/<str:id>', views.examFormatDelete, name ='examFormatDelete'),

    path('BankQuestionTable', views.BankQuestionTable, name = 'BankQuestionTable'),
    path('examList', views.examList, name = 'examList'),
    path('LoginAgin/<str:id>', views.LoginAgin, name = 'LoginAgin'),
    path('Exam/<str:id>', views.Exam, name = 'Exam'),
    
    path('SubmittingExamination/<int:stEx>', views.SubmittingExamination, name = 'SubmittingExamination'),
    path('UserSubmittedExamList/<int:id>/<int:stexm_id>', views.UserSubmittedExamList, name = 'UserSubmittedExamList'),
    path('TeacherMarking/<int:id>', views.TeacherMarking, name = 'TeacherMarking'),
    path('UpdateMarks/<int:id>', views.UpdateMarks, name = 'UpdateMarks'),
    
    path('ExaminationDone', views.ExaminationDone, name='ExaminationDone'),
    path('ViewBankOfQuestions/<int:id>', views.ViewBankOfQuestions, name='ViewBankOfQuestions'),
    path('UpdateQuestionGenerated/<int:id>', views.UpdateQuestionGenerated, name='UpdateQuestionGenerated'),

    path('DeleteexamList/<str:id>', views.DeleteexamList, name ='DeleteexamList'),
    path('MakeApointmentAdd', views.MakeApointmentAdd, name = 'MakeApointmentAdd'),
    path('examRegulation', views.examRegulation, name= 'examRegulation'),

    path('GeneratingStudentResult', views.GeneratingStudentResult, name= 'GeneratingStudentResult'),
    path('CurrentStudentResult', views.CurrentStudentResult, name= 'CurrentStudentResult'),
    path('FullStudentResult', views.FullStudentResult, name= 'FullStudentResult'),
    path('Checking_student_Results', views.Checking_student_Results, name= 'Checking_student_Results'),
    path('CheckingYouCurrentResults', views.CheckingYouCurrentResults, name='CheckingYouCurrentResults'),
    
    path('uploadingExaminationQuestions', views.uploadingExaminationQuestions, name='uploadingExaminationQuestions'),
    path('gettingStudentData', views.gettingStudentData, name='gettingStudentData'),
    # path('webcam-analysis', views.webcam_analysis, name='webcam_analysis'),
        
   ]
