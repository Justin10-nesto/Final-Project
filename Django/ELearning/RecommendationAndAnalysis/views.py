import numpy as np
import pandas as pd
import random
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import  train_test_split
from sklearn.metrics import  mean_squared_error, mean_absolute_error
import joblib
import io
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from OnlineExamination.ExamsDoc import results
from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask,TutorialTimeTacking
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import User, Group, Permission
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, UserLog
from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentAnswer, StudentExam, StudentResult
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
import os
import joblib
import datetime

# Create your views here.
model_path = settings.STATICFILES_DIRS[0] +r'\models'
def studentMarksPrediction(request):
    exam_type_ID = 1
    student_details = {'subject':[], 'exam_type':[], 'class':[],
    'hours_of_studying':[], 'participation_in_group':[], 'group_parlagrims':[],
    'individual_paralligms':[], 'assigments_individual':[], 'assigments_group':[],
    'previous_marks':[], 'panctuality':[]}
    student = Student.objects.filter(user = request.user)
    if student.exists():
        studentInfo = student.first()
        subjects = StudentSubject.objects.filter(student = studentInfo)
        for subject in subjects:
            panctuality_arr = []
            panctuality = 0
            total_tasks =GroupWorkDivision.objects.filter(student = studentInfo, group__subject__gt = subject.subject).count()
            task_done =GroupWorkDivision.objects.filter(student = studentInfo, group__subject__gt = subject.subject, is_presented=True).count()
            try:
                partipation = (task_done/total_tasks)*100
            except ZeroDivisionError:
                partipation =0
            panctuality_arr = []
            assigments =AssigmentSubmission.objects.filter(subject=subject.subject, user=studentInfo.user, assigniment__type__name__gt = 'Individual')
            all_assigments = Assigment.objects.filter(subject=subject.subject, type__name__gt = 'Individual')
            weights = [ass.marks*ass.assigniment.Weight for ass in assigments]
            total_weigths_submited_assiments = sum(weights)
            all_assigments_arr= [ass.Weight**2 for ass in all_assigments]
            total_weights = sum(all_assigments_arr)
            try:
                individual_assigment = (total_weigths_submited_assiments/total_weights)*100
            except ZeroDivisionError:
                individual_assigment = 0
            if assigments:
                for ass in assigments:
                    if ass.status == 'submission':
                        panctuality_arr.append(1)
                    elif ass.status == 'Late submission':
                        panctuality_arr.append(0.5)
            group_assigment = 0
            previous_marks = 59
            group_assigments = []
            if StudentGroupManyToMany.objects.filter(student = studentInfo).exists():

                student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
                group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group, assigniment__type__name__gt = 'Group')
                all_assigments_gr = Assigment.objects.filter(subject=subject.subject, type__name__gt = 'Group')
                weights_for_group = [ass.marks*ass.assigniment.Weight for ass in group_assigments]
                total_weigths_submited_assiments_for_group = sum(weights_for_group)
                all_assigments_arr_gr= [ass.Weight**2 for ass in all_assigments]
                total_weights_group = sum(all_assigments_arr_gr)
                try:
                    group_assigment = (total_weigths_submited_assiments_for_group/total_weights_group)*100
                except ZeroDivisionError:
                    group_assigment =0
                student_marks = StudentExam.objects.filter(subject=subject.subject).order_by('date_created')
                student_marks_arr = [st.marks for st in student_marks if st.status == 'EXAM END']

                if group_assigments:
                    for ass in group_assigments:
                        if ass.status == 'submission':
                            panctuality_arr.append(1)
                        elif ass.status == 'Late submission':
                            panctuality_arr.append(0.5)

                panctuality = sum(panctuality_arr)
                previous_marks = 0
                if len(student_marks_arr)>0:
                    previous_marks= student_marks_arr[0]
            data_returned = checking_task(request=request, task_recived='viewing tutorial page')
            tutorials = Tutorial.objects.filter(subject = subject.subject)
            video_tracking = TutorialTimeTacking.objects.filter(user = studentInfo.user)
            Tutorial_learning_arr = []
            for tutorial in tutorials:
                for tr_tutorials in video_tracking:
                    if tr_tutorials.tutorial == tutorial:
                        Tutorial_learning_arr.append(tr_tutorials.video_complition_percentage)
                    try:
                        Tutorial_learning_pecentage  = sum(Tutorial_learning_arr)/tutorials.count()
                    except:
                        pass
            time_tutorial = checking_task(request=request, task_recived='viewing tutorial page')
            time_Resubmitting_for_assiment = checking_task(request=request, task_recived='Resubmitting an assiment')
            time_viewing_an_assigment = checking_task(request=request, task_recived='Viewing assigment to be done')
            time_view_assigment = checking_task(request=request, task_recived='Viewing Assigments List')
            time_viewing_book = checking_task(request=request, task_recived='Viewing Books List')
            time_Viewing_topic  = checking_task(request=request, task_recived='Viewing topic List')
            time_required = time_tutorial['time_used_per_day']['difference'] +time_Resubmitting_for_assiment['time_used_per_day']['difference'] + time_viewing_an_assigment['time_used_per_day']['difference'] + time_view_assigment['time_used_per_day']['difference'] + time_viewing_book['time_used_per_day']['difference'] + time_Viewing_topic['time_used_per_day']['difference']
            total_time_used =time_required.sum()
            time_current = datetime.datetime.now()
            joined_date = studentInfo.user.date_joined
            joined_date_datetime = datetime.datetime(joined_date.year, joined_date.month, joined_date.day, joined_date.hour, joined_date.minute, joined_date.second)
            difference_in_time = time_current - joined_date_datetime
            hours_studying = (total_time_used/difference_in_time) *100

            individual_paralligms = random.randint(0, 100)
            group_parlagrims = random.randint(0, 100)
            student_details['subject'].append(subject.subject.subject_name.capitalize())
            student_details['exam_type'].append(exam_type_ID)
            student_details['class'].append(studentInfo.classCurrent.name)
            student_details['hours_of_studying'].append(hours_studying)
            student_details['participation_in_group'].append(partipation)
            student_details['assigments_individual'].append(individual_assigment)
            student_details['assigments_group'].append(group_assigment)
            student_details['previous_marks'].append(previous_marks)
            student_details['panctuality'].append(panctuality)
            student_details['group_parlagrims'].append(group_parlagrims)
            student_details['individual_paralligms'].append(individual_paralligms)
    else:
        sutentInfos = Student.objects.all()
        print('absent')

    marks_model = model_path + '\studentmarks.pkl'
    loaded_moddel = joblib.load(open(marks_model, 'rb'))
    data = pd.DataFrame(student_details)
    class_mapping = {'Form one':1, 'Form Two':2, 'Form Three':3, 'Form Four':4, 'Form Five':5, 'Form Six':6}
    subject_mapping = {'Neutrition': 0, 'Commerce': 1, 'Computer,': 2, 'Civics': 3, 'Physics': 4, 'History': 5, 'Agriculture': 6, 'Basic Mathematics': 7, 'Franch': 8, 'Kiswahili': 9, 'Bilogy': 10, 'Chemistry': 11, 'Geography': 12, 'Advance Mathematics': 13, 'English Language': 14, 'Economics': 15, '--':16}
    data['subject'] = data['subject'].map(subject_mapping)
    data['class'] = data['class'].map(class_mapping)
    data  = data.dropna()
    marks = loaded_moddel.predict(data)
    marks = np.abs(marks)
    reverse_subject_mapping = {v: k for k, v in subject_mapping.items()}
    data['subject'] = data['subject'].map(reverse_subject_mapping)
    suject = [sub for sub in data['subject']]
    marks_list =  [mark for mark in marks]
    return {'data':marks_list, 'subject':suject}
    # return redirect('examList')
    
