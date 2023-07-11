from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult, Generated_exam, ExaminationDump, StudentAnswer
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass, UserLog
from OnlineLearning.models import Student, StudentSubject, Teacher, Topic
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from OnlineExamination.ExamsDoc import results, timetable
from OnlineExamination.ExamGenerator.exam_generator import ExamGerator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from django.template.defaultfilters import date
from RecommendationAndAnalysis.views import *
import cv2
from datetime import datetime


def studentVerification(request):
    return render(request, 'OnlineExamination/student-verification.html')

@login_required(login_url='/')
def gradeList(request):
    Grades = Grade.objects.all()
    levels = SchoolLevel.objects.all()
    context = {'levels': levels, 'Grades': Grades}
    UserLog.objects.create(task='Viewing Grade List', user=request.user)
    return render(request, 'OnlineExamination/gradeList.html', context)


@login_required(login_url='/')
def gradeAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_marks = request.POST.get('lower_marks')
        upper_marks = request.POST.get('upper_marks')
        weight = request.POST.get('weight')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id=level).first()
        Grade.objects.create(name=name, lower_marks=lower_marks, upper_marks=upper_marks,
                             weight=weight, description=description, level=level_obj)
        messages.success(request, 'grade added successful')
        UserLog.objects.create(task='Add Grade', user=request.user)
        return redirect('gradeList')

    levels = SchoolLevel.objects.all()
    context = {'levels': levels}
    return render(request, 'OnlineExamination/Add-Grades.html', context)


@login_required(login_url='/')
def gradeEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_marks = request.POST.get('lower_marks')
        upper_marks = request.POST.get('upper_marks')
        weight = request.POST.get('weight')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id=level).first()
        grade = Grade.objects.filter(id=id).first()
        grade.name = name
        grade.lower_marks = lower_marks
        grade.upper_marks = upper_marks
        grade.weight = weight
        grade.description = description
        grade.level = level_obj
        grade.save()
        messages.success(request, 'grade updated successful')
        UserLog.objects.create(task='Edit Grade', user=request.user)
        return redirect('gradeList')


@login_required(login_url='/')
def gradeDelete(request, id):
    grade = Grade.objects.filter(id=id).first()
    grade.delete()
    messages.success(request, 'grade deleted successful')
    UserLog.objects.create(task='Delete Grade', user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def divisionList(request):
    divisions = Division.objects.all()
    levels = SchoolLevel.objects.all()
    context = {'levels': levels, 'divisions': divisions}
    UserLog.objects.create(task='Viewing Division List', user=request.user)
    return render(request, 'OnlineExamination/divisionList.html', context)


@login_required(login_url='/')
def divisionAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_point = request.POST.get('lower_point')
        upper_point = request.POST.get('upper_point')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id=level).first()
        Division.objects.create(name=name, lower_point=lower_point,
                                upper_point=upper_point, description=description, level=level_obj)
        messages.success(request, 'division added successful')
        UserLog.objects.create(task='Add Division', user=request.user)
        return redirect('divisionList')

    levels = SchoolLevel.objects.all()
    context = {'levels': levels}
    return render(request, 'OnlineExamination/Add-Divisions.html', context)


@login_required(login_url='/')
def divisionEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_point = request.POST.get('lower_point')
        upper_point = request.POST.get('upper_point')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id=level).first()
        division = Division.objects.filter(id=id).first()
        division.name = name
        division.lower_point = lower_point
        division.upper_point = upper_point
        division.description = description
        division.level = level_obj
        division.save()
        messages.success(request, 'division updated successful')
        UserLog.objects.create(task='Edit Division', user=request.user)

        return redirect('divisionList')
    return redirect('divisionList')


