from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
import joblib
import pandas as pd
from django.contrib.auth.models import User, Group, Permission
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, UserLog
from schools.ApiDevt.serializers import TutorialTimeTackingSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking
from OnlineExamination.ExamGenerator.exam_generator import ExamGerator
from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult, Generated_exam, ExaminationDump
from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking
from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult, Generated_exam
from OnlineExamination.ExamsDoc import results, timetable
from OnlineExamination.ExamGenerator.exam_generator import ExamGerator
from schools.models import Department, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass
from django.db.models import Q
import random
import datetime
from RecommendationAndAnalysis.views import checking_task
from OnlineLearning.sms import SendSMS

# Create your views here.
def ShowUserApi(request):
    user = request.user
    return JsonResponse({'data':user})

def GettingSubject(request, id):
    dataset = []
    obj= Subject.objects.filter(id = id).first()
    
    dataset.append(obj.subject_name)

    return JsonResponse({'data':dataset})


def tracking(request, tuid, time, full_length):
    dataset = []
    if float(time)>=1:
        user = request.user
        tutorial = Tutorial.objects.filter(id = tuid).first()
        obj_exist = TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial).exists()
        if obj_exist:
            obj= TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial).first()

            if float(obj.time) < float(time):
                obj.time = time
                obj.save()
        else:
            TutorialTimeTacking.objects.create(time = time, full_length = full_length, user = user, tutorial = tutorial)
        obj= TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial)
        for i in obj:
            arr = [i.time, i.user.username, i.tutorial.id]
            dataset.append(arr)

    return JsonResponse({'data':dataset})

def GettingTutorialBsedOnUser(request):
    dataset = []
    obj= TutorialTimeTacking.objects.filter(user = request.user)
    if obj.exists():
        for i in obj:
            arr = [i.time, i.user.username, i.tutorial.id]
            dataset.append(arr)

    return JsonResponse({'data':dataset})

def ExamNotification(request):
    st_exam = StudentExam.objects.filter(is_notified = False)
    if st_exam.exists():
        for exam in st_exam:
            if exam.status == 'INITIAL PREPARATION':
                phnone_number = exam.phone_number
                name = exam.name.split(' ')[0]
                message =f"Dear {name} Examination {exam.subject.subject_name} of has been started please login to your account"
                sms = SendSMS()
                sms.sending(message=message, phone_number=phnone_number)
                exam.is_notified = True
                exam.save()
        return JsonResponse({'data':'data is generated sucessfully'})
    return JsonResponse({'data':''})

def generatingQuestions(request):
    topics = Topic.objects.all()
    for topic in topics:
        notes_paths = []
        questiontype = QuestionsType.objects.all()
        notes = Notes.objects.filter(topic = topic, is_questions_exacted = False)
        books = Book.objects.filter(topic = topic, is_questions_exacted = False)
        if books.exists():
            for book in books:
                book.is_questions_exacted =True
                book.save()
                notes_paths.append(settings.STATICFILES_DIRS[0] +book.file.url)
        if notes.exists():
            for note in notes:
                note.is_questions_exacted =True
                note.save()
                notes_paths.append(settings.STATICFILES_DIRS[0] +note.file.url)
        if len(notes_paths)>0:
            path = notes_paths
            hist = ExamGerator(path)
            doc =hist.doc_opening()
            taging = hist.chicking_doc_tags()
            for qntype in questiontype:
                questions, answers= hist.generate_exams(qntype.name)
                for index, qust in enumerate(questions):
                    if qust != '':
                        ExaminationDump.objects.get_or_create(questions=qust, answers=answers[index], is_generated_Model=True, questionType=qntype, topic=topic)
                        print(' question generates sucessfully')
                
        return JsonResponse({'data':'data is generated sucessfully'})
    return JsonResponse({'data':''})