def concate_columns(row):
    return str(row["CIV"])+str(row["HIST"])+str(row["GEO"])+str(row["KISW"])+str(row["ENGL"])+str(row["LIT ENG"])+str(row["PHY"])+str(row["CHEM"])+str(row["BIO"])+str(row["B/MATH"])

def studentCourseRecomendation(request):
    student = Student.objects.filter(user = request.user)
    level = SchoolLevel.objects.filter(name = 'O-Level').first()
    grade = Grade.objects.filter(level = level)
    student_data = {'CIV': [], 'HIST': [], 'GEO': [], 'KISW': [], 'ENGL': [], 'LIT ENG': [], 'PHY': [], 'CHEM': [], 'BIO': [], 'B/MATH': [], 'division':[], 'points':[]}
    course_subjects = {'CIV': [], 'HIST': [], 'GEO': [], 'KISW': [], 'ENGL': [], 'LIT ENG': [], 'PHY': [], 'CHEM': [], 'BIO': [], 'B/MATH': [], 'Capacity':[]}
    class_mapping_all_subjects = {'Civics':'CIV', 'Basic Mathematics': 'B/MATH', 'History':'HIST', 'Geography':'GEO', 'Kiswahili':'KISW', 'English Language':'ENGL',  'Chemistry':'CHEM', 'Bilogy':'BIO', 'Physics':'PHY', 'Literature in English':'LIT ENG'}
    class_mapping_grade= {'A':5, 'B':4, 'C':3, 'D':2, 'F':1, "not-done":0}
    subjects_arr = []
    if student.exists():
        studentInfo = student.first()
        current_class = studentInfo.classCurrent.name
        if current_class == 'Form One':
            student_marks = StudentExam.objects.filter(student=studentInfo)
            for marks in student_marks:
                if marks.exam.is_final == False:
                    subjects_arr.append(marks.subject)

        if request.method == 'POST':
            capacity = request.POST.get('capacity')
            course_subjects['Capacity'].append(capacity)
            for sub in subjects_arr:
                text = 'subject_' + str(sub.id)
                marks_for_college = request.POST.get(text)
                for key, value in class_mapping_all_subjects.items():
                    if key == sub.subject_name:
                        course_subjects[value].append(int(marks_for_college))
                                                  
            studentInfo = student.first()
            current_class = studentInfo.classCurrent.name
            if current_class == 'Form One':
                student_marks = StudentExam.objects.filter(student=studentInfo)
                for marks in student_marks:
                    if marks.exam.is_final == False:
                        subject_name = marks.subject.subject_name
                        subjects_arr.append(marks.subject)
                        marks_scored = marks.marks
                        points_exam = results.getting_points(grades=grade, marks=[marks_scored, marks_scored])
                        marks_grade =points_exam['grade'][0]
                        for key, value in class_mapping_all_subjects.items():
                            if key == subject_name:
                                for grade_name, point in class_mapping_grade.items():
                                    if marks_grade == grade_name:
                                        student_data[value].append(point)

                for key, value in student_data.items():
                    if len(student_data[key])<1:
                        student_data[key] = 0
                        
                for key, value in course_subjects.items():
                    if len(course_subjects[key])<1:
                        course_subjects[key] = 0
                        
                subject_data = pd.DataFrame(student_data)
                subject_data["minAdmissionRequirement"]=subject_data.apply(concate_columns,axis=1)
                print(subject_data)
                subjects=["CIV","HIST","GEO","KISW","ENGL","LIT ENG","PHY","CHEM","BIO","B/MATH"]
                for index ,row  in subject_data.iterrows():
                    sum=row["CIV"]+row["HIST"]+row["GEO"]+row["KISW"]+row["ENGL"]+row["LIT ENG"]+row["PHY"]+row["CHEM"]+row["BIO"]+row["B/MATH"]
                
                    subject_data.at[index,"SAPG"]=sum
                    
                subject_data["SARG"]=subject_data.apply(concate_columns,axis=1)
                cag = pd.DataFrame(course_subjects)
                            
                for index ,row  in cag.iterrows():
                    sum=row["CIV"]+row["HIST"]+row["GEO"]+row["KISW"]+row["ENGL"]+row["LIT ENG"]+row["PHY"]+row["CHEM"]+row["BIO"]+row["B/MATH"]
                
                    cag.at[index,"Min Admition Point"]=sum   

                cag["minAdmissionRequirement"]=cag.apply(concate_columns,axis=1)
                for i in subjects:
                    subject_data.drop(i,axis=1,inplace=True)
                    cag.drop(i,axis=1,inplace=True)
                fdf = pd.concat([subject_data, cag], axis=1)
                print(fdf)
                fdf=fdf[['division', 'points', 'SAPG', 'SARG','Min Admition Point', 'minAdmissionRequirement','Capacity',]]
                # for index, row in fdf.iterrows():
                #     item_joined =''
                #     new_item = row['SARG'].split('.')
                #     for item in new_item:
                #         a = str(int(item))
                #         item_joined +=a
                #         fdf.at[index,"SARG"]=int(item_joined)
                #         item_joined =''
                #         new_item = row['minAdmissionRequirement'].split('.')
                #         for item in new_item:
                #             a = str(int(item))
                #             item_joined +=a
                #         fdf.at[index,"minAdmissionRequirement"]=int(item_joined)
                x = fdf[['points', 'SAPG', 'SARG','Min Admition Point', 'minAdmissionRequirement','Capacity']]
                print(x)
                marks_model = model_path + '\Course Recomendation System.pkl'
                loaded_moddel = joblib.load(open(marks_model, 'rb'))
                marks = loaded_moddel.predict(x)
                marks = np.abs(marks)
            
                return JsonResponse({'data':marks})
    context = {'subjects_arr':subjects_arr}
    return render(request, 'RecommendationAndAnalysis/Srudent-course-recommendation.html', context)

