from django.shortcuts import render, redirect, HttpResponseRedirect
from schools.models import Department, Course, Subject, SchoolLevel, StudentClass, CourseSubject, SubjectClass, UserLog
from OnlineLearning.models import Student,DefaultUsers,StudentSubject, Book, Assigment, AssigmentType, Topic
from OnlineLearning.models import Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd

@login_required(login_url='/')
def view_schools(request, id):
    UserLog.objects.create(task='Viewing schools List', user= request.user)
    school_info = schools.objects.filter(id = id).first()
    context = {'school_info':school_info}
    return render(request, 'UAA/view-school.html', context)


@login_required(login_url='/')
def schoolList(request):
    school_info = School.objects.all()
    context = {'school_info':school_info}
    UserLog.objects.create(task='Viewing schools List', user= request.user)
    return render(request, 'Admin/list-school.html', context)


@login_required(login_url='/')
def schoolAdd(request):
    if request.method == "POST":
        school_name = request.POST.get('school_name')
        schoo_logo = request.POST.get('schoo_logo')
        school_level = request.POST.get('school_level')
        school_adress = request.POST.get('school_adress')
        head_of_school = request.POST.get('head_of_school')
        school_domain = request.POST.get('school_domain')
        school_obj =School(schema_name = school_name, school_name= school_name,schoo_logo =schoo_logo, school_level= school_level, school_adress =school_adress, head_of_school = head_of_school)
        school_obj.save()
        domain = Domain()
        domain.domain = school_domain # don't add your port or www here! on a local server you'll want to use localhost here
        domain.tenant = school_obj
        domain.is_primary = True
        domain.save()
        UserLog.objects.create(task='Adding schools', user= request.user)
        return redirect('schoollist')
    context ={}
    return render(request, 'Admin/add-school.html', context)


@login_required(login_url='/')
def schoolEdit(request, id):
    context = {}
    UserLog.objects.create(task='Edit schools', user= request.user)
    return render(request, 'Admin/edit-school.html', context)


@login_required(login_url='/')
def schoolDelete(request, id):
    School.objects.filter(id = id).first().delete()
    UserLog.objects.create(task='Delete School', user= request.user)
    return redirect('schoollist')

@login_required(login_url='/')
def DepartmentList(request):
    UserLog.objects.create(task='Viewing Department List', user= request.user)
    department = Department.objects.all()
    context = {'department':department}
    return render(request, 'Admin/list-department.html', context)