def fakeGenerator(request):
    SubjectClasses =SubjectClass.objects.all()
    for subjClass in SubjectClasses:
        topics = Topic.objects.filter(subject = subjClass)
        if topics.exists():
            for topic in topics:
                questionsList = ExaminationDump.objects.filter(topic = topic, is_generated_Model = False)
                students = Student.objects.filter(classCurrent = subjClass.studentClass)
                status = True
                for student in students:    
                    student_exams = StudentExam.objects.filter(student = student)
                    for student_examination in student_exams:
                        status = Generated_exam.objects.filter(examination_identity = student_examination.examination_identity).exists()
                        format_exam = ExamFormat.objects.filter(exam_type=student_examination.exam)

                        if student_examination.status == 'INITIAL PREPARATION' or student_examination.status == "PENDING":
                            examinatingene =Generated_exam.objects.filter(exam_type=student_examination.exam)
                            if examinatingene.exists():
                                exam_generated_previous = examinatingene.first()
                                if exam_generated_previous.status == 'Invalid':
                                    status = False
                                    
                        if status:
                            i = 0
                            if questionsList:
                                previous = []
                                random_qn = random.choice(questionsList)
                                questionType = random_qn.questionType.name
                                random_number = random_qn.questionType.number_of_questions
                                if questionType not in previous:
                                    
                                    for i in range(random_number):
                                        random_qn = random.choice(questionsList)
                                        format_exam_obj = ExamFormat.objects.filter(type_questions = random_qn.questionType).first()
                                        generated_question_fromDump=ExaminationDump.objects.filter(id = random_qn.id).first()
                                        Generated_exam.objects.create(question =generated_question_fromDump.questions, answers=generated_question_fromDump.answers, examination_identity = student_examination.examination_identity, is_generated = True, subject= student_examination.subject, topic = generated_question_fromDump.topic, exam_format =format_exam_obj, exam_type =student_examination.exam)
                                        previous.append(questionType)
                                
    return JsonResponse({'data':''})

def StudentPromotin(request):
      #making student promotions
    students = Student.objects.all()
    for studentInfo in students:
        promotion = False
        subjects_pass_arr = []
        print('promoting student')
        # studentInfo = Student.objects.filter(user= kwargs['instance'].user).first()
        classCurrent = studentInfo.classCurrent
        exam_types = ExamType.objects.filter(studentClass = classCurrent)
        subjects = StudentSubject.objects.filter(student = studentInfo)
        grade = Grade.objects.filter(level=studentInfo.classCurrent.level)
        if subjects.exists():
            for subject in subjects:
                for exam_type in exam_types:
                # print(subject.subject.subject_name)
                    continue_excusion = False
                    subjects_pass_status = 0
                    exam = StudentExam.objects.filter(subject = subject.subject, exam= exam_type).order_by('date_created')
                    if exam.exists():
                        points_exam = results.getting_points(grades=grade, marks=[exam[0].marks, exam[0].marks])
                        marks_grade =points_exam['grade'][0]
                        if studentInfo.classCurrent.level.name == 'A-Level':
                            if marks_grade <= 'D':
                                continue_excusion = True
                        else:
                            if marks_grade <= 'C':
                                continue_excusion = True

                        if continue_excusion:
                            assigments =AssigmentSubmission.objects.filter(subject=subject.subject, user=studentInfo.user)
                            student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
                            no_group_work = 0
                            if student_group:
                                group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group)
                                no_group_work +=group_assigments.count()
                            all_assigments = Assigment.objects.filter(subject=subject.subject).count()
                            no_assigments = no_group_work + assigments.count()

                            final_percentage = 0
                            Tutorial_learning_pecentage = 0
                            Tutorial_learning_arr = []
                            tutorials = Tutorial.objects.filter(subject = subject.subject)
                            video_tracking = TutorialTimeTacking.objects.filter(user = studentInfo.user)
                            for tutorial in tutorials:
                                for tr_tutorials in video_tracking:
                                    if tr_tutorials.tutorial == tutorial:
                                        Tutorial_learning_arr.append(tr_tutorials.video_complition_percentage)
                            try:
                                Tutorial_learning_pecentage  = sum(Tutorial_learning_arr)/tutorials.count()
                            except:
                                pass

                            try:
                                final_percentage = (no_assigments/all_assigments)*100
                            except ZeroDivisionError:
                                final_percentage = 0
                            # print(final_percentage)
                            if final_percentage>=0:
                                if student_group:
                                    assigment_submitted = AssigmentSubmission.objects.filter(Q(group =student_group.group) | Q(user= studentInfo.user))
                                    if assigment_submitted.exists():
                                        assigment_marks = [ass.marks*ass.assigniment.Weight for ass in assigment_submitted]
                                        total_marks_scored = sum(assigment_marks)
                                        all_assigments = Assigment.objects.filter(subject=subject.subject)
                                        total_assigments = [ass.Weight**2 for ass in all_assigments]
                                        try:
                                            total_marks = (total_marks_scored/sum(total_assigments))*100

                                        except:
                                            total_marks = 0
                                        if total_marks>80 or Tutorial_learning_pecentage >80:
                                            subjects_pass_status = 1

                                        if total_marks>60 and Tutorial_learning_pecentage >70:
                                            subjects_pass_status = 1
                    subjects_pass_arr.append(subjects_pass_status)

            passed_subject = sum(subjects_pass_arr)
            print(subjects.count())
            if passed_subject == subjects.count()/2:
                promotion  = True

            if promotion:
                StudentClassManyToMany.objects.create(classCurrent = studentInfo.classCurrent,student = studentInfo)
                if not classCurrent.get_final_class:
                    next_class_id = classCurrent.id+1
                    next_class = StudentClass.objects.filter(id = next_class_id)
                    studentInfo.classCurrent = next_class
                    studentInfo.save()
        return JsonResponse({'data':'data is generated sucessfully'})
    return JsonResponse({'data':''})