def studentResults(request):
    try:
        if request.method == 'POST':
            subject = request.POST.get('subject')
        student_data = {'exam type':[],'marks':[]}
        studentInfo = Student.objects.filter(user= request.user).first()
        # studentInfo = Student.objects.filter(user__id__gt = 1).first()
        subjects = StudentSubject.objects.filter(student = studentInfo)
        for subject in subjects:
            student_marks = StudentExam.objects.filter(subject=subject).order_by('date_created')
            for st in student_marks:
                if st.status == 'EXAM END':

                    student_data['exam type'].append(st.exam.name + ' '+ st.date_created.year)
                    student_data['marks'].append(st.marks)
        print('present')
    except:
        sutentInfos = Student.objects.all()
        print('absent')
    return JsonResponse({'data':student_data})

def checking_task(request, task_recived):

    studentInfo = Student.objects.filter(user= request.user)
    if studentInfo.exists():
        user_log = UserLog.objects.filter(user=request.user)
        previous_date = user_log[0].date_created
        logs = {'task':[], 'user':[], 'date':[], 'difference':[]}
        for index, log in enumerate(user_log):
            task = log.task
            user = log.user.username
            current_time = log.date_created
            difference = current_time -previous_date
            logs['task'].append(task)
            logs['user'].append(user)
            logs['date'].append(current_time)
            logs['difference'].append(difference)
            previous_date =  current_time
        copy_list = logs['difference'][1:]
        first_item = logs['difference'][0]
        copy_list.append(first_item)
        logs['difference'] = copy_list
        data = pd.DataFrame(logs)
        data['date only'] =data['date'].dt.date
        data['day'] = data['date'].dt.day_name()
        student_logs = data[data['user'] == request.user.username]
        tutorials_time = data[data['task'] == task].groupby('date only').sum()
        tutorials_time_dayname = data[data['task'] == task].groupby('day').sum()
        task_dict = {'time_used_per_day':tutorials_time,'time_per_dayname':tutorials_time_dayname}
        return task_dict

