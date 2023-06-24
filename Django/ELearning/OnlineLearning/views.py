from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
import pandas as pd
from OnlineLearning.models import OtpCode, Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers, Teacher,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass, UserLog
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from rest_framework.decorators import api_view
import random
from django.db import transaction
import os
import PyPDF2
import docx2txt
import string
from fuzzywuzzy import fuzz

# Create your views here.

def random_date(start, end):
    delta = start - end
    int_delta = (delta.days*24*60*60)+delta.seconds
    random_seconds = random.randint(0, -int_delta)
    return start+timedelta(seconds=random_seconds)


def UploadSelectedStudentPage(request):
    levels = ['O-Level', 'A-Level']
    for i in levels:
        SchoolLevel.objects.create(name = i)
    a_level = SchoolLevel.objects.filter(name= levels[1]).first()
    o_level = SchoolLevel.objects.filter(name= levels[0]).first()

    csv_path = settings.STATICFILES_DIRS[0] +r'\csv files\advance.csv'
    data = pd.read_csv(csv_path)
    data = data.iloc[:1000]
    for index, row in data.iterrows():
        DefaultUsers.objects.create(number=row['number'], name=row['name'], school_selected=row['school_selected'], course=row['course'], type=row['type'], location=row['location'], level = a_level)

    csv_path = settings.STATICFILES_DIRS[0] +r'\csv files\selected_standard7.csv'
    data1 = pd.read_csv(csv_path)
    data1 = data1.iloc[:1000]
    for index, row in data1.iterrows():
        DefaultUsers.objects.create(number=row['Namba ya Mtihani'], name=row['Jina la Mwanafunzi'], school_selected=row['Amechaguliwa kwenda'], course='Science & Arts', type=row['Aina'], location=row['Wilaya Shule Ilipo'], level = o_level)

    classes_advance = ['Form Five', 'Form Six']
    for i in classes_advance:
        level = SchoolLevel.objects.filter(name = 'A-Level').first()
        StudentClass.objects.create(name = i, level = level)

    classes = ['Form One', 'Form Two', 'Form Three', 'Form Four']
    for i in classes:
        level = SchoolLevel.objects.filter(name = 'O-Level').first()
        StudentClass.objects.create(name = i, level = level)
    departments = data['Subjects1_deparment'].unique()
    for i in departments:
        start_date = datetime.strptime('1/1/2010', '%d/%m/%Y')
        end_date = datetime.strptime('12/31/2022', '%m/%d/%Y')
        generated_date = random_date(start_date, end_date)
        Department.objects.create(name = i, department_Hod = 'Not Known', start_date = generated_date)

    courses = data['course'].unique()
    for i in courses:
        depart =data[data['course'] == i]['Department'].iloc[0]
        depart_obj =Department.objects.filter(name=depart).first()
        Course.objects.create(name=i, department = depart_obj)
    science_department_obj =Department.objects.filter(name='Science').first()
    Course.objects.create(name='Science & Arts', department = science_department_obj)

    for i in range(1,6):
        subject_head = 'Subjects' + str(i)
        subject_dep_head = 'Subjects' + str(i)+ '_deparment'
        subject1 = data[subject_head].unique()
        for i in subject1:
            depart =data[data[subject_head] == i][subject_dep_head].iloc[0]
            depart_obj =Department.objects.filter(name=depart).first()
            code = random.randint(1, 190)
            try:
                Subject.objects.get_or_create(subject_code = code, subject_name = i, department = depart_obj)
                subject = Subject.objects.filter(subject_code = code).first()
                Alevel = SchoolLevel.objects.filter(name = 'A-Level').first()
                classes = StudentClass.objects.filter(level=Alevel)
                for k in classes:
                    SubjectClass.objects.create(studentClass = k, subject = subject)
            except:
                pass
    OLevel_subject = ['Civics', 'Basic Mathematics', 'History', 'Geography', 'Kiswahili', 'English Language',  'Chemistry', 'Biology' 'Physics', 'Literature in English']
    Olevel = SchoolLevel.objects.filter(name = 'O-Level').first()
    OLevel_classes = StudentClass.objects.filter(level=Olevel)
    loaded_subjects_path =  settings.STATICFILES_DIRS[0] +r'\csv files\configurations\olevel-department.csv'
    OLevel_subject = pd.read_csv(loaded_subjects_path)
    course = Course.objects.filter(name= 'Science & Arts').first()
    for index in OLevel_subject.index:
        subject_exist = Subject.objects.filter(subject_name = OLevel_subject['Subject'][index])
        if not subject_exist.exists():
            department_obj = Department.objects.filter(name= OLevel_subject['Department'][index]).first()
            Subject.objects.create(subject_code = code, subject_name = OLevel_subject['Subject'][index], department = department_obj)
            current_subject = Subject.objects.filter(subject_code = code).first()
        else:
            current_subject = subject_exist.first()
        for classes in OLevel_classes:
            SubjectClass.objects.create(studentClass = classes, subject= current_subject)
            CourseSubject.objects.create(course = course, subject=current_subject, studentClass=classes)

    courses = data['course'].unique()
    for i in courses:
        course_data =data[data['course'] == i]
        course_obj = Course.objects.filter(name= i).first()
        for j in range(1,6):
            subject_head = 'Subjects' + str(j)
            subject = course_data[subject_head].iloc[0]
            level = SchoolLevel.objects.filter(name = 'A-Level').first()

            subject_obj = Subject.objects.filter(subject_name=subject).first()
            classes = StudentClass.objects.filter(level=level)
            for k in classes:
                try:
                    CourseSubject.objects.create(course = course_obj, subject=subject_obj, studentClass=k)
                except:
                    pass

    # for subject in OLevel_subject:
    #     level = SchoolLevel.objects.filter(name = 'O-Level').first()
    #     classes = StudentClass.objects.filter(level=level)
    #     for k in classes:
    #         CourseSubject.objects.create(course = course, subject=subject, studentClass=k)

    roles = ['Student', 'Admin', 'Teachers', 'GroupLeader', 'CR']
    for role in roles:
        Group.objects.create(name = role)
    admin_group = Group.objects.filter(name = 'Admin').first()
    student_group = Group.objects.filter(name = 'Student').first()
    permissions = Permission.objects.all()
    for per in permissions:
        admin_group = Group.objects.filter(name = 'Admin').first()
        admin_group.permissions.add(per)
    student_permisions = student = [9,10,11,12, 28, 36, 141,42,43,44,45,46,47,48,49,50,51,52,53,54,54, 72,76,77,87,91,95,99,100,101,102,111,118,122,123,126,138,139,141,142,143,144,148,149,150,154,172,176,186,188,192,192,204,212,216,201]
    for per in student_permisions:
        permision = Permission.objects.filter(id = per).first()
        student_group.permissions.add(permision)
    return redirect('registerPage')

