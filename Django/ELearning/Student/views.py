from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
from Student.models import Student,DefaultUsers, Book, Assigment, AssigmentType, Topic, Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from schools.models import Subject, Department, StudentClass
import random

# Create your views here.
def UploadSelectedStudentPage(request):
    csv_path = settings.STATICFILES_DIRS[0] +r'\csv files\school.csv'
    data = pd.read_csv(csv_path)
    for index, row in data.iterrows():
        DefaultUsers.objects.create(number=row['number'], name=row['name'], school_selected=row['school_selected'], course=row['course'], type=row['type'], location=row['location'])
    courses = data['course'].unique()
    for i in courses:
        Course.objects.create(name=i)
    return render(request, 'UAA/register.html')

def searchUserSelected(request):

    index_number = request.POST.get('index_number')
    user_info = DefaultUsers.objects.filter(number=index_number).first()
    current_class = StudentClass.objects.all()
    context = {'user_info':user_info, 'current_class':current_class}
    return render(request, 'UAA/register.html', context)

def submitRegistration(request):
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
        user_info_details = User.objects.filter(username=email).first()
        current_class = StudentClass.objects.filter(id = class_level).first()
        course = Course.objects.filter(name = user_info.course).first()
        student = Student.objects.create(name=user_info.name,
                                         registration_no=registration_no, 
                                         index_number=index_number, 
                                         gender= 'M', 
                                         date_of_birth=bod, 
                                         phone_number=phone_no, 
                                         user=user_info_details, 
                                         course=course, 
                                         classCurrent=current_class)
        return redirect('loginPage')
    
def registerPage(request):
    current_class = StudentClass.objects.all()
    context = {'current_class':current_class}
    return render(request, 'UAA/register.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user =authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('DashboardPage')
        else:
            return redirect('loginPage')

    return render(request, 'UAA/login.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

def userProfilePage(request):
    return render(request, 'Admin/profile.html')

def DashboardPage(request):
    return render(request, 'Admin/dashboard.html')


def studentList(request):
    stud = Student.objects.all()
    context = {'stud':stud}
    return render(request, 'Admin/list-student.html', context)

def studentAdd(request):
    return render(request, 'Admin/add-student.html')

def studentEdit(request, id):
    return render(request, 'Admin/edit-student.html')

def studentDelete(request, id):
    Student.objects.filter(id = id).delete()
    return redirect('studentlist')

def examList(request):
    context = {}
    return render(request, 'Admin/list-exam.html', context)

def MakeApointmentAdd(request):
    return render(request, 'Admin/add-exam.html')



def TopicList(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    Topic_info = Topic.objects.filter(subject = subject)
    context = {'Topic_info':Topic_info, 'subject':subject}
    return render(request, 'Student/topics.html', context)

def TopicAdd(request, sid):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        subject = request.POST.get('subject')
        subject =Subject.objects.filter(id = sid).first()
        depart = Topic(name=name, description=description, subject=subject)
        depart.save()
        return redirect(f'../TopicList/{sid}')
    
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/add-topics.html', context)

def TopicEdit(request, sid, id):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        subject_id = request.POST.get('subject')
        subject =Subject.objects.filter(id = subject_id).first()
        topic = Topic.objects.filter(id=id).first()
        topic.name=name
        topic.description=description
        topic.subject=subject
        topic.save()
        return redirect(f'../../TopicList/{sid}')
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id=id).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/edit-Topic.html', context)

def TopicDelete(request, sid, id):
    topic = Topic.objects.filter(id = id).first()
    topic.delete()
    return redirect(f'../../TopicList/{sid}')

def ElearningPage(request, sid, tid,):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/elearning.html', context)

def NotesPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/notes.html', context)


def booksPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()

    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/books.html', context)
 
def BooksAdd(request, sid, tid):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        description = request.POST.get('description')
        type = request.POST.get('type')
        file = request.POST.get('file')
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        books = Book.objects.create(name=name, author=author, type=type, description=description, file= file, topic = topic, subject= subject)
        return redirect('booksPage')
    
    department = Department.objects.all()
    topic = Topic.objects.filter(id = tid).first()
    subject =Subject.objects.filter(id = sid).first()
    context = {'department':department, 'topic':topic, 'subject':subject}
  
    return render(request, 'Student/add-Books.html', context)

def BooksEdit(request, sid, tid, id):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        description = request.POST.get('description')
        type = request.POST.get('type')
        file = request.POST.get('file')
            
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        Books_obj = Book.objects.filter(id=id).first()
        level = Books_obj.update(name = name)
        Books_obj.name=name 
        Books_obj.author=author 
        Books_obj.type=type 
        Books_obj.description=description 
        Books_obj.file= file
        Books_obj.subject = subject
        Books_obj.topic = topic
        Books_obj.save()
        return redirect('booksPage')
    
    books = Book.objects.filter(id=id).first()
    subject =Subject.objects.filter(id = sid).first()

    context = {'books':books, 'subject':subject}
    return render(request, 'Student/edit-Books.html', context)

def BooksDelete(request, sid, id):
    books =Book.objects.filter(id = id).first()
    books.delete()
    return redirect('booksPage')


def assigmentsPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigment = Assigment.objects.all()
    context = {'topic':topic, 'subject':subject, 'assigment':assigment}
    return render(request, 'Student/assigments.html', context)

def AssigmentsAdd(request, sid, tid):
    if request.method == "POST":
        Assigment_number = request.POST.get('Assigment_number')
        sub_Topic_id = request.POST.get('sub_Topic')
        Weight = request.POST.get('Weight')
        Description = request.POST.get('Description')
        task = request.POST.get('Task')
        date = request.POST.get('date')
        time = request.POST.get('time')
        Category = request.POST.get('Category')
        
        subject = Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        type_assigment = AssigmentType.objects.filter(id = Category).first()
        Assigment.objects.create(name = Assigment_number, description=Description, task = task, date = date, time = time, Weight = Weight, subject = subject,  topic = topic, type= type_assigment)
        return redirect(f'../../assigmentsPage/{sid}/{tid}')
    
    
    try:
        task_assigment = ['Individual', 'Group']
        for i in task_assigment:
            AssigmentType.objects.create(name=i ,weight= 10)
    except:
        pass
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigment = AssigmentType.objects.all()
    context = {'topic':topic, 'subject':subject, 'assigment':assigment}
  
    return render(request, 'Student/add-assigmnents.html', context)

def AssigmentsEdit(request, sid, tid, id):
    if request.method == "POST":
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
        return redirect(f'../../../assigmentsPage/{sid}/{tid}')
    
    assigments = Assigment.objects.filter(id=id).first()
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigment = AssigmentType.objects.all()
    context = {'topic':topic, 'subject':subject, 'assigments':assigments, 'assigment':assigment}
    return render(request, 'Student/edit-Assigments.html', context)

def AssigmentsDelete(request, sid, id):
    Assigment.objects.filter(id = id).first().delete()
    return redirect(f'../../assigmentsPage/{sid}/{id}')

def UploadAssigments(request, sid, tid, aid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigments = Assigment.objects.filter(id=aid).first()
    context = {'topic':topic, 'subject':subject, 'assigments':assigments}
    return render(request, 'Student/assigment-upload.html', context)

def marksAssigments(request, sid, aid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/assigment-marks.html', context)

def AddAssigmentMarks(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/add-assigmnents-marks.html', context)

def discussionsPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/discussions.html', context)
 
def groupsPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/groups.html', context)
 
def anauncementPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}

    return render(request, 'Student/anauncement.html', context)