def analyzingStudentFactorByMl(Request):
    student_dataset_url = settings.STATICFILES_DIRS[0] +r'\models\student marks.csv'
    data = pd.read_csv(student_dataset_url)
    class_mapping = {value:index for index, value in enumerate(data['subject'].unique())}
    data['subject']= data['subject'].map(class_mapping)
    class_mapping = {value:index for index, value in enumerate(data['exam_type'].unique())}
    data['exam_type']= data['exam_type'].map(class_mapping)
    class_mapping = {value:index for index, value in enumerate(data['exam_type'].unique())}
    data['exam_type']= data['exam_type'].map(class_mapping)
    data.drop('exam_type_markers', axis=1, inplace=True)
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    tree = DecisionTreeRegressor()
    tree.fit(x,y)
    dictt = pd.DataFrame(tree.feature_importances_)
    dictt.index = x.columns
    x_data = [i for i in x.columns]
    y_data = [i*100 for i in tree.feature_importances_]
    print(y_data)

    final_data_returned = {'x_data':x_data, 'y_data':y_data}
    return JsonResponse({'data':final_data_returned})


def student_reults_progress(request):

    try:
        studentInfo = Student.objects.filter(user= request.user).first()
        subjects = StudentSubject.objects.filter(student = studentInfo)
    except:
        subjects = Subject.objects.all()
    data_returned = checking_task(request=request, task_recived='viewing tutorial page')
    context = {'subjects':subjects}
    return render(request, 'RecommendationAndAnalysis/student results analysis.html', context)

