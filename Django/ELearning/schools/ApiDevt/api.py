from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from django.contrib.auth.models import User, Group, Permission
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, UserLog
from schools.ApiDevt.serializers import TutorialTimeTackingSerializer
from datetime import datetime, timedelta
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
import os
import PyPDF2
import docx2txt
from fuzzywuzzy import fuzz
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
                notes_paths.append(settings.STATICFILES_DIRS[0] +book.file.url)
        if notes.exists():
            for note in notes:
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
                        ExaminationDump.objects.create(questions=qust, answers=answers, is_generated_Model=True, questionType=qntype, topic=topic)
                        print(' question generates sucessfully')
        if books.exists():
            for book in books:
                book.is_questions_exacted =True
                book.save()
        if notes.exists():
            for note in notes:
                note.is_questions_exacted =True
                note.save()
                
        return JsonResponse({'data':'data is generated sucessfully'})
    return JsonResponse({'data':''})


def generatingExams(request):
    student_exams = StudentExam.objects.all()
    if student_exams.exists():
    # Assuming `end_time` is a datetime object
        for student_examination in student_exams:
            status = True
            if student_examination.status == 'INITIAL PREPARATION':
                examinatingene =Generated_exam.objects.filter(exam_type=student_examination.exam)
                if examinatingene.exists():
                    exam_generated_previous = examinatingene.first()
                    if exam_generated_previous.status == 'Valid':
                        status = False
            if status:
                format_exam = ExamFormat.objects.filter(exam_type=student_examination.exam)
                studentClass = student_examination.student.classCurrent
                subjectClass_obj =SubjectClass.objects.filter(studentClass = studentClass, subject =student_examination.subject).first()
                topics =Topic.objects.filter(subject = subjectClass_obj)
                QuestionPerTopic = {'Essay':[], 'Short Note':[], 'fill the blanks':[], 'True':[], 'Match item':[], 'multiple_coice':[], 'Short Answers':[]}

                for topic in topics:
                    for format in format_exam:
                        dump_qns=ExaminationDump.objects.filter(topic =topic, questionType =format.type_questions)
                        if dump_qns.exists():
                            for dump_qn in dump_qns:
                                QuestionPerTopic[format.type_questions.name].append(dump_qn.id)
                question_number = 0
                for format in format_exam:
                    if question_number <=format.number_of_questions:
                        
                        try:
                            question_selected = random.choice(QuestionPerTopic[format.type_questions.name])
                            generated_question_fromDump=ExaminationDump.objects.filter(id = question_selected).first()
                            Generated_exam.objects.create(question =generated_question_fromDump.questions, answers=generated_question_fromDump.answers, examination_identity = student_examination.examination_identity, is_generated = True, subject= student_examination.subject, topic = generated_question_fromDump.topic, exam_format =format, exam_type =student_examination.exam)
                        except:
                            pass
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
        exam_type = ExamType.objects.filter(studentClass = classCurrent).first()
        subjects = StudentSubject.objects.filter(student = studentInfo)
        grade = Grade.objects.filter(level=studentInfo.classCurrent.level)
        if subjects.exists():
            for subject in subjects:
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
                    print('ok')
        return JsonResponse({'data':'data is generated sucessfully'})
    return JsonResponse({'data':''})

def UpdateQuestionGeneratedCheckBox(request, id):
    Unverified_questions = ExaminationDump.objects.filter(id = id).first()
    Unverified_questions.is_generated_Model =  False
    Unverified_questions.save()
    return JsonResponse({'data':'data is generated sucessfully'})

# # @receiver(post_save, sender='schools.UserLog')
# def generating_exam_appointment(request):
#     #generating exam
#     exam_type = ExamType.objects.all()
#     for examty in exam_type:
#         exam_exists = False
#         exam_exist = Generated_exam.objects.filter(exam_type=examty)
#         if exam_exist.exists():
#             for exam in exam_exist:
#                 if exam.getting_academic_Year == datetime.datetime.now().year:
#                     exam_exists = True

#         if not exam_exists:
#             subjects = Subject.objects.all()
#             for subject in subjects:
#                 st_exam = StudentExam.objects.filter(exam = examty).first()
#                 exam_type = ExamType.objects.filter(name = examty.name).first()
#                 format_exam =ExamFormat.objects.filter(exam_type = exam_type, subject=subject)