@login_required(login_url='/')
def divisionDelete(request, id):
    division = Division.objects.filter(id=id).first()
    division.delete()
    messages.success(request, 'division deleted successful')
    UserLog.objects.create(task='Delete Division', user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def examTypeList(request):
    examtypes = ExamType.objects.all()
    studentClass = StudentClass.objects.all()
    context = {'examtypes': examtypes, 'studentClass': studentClass}
    UserLog.objects.create(task='Viewing Examination Types', user=request.user)

    return render(request, 'OnlineExamination/examTypeList.html', context)


@login_required(login_url='/')
def examTypeAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        weight_annual = request.POST.get('weight_annual')
        weight_final = request.POST.get('weight_final')
        studentClass = request.POST.get('studentClass')
        class_obj = StudentClass.objects.filter(id=studentClass).first()
        examType = ExamType.objects.create(
            name=name, weight_annual=weight_annual, weight_final=weight_final, studentClass=class_obj)
        messages.success(request, 'exam type aded successful')
        UserLog.objects.create(task='Add Examination Type', user=request.user)
        return redirect('examTypeList')

    studentClass = StudentClass.objects.all()
    context = {'studentClass': studentClass}
    return render(request, 'OnlineExamination/Add-examType.html', context)


@login_required(login_url='/')
def examTypeEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        weight_annual = request.POST.get('weight_annual')
        weight_final = request.POST.get('weight_final')
        studentClass = request.POST.get('studentClass')
        class_obj = StudentClass.objects.filter(id=studentClass).first()
        examType = ExamType.objects.filter(id=id).first()
        examType.name = name
        examType.weight_annual = weight_annual
        examType.weight_final = weight_final
        examType.studentClass = class_obj
        examType.save()
        messages.success(request, 'exam type updated successful')
        UserLog.objects.create(task='Edit Examination type', user=request.user)

        return redirect('examTypeList')
    return redirect('examTypeList')


@login_required(login_url='/')
def examTypeDelete(request, id):
    examType = ExamType.objects.filter(id=id).first()
    examType.delete()
    messages.success(request, 'exam type deletef successful')
    UserLog.objects.create(task='Delete Examination type', user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def QuestionsTypeList(request):
    questions_type = ['Essay', 'Short Note', 'fill the blanks',
                      'True', 'Match item', 'multiple_coice', 'Short Answers']
    for question_type in questions_type:
        checking_qn_existance = QuestionsType.objects.filter(
            name=question_type).exists()
        if not checking_qn_existance:
            number_of_questions = 0
            if question_type == 'Essay':
                number_of_questions = 1
            elif question_type == 'Short Note':
                number_of_questions = 5
            else:
                number_of_questions = 10

            QuestionsType.objects.create(
                name=question_type, number_of_questions=number_of_questions)

    QuestionsTypes = QuestionsType.objects.all()
    context = {'QuestionsTypes': QuestionsTypes}
    UserLog.objects.create(task='Viewing Question Types', user=request.user)
    return render(request, 'OnlineExamination/QuestionsTypeList.html', context)


@login_required(login_url='/')
def QuestionsTypeAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        number_of_questions = request.POST.get('number_of_questions')
        type_questions = QuestionsType.objects.create(
            name=name, number_of_questions=number_of_questions, weight=weight)
        messages.success(request, 'Question type added successful')
        UserLog.objects.create(task='adding Question Types', user=request.user)
        return redirect('QuestionsTypeList')

    return render(request, 'OnlineExamination/Add-QuestionsType.html')


@login_required(login_url='/')
def QuestionsTypeEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        number_of_questions = request.POST.get('number_of_questions')
        type_questions = QuestionsType.objects.filter(id=id).first()
        type_questions.name = name
        type_questions.number_of_questions = number_of_questions
        type_questions.weight = weight
        type_questions.save()
        messages.success(request, 'Question type updated successful')
        UserLog.objects.create(task='Edit Question Types', user=request.user)
        return redirect('QuestionsTypeList')

    return redirect('QuestionsTypeList')


@login_required(login_url='/')
def QuestionsTypeDelete(request, id):
    QuestionsTypes = QuestionsType.objects.filter(id=id).first()
    QuestionsTypes.delete()
    messages.success(request, 'Question type deleted successful')
    UserLog.objects.create(task='Delete Question Types', user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def examFormatList(request):
    examFormats = ExamFormat.objects.all()
    type_questions = QuestionsType.objects.all()
    subject = Subject.objects.all()
    examTpe = ExamType.objects.all()
    context = {'type_questions': type_questions, 'examTpe': examTpe,
               'subject': subject, 'examFormats': examFormats}
    UserLog.objects.create(
        task='Viewing Examination Format List', user=request.user)
    return render(request, 'OnlineExamination/examFormatList.html', context)


@login_required(login_url='/')
def examFormatAdd(request):
    if request.method == "POST":
        section = request.POST.get('section')
        weight = request.POST.get('weight')
        number_of_questions = request.POST.get('number_of_questions')
        type_questions_id = request.POST.get('type_questions')
        subject_id = request.POST.get('subject')
        exam_type_id = request.POST.get('exam_type')
        type_questions = QuestionsType.objects.filter(
            id=type_questions_id).first()
        subject = Subject.objects.filter(id=subject_id).first()
        exam_type = ExamType.objects.filter(id=exam_type_id).first()
        examFormat = ExamFormat.objects.create(section=section, weight=weight, number_of_questions=number_of_questions,
                                               exam_type=exam_type, type_questions=type_questions, subject=subject)
        messages.success(request, 'exam format added deleted successful')
        UserLog.objects.create(
            task='adding Examination Format', user=request.user)
        return redirect('examFormatList')

    type_questions = QuestionsType.objects.all()
    subject = Subject.objects.all()
    examTpe = ExamType.objects.all()
    context = {'type_questions': type_questions,
               'examTpe': examTpe, 'subject': subject}
    return render(request, 'OnlineExamination/Add-examFormat.html', context)


@login_required(login_url='/')
def examFormatEdit(request, id):
    if request.method == "POST":
        section = request.POST.get('section')
        weight = request.POST.get('weight')
        number_of_questions = request.POST.get('number_of_questions')
        type_questions_id = request.POST.get('type_questions')
        subject_id = request.POST.get('subject')
        exam_type_id = request.POST.get('exam_type')
        subject = Subject.objects.filter(id=subject_id).first()
        exam_type = ExamType.objects.filter(id=exam_type_id).first()
        type_questions = QuestionsType.objects.filter(
            id=type_questions_id).first()
        type_questions = ExamFormat.objects.filter(id=id).first()
        type_questions.section = section
        type_questions.weight = weight
        type_questions.number_of_questions = number_of_questions
        type_questions.exam_type = exam_type
        type_questions.subject = subject
        type_questions.save()
        UserLog.objects.create(
            task='Editing Examination Format', user=request.user)
        return redirect('examFormatList')
    messages.success(request, 'exam format updated successful')
    return redirect('examFormatList')


@login_required(login_url='/')
def examFormatDelete(request, id):
    UserLog.objects.create(
        task='Deleting Examination Format', user=request.user)
    examFormat = ExamFormat.objects.filter(id=id).first()
    examFormat.delete()
    messages.success(request, 'exam format deleted successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def MakeApointmentAdd(request):
    if request.method == "POST":
        UserLog.objects.create(task='Viewing Making an Appointment', user=request.user)
        email = request.POST.get('email')
        phone_number_withoutCountry = request.POST.get('phone_number')
        registration_number = request.POST.get('registration_number')
        date = request.POST.get('date')
        exam_type_id = request.POST.get('exam_type')
        codeField = request.POST.get('codeField')
        date_object = datetime.strptime(date, '%Y-%m-%d')

        unique_value = 0
        if str(phone_number_withoutCountry)[0] == '0':
            phone_number_withoutCountry = phone_number_withoutCountry[1:]

        phone_number =str(codeField) + phone_number_withoutCountry
        exam_type = ExamType.objects.filter(id=exam_type_id).first()
        appointment = False
        user_id = request.user.id
        user = User.objects.filter(id=user_id).first()
        student_info = Student.objects.filter(user=user).first()
        grade = Grade.objects.filter(level = student_info.classCurrent.level)
        student_exam_info = StudentExam.objects.filter(student=student_info, exam=exam_type)
        if student_exam_info.exists():
            if student_exam_info.first().student.classCurrent == student_info.classCurrent:
                appointment = True
                
        
        date_formated = datetime.strptime(f'{date}', '%Y-%m-%d')
        # appointment = StudentExam.objects.filter(student=student_info, exam=exam_type).delete()
        if not appointment:
            if user.email == email:
                if student_info.registration_no == registration_number:
                    student_exams = StudentExam.objects.filter(exam=exam_type)
                    if student_exams.exists():
                        for student_exam in student_exams:
                            muximun_time = datetime.combine(student_exam.date_of_exam, student_exam.start_time) + timedelta(days = 15)
                            user_appointment_date = datetime.combine(date_object, student_exam.start_time)
                            if user_appointment_date <muximun_time and student_exam.student.classCurrent == student_info.classCurrent:
                                unique_value = student_exam.examination_identity
                                StudentExam.objects.create(name=user.first_name, phone_number=phone_number, date_of_exam=student_exam.date_of_exam, start_time=student_exam.start_time, end_time=student_exam.end_time, examination_identity = unique_value, subject=student_exam.subject, student=student_info, exam=exam_type)

                    subjects = StudentSubject.objects.filter(
                        classCurrent=student_info.classCurrent)
                    subjects_array = []
                    timetable_generation = []
                    for sub in subjects:
                        subjects_array.append(sub.subject.subject_name)

                    # data = studentMarksPrediction(request)
                    status_exam = True
                    # for dat in data['data']:
                    #     result_one_suject = results.getting_points(grade, [int(dat)])
                    #     if result_one_suject['grade'][0] >'f':
                    #         stutus = False
                    #         messages.success(request, 'You have not yet well prepared on doing this exam use different studying techniques')
                    #         return redirect('examList')
                    unique_value = random.randint(0, 9999)
                    if status_exam:
                        if student_info.classCurrent.level.name == 'A-Level':
                            timetable_generation =timetable.A_Level_timetable(student_info.course.name)
                        else:
                            timetable_generation = timetable.O_level_timetable(
                                subjects_array, date_formated)
                        for tmtable in timetable_generation:
                            sunject_selected = Subject.objects.filter(
                                subject_name=tmtable['subject']).first()
                            StudentExam.objects.create(name=user.first_name, phone_number=phone_number, date_of_exam=tmtable['date'], start_time=tmtable['start_time'], end_time=tmtable['end_time'], examination_identity = unique_value, subject=sunject_selected, student=student_info, exam=exam_type)
                        messages.success(
                            request, 'Congratulations you have made an appointment successful')
                        return redirect('examList')
                else:
                    messages.error(
                        request, 'You have enter incorrect registration number please try again')
                    return redirect('MakeApointmentAdd')
            else:
                messages.error(
                    request, 'You have enter incorrect email please try again')
                return redirect('MakeApointmentAdd')
        else:
            messages.info(
                request, 'You have arleady make appointment to those exams')
            return redirect('examList')

    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    student_info = Student.objects.filter(user=user).first()
    exam_types = ExamType.objects.filter(
        studentClass=student_info.classCurrent)

    context = {'exam_types': exam_types}
    UserLog.objects.create(task='Viewing Appointment Made', user=request.user)
    return render(request, 'OnlineExamination/create appointment.html', context)

def CheckingYouCurrentResults(request):
    data = studentMarksPrediction(request)
    user = User.objects.filter(id=request.user.id).first()
    student_info = Student.objects.filter(user=user).first()
    grade = Grade.objects.filter(level = student_info.classCurrent.level)
    result_one_suject = results.getting_points(grade, data['data'])
    dataset = pd.DataFrame(data)
    dataset['Grade'] =result_one_suject['grade']
    dataset.columns = [ 'Marks', 'Subject', 'Grade']
    dataset = dataset[['Subject', 'Marks', 'Grade']]
    # print(dataset) 
    table = dataset.to_html(classes='table table-stripped table-center', index=False)
    exam_types = ExamType.objects.filter(studentClass=student_info.classCurrent)

    context = {'exam_types': exam_types, 'table':table}
    UserLog.objects.create(task='Viewing marks predicted', user=request.user)
    return render(request, 'OnlineExamination/create appointment.html', context)

@login_required(login_url='/')
def examList(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    student_info = Student.objects.filter(user=user).first()
    st_exam = StudentExam.objects.filter(student=student_info)
    context = {'st_exam': st_exam}
    UserLog.objects.create(task='Viewing examination List', user=request.user)

    return render(request, 'OnlineExamination/list-exam.html', context)


def LoginAgin(request, id):
    user1 = request.user
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if request.user == user1:
                st_exam = StudentExam.objects.filter(id=id).first()
                messages.success(request, 'Login successful')
                return redirect(f'../Exam/{st_exam.id}')
            else:
                messages.error(request, 'You cant able to do exam for other persorn')

        else:
            messages.error(request, 'inncorect username or password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def DeleteexamList(request, id):
    UserLog.objects.create(task='Delete examination List', user=request.user)
    st_exam = StudentExam.objects.filter(id=id).first().delete()
    messages.success(request, 'exam deleted successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def Exam(request, id):
    student_examination = StudentExam.objects.filter(id=id).first()
    # Assuming `end_time` is a datetime object
    formatted_end_time = date(student_examination.getting_fully_endtime, 'Y-m-d H:i:s')
    format_exam = ExamFormat.objects.filter(exam_type=student_examination.exam)
    studentClass = student_examination.student.classCurrent
    subjectClass_obj = SubjectClass.objects.filter(studentClass=studentClass, subject=student_examination.subject).first()
    topics = Topic.objects.filter(subject=subjectClass_obj)
    QuestionPerTopic = {
        'Essay': [],
        'Short Note': [],
        'fill the blanks': [],
        'True': [],
        'Match item': [],
        'multiple_coice': [],
        'Short Answers': []
    }

    for topic in topics:
        for format in format_exam:
            dump_qns = ExaminationDump.objects.filter(topic=topic, questionType=format.type_questions)
            if dump_qns.exists():
                for dump_qn in dump_qns:
                    QuestionPerTopic[format.type_questions.name].append(dump_qn.id)

    question_number = 0
    for format in format_exam:
        if question_number <= format.number_of_questions:
            question_selected = random.choice(QuestionPerTopic[format.type_questions.name])
            generated_question_fromDump = ExaminationDump.objects.filter(id=question_selected).first()
            # Generated_exam.objects.create(question=generated_question_fromDump.questions, answers=generated_question_fromDump.answers, is_generated=True, subject=student_examination.subject, exam_format=format, exam_type=student_examination.exam)

    examination_Questions = {
        'A': {'question_type': '', 'others': []},
        'B': {'question_type': '', 'others': []},
        'C': {'question_type': '', 'others': []},
        'D': {'question_type': '', 'others': []},
        'E': {'question_type': '', 'others': []},
        'F': {'question_type': '', 'others': []},
        'G': {'question_type': '', 'others': []},
        'H': {'question_type': '', 'others': []},
        'I': {'question_type': '', 'others': []}
    }

    exams_generated = Generated_exam.objects.filter(exam_type=student_examination.exam, subject=student_examination.subject)
    i = 1
    for exam_generated in exams_generated:
        section = exam_generated.exam_format.section
        examination_Questions[section]['question_type'] = exam_generated.exam_format.type_questions.name
        examination_Questions[section]['others'].append({'Sn':i, 'id': exam_generated.id, 'question': exam_generated.question})
        i+=1
    context = {
        'student_examination': student_examination,
        'formatted_end_time': formatted_end_time,
        'examination_Questions': examination_Questions,
        'exams_generated': exams_generated
    }

    UserLog.objects.create(task='doing an exam', user=request.user)
    return render(request, 'OnlineExamination/examination.html', context)

def SubmittingExamination(request, stEx):
    user1 = request.user
    length_questions = Generated_exam.objects.all().count()
    exam = StudentExam.objects.filter(id=stEx).first()
    if request.method == "POST":
        for i in range(length_questions):
            answer_name = 'question-'+str(i)
            answer =request.POST.get(answer_name)
            if answer != '' and answer != None:
                questions_obj = Generated_exam.objects.filter(id = i).first()
                question_answered = StudentAnswer.objects.filter(studentExam = exam, generated_question = questions_obj)
                if question_answered.exists():
                    qn = question_answered.first()
                    qn.user_answers = answer
                    qn.save()
                else:
                    StudentAnswer.objects.create(user_answers = answer, studentExam = exam, generated_question = questions_obj)
        exam.is_submitted = 1
        exam.save()
        messages.success(request, 'Congratulation you have submited your examination successful')
        return redirect('examList')

def ExaminationMarking(request):
    return render(request, 'OnlineExamination/webcam_analysis.html')


def examRegulation(request):
    context = {}
    UserLog.objects.create(task='Viewing examination Regulations', user=request.user)
    return render(request, 'OnlineExamination/examination-regulation.html', context)

def GeneratingStudentResult(request):
    # UserLog.objects.create(task='Viewing Student Results', user=request.user)
    students = Student.objects.all()
    for student_info in students:
        student_exams = StudentExam.objects.filter(student = student_info, is_result_generated = False, is_submitted = True)
        if student_exams.exists():
            for exam in student_exams:
                division, total_points, average, grade = 0,0,0,''
                grade = Grade.objects.all()
                student = {'student': [], 'exam': [], 'subject': []}
                exam_done = exam.exam
                marks = []
                stud_marks = StudentExam.objects.filter(examination_identity = exam.examination_identity)
                for st_mark in stud_marks:
                    marks.append(st_mark.marks)
                    result_one_suject = results.getting_points(grade, [st_mark.marks])
                    grade_scored = Grade.objects.filter(
                        name=result_one_suject['grade'][0]).first()
                    exam.grade = grade_scored
                    exam.save()
                result = results.getting_points(grade, marks)
                
                if student_info.classCurrent.level.name == 'O-Level':
                    divisions = Division.objects.filter(name='O-Level')
                    total_points = results.getting_pass_subject(points=result['point'], level=student_info.classCurrent.level.name)
                    division = results.checking_division(total_points=total_points, divisions=divisions)

                if student_info.classCurrent.level.name == 'A-Level':
                    divisions = Division.objects.filter(name='A-Level')
                    total_points = results.getting_pass_subject(result['point'])
                    division = results.checking_division(total_points=total_points, divisions=divisions)
                average = results.getting_average(marks)
                grade_obtained = results.gettingGrade(grades=grade, mark=average)
                StudentResult.objects.create(point= total_points,grade = grade_obtained, average= int(average), division= division, exam =exam, student = student_info)
                student_info.is_result_generated = True
                student_info.save()
    return render(request, 'OnlineExamination/student-results.html')

def Checking_student_Results(request):
    students = Student.objects.all()
    for student in students:
        grade = Grade.objects.filter(level =student.classCurrent.level)
        student_result_dict = {'subject': [], 'marks':[], 'Grade': [], 'Pass':[]}
        student_exam = StudentExam.objects.filter(student = student)
        if student_exam.exists():
            exam_type = student_exam.first().exam
            student_exams = StudentExam.objects.filter(exam = exam_type)
            for exam in student_exams:
                if exam.exam.studentClass ==student.classCurrent:
                    result_one_suject = results.getting_points(grade, [exam.marks])
                    try:
                        grade_scored = Grade.objects.filter(name=result_one_suject['grade'][0]).first()
                        student_result_dict['subject'].append(exam.subject.subject_name)
                        student_result_dict['Grade'].append(grade_scored.name)
                        student_result_dict['Pass'].append(grade_scored.description)
                        student_result_dict['marks'].append(exam.marks)
                    except:
                        pass
                student_subject = StudentSubject.objects.filter(student=student, classCurrent = student.classCurrent)
                if len(student_result_dict['Grade']) == student_subject.count():
                    all_division = Division.objects.filter(level =student.classCurrent.level)
                    pass_subject = results.getting_pass_subject(result_one_suject['point'], student.classCurrent.level.name)
                    division = results.checking_division(pass_subject, all_division)
                    average = results.getting_average(student_result_dict['marks'])
                    grade = results.getting_points(grade, [average, average])
                    StudentResult.objects.create(point = pass_subject, grade = grade['grade'][0],average = average, division =division, exam = exam, student = student)


def CurrentStudentResult(request):
    UserLog.objects.create(task='Viewing Student Results', user=request.user)
    student = Student.objects.filter(user = request.user)
    if student.exists():
        grade = Grade.objects.filter(level =student.first().classCurrent.level)
        student_result_dict = {'subject': [], 'Grade': [], 'Pass':[]}
        student_exam = StudentExam.objects.filter(student = student.first())
        if student_exam.exists():
            exam = student_exam.first()
            examination_identity = exam.examination_identity
            student_exams = StudentExam.objects.filter(examination_identity = examination_identity)
            for exam in student_exams:
                result_one_suject = results.getting_points(grade, [exam.marks])
                try:
                    grade_scored = Grade.objects.filter(name=result_one_suject['grade'][0]).first()
                    student_result_dict['subject'].append(exam.subject.subject_name)
                    student_result_dict['Grade'].append(grade_scored.name)
                    student_result_dict['Pass'].append(grade_scored.description)
                except:
                    pass
        result_table = []
        print(student_result_dict)
        results_arrs = StudentResult.objects.filter(exam = student_exam.first(), student = student.first())
        if results_arrs.exists():
            result_arr = results_arrs.first()
            result_arr_dict = {'student':[student.first().name], 'exam':[result_arr.exam.name], 'points':[result_arr.point], 'division':[result_arr.division], 'average':[result_arr.average]}
            result_data = pd.DataFrame(result_arr_dict)
            result_table = result_data.to_html(classes='table table-stripped table-center', index=False)
            # print(student_result_dict)

        accademic_year = exam.exam.date_created.year
        dataset = pd.DataFrame(student_result_dict)
        dataset.columns = ['Subject', 'Grade', 'Status']
        # print(dataset)
        table = dataset.to_html(classes='table table-stripped table-center', index=False)
        context = {'table':table, 'exam_type':exam.exam, 'accademic_year':accademic_year, 'result_table':result_table}
        return render(request, 'OnlineExamination/student-results.html', context)
    context = {} 
    return render(request, 'OnlineExamination/student-results.html', context)

def FullStudentResult(request):
    UserLog.objects.create(task='Viewing Student Results', user=request.user)
    student_class = StudentClassManyToMany.objects.filter(student__user__gt = request.user)
    dataset = []
    for cls in student_class:
        class_belong = cls.classCurrent.name
        class_belong_id = cls.classCurrent.id
        dataset.append({'id':class_belong_id, 'class':class_belong})
    context = {'dataset':dataset}
    return render(request, 'OnlineExamination/View all results.html', context)

def gettingStudentData(request):
    return render(request, 'OnlineExamination/webcam_analysis.html')

def SubmitingExam(request, id):
    exam = StudentExam.objects.filter(id = id).first()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def webcam_analysis(request):
#     # Implement the image capture and analysis logic using cv2 and MediaPipe
#     # ...
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Detect faces in the frame
#     results = face_detection.process(rgb_frame)

#     # Reset counters if no faces detected
#     if not results.detections:
#         talk_counter = 0
#         look_counter = 0
#     result = {
#         'message': 'Analysis result',
#         'flagged_actions': []
#     }

#     # Check for mouth covering
#     mouth_covered_counter = 0
#     # Number of consecutive frames to consider as mouth covering
#     mouth_covered_threshold = 60
#     for detection in results.detections:
#         # Calculate mouth area based on facial landmarks
#         landmarks = detection.location_data.relative_keypoints
#         mouth_area = calculate_mouth_area(landmarks)

#         # Check if mouth area indicates mouth covering
#         if mouth_area < threshold_value:
#             mouth_covered_counter += 1
#         else:
#             mouth_covered_counter = 0

#         # Check if student's mouth is covered for a long duration
#         if mouth_covered_counter >= mouth_covered_threshold:
#             result['flagged_actions'].append('Mouth covered for too long')
#             # Add your action here, such as displaying a warning message or notifying the exam proctor

#     return JsonResponse(result)

def uploadingExaminationQuestions(request):
    questions_path = settings.STATICFILES_DIRS[0] +r'\csv files\final_generatedQuestions.csv'
    data = pd.read_csv(questions_path)
    for index in data.index:
        subject = data['Subject'][index]
        studentclass = data['Class'][index]
        topic = data['Topic'][index]
        questions = data['Questions'][index]
        questionCategory = data['category'][index]
        answers = data['answers'][index]
        studentclass_obj = StudentClass.objects.filter(name = studentclass).first()
        subject_obj = Subject.objects.filter(subject_name = subject).first()
        subject_class_obj = SubjectClass.objects.filter(studentClass =studentclass_obj, subject = subject_obj).first()
        topic_obj =Topic.objects.filter(name =topic, subject = subject_class_obj).first()
        questionType_obj =QuestionsType.objects.filter(name = questionCategory).first()
        ExaminationDump.objects.create(questions =questions, answers =answers, is_generated_Model = False, questionType = questionType_obj, topic= topic_obj)
    return redirect('examList')

def ExaminationDone(request):
    try:
        examination_data = []
        user = request.user
        teacher = Teacher.objects.filter(user=user).first()
        teacher_subjects_class = teacher.classSubject.all()
        try:
            for teacher_subject_class in teacher_subjects_class:
                no_student = 0
                student_detail ={}
                student_exams = StudentExam.objects.filter(subject = teacher_subject_class.subject, is_submitted = 1)
                for student_exam in student_exams:
                    if student_exam.student.classCurrent == teacher_subject_class.studentClass:
                        no_student += 1
                        student_detail= student_exam
                examination_data.append({
                    'id':teacher_subject_class.id,
                    'stexm_id':student_detail.id,
                    'class':student_detail.student.classCurrent.name,
                    'subject':student_detail.subject.subject_name,
                    'no_students':no_student,
                    'stusent_examination':student_detail.examination_identity,
                    'examination_type':student_detail.exam.name,
                })
        except:
            pass
        print(student_detail)
        context = {'examination_data':examination_data}
        return render(request, 'OnlineExamination/student-ExaminationDone.html', context)
    except:
        messages.error(request,'You have not access previllage to this page')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def UserSubmittedExamList(request, id, stexm_id):
    Student_details = []
    user = request.user
    teacher = Teacher.objects.filter(user=user).first()
    if teacher.classSubject.exists():
        teacher_subjects_class = teacher.classSubject.filter(id = id)
        if teacher_subjects_class.exists():
            teacher_subject_class = teacher_subjects_class.first()
            student_exams = StudentExam.objects.filter(examination_identity =stexm_id, subject=teacher_subject_class.subject)
            i = 1
            for st_exam in student_exams:
                student_answs =StudentAnswer.objects.filter(studentExam =st_exam)
                if student_answs.exists():
                    student_answ = student_answs.first()
                    Student_details.append({
                        'index':i,
                        'id':student_answ.studentExam.id,
                        'name':student_answ.studentExam.student.name,
                        'status':student_answ.is_verified_teacher,
                        'marks':student_answ.studentExam.marks,
                        'Exam_type':student_answ.studentExam.exam.name
                    })
                    i+=1
                    
    else:
        pass
    context = {'Student_details':Student_details, 'teacher':teacher}
    return render(request, 'OnlineExamination/Examinanation-list-student.html', context)

def TeacherMarking(request, id):
    student_answers = []
    student_exams ={}
    user = request.user
    teacher_exist = Teacher.objects.filter(user=user)
    if teacher_exist.exists():
        teacher = teacher_exist.first()
        if teacher.classSubject.exists():
            teacher_subjects_class = teacher.classSubject.all()
            for teacher_subject_class in teacher_subjects_class:
                student_exams = StudentExam.objects.filter(id = id, subject=teacher_subject_class.subject).first()
                student_answers = StudentAnswer.objects.filter(studentExam = student_exams)    
        else:
            pass
        context = {'student_answers':student_answers, 'student_exams':student_exams}
        return render(request, 'OnlineExamination/teacher-marking.html', context)
    else:
        messages.error(request,'You have not access previllage to this page')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def UpdateMarks(request, id):
    if request.method == "POST":
        UserLog.objects.create(task='Updating student marks', user=request.user)
        marks = request.POST.get('marks')
        feedback = request.POST.get('feedback')
        answer = StudentAnswer.objects.filter(id = id).first()
        answer.marks_scored = marks
        answer.is_verified_teacher = True
        answer.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def BankQuestionTable(request):
    bank_questions = []
    user = request.user
    teacher_exist = Teacher.objects.filter(user=user)
    if teacher_exist.exists():
        teacher = teacher_exist.first()
        if teacher.classSubject.exists():
            teacher_subjects_class = teacher.classSubject.all()
            for teacher_subject_class in teacher_subjects_class:
                Verified_questions = 0
                Unverified_questions = 0
                topics = Topic.objects.filter(subject = teacher_subject_class)
                if topics.exists():
                    for topic in topics:
                        Unverified_questions += ExaminationDump.objects.filter(topic = topic, is_generated_Model = True).count()
                        Verified_questions += ExaminationDump.objects.filter(topic = topic, is_generated_Model = False).count()
                    
                bank_questions.append({
                    'id':teacher_subject_class.id,
                    'subject':teacher_subject_class.subject.subject_name,
                    'class':teacher_subject_class.studentClass.name,
                    'Verified':Verified_questions,
                    'Unverified':Unverified_questions,
                })
        else:
            pass
        context = {'bank_questions':bank_questions, 'teacher':teacher}
        return render(request, 'OnlineExamination/bank-question-table.html', context)
    else:
        messages.error(request,'You have not access previllage to this page')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def ViewBankOfQuestions(request, id):
    full_questions = []
    teacher = Teacher.objects.filter(user=request.user).first()
    if teacher.classSubject.exists():
        teacher_subjects_class = teacher.classSubject.filter(id = id).first()
        topics = Topic.objects.filter(subject = teacher_subjects_class)
        if topics.exists():
            for topic in topics:
                qn_per_topic = {'topic':'', 'Questions':[]}
                Unverified_questions = ExaminationDump.objects.filter(topic = topic, is_generated_Model = False)
                for qns in Unverified_questions:
                    qn_per_topic['topic']= topic
                    qn_per_topic['Questions'].append(qns)
                full_questions.append(qn_per_topic)
    question_type = QuestionsType.objects.all()
    context = {'teacher_subjects_class':teacher_subjects_class, 'full_questions':full_questions, 'question_type':question_type}
    return render(request, 'OnlineExamination/view-bank-question.html', context)

def UpdateQuestionGenerated(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        answers = request.POST.get('answers')
        question_type = request.POST.get('question_type')
        question_type_obj = QuestionsType.objects.filter(id = question_type).first()
        Unverified_questions = ExaminationDump.objects.filter(id = id).first()
        if name:
            Unverified_questions.questions = name
        if answers:
            Unverified_questions.answers = answers
        Unverified_questions.questionType = question_type_obj
        Unverified_questions.is_generated_Model =  False
        Unverified_questions.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