def analyze_logs(request):
    data_returned = checking_task(request=request, task_recived='viewing tutorial page')
    # print(data_returned['time_used_per_day'].indax)
    date = [d for d in data_returned['time_used_per_day'].index]
    date_value = [d for d in data_returned['time_used_per_day'].difference]
    day = [d for d in data_returned['time_per_dayname'].index]
    day_value = [d for d in data_returned['time_per_dayname'].difference]
    final_data_returned = {'date':date, 'date_value':date_value, 'day':day, 'day_value':day_value}
    return JsonResponse({'data':final_data_returned})

def analyzing_studentPeformance(request, id):
    studentInfo = Student.objects.filter(user= request.user).first()
    subjects = StudentSubject.objects.filter(student = studentInfo).first()
    if id ==0:
        id = subjects.subject.id
    student_marks = StudentExam.objects.filter(subject__id__gt=id).order_by('date_created')
    x_data = [data.exam.name + '' + str(data.date_created.year) for data in student_marks]
    y_data = [data.marks for data in student_marks]
    final_data_returned = {'x_data':x_data, 'y_data':y_data}
    return JsonResponse({'data':final_data_returned})

def convert_html_to_pdf(request):
    # Fetch data from the database or any other source
    # For example, let's assume you have a model called 'Book' with a 'title' field
    student = Student.objects.filter(user = request.user).first()  # Fetch all student from the database

    # Get the HTML template
    template = get_template('PdfTemplates/student-centificates.html')
    context = {'student': student}  # Pass the data to the template context

    # Render the template with the context data
    html = template.render(context)

    # Create a PDF file-like object
    result = io.BytesIO()
    pdf = pisa.pisaDocument(
        io.BytesIO(html.encode('UTF-8')),
        result,
        encoding='UTF-8',
        link_callback=lambda uri, rel: staticfiles_storage.url(uri) if uri.startswith('/') else uri
    )
    # Check if PDF generation was successful
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response

    return HttpResponse('Error generating PDF')

def TopicRecommendations(request):
    context = {}
    if request.method == "POST":
        UserLog.objects.create(task='Viewing Making an Topic recommendations', user=request.user)
        subject_id = request.POST.get('subject')

        subject_obj = Subject.objects.filter(id = subject_id).first()
        student = Student.objects.filter(user=request.user).first()
        student_exams = StudentExam.objects.filter(student=student, subject = subject_obj, is_result_generated=True, is_submitted=True)
        
        if student_exams.exists():
            topic_dataset = {'subject': [], 'topic': [], 'mark scored': [], 'total marks': [], 'difference': []}
            for exam in student_exams:
                responses = StudentAnswer.objects.filter(studentExam=exam)
                if responses.exists():
                    for response in responses:
                        subject = response.studentExam.subject.subject_name
                        marks_scored = response.marks_scored
                        total_marks = response.generated_question.exam_format.gettingMarks
                        topic = response.generated_question.topic.name
                        difference = (marks_scored-total_marks)//100
                        
                        topic_dataset['subject'].append(subject)
                        topic_dataset['topic'].append(topic)
                        topic_dataset['mark scored'].append(marks_scored)
                        topic_dataset['total marks'].append(total_marks)
                        topic_dataset['difference'].append(difference)
                        
            data = pd.DataFrame(topic_dataset)
            grouped_data = data.groupby(['subject', 'topic']).sum()
            grouped_data = grouped_data.reset_index()  # Reset index for further processing
            
            # Find the subjects with the lowest marks
            lowest_subjects = grouped_data.groupby('subject')['difference'].sum().nsmallest(3).index.tolist()
            
            # Generate recommendations for the low-scoring topics
            recommendations = {}
            for subject in lowest_subjects:
                topics = grouped_data[grouped_data['subject'] == subject]['topic'].tolist()
                recommendations['topics'] = topics        
            context = {'recommendations': recommendations}
        return render(request, 'RecommendationAndAnalysis/student-topic-recommendation.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def StudentProgress(request):
    context ={}
    return render(request, 'RecommendationAndAnalysis/student-progress.html', context)