#                 exam_generated = []
#                 for forma in format_exam:
#                     print('format present')
#                     sections = {'questions':[],'format':'', 'answers':[] }
#                     notes_paths = []
#                     books = Book.objects.filter(subject = forma.subject)
#                     notes = Notes.objects.filter(subject = forma.subject)
#                     if books.exists():
#                         print('book exist')
#                         for book in books:
#                             notes_paths.append(settings.STATICFILES_DIRS[0] +book.file.url)
#                     if notes.exists():
#                         for note in notes:
#                             notes_paths.append(settings.STATICFILES_DIRS[0] +note.file.url)
#                     print(notes_paths)
#                     path = notes_paths
#                     hist = ExamGerator(forma.subject.subject_name, path)
#                     doc =hist.doc_opening()
#                     taging = hist.chicking_doc_tags()
#                     questions, answers= hist.generate_exams(forma.type_questions.name, forma.type_questions.number_of_questions)
#                     sections['format']= forma
#                     print(questions)
#                     for index, qust in enumerate(questions):
#                         sections['questions'].append(qust)
#                         sections['answers'].append(answers[index])
#                     sections['questions']= list(set(sections['questions']))[:forma.type_questions.number_of_questions]
#                     exam_generated.append(sections)
#                     print('the generated exam id')
#                     print(exam_generated)
#                 for exm in exam_generated:
#                     exam_format =exm['format']
#                     for index, quest in enumerate(exm['questions']):
#                         question = quest
#                         answer = ''
#                         try:
#                             answer = exm['answers'][index]
#                         except:
#                             answer = ''
#                         Generated_exam.objects.create(question= question, answers =answer, is_generated = True, subject =subject, exam_format=exam_format, exam_type=exam_type )
#                         print('data sent to database sucessfully')
#     #making student promotions
#     students = Student.objects.all()
#     for studentInfo in students:

#         promotion = False
#         subjects_pass_arr = []
#         # studentInfo = Student.objects.filter(user= kwargs['instance'].user).first()
#         classCurrent = studentInfo.classCurrent
#         exam_type = ExamType.objects.filter(studentClass = classCurrent).first()
#         subjects = StudentSubject.objects.filter(student = studentInfo)
#         grade = Grade.objects.filter(level=studentInfo.classCurrent.level)
#         if subjects.exists():
#             for subject in subjects:
#                 # print(subject.subject.subject_name)
#                 continue_excusion = False
#                 subjects_pass_status = 0
#                 exam = StudentExam.objects.filter(subject = subject.subject, exam= exam_type).order_by('date_created')
#                 if exam.exists():
#                     points_exam = results.getting_points(grades=grade, marks=[exam[0].marks, exam[0].marks])
#                     marks_grade =points_exam['grade'][0]
#                     if studentInfo.classCurrent.level.name == 'A-Level':
#                         if marks_grade <= 'D':
#                             continue_excusion = True
#                     else:
#                         if marks_grade <= 'C':
#                             continue_excusion = True

#                     if continue_excusion:
#                         assigments =AssigmentSubmission.objects.filter(subject=subject.subject, user=studentInfo.user)
#                         student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
#                         no_group_work = 0
#                         if student_group:
#                             group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group)
#                             no_group_work +=group_assigments.count()
#                         all_assigments = Assigment.objects.filter(subject=subject.subject).count()
#                         no_assigments = no_group_work + assigments.count()

#                         final_percentage = 0
#                         Tutorial_learning_pecentage = 0
#                         Tutorial_learning_arr = []
#                         tutorials = Tutorial.objects.filter(subject = subject.subject)
#                         video_tracking = TutorialTimeTacking.objects.filter(user = studentInfo.user)
#                         for tutorial in tutorials:
#                             for tr_tutorials in video_tracking:
#                                 if tr_tutorials.tutorial == tutorial:
#                                     Tutorial_learning_arr.append(tr_tutorials.video_complition_percentage)
#                         try:
#                             Tutorial_learning_pecentage  = sum(Tutorial_learning_arr)/tutorials.count()
#                         except:
#                             pass

#                         try:
#                             final_percentage = (no_assigments/all_assigments)*100
#                         except ZeroDivisionError:
#                             final_percentage = 0
#                         # print(final_percentage)
#                         if final_percentage>=0:
#                             if student_group:
#                                 assigment_submitted = AssigmentSubmission.objects.filter(Q(group =student_group.group) | Q(user= studentInfo.user))
#                                 if assigment_submitted.exists():
#                                     assigment_marks = [ass.marks*ass.assigniment.Weight for ass in assigment_submitted]
#                                     total_marks_scored = sum(assigment_marks)
#                                     all_assigments = Assigment.objects.filter(subject=subject.subject)
#                                     total_assigments = [ass.Weight**2 for ass in all_assigments]
#                                     try:
#                                         total_marks = (total_marks_scored/sum(total_assigments))*100

#                                     except:
#                                         total_marks = 0
#                                     if total_marks>80 or Tutorial_learning_pecentage >80:
#                                         subjects_pass_status = 1

#                                     if total_marks>60 and Tutorial_learning_pecentage >70:
#                                         subjects_pass_status = 1
#                 subjects_pass_arr.append(subjects_pass_status)

#             passed_subject = sum(subjects_pass_arr)
#             print(subjects.count())
#             if passed_subject == subjects.count()/2:
#                 promotion  = True

#             if promotion:
#                 StudentClassManyToMany.objects.create(classCurrent = studentInfo.classCurrent,student = studentInfo)
#                 if not classCurrent.get_final_class:
#                     next_class_id = classCurrent.id+1
#                     next_class = StudentClass.objects.filter(id = next_class_id)
#                     studentInfo.classCurrent = next_class
#                     studentInfo.save()
#         return JsonResponse({'data':'data is generated sucessfully'})
#     return JsonResponse({'data':''})