@login_required(login_url='/')
def DepartmentAdd(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        department_start_date = request.POST.get('department_start_date')
        department_Hod = request.POST.get('department_Hod')

        depart = Department(name=department_name, department_Hod=department_Hod, start_date=department_start_date)
        depart.save()
        UserLog.objects.create(task='Adding Department', user= request.user)

        return redirect('Departmentlist')
    return render(request, 'Admin/add-department.html')


@login_required(login_url='/')
def DepartmentEdit(request, id):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        department_start_date = request.POST.get('department_start_date')
        department_Hod = request.POST.get('department_Hod')
        department = Department.objects.filter(id=id).first()
        department.name=department_name
        department.department_Hod=department_Hod
        department.start_date=department_start_date
        department.save()
        UserLog.objects.create(task='Edit Department', user= request.user)
        return redirect('Departmentlist')

    department = Department.objects.filter(id=id).first()
    context = {'department':department}
    return render(request, 'Admin/edit-department.html', context)


@login_required(login_url='/')
def DepartmentDelete(request, id):
    Department.objects.filter(id = id).first().delete()
    UserLog.objects.create(task='Delete Department', user= request.user)
    return redirect('Departmentlist')



@login_required(login_url='/')
def SubjectList(request):
    user_id = request.user.id
    user = User.objects.filter(id = user_id).first()
    student_info = Student.objects.filter(user=user).first()
    Subjects = StudentSubject.objects.filter(student=student_info, classCurrent = student_info.classCurrent)
    context = {'Subjects':Subjects}
    UserLog.objects.create(task='Viewing Subject List', user= request.user)
    return render(request, 'Admin/list-subject.html', context)


@login_required(login_url='/')
def SubjectRegistration(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.filter(id = user_id).first()
        student_info = Student.objects.filter(user=user).first()
        stud_subjects = CourseSubject.objects.filter(course=student_info.course)
        student = Student.objects.filter(user=user).first()

        for sub_course in stud_subjects:
            subject_exist =StudentSubject.objects.filter(student=student, subject=sub_course.subject, classCurrent=student_info.classCurrent).exists()
            if not subject_exist:
                StudentSubject.objects.create(student=student, subject=sub_course.subject, classCurrent=student_info.classCurrent)
                UserLog.objects.create(task='Making Subject Registration', user= request.user)

        return redirect('Subjectlist')

    user_id = request.user.id
    user = User.objects.filter(id = user_id).first()
    student_info = Student.objects.filter(user=user).first()
    stud_subjects = SubjectClass.objects.filter(studentClass=student_info.classCurrent)
    context = {'stud_subjects':stud_subjects,}
    return render(request, 'Admin/subject registration.html', context)

def Curruculum(request):
    if request.method == 'POST':
        file_doc = request.FILES['file']

        # questions_path = settings.STATICFILES_DIRS[0] +r'\csv files\final_generatedQuestions.csv'
        data = pd.read_csv(file_doc)
        for index in data.index:
            subject = data['subject'][index]
            studentclass = data['class'][index]
            topic = data['topic'][index]
            # course = Course.objects.filter(name= 'Science & Arts').first()
            studentclass_obj = StudentClass.objects.filter(name = studentclass).first()
            subject_obj = Subject.objects.filter(subject_name = subject).first()
            subject_class_obj = SubjectClass.objects.filter(studentClass =studentclass_obj, subject = subject_obj).first()
            # CourseSubject.objects.create(course = course, subject = subject_obj, studentClass =subject_class_obj )
            Topic.objects.create(name = topic, description = '', subject = subject_class_obj)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def SubjectAdd(request):
    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        department = request.POST.get('department')
        department_selected = Department.objects.filter(id=department).first()
        subject = Subject(subject_code =subject_code, subject_name=subject_name)
        subject.department = department_selected
        subject.save()
        UserLog.objects.create(task='Adding Subject', user= request.user)
        return redirect('Subjectlist')
    department = Department.objects.all()
    context = {'department':department}

    return render(request, 'Admin/add-subject.html', context)


@login_required(login_url='/')
def SubjectEdit(request, id):
    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        department = request.POST.get('department')
        Subject_obj = Subject.objects.filter(id=id).first()

        department_selected = Department.objects.filter(id=department).first()
        Subject_obj.subject_code = subject_code
        Subject_obj.subject_name = subject_name
        Subject_obj.department = department_selected
        subect_obj.save()
        UserLog.objects.create(task='Edit Subjects', user= request.user)
        return redirect('Subjectlist')

    Subject = Subject.objects.filter(id=id).first()
    context = {'Subject':Subject}
    return render(request, 'Admin/edit-subject.html', context)

@login_required(login_url='/')
def SubjectDelete(request, id):
    subject =Subject.objects.filter(id = id).first()
    subject.delete()
    UserLog.objects.create(task='Delete Subject', user= request.user)
    return redirect('Subjectlist')



@login_required(login_url='/')
def SchoolLevelList(request):
    schoolLevels = SchoolLevel.objects.all()
    context = {'schoolLevels':schoolLevels}
    UserLog.objects.create(task='Viewing Levels List', user= request.user)
    return render(request, 'Admin/list-SchoolLevel.html', context)


@login_required(login_url='/')
def SchoolLevelAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        schoolLevel = SchoolLevel.objects.create(name=name)
        UserLog.objects.create(task='Adding School Level', user= request.user)
        return redirect('SchoolLevellist')
    department = Department.objects.all()
    context = {'department':department}

    return render(request, 'Admin/add-SchoolLevel.html', context)


@login_required(login_url='/')
def SchoolLevelEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        SchoolLevel_obj = SchoolLevel.objects.filter(id=id).first()
        SchoolLevel_obj.name = name
        SchoolLevel_obj.save()
        UserLog.objects.create(task='Edit levels', user= request.user)
        return redirect('SchoolLevellist')

    schoolLevel = SchoolLevel.objects.filter(id=id).first()
    context = {'schoolLevel':schoolLevel}
    return render(request, 'Admin/edit-SchoolLevel.html', context)


@login_required(login_url='/')
def SchoolLevelDelete(request, id):
    schoolLevel =SchoolLevel.objects.filter(id = id).first()
    schoolLevel.delete()
    UserLog.objects.create(task='Delete Level', user= request.user)
    return redirect('SchoolLevellist')



@login_required(login_url='/')
def StudentClassList(request):
    studentClasss = StudentClass.objects.all()
    context = {'studentClasss':studentClasss}
    UserLog.objects.create(task='Viewing classes List', user= request.user)
    return render(request, 'Admin/list-StudentClass.html', context)


@login_required(login_url='/')
def StudentClassAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id = level).first()
        StudentClass.objects.create(name=name, level=level_obj)
        UserLog.objects.create(task='Adding class', user= request.user)
        return redirect('StudentClasslist')
    schoolLevels = SchoolLevel.objects.all()
    context = {'schoolLevels':schoolLevels}

    return render(request, 'Admin/add-StudentClass.html', context)


@login_required(login_url='/')
def StudentClassEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id = level).first()
        StudentClass_obj = StudentClass.objects.filter(id=id).first()

        level = StudentClass_obj.update(name = name, level=level_obj)
        level.save()
        UserLog.objects.create(task='Edit student Class', user= request.user)
        return redirect('StudentClasslist')

    schoolLevels = SchoolLevel.objects.all()
    studentClass = StudentClass.objects.filter(id=id).first()
    context = {'studentClass':studentClass, 'schoolLevels':schoolLevels}
    return render(request, 'Admin/edit-StudentClass.html', context)