def UpdateQuestionGeneratedCheckBox(request, id):
    Unverified_questions = ExaminationDump.objects.filter(id = id).first()
    Unverified_questions.is_generated_Model =  False
    Unverified_questions.save()
    return JsonResponse({'data':'data is generated sucessfully'})

def training_model_marks_prediction(request):
    student_exams = StudentExam.objects.filter(is_verified = True)
    student_details = {'subject':[], 'exam_type':[], 'class':[],
        'hours_of_studying':[], 'participation_in_group':[], 'group_parlagrims':[],
        'individual_paralligms':[], 'assigments_individual':[], 'assigments_group':[],
        'previous_marks':[], 'panctuality':[], 'Predicted Marks':[]}
       
    for student_exam in student_exams:
        student = Student.objects.filter(user = request.user)
        if student.exists():
            studentInfo = student.first()
            subjects = StudentSubject.objects.filter(student = studentInfo)
            for subject in subjects:
                panctuality_arr = []
                panctuality = 0
                individual_paralligms_all = 0
                total_pallagirsm_group = 0
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
                pallarism_individual_arr = [ass.parlagrims**2 for ass in all_assigments]
                try:
                    individual_paralligms_all = sum(pallarism_individual_arr)/len(pallarism_individual_arr)
                except:
                    pass
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
            student_exams = StudentExam.objects.filter(student =studentInfo, subject = subject.subject).order_by('date_created')
            if student_exams.exists():
                previous_marks = student_exams.first().marks
            else:
                previous_marks = 50
                group_assigments = []
                if StudentGroupManyToMany.objects.filter(student = studentInfo).exists():

                    student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
                    group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group, assigniment__type__name__gt = 'Group')
                    all_assigments_gr = Assigment.objects.filter(subject=subject.subject, type__name__gt = 'Group')
                    weights_for_group = [ass.marks*ass.assigniment.Weight for ass in group_assigments]
                    total_weigths_submited_assiments_for_group = sum(weights_for_group)
                    all_assigments_arr_gr= [ass.Weight**2 for ass in all_assigments]
                    total_weights_group = sum(all_assigments_arr_gr)
                    pallarism_group_arr = [ass.parlagrims**2 for ass in all_assigments]
                    try:
                        total_pallagirsm_group = sum(pallarism_group_arr)/len(pallarism_group_arr)
                    except:
                        pass
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
                    
                    student_exams = StudentExam.objects.filter(student =studentInfo, subject = subject).order_by('date_created')
                    if student_exams.exists():
                        previous_marks = student_exams.first().marks
                    else:
                        previous_marks = 50
                        
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

                individual_paralligms = individual_paralligms_all
                group_parlagrims = total_pallagirsm_group
                student_details['subject'].append(subject.subject.id)
                student_details['exam_type'].append(student_exam.exam.id)
                student_details['class'].append(studentInfo.classCurrent.id)
                student_details['hours_of_studying'].append(hours_studying)
                student_details['participation_in_group'].append(partipation)
                student_details['assigments_individual'].append(individual_assigment)
                student_details['assigments_group'].append(group_assigment)
                student_details['previous_marks'].append(previous_marks)
                student_details['panctuality'].append(panctuality)
                student_details['group_parlagrims'].append(group_parlagrims)
                student_details['individual_paralligms'].append(individual_paralligms)
                student_details['Predicted Marks'].append(student_exam.marks)
    model_path = settings.STATICFILES_DIRS[0] +r'\models'
    marks_model = model_path + '\studentmarks.pkl'
    csv_file = settings.STATICFILES_DIRS[0] +r'\models\student marks.csv'
    df1 = pd.DataFrame(student_details)
    df2 = pd.read_csv(csv_file)
    frames = [df1, df2]
    data = pd.concat(frames)
    data.to_csv(csv_file, index=False)
    data  = data.dropna()
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    tree = DecisionTreeRegressor()
    tree.fit(x,y)

    joblib.dump(tree, open(marks_model, 'wb'))
    return JsonResponse({'data':'model trained sucessfully'})