def check_file_similarity(filepath):
    similarity_scores = []
    file_content = ''
    obj_content = ''

    loaded_path = settings.STATICFILES_DIRS[0] +filepath[1:-1]
    # extract text content from PDF files
    file_path =loaded_path.replace(string.punctuation[23]+string.punctuation[23], string.punctuation[14])
    # file_path = loaded_path.replace(string.punctuation[14], string.punctuation[23])
    _, extenstion = file_path.split('.')
    print(extenstion)
    if extenstion == 'pdf':
        print('ok')
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                file_content += page.extract_text()

    # extract text content from Word files
    elif extenstion == 'docx':
        file_content = docx2txt.process(file_path)

    # other file types not supported
    else:
        raise ValueError('Unsupported file type')

    for obj in AssigmentSubmision.objects.all():
        # extract text content from object file
        _, extenstion_path = obj.doc.path.split('.')
        if extenstion_path =='pdf':
            with open(obj.file.path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    obj_content += page.extract_text()
        elif extenstion_path == 'docx':
            obj_content = docx2txt.process(obj.file.path)
        else:
            continue
        name = (obj.doc.name)[9:]

        # calculate similarity score
        similarity_score = fuzz.token_set_ratio(obj_content, file_content)
        similarity_scores.append(similarity_score)
        print(similarity_scores)
    return similarity_scores

def searchUserSelected(request):
    try:
        index_number = request.POST.get('index_number')
        user_info = DefaultUsers.objects.filter(number=index_number).first()
        current_class = StudentClass.objects.filter(level = user_info.level)
        context = {'user_info':user_info, 'current_class':current_class}
        return render(request, 'UAA/register.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@transaction.atomic()
def submitRegistration(request):
    # try:
    if request.method == "POST":
        index_number = request.POST.get('index_number')
        email = request.POST.get('email')
        bod = request.POST.get('bod')
        class_level = request.POST.get('class_level')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        index_number = request.POST.get('index_number')
        registration_no = random.randint(1000000, 9999999999)

        user =User.objects.create_user(username=email, email=email, password=password)
        user_info = DefaultUsers.objects.filter(number=index_number).first()
        user.first_name = user_info.name
        user.save()
        messages.success(request,'Student is registered  successful')

        user_info_details = User.objects.filter(username=email).first()
        current_class = StudentClass.objects.filter(id = class_level).first()
        course = Course.objects.filter(name = user_info.course).first()
        student = Student.objects.create(name=user_info.name,
                                        registration_no=registration_no,
                                        index_number=index_number,
                                        gender= 'M',
                                        date_of_birth=bod,
                                        phone_number=phone_no,
                                        school=user_info.school_selected,
                                        user=user_info_details,
                                        course=course,
                                        classCurrent=current_class,
                                        )
        StudentClassManyToMany.objects.create(classCurrent = current_class, student= student)
        role = Group.objects.filter(name = 'Student').first()
        user_info_details.groups.add(role)
        return redirect('loginPage')

def updateStudent(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            file = request.FILES['file']
            phone_no = request.POST.get('phone_no')

            user_id = request.user.id
            user = User.objects.filter(id = user_id).first()
            student_info = Student.objects.filter(user=user).first()
            student_info.phone_number = phone_no
            student_info.email = email
            student_info.photo = file
            student_info.save()
            messages.success(request,'Student is deleted successful')

            return redirect('userProfilePage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def changePassword(request):
    try:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user_id = request.user.id
                user = User.objects.filter(id = user_id).first()
                user.set_password(password1)
                return redirect('userProfilePage')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def foggotenPassword(request):
    user = request.user
    if request.method == "POST":
        email = request.POST.get('email')
        is_user_exists = User.objects.filter(email=email).exists()
        opt_generated = ''
        status = True
        if is_user_exists:
            user = User.objects.filter(email=email).first()
            opt_objs = OtpCode.objects.filter(user = request.user)
            if opt_objs.exists():
                opt_obj = opt_objs.first()
                if opt_obj.get_status == 'Valid':
                    opt_generated = opt_obj.code
                    status = True
                else:
                    status = False
            else:
                status = False
            if not status:
                opt = random.randint(100000,999999)
                opt_generated = 'E-' + str(opt)
                OtpCode.objects.create(code = opt_generated, user = user)
            header = 'Resset Password'
            message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(header, message, email_from, email)
            return redirect(f'../opt_sent/{user.id}')
        return redirect(f'../opt_sent/{user.id}')
    return render(request, 'UAA/foggotpassword.html')

def resend_password(request, id):
    user = User.objects.filter(id=id).first()
    opt = random.randint(100000,999999)
    opt_generated = 'E-' + str(opt)
    OtpCode.objects.create(code = opt_generated, user = user)
    header = 'Resset Password'
    message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(header, message, email_from, email_from)
    return redirect(f'../opt_sent/{user.id}')

def opt_sent(request, id):
    if request.method == "POST":
        code = request.POST.get('code')
        opts = OtpCode.objects.filter(user__id__gt = id, is_used=False)
        for opt in opts:
            if opt == code:
                if opt.get_status == 'Valid':
                    opt.is_used = True
                    opt.save()
                    return redirect(f'../setting_password/{user.id}')
                else:
                    messages.error(request,'Code used has been arleady expired')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request,'Incorrect code used')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/opt-sent.html', context)

def setting_password(request, id):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.filter(id=id).first()
            user.set_password(password1)
            messages.success(request,'Your password Account is reseted successfully')
            return redirect('')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/new-password.html')


def registerPage(request):
    try:
        current_class = StudentClass.objects.all()
        context = {'current_class':current_class}
        return render(request, 'UAA/register.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def loginPage(request):
    try:
        if request.method == "POST":
            username = request.POST.get('email')
            password = request.POST.get('password')
            user =authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_active:
                    messages.success(request,'User is successful logged in')
                    return redirect('DashboardPage')
                elif user.is_superuser:
                    return redirect('admin')
                else:
                    messages.error(request,'Account is blocked')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request,'Incorrect username or password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'UAA/login.html')

def logoutPage(request):
    try:
        UserLog.objects.create(task='Log out', user= request.user)
        logout(request)
        return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def manageroles(request):
    try:
        UserLog.objects.create(task='Viewing Roles', user= request.user)
        roles_dict= []
        Roles = Group.objects.all().order_by('id')
        for role in Roles:
            permisions = role.permissions.all()
            roles_dict.append({'role':role, 'permissions':permisions})

        context = {'roles_dict':roles_dict}
        return render(request,'UAA/manageroles.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def addroles(request):
    p = Group()
    if request.method == "POST":
        try:
            UserLog.objects.create(task='Add role', user= request.user)
            name = request.POST.get("name")
            permission = [x.name for x in Permission.objects.all()]
            s_id = []
            p.name=name
            for x in permission:
                    s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
            p.save()
            messages.success(request,'Student is deleted successful')

            for s in s_id:
                p.permissions.add(Permission.objects.filter(id=s).first())
                p.save()
                messages.success(request,'Student is deleted successful')

            messages.success(request,'Role added successful')
            return redirect('/manageroles')

        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        UserLog.objects.create(task='Roles List', user= request.user)
        permission = Permission.objects.all()
        context = {'permission':permission}
        return render(request, 'UAA/add-role.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def RemoveRole(request, rid, pid):
    try:
        UserLog.objects.create(task='Deleting roles', user= request.user)
        permission = Permission.objects.filter(id = pid).first()
        roles = Group.objects.filter(id = rid).first()
        roles.permissions.remove(permission)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def AssignUserRole(request, uid):
    user = User.objects.filter(id = uid).first()
    if request.method == 'POST':
        UserLog.objects.create(task='assigning role to user', user= request.user)
        for j in user.groups.all():
            user.groups.remove(j)
        groups = [x.name for x in Group.objects.all()]

        s_id = []
        for x in groups:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        print(s_id)
        for s in s_id:
            user.groups.add(Group.objects.filter(id=s).first())
        messages.success(request,'roles are assigned to user successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def editroles(request,id):
    exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
    p = Permission.objects.exclude(id__in=exclude_perm)
    r = Group.objects.filter(id=id)
    y=Group.objects.filter(id=id).first()
    if request.method == 'POST':
        UserLog.objects.create(task='Update Roles', user= request.user)
        name = request.POST.get('name')
        for j in Permission.objects.all():
            y.permissions.remove(j)
        permission = [x.name for x in Permission.objects.all()]

        s_id = []
        Group.objects.filter(id=id)
        for x in permission:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        r=Group.objects.filter(id=id).update(name=name)

        for s in s_id:
            y.permissions.add(Permission.objects.get(id=s))
        messages.success(request,'permissions are added successful')
        return redirect('/manageroles')

    UserLog.objects.create(task='Edit Roles', user= request.user)
    role = Group.objects.filter(id = id).first()
    permission = Permission.objects.all()
    context = {'permission':permission, 'role':role}
    return render(request, 'UAA/edit-role.html', context)

@login_required(login_url='/login')
def blockuser(request,id):
      try:
        UserLog.objects.create(task='Blocking User', user= request.user)
        u = User.objects.filter(id=id).filter(is_active='True').exists()
        if u:
            User.objects.filter(id=id).update(is_active='False')
            messages.success(request,'block successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            User.objects.filter(id=id).update(is_active='True')
            messages.success(request,'Activation successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def deleteroles(request,id):
    UserLog.objects.create(task='Delete Roles', user= request.user)
    g = Group.objects.filter(id=id).delete()
    messages.success(request,'Student is deleted successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def userProfilePage(request):
    UserLog.objects.create(task='Viewing User Profile', user= request.user)
    return render(request, 'Admin/profile.html')

@login_required(login_url='/')
def DashboardPage(request):
    UserLog.objects.create(task='Viewing Dashboard Page', user= request.user)
    return render(request, 'Admin/dashboard.html')

def Admision_statusPage(request):
    return render(request, 'Student/admission_status.html')

@login_required(login_url='/')
def studentList(request):
# try:
    UserLog.objects.create(task='Viewing Student List', user= request.user)
    stud = Student.objects.all()
    users = User.objects.all()
    group = Group.objects.all()

    users_groups = []
    for user in users:
        groups = user.groups.all()
        users_groups.append({'user':user, 'groups':groups})
    context = {'users_groups':users_groups, 'group':group}
    return render(request, 'Admin/list-student.html', context)

    # except:
    #     messages.error(request,'Something went wrong')
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def studentAdd(request):
    departments = Department.objects.all()
    courses = SubjectClass.objects.all()
    context = {'departments':departments, 'courses':courses}
    return render(request, 'Admin/add-student.html', context)

@transaction.atomic()
def AddTeacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        bod = request.POST.get('bod')
        department = request.POST.get('department')
        class_level = request.POST.get('class_level')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        password = str(name).split(' ')[-1]
        User.objects.create_user(username=email, email=email, password=password)
        user = User.objects.filter(username = email).first()
        user.first_name = str(name).split(' ')[0]
        user.last_name = str(name).split(' ')[-1]
        user.save()
        no_subject_teacher_tought = SubjectClass.objects.all().count()
        department_obj = Department.objects.filter(id = department).first()
        Teacher.objects.create(name=  name, gender= gender, date_of_birth = bod, phone_number = phone_no, user = user, department = department_obj)
        teacher = Teacher.objects.filter(user = user).first()
        for i in class_level:
            subject_class_id = i
            subject_class_obj = SubjectClass.objects.filter(id = subject_class_id).first()
            teacher.classSubject.add(subject_class_obj)
            group =Group.objects.filter(name = 'Teachers').first()
            user.groups.add(group)

        messages.success(request,'Teacher is created successful')
        return redirect('studentlist')

@login_required(login_url='/')
def studentEdit(request, id):
    return render(request, 'Admin/edit-student.html')

@login_required(login_url='/')
def studentDelete(request, id):
    try:
        UserLog.objects.create(task='delete student', user= request.user)
        Student.objects.filter(id = id).delete()
        messages.success(request,'Student is deleted successful')
        return redirect('studentlist')

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def TopicList(request, sid):
    # try:
        UserLog.objects.create(task='Viewing topic List', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        user_id = request.user.id
        user_data = User.objects.filter(id = user_id).first()
        student_data = Student.objects.filter(user = user_data).first()
        subject_class =SubjectClass.objects.filter( studentClass =student_data.classCurrent, subject = subject).first()
        Topic_info = Topic.objects.filter(subject = subject_class)
        groups = StudentGroup.objects.filter(subject=subject)
        users_groups = StudentGroupManyToMany.objects.filter(student = student_data)
        is_student_present =[]
        context = {'Topic_info':Topic_info, 'subject':subject, 'users_groups':users_groups, 'groups':groups, 'is_student_present':is_student_present}
        return render(request, 'Student/topics.html', context)
    # except:
    #     messages.error(request,'Something went wrong')
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def TopicAdd(request, sid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='adding topic', user= request.user)
            name = request.POST.get('name')
            description = request.POST.get('description')
            subject = request.POST.get('subject')
            subject =Subject.objects.filter(id = sid).first()
            subject_class =SubjectClass.objects.filter(subject = subject).first()

            depart = Topic(name=name, description=description, subject=subject_class)
            depart.save()
            messages.success(request,'Topic is added successful')
            return redirect(f'../TopicList/{sid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        UserLog.objects.create(task='add topic page', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        context = {'subject':subject}
        return render(request, 'Student/add-topics.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def TopicEdit(request, sid, id):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='update topic', user= request.user)
            name = request.POST.get('name')
            description = request.POST.get('description')
            subject_id = request.POST.get('subject')
            subject =Subject.objects.filter(id = subject_id).first()
            subject_class =SubjectClass.objects.filter(subject = subject).first()
            topic = Topic.objects.filter(id=id).first()
            topic.name=name
            topic.description=description
            topic.subject=subject_class
            topic.save()
            messages.success(request,'Topic is updated successful')
            return redirect(f'../../TopicList/{sid}')

        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        UserLog.objects.create(task='edit topic page', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id=id).first()
        context = {'topic':topic, 'subject':subject}
        return render(request, 'Student/edit-Topic.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def TopicDelete(request, sid, id):
    try:
        UserLog.objects.create(task='delete topic', user= request.user)
        topic = Topic.objects.filter(id = id).first()
        topic.delete()
        messages.success(request,'Topic is deleted successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def ElearningPage(request, sid, tid,):
    try:
        UserLog.objects.create(task='Viewing Elearnig Page', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        context = {'topic':topic, 'subject':subject}
        return render(request, 'Student/elearning.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def NotesPage(request, sid, tid):
    try:
        UserLog.objects.create(task='Viewing Notes List', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        notes = Notes.objects.filter(subject=subject, topic=topic)
        context = {'topic':topic, 'subject':subject, 'notes':notes}
        return render(request, 'Student/notes.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def NotesAdd(request, sid, tid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='add notes', user= request.user)
            title = request.POST.get('title')
            Description = request.POST.get('Description')
            content = request.POST.get('written_notes')
            file_doc = request.FILES['file']
            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            notes = Notes.objects.create(title=title, description=Description, content=content, file=file_doc, topic = topic, subject= subject)

            path = settings.STATICFILES_DIRS[0] +r'/media/Notes/' + str(file_doc)
            doc = aw.Document(path)
            # Enable round-trip information
            saveOptions = aw.saving.HtmlSaveOptions()
            saveOptions.export_roundtrip_information = True

            saveOptions.export_font_resources = True
            saveOptions.resource_folder = settings.STATICFILES_DIRS[0] +r'/media/Notes/'
            # Save the document as HTML
            file_data = doc.save("Document.html", saveOptions)
            notes.html = file_data
            notes.save()
            messages.success(request,'  Notes is added successful')
            return redirect(f'../../NotesPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        UserLog.objects.create(task='view add notes page', user= request.user)
        topic = Topic.objects.filter(id = tid).first()
        subject =Subject.objects.filter(id = sid).first()
        context = {'topic':topic, 'subject':subject}
        return render(request, 'Student/Add-Notes.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def booksPage(request, sid, tid):
    try:
        UserLog.objects.create(task='Viewing Books List', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        books = Book.objects.filter(topic=topic, subject=subject)
        context = {'topic':topic, 'subject':subject, 'books':books}
        return render(request, 'Student/books.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def BooksAdd(request, sid, tid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='add book', user= request.user)
            name = request.POST.get('name')
            author = request.POST.get('author')
            description = request.POST.get('description')
            type = request.POST.get('type')
            file_data = request.FILES['file']
            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            books = Book.objects.create(name=name, author=author, type=type, description=description, file= file_data, topic = topic, subject= subject)
            messages.success(request,'  Book is added successful')
            return redirect(f'../../booksPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        UserLog.objects.create(task='view add book page', user= request.user)
        department = Department.objects.all()
        topic = Topic.objects.filter(id = tid).first()
        subject =Subject.objects.filter(id = sid).first()
        context = {'department':department, 'topic':topic, 'subject':subject}
        return render(request, 'Student/add-Books.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def BooksEdit(request, sid, tid, bid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='update book', user= request.user)
            name = request.POST.get('name')
            author = request.POST.get('author')
            description = request.POST.get('description')
            type = request.POST.get('type')
            file_data = request.FILES['file']

            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            Books_obj = Book.objects.filter(id=bid).first()
            books_url = settings.STATICFILES_DIRS[0] +books.file.url
            os.remove(books_url)
            Books_obj.name=name
            Books_obj.author=author
            Books_obj.type=type
            Books_obj.description=description
            Books_obj.file= file_data
            Books_obj.subject = subject
            Books_obj.topic = topic
            Books_obj.save()
            messages.success(request,'Book is updated successful')
            return redirect(f'../../booksPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        UserLog.objects.create(task='edit book page', user= request.user)
        books = Book.objects.filter(id=bid).first()
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        context = {'books':books,'topic':topic, 'subject':subject}
        return render(request, 'Student/edit-Books.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def BooksDelete(request, sid, tid,  id):
    try:
        UserLog.objects.create(task='delete book', user= request.user)
        books =Book.objects.filter(id = id).first()
        books_url = settings.STATICFILES_DIRS[0] +books.file.url
        os.remove(books_url)
        books.delete()
        messages.success(request,'Book is deleted successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def assigmentsPage(request, sid, tid):
    try:
        UserLog.objects.create(task='Viewing Assigments List', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        assigment = Assigment.objects.filter(subject = subject, topic=topic)
        user_id = request.user.id
        user_data = User.objects.filter(id = user_id).first()
        submission_ass =AssigmentSubmission.objects.filter(user=user_data, subject = subject, topic=topic)
        previous = []
        submission = []
        submission_late = []
        for ass in submission_ass:
            if ass.status == "submission":
                submission.append(ass)
            elif ass.status == 'Previous assigments':
                previous.append(ass)
            else:
                submission_late.append(ass)

        context = {'topic':topic, 'subject':subject, 'assigment':assigment, 'submission_late':submission_late, 'previous':previous, 'submission':submission}
        return render(request, 'Student/assigments.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def AssigmentsAdd(request, sid, tid):
    if request.method == "POST":
        try:
            Assigment_number = request.POST.get('Assigment_number')
            sub_Topic_id = request.POST.get('sub_Topic')
            Weight = request.POST.get('Weight')
            Description = request.POST.get('Description')
            task = request.POST.get('Task')
            date = request.POST.get('date')
            time = request.POST.get('time')
            Category = request.POST.get('Category')
            file = request.FILES['file']
            subject = Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            type_assigment = AssigmentType.objects.filter(id = Category).first()
            if file == None:
                Assigment.objects.create(name = Assigment_number, description=Description, task = task, date = date, time = time, Weight = Weight, subject = subject,  topic = topic, type= type_assigment)
            else:
                Assigment.objects.create(name = Assigment_number, description=Description, task = task, date = date, time = time, Weight = Weight, file = file, subject = subject,  topic = topic, type= type_assigment)

            messages.success(request,'  Assigment is added successful')
            return redirect(f'../../assigmentsPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        task_assigment = ['Individual', 'Group']
        for i in task_assigment:
            AssigmentType.objects.create(name=i ,weight= 10)
    except:
        pass

    try:
        user_id = request.user.id
        user_data = User.objects.filter(id = user_id).first()
        subject =Subject.objects.filter(id = sid).first()
        user_belong_group = StudentGroup.objects.filter(subject=subject).first()
        topic = Topic.objects.filter(id = tid).first()
        assigment = AssigmentType.objects.all()
        submission_ass =AssigmentSubmission.objects.filter(group=user_belong_group, subject=subject)
        submission = AssigmentSubmission.objects.filter(user=user_data)
        context = {'topic':topic, 'subject':subject, 'assigment':assigment, 'submission':submission, 'submission_ass':submission_ass}
        return render(request, 'Student/add-assigmnents.html', context)
    except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def AssigmentSubmision(request, sid, tid, aid):
    if request.method == "POST":
        # try:
        UserLog.objects.create(task='Submitting assigment', user= request.user)
        file_submitted = request.FILES['file_submitted']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        assigments = Assigment.objects.filter(id=aid).first()

    # try:
        if assigments.type.name == 'Group':
            user_id = request.user.id
            user_data = User.objects.filter(id = user_id).first()
            user_belong_group = StudentGroup.objects.filter(subject=subject).first()
            AssigmentSubmission.objects.create(doc = file_submitted, is_group=True, group=user_belong_group, subject=subject, topic=topic, assigniment=assigments, user=user_data)
            messages.success(request,'Assigment is Submitted  successful')
            return redirect(f'../../../assigmentsPage/{sid}/{tid}')

        else:
            user_id = request.user.id
            user_data = User.objects.filter(id = user_id).first()
            submission = AssigmentSubmission.objects.create(doc = file_submitted, subject=subject, topic=topic, assigniment=assigments, user=user_data)
            assigments_submited = AssigmentSubmission.objects.filter(subject=subject, topic=topic).exists()
            if assigments_submited:
                doc_url_gt = str(submission.doc.url)
                new_url = doc_url_gt.split(r'/')
                new_doc_url_gt = doc_url_gt.join(r'\\')
                print(new_doc_url_gt)
                # similarity= check_file_similarity(new_doc_url_gt)
                similarity = 0.5
                print(similarity)
                if similarity >0.7:
                    submission.delete()
                    messages.info(request,f'Assigment is similar with another assimment in {similarity*100}' )

            messages.success(request,'Assigment is Submitted  successful')
            return redirect(f'../../../assigmentsPage/{sid}/{tid}')
            # except:
            #     messages.error(request,'Something went wrong')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # except:
        #     messages.error(request,'Something went wrong')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        UserLog.objects.create(task='Viewing assigment to be done', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        context = {'topic':topic, 'subject':subject}
        return render(request, 'Student/submit-assigniment.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def UploadAssigments(request, sid, tid, aid):
    UserLog.objects.create(task='Uploading an assigment', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigments = Assigment.objects.filter(id=aid).first()
    user_id = request.user.id
    user_data = User.objects.filter(id = user_id).first()
    student = Student.objects.filter(user = user_data).first()
    student_group = StudentGroupManyToMany.objects.filter(student = student).first()
    stgroup = StudentGroup.objects.filter(id= student_group).first()
    submission_status = AssigmentSubmission.objects.filter(assigniment=assigments, group= stgroup).exists() or AssigmentSubmission.objects.filter(assigniment=assigments, user= user_data).exists()
    context = {'topic':topic, 'subject':subject, 'assigments':assigments, 'submission_status':submission_status}
    return render(request, 'Student/assigment-upload.html', context)

@login_required(login_url='/')
def marksAssigments(request, sid, tid, aid):
    UserLog.objects.create(task='Viewing page for assign marks to assigment', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    submission_ass =AssigmentSubmission.objects.all()

    context = {'topic':topic, 'subject':subject, 'submission_ass':submission_ass}
    return render(request, 'Student/assigment-marks.html', context)

def resubmit(request, sid, tid, aid):
    if request.method == "POST":
        UserLog.objects.create(task='Resubmitting an assiment', user= request.user)
        file_submitted = request.FILES['file_submitted']
        assigment =Assigment.objects.filter(id = aid).first()
        submission_ass =AssigmentSubmission.objects.filter(assigniment = assigment).first()
        try:
            submission_ass_url = submission_ass.doc.url
            os.remove(submission_ass_url)
        except:
            pass

        submission_ass.doc = file_submitted
        submission_ass.save()
        messages.success(request,'assigment is submitted successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def assignMarksToAssigment(request, sid, tid, aid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='assignining marks to an assiment', user= request.user)
            marks = request.POST.get('marks')
            remark = request.POST.get('remark')
            submission_ass =AssigmentSubmission.objects.filter(id = aid).first()
            submission_ass.marks = marks
            submission_ass.remark =remark
            submission_ass.save()
            messages.success(request,'marks is assigned successful')
            return redirect(f'../../../assigmentsPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def AssigmentsEdit(request, sid, tid, id):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='updating an assiment', user= request.user)
            Assigment_number = request.POST.get('Assigment_number')
            sub_Topic_id = request.POST.get('sub_Topic')
            Description = request.POST.get('Description')
            Weight = request.POST.get('Weight')
            task = request.POST.get('Task')
            date = request.POST.get('date')
            time = request.POST.get('time')
            Category = request.POST.get('Category')

            subject = Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            type_assigment = AssigmentType.objects.filter(id = Category).first()
            assigment = Assigment.objects.filter(id = id).first()
            assign_url = settings.STATICFILES_DIRS[0] +assign.file.url
            assigment.name = Assigment_number
            assigment.description=Description
            assigment.task = task
            assigment.date = date
            assigment.time = time
            assigment.subject = subject
            assigment.Weight =Weight
            assigment.topic = topic
            assigment.type= type_assigment
            assigment.save()
            os.remove(assign_url)
            messages.success(request,'Assigment is updated successful')
            return redirect(f'../../../assigmentsPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    UserLog.objects.create(task='Edit an assiment', user= request.user)
    assigments = Assigment.objects.filter(id=id).first()
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigment = AssigmentType.objects.all()
    context = {'topic':topic, 'subject':subject, 'assigments':assigments, 'assigment':assigment}
    return render(request, 'Student/edit-Assigments.html', context)

@login_required(login_url='/')
def AssigmentsDelete(request, sid, id):
    UserLog.objects.create(task='deleting an assiment', user= request.user)
    assign = Assigment.objects.filter(id = id).first()
    try:
        assign_url = settings.STATICFILES_DIRS[0] +assign.file.url
        os.remove(assign_url)
    except:
        pass
    finally:
        assign.delete()
        messages.success(request,'Student is deleted successful')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def AddAssigmentMarks(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/add-assigmnents-marks.html', context)

@login_required(login_url='/')
def discussionsPage(request, sid, tid):
    if request.method == 'POST':
        try:
            UserLog.objects.create(task='sending a message', user= request.user)
            message = request.POST.get('message')
            user_id = request.user.id
            user_data = User.objects.filter(id= user_id).first()
            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            GroupDiscussionsMessage.objects.create(message=message, topic=topic, subject=subject, sender=user_data)
            return redirect(f'../../discussionsPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    UserLog.objects.create(task='viewing Discussion Page', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    messages = GroupDiscussionsMessage.objects.all()
    context = {'topic':topic, 'subject':subject, 'messages':messages}
    return render(request, 'Student/discussions.html', context)

@login_required(login_url='/')
def groupsPage(request, sid, tid):
    UserLog.objects.create(task='viewing group page', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    groups = StudentGroup.objects.filter(subject=subject)
    context = {'topic':topic, 'subject':subject, 'groups':groups}
    return render(request, 'Student/groups.html', context)

@login_required(login_url='/')
def groupAdd(request, sid):
    if request.method == "POST":
        UserLog.objects.create(task='add group Discussion', user= request.user)
        name = request.POST.get('name')
        logo = request.FILES['logo']
        description = request.POST.get('description')
        type_group = request.POST.get('type_group')
        participants = request.POST.get('participants')

        print(sid)
        try:
            grouptype = StudentGroupType.objects.filter(id = type_group).first()
            if grouptype.name == 'Public':
                subject = Subject.objects.filter(id = int(sid)).first()
                for user_id in participants:
                    user_data = User.objects.filter(id = user_id).first()
                    student_data = Student.objects.filter(user = user_data).first()
                    group =StudentGroup.objects.create(name = name, description= description, file = logo, type_group= grouptype, subject = subject)
                    StudentGroupManyToMany.objects.create(student = student_data, group=group)
                    messages.success(request,'group is created sacessfull')
                return redirect(f'../../TopicList/{sid}')

            else:
                subject = Subject.objects.filter(id = sid).first()
                for user_id in participants:
                    user_data = User.objects.filter(id= user_id).first()
                    token = ''
                    letter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'l', 'k', 'j', 'h', 'g', 'f', 'd', 's', 'a', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
                    random_number = str(random.randint(1000, 9999))
                    genereted_letter = ''
                    for i in range(3):
                        index_letter = random.randint(0, len(letter)-1)
                        letter_selected = letter[index_letter]
                        genereted_letter += letter_selected + random_number[i]
                    group = StudentGroup.objects.create(name = name, description= description, token=genereted_letter, file = logo, type_group= grouptype, subject = subject)
                    StudentGroupManyToMany.objects.create(user = user_data, group=group, user_isaccept='Accepted')
                    messages.success(request,'group is created sacessfull')
                return redirect(f'../../TopicList/{sid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        groups_dtype = ['Public', 'Private']
        for i in groups_dtype:
            StudentGroupType.objects.create(name=i)
    except:
        pass

    UserLog.objects.create(task='add group Discussion Page', user= request.user)
    user_id = request.user.id
    student_info = Student.objects.filter(id = user_id).first()

    subject =Subject.objects.filter(id = sid).first()
    users = Student.objects.all()
    assigment = AssigmentType.objects.all()
    Grouptype = StudentGroupType.objects.all()
    context = {'subject':subject, 'Grouptype':Grouptype, 'users':users}
    return render(request, 'Student/create-group.html', context)

@login_required(login_url='/')
def JoinToGroup(request, id):
    try:
        UserLog.objects.create(task='joining to  group Discussion', user= request.user)
        user_id = request.user.id
        user = User.objects.filter(id = user_id).first()
        student = Student.objects.filter(user = user).first()
        group = StudentGroup.objects.filter(id= id).first()
        group_id = group.id
        StudentGroupManyToMany.objects.create(group = group, student = student)
        messages.success(request,'Congratulation you have sacessfull joined to the group')
        return redirect(f'../groupContent/{group_id}')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def groupContent(request, id):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='add comment', user= request.user)
            message = request.POST.get('message')
            user_id = request.user.id
            User_info = User.objects.filter(id = user_id).first()
            post = GroupPost.objects.filter(id = id).first()
            GroupPostComent.objects.create(message= message, post = post, sender = User_info)
            messages.success(request,'comment is sent')
            return redirect(f'../groupContent/{id}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    UserLog.objects.create(task='Viewing group content', user= request.user)
    group = StudentGroup.objects.filter(id= id).first()
    posts = GroupPost.objects.filter(group = group)
    assigment_group = AssigmentType.objects.filter(name = 'Group').first()
    assigment_assigned = Assigment.objects.filter(type = assigment_group).count()
    assigmentNotComplited = AssigmentSubmission.objects.filter(group = group, marks = 0).count()
    assigmentSubmitted = AssigmentSubmission.objects.filter(group = group).count()
    assigmentComplited = assigmentSubmitted- assigmentNotComplited
    user_id = request.user.id
    users = Student.objects.all()
    students_data = StudentGroupManyToMany.objects.filter(group = group)
    # students = []
    # for student in students_data:
    #     data = student.student.registration_no
    #     print(data)
    #     students.append(student)

    post_comment = []
    for post in posts:
       comments = GroupPostComent.objects.filter(post=post)
       no_likes = GroupPostLike.objects.filter(message_liked = post).count()
       no_comments = comments.count()
       comments_dict ={'post':post, 'comments':comments, 'no_comments':no_comments, 'no_likes':no_likes}
       post_comment.append(comments_dict)

    submitted = AssigmentSubmission.objects.filter(group = group)
    marks =0
    for sub in submitted:
        marks += sub.marks
    student_group = StudentGroupManyToMany.objects.filter(group = group).first()
    tasks = StudentTask.objects.filter(groupStudent = student_group)
    print(tasks)
    context = {'group':group, 'users':users, 'students_data':students_data, 'post_comment':post_comment, 'assigment_assigned':assigment_assigned, 'assigmentComplited': assigmentComplited, 'assigmentSubmitted':assigmentSubmitted, 'marks':marks, 'tasks':tasks}
    return render(request, 'Student/group-content.html', context)

@login_required(login_url='/')
def groupPost(request, id):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='add group post', user= request.user)
            message = request.POST.get('message')
            user_id = request.user.id
            group = StudentGroup.objects.filter(id= id).first()
            User_info = User.objects.filter(id = user_id).first()
            group_id = group.id
            GroupPost.objects.create(message= message, has_topic = False, subject = group.subject, group= group, sender = User_info)
            messages.success(request,'group post is created successful')
            return redirect(f'../groupContent/{group_id}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    UserLog.objects.create(task='add group post page', user= request.user)
    group = StudentGroup.objects.filter(id= id).first()
    context = {'group':group}
    return render(request, 'Student/add-post.html', context)

@login_required(login_url='/')
def groupPostLikes(request, id):
    UserLog.objects.create(task='add group like', user= request.user)
    user_id = request.user.id
    User_info = User.objects.filter(id = user_id).first()
    post = GroupPost.objects.filter(id = id).first()
    like = GroupPostLike.objects.filter(sender = User_info, message_liked = post)
    if like:
        print('present')
        GroupPostLike.objects.create(likes= True, message_liked = post, sender = User_info)
        messages.success(request,'like is added successful')

        # like.delete()
#             messages.success(request,'Student is deleted successful')

        return redirect(f'../groupContent/{id}')
    else:
        GroupPostLike.objects.create(likes= True, message_liked = post, sender = User_info)
        messages.success(request,'like is added successful')
        return redirect(f'../groupContent/{id}')
    return redirect(f'../groupContent/{id}')

@login_required(login_url='/')
def groupEdit(request, sid, id):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='update group Discussion', user= request.user)
            Assigment_number = request.POST.get('Assigment_number')
            sub_Topic_id = request.POST.get('sub_Topic')
            Description = request.POST.get('Description')
            Weight = request.POST.get('Weight')
            task = request.POST.get('Task')
            date = request.POST.get('date')
            time = request.POST.get('time')
            Category = request.POST.get('Category')

            subject = Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            type_assigment = AssigmentType.objects.filter(id = Category).first()
            assigment = Assigment.objects.filter(id = id).first()
            assigment.name = Assigment_number
            assigment.description=Description
            assigment.task = task
            assigment.date = date
            assigment.time = time
            assigment.subject = subject
            assigment.Weight =Weight
            assigment. topic = topic
            assigment.type= type_assigment
            assigment.save()
            messages.success(request,'assigment is added successful')
            return redirect(f'../../../groupPage/{sid}')
        except:
                messages.error(request,'Something went wrong')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    UserLog.objects.create(task='edit group Discussion page', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject, 'group':group, }
    return render(request, 'Student/edit-group.html', context)

@login_required(login_url='/')
def groupDelete(request, sid):
    try:
        UserLog.objects.create(task='delete group Discussion', user= request.user)
        Assigment.objects.filter(id = id).first().delete()
        messages.success(request,'group is deleted successful')
        return redirect(f'../../TopicList/{sid}')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def RemoveStudentGroup(request, gid, sid):
    try:
        UserLog.objects.create(task='remove student from group', user= request.user)
        group = StudentGroup.objects.filter(id=gid).first()
        students = Student.objects.filter(id =sid).first()
        students_data = StudentGroupManyToMany.objects.filter(group = group, student= students)
        students_data.delete()
        messages.success(request,'Student is removed successful')
        return redirect(f'../../groupContent/{gid}')

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def LeftStudentGroup(request, gid):
    try:
        UserLog.objects.create(task='student left group Discussion', user= request.user)
        group = StudentGroup.objects.filter(id=gid).first()
        user_id = request.user.id
        User_info = User.objects.filter(id = user_id).first()
        students = Student.objects.filter(user= User_info).first()
        students_data = StudentGroupManyToMany.objects.filter(group = group, student= students)
        students_data.delete()
        messages.success(request,'Student is left the successful')
        return redirect(f'../../groupContent/{gid}')

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def AddGroupActivities(request, gid):
    if request.method == "POST":
        UserLog.objects.create(task='assigning task to each group member', user= request.user)
        group = StudentGroup.objects.filter(id=gid).first()
        students_data = StudentGroupManyToMany.objects.filter(group__id = gid)
        tasks = []
        date =[]
        for stud in students_data:
            work =  request.POST.get(f'work_{stud.student.id}')
            task = request.POST.get(f'task_{stud.student.id}')
            date = request.POST.get(f'date_{stud.student.id}')
            group = StudentGroup.objects.filter(id=gid).first()
            sender = User.objects.filter(id = request.user.id).first()
            GroupWorkDivision.objects.create(work_description= work, task = task, sender = sender)
            work_division = GroupWorkDivision.objects.all().order_by('-id').first()
            StudentTask.objects.create(groupStudent = stud, work = work_division)
        return redirect(f'../../groupContent/{gid}')

    UserLog.objects.create(task='viewing  assigned task', user= request.user)
    group = StudentGroup.objects.filter(id=gid).first()
    students_group = StudentGroupManyToMany.objects.filter(group = group)
    context ={'students_group':students_group}
    return render(request, 'Student/Add-activity.html', context)


@login_required(login_url='/')
def anauncementPage(request, sid, tid):
    UserLog.objects.create(task='viewing an anounciments', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    user_id = request.user.id
    user_info = User.objects.filter(id = user_id).first()
    anaunciment_type = AnnouncimentType.objects.filter(name= 'Inbox').first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, announcimentType=anaunciment_type, is_deleted=False)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

@login_required(login_url='/')
def anauncementSentPage(request, sid, tid):
    UserLog.objects.create(task='viewing sent anounciments', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    user_id = request.user.id
    user_info = User.objects.filter(id = user_id).first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, sender=user_info, is_deleted=False)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

@login_required(login_url='/')
def anauncementTrashPage(request, sid, tid):
    UserLog.objects.create(task='viewing trash anounciments', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, is_deleted=True)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

@login_required(login_url='/')
def anauncementContentPage(request, sid, tid, anid):
    try:
        UserLog.objects.create(task='viewing an anounciments content', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        anaunciment = Announciment.objects.filter(id = anid).first()
        anaunciment.is_opened = True
        anaunciment.save()
        messages.success(request,'Student is deleted successful')

        context = {'topic':topic, 'subject':subject, 'anaunciment':anaunciment}
        return render(request, 'Student/anauncement-content.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def anauncementSoftDeletePage(request, sid, tid, anid):
    UserLog.objects.create(task='deleting an anounciments', user= request.user)
    anaunciment = Announciment.objects.filter(id = anid).first()
    if anaunciment.is_deleted == False:
        anaunciment.is_deleted= True
        anaunciment.save()
        messages.success(request,'Anounciment is deleted successful')

    else:
        anaunciment.delete()
        messages.success(request,'Anounciment is deleted successful')

    return redirect(f'../../../anauncementPage/{sid}/{tid}')

@login_required(login_url='/')
def ComposeAnaunciment(request, sid, tid):
    if request.method == 'POST':
        UserLog.objects.create(task='sending an anounciments', user= request.user)
        message = request.POST.get('message')
        title = request.POST.get('title')
        reciever = request.POST.get('reciever')
        user_id = request.user.id
        user_info = User.objects.filter(id = user_id).first()

        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        anaunciment_type = AnnouncimentType.objects.filter(name= 'Inbox').first()
        anaunciment = Announciment.objects.create(title = title, message=message, sender=user_info, announcimentType=anaunciment_type, topic=topic, subject=subject)

        if reciever == 'all':
            studentSubject = StudentSubject.objects.filter(subject= subject)
            for i in studentSubject:
                i.student.anaunciment = anaunciment
                i.save()
                messages.success(request,'Student is deleted successful')

        return redirect(f'../../anauncementPage/{sid}/{tid}')

    types = ['Inbox', 'Important', 'Sent', 'Draft', 'Trash']
    for i in types:
        try:
            AnnouncimentType.objects.create(name =i)
        except:
            pass


    UserLog.objects.create(task='composing an anounciments', user= request.user)
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/compose-anaunciments.html', context)

def Draft_add(request, sid, tid):
    if request.method == 'POST':
        try:
            UserLog.objects.create(task='adding to draft anounciments', user= request.user)
            message = request.POST.get('message')
            title = request.POST.get('title')
            reciever = request.POST.get('reciever')
            user_id = request.user.id
            user_info = User.objects.filter(id = user_id).first()

            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            anaunciment_type = AnnouncimentType.objects.filter(name= 'Draft').first()
            anaunciment = Announciment.objects.create(title = title, message=message, sender=user_info, announcimentType=anaunciment_type, topic=topic, subject=subject)
            messages.success(request,'Announciment is added successful')
            return redirect(f'../../anauncementPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def TutorialPage(request, sid, tid):
    try:
        UserLog.objects.create(task='viewing tutorial page', user= request.user)
        tutorial_id = 1
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(subject = subject, topic=topic).first()
        context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
        return render(request, 'Student/tutorials.html', context)
    except:
        return redirect(f'../../TutorialAdd/{sid}/{tid}')

@login_required(login_url='/')
def PreviousPage(request, sid, tid, preid):
    try:
        UserLog.objects.create(task='viewing previous tutorial', user= request.user)
        tutorial_id = int(preid) -1
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(id = tutorial_id).first()
        context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
        return render(request, 'Student/tutorials.html', context)
    except:
        return redirect(f'TutorialAdd/{sid}/{tid}')


@login_required(login_url='/')
def NextTuturial(request, sid, tid, tuid):
    try:
        UserLog.objects.create(task='viewing next tutorial', user= request.user)
        tutorial_id = int(tuid)+1
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(id = tutorial_id).first()
        context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
        return render(request, 'Student/tutorials.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def TutorialAdd(request, sid, tid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='add tutorial', user= request.user)
            Tutorial_title = request.POST.get('Tutorial_title')
            Description = request.POST.get('Description')
            file_data = request.FILES['file']
            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            books = Tutorial.objects.create(title = Tutorial_title, description=Description, file= file_data, topic = topic, subject= subject)
            messages.success(request,'tutorial is added successful')
            return redirect(f'../../TutorialPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        UserLog.objects.create(task='view add tutorial page', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        context = {'topic':topic, 'subject':subject}
        return render(request, 'Student/add-tutorial.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def TutorialEdit(request, sid, tid, tuid):
    if request.method == "POST":
        try:
            UserLog.objects.create(task='update tutorial', user= request.user)
            Tutorial_title = request.POST.get('Tutorial_title')
            Description = request.POST.get('Description')
            file_data = request.FILES['file']
            subject =Subject.objects.filter(id = sid).first()
            topic = Topic.objects.filter(id = tid).first()
            tutorial = Tutorial.objects.filter(id = tuid).first()
            tutorial_url = settings.STATICFILES_DIRS[0] +tutorial.file.url
            tutorial.title = Tutorial_title
            tutorial.description=Description
            tutorial.file= file_data
            tutorial.topic = topic
            tutorial.subject= subject
            tutorial.save()
            os.remove(tutorial_url)
            messages.success(request,'tutorial is updated successful')
            return redirect(f'../../../TutorialPage/{sid}/{tid}')
        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        UserLog.objects.create(task='edit tutorial', user= request.user)
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(id = tuid).first()

        context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
        return render(request, 'Student/edit-tutorial.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@api_view(['GET', 'POST'])
def tutorialTrackingApi(request, tuid, time):
 # if request.method == "POST":
    print(request)
    time = request.GET.get('time')
    tutorialId = request.GET.get('tutorialId')
    if time:
        user = request.user
        obj_exist = TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial).exists()
        if obj_exist:
            obj= TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial).first()
            if obj.time < time:
                obj.time = time
                obj.save()
        else:
            TutorialTimeTacking.objects.create(time = time, user = user, tutorial__id__gt = tutorialId)

    obj= TutorialTimeTacking.objects.filter(user = request.user, tutorial = tutorial).first()
    data = {'tuturiatdata':obj}

    return data