@login_required(login_url='/')
def StudentClassDelete(request, id):
    studentClass =StudentClass.objects.filter(id = id).first()
    studentClass.delete()
    UserLog.objects.create(task='Delete classes', user= request.user)
    return redirect('StudentClasslist')

@login_required(login_url='/')
def CourseList(request):
    Courses = Course.objects.all()
    context = {'Courses':Courses}
    UserLog.objects.create(task='Viewing Course List', user= request.user)
    return render(request, 'Admin/list-Course.html', context)

@login_required(login_url='/')
def CourseAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        department = request.POST.get('department')
        department_selected = Department.objects.filter(id=department).first()
        Course = Course.objects.create(name=name, department=department_selected)
        messages.success(request,'Course added successful')
        UserLog.objects.create(task='Adding Course', user= request.user)
        return redirect('Courselist')
    department = Department.objects.all()
    context = {'department':department}

    return render(request, 'Admin/add-Course.html', context)


@login_required(login_url='/')
def CourseEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        department = request.POST.get('department')

        Course_obj = Course.objects.filter(id=id).first()
        department_selected = Department.objects.filter(id=department).first()
        Course_obj.name = name
        Course_obj.department = department_selected
        Course_obj.save()
        messages.success(request,'Course updated successful')
        UserLog.objects.create(task='Edit Course', user= request.user)
        return redirect('Courselist')

    Courses = Course.objects.filter(id=id).first()
    department = Department.objects.all()
    context = {'department':department, 'Courses':Courses}
    return render(request, 'Admin/edit-Course.html', context)


@login_required(login_url='/')
def CourseDelete(request, id):
    Course.objects.filter(id = id).first().delete()
    messages.success(request,'Course deleted successful')
    UserLog.objects.create(task='Delete Course', user= request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