def studentAnalysisByExam(request, id):
    exam_type_obj = ExamType.objects.filter(id = id).first()
    student_exams = StudentExam.objects.filter(is_verified = True, exam = exam_type_obj)
    student_details = {'subject':[], 'exam_type':[], 'class':[],
        'hours_of_studying':[], 'participation_in_group':[], 'group_parlagrims':[],
        'individual_paralligms':[], 'assigments_individual':[], 'assigments_group':[],
        'previous_marks':[], 'panctuality':[], 'Predicted Marks':[]}
       
    for student_exam in student_exams:
        student = Student.objects.filter(user = request.user)
        if student.exists():
            studentInfo = student.first()
            subjects = StudentSubject.objects.filter(student = studentInfo)
            for subject in subjects:
                panctuality_arr = []
                panctuality = 0
                individual_paralligms_all = 0
                total_pallagirsm_group = 0
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
                pallarism_individual_arr = [ass.parlagrims**2 for ass in all_assigments]
                try:
                    individual_paralligms_all = sum(pallarism_individual_arr)/len(pallarism_individual_arr)
                except:
                    pass
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
            student_exams = StudentExam.objects.filter(student =studentInfo, subject = subject.subject).order_by('date_created')
            if student_exams.exists():
                previous_marks = student_exams.first().marks
            else:
                previous_marks = 50
                group_assigments = []
                if StudentGroupManyToMany.objects.filter(student = studentInfo).exists():

                    student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
                    group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group, assigniment__type__name__gt = 'Group')
                    all_assigments_gr = Assigment.objects.filter(subject=subject.subject, type__name__gt = 'Group')
                    weights_for_group = [ass.marks*ass.assigniment.Weight for ass in group_assigments]
                    total_weigths_submited_assiments_for_group = sum(weights_for_group)
                    all_assigments_arr_gr= [ass.Weight**2 for ass in all_assigments]
                    total_weights_group = sum(all_assigments_arr_gr)
                    pallarism_group_arr = [ass.parlagrims**2 for ass in all_assigments]
                    try:
                        total_pallagirsm_group = sum(pallarism_group_arr)/len(pallarism_group_arr)
                    except:
                        pass
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
                    
                    student_exams = StudentExam.objects.filter(student =studentInfo, subject = subject).order_by('date_created')
                    if student_exams.exists():
                        previous_marks = student_exams.first().marks
                    else:
                        previous_marks = 50
                        
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

                individual_paralligms = individual_paralligms_all
                group_parlagrims = total_pallagirsm_group
                student_details['subject'].append(subject.subject.id)
                student_details['exam_type'].append(student_exam.exam.id)
                student_details['class'].append(studentInfo.classCurrent.id)
                student_details['hours_of_studying'].append(hours_studying)
                student_details['participation_in_group'].append(partipation)
                student_details['assigments_individual'].append(individual_assigment)
                student_details['assigments_group'].append(group_assigment)
                student_details['previous_marks'].append(previous_marks)
                student_details['panctuality'].append(panctuality)
                student_details['group_parlagrims'].append(group_parlagrims)
                student_details['individual_paralligms'].append(individual_paralligms)
                student_details['Predicted Marks'].append(student_exam.marks)
    # csv_file = settings.STATICFILES_DIRS[0] +r'\models\student marks.csv'
    data = pd.DataFrame(student_details)
    data  = data.dropna()
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    tree = DecisionTreeRegressor()
    tree.fit(x,y)
    dictt = pd.DataFrame(tree.feature_importances_)
    dictt.index = x.columns
    x_data = [i for i in x.columns]
    y_data = [i*100 for i in tree.feature_importances_]

    final_data_returned = {'x_data':x_data, 'y_data':y_data}
    return JsonResponse({'data':final_data_returned})

def examinationMarking(request):
    student_exam = StudentExam.objects.filter(is_submitted = 1, is_verified = False)
    if student_exam.exists():
        print('oo')