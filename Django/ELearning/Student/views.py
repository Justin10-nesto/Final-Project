from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
from Student.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from schools.models import Subject, Department, StudentClass,SchoolLevel, Course, CourseSubject
from datetime import datetime, timedelta
import random

# Create your views here.

def random_date(start, end):
    delta = start - end
    int_delta = (delta.days*24*60*60)+delta.seconds
    random_seconds = random.randint(0, -int_delta)
    return start+timedelta(seconds=random_seconds)

def UploadSelectedStudentPage(request):
    csv_path = settings.STATICFILES_DIRS[0] +r'\csv files\advance.csv'
    data = pd.read_csv(csv_path)
    for index, row in data.iterrows():
        DefaultUsers.objects.create(number=row['number'], name=row['name'], school_selected=row['school_selected'], course=row['course'], type=row['type'], location=row['location'])
    
    levels = ['O-Level', 'A-Level']
    for i in levels:
        SchoolLevel.objects.create(name = i)
    
    classes = ['Form Five', 'Form Six'] 
    for i in classes:
        level = SchoolLevel.objects.filter(name = 'A-Level').first()
        StudentClass.objects.create(name = i, level = level)

    # classes = ['Form One', 'Form Two', 'Form Three', 'Form Four'] 
    # for i in classes:
    #     level = SchoolLevel.objects.filter(name = 'O-Level').first()
    #     StudentClass.objects.create(name = i, level = level)
        
    department = data['Department'].unique()
    for i in department:
        start_date = datetime.strptime('1/1/2010', '%d/%m/%Y')
        end_date = datetime.strptime('12/31/2022', '%m/%d/%Y')
        generated_date = random_date(start_date, end_date)
        Department.objects.create(name = i, department_Hod = 'Not Known', start_date = generated_date)
    
    courses = data['course'].unique()
    for i in courses:
        depart =data[data['course'] == i]['Department'].iloc[0]
        depart_obj =Department.objects.filter(name=depart).first()
        Course.objects.create(name=i, department = depart_obj)
        
    for i in range(1,6):
        subject_head = 'Subjects' + str(i)
        subject_dep_head = 'Subjects' + str(i)+ '_deparment'
        subject1 = data[subject_head].unique()
        for i in subject1:
            depart =data[data[subject_head] == i][subject_dep_head].iloc[0]
            depart_obj =Department.objects.filter(name=depart).first()
            code = random.randint(1, 190)
            Subject.objects.create(subject_code = code, subject_name = i, department = depart_obj)

    courses = data['course'].unique()
    for i in courses:
        course_data =data[data['course'] == i]
        course_obj = Course.objects.filter(name= i).first()
        for j in range(1,6):
            subject_head = 'Subjects' + str(j)
            subject = course_data[subject_head].iloc[0]
            subject_obj = Subject.objects.filter(subject_name=subject).first()
            for k in classes:
                class_student = StudentClass.objects.filter(name = k).first()
                CourseSubject.objects.create(course = course_obj, subject=subject_obj, studentClass=class_student)
    
    return redirect('registerPage')

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
                                         school=user_info.school_selected, 
                                         user=user_info_details, 
                                         course=course, 
                                         classCurrent=current_class,
                                         )
        StudentClassManyToMany.objects.create(classCurrent = current_class, student= student)
        return redirect('loginPage')
    
def updateStudent(request):
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
        return redirect('userProfilePage')

def changePassword(request):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user_id = request.user.id
            user = User.objects.filter(id = user_id).first()
            user.set_password(password1)
            return redirect('userProfilePage')
        
        else:
            print('incorrect password')
            return redirect('userProfilePage')


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

def TopicList(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    Topic_info = Topic.objects.filter(subject = subject)
    groups = StudentGroup.objects.filter(subject=subject)
    user_id = request.user.id
    user_data = User.objects.filter(id = user_id).first()
    student_data = Student.objects.filter(user = user_data).first()
    users_groups = StudentGroupManyToMany.objects.filter(student = student_data)
    context = {'Topic_info':Topic_info, 'subject':subject, 'users_groups':users_groups, 'groups':groups}
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
    notes = Notes.objects.filter(subject=subject, topic=topic)
    context = {'topic':topic, 'subject':subject, 'notes':notes}
    return render(request, 'Student/notes.html', context)

def NotesAdd(request, sid, tid):
    if request.method == "POST":
        title = request.POST.get('title')
        Description = request.POST.get('Description')
        file_data = request.FILES['file']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        Notes.objects.create(title=title, description=Description, type=type, file=file_data, topic = topic, subject= subject)
        return redirect(f'../../NotesPage/{sid}/{tid}')
    
    topic = Topic.objects.filter(id = tid).first()
    subject =Subject.objects.filter(id = sid).first()
    context = {'topic':topic, 'subject':subject}
  
    return render(request, 'Student/Add-Notes.html', context)


def booksPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()

    topic = Topic.objects.filter(id = tid).first()
    books = Book.objects.filter(topic=topic, subject=subject)
    context = {'topic':topic, 'subject':subject, 'books':books}
    return render(request, 'Student/books.html', context)
 
def BooksAdd(request, sid, tid):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        description = request.POST.get('description')
        type = request.POST.get('type')
        file_data = request.FILES['file']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        books = Book.objects.create(name=name, author=author, type=type, description=description, file= file_data, topic = topic, subject= subject)
        return redirect(f'../../booksPage/{sid}/{tid}')
    
    department = Department.objects.all()
    topic = Topic.objects.filter(id = tid).first()
    subject =Subject.objects.filter(id = sid).first()
    context = {'department':department, 'topic':topic, 'subject':subject}
  
    return render(request, 'Student/add-Books.html', context)

def BooksEdit(request, sid, tid, bid):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        description = request.POST.get('description')
        type = request.POST.get('type')
        file_data = request.FILES['file']
            
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        Books_obj = Book.objects.filter(id=bid).first()
        Books_obj.name=name 
        Books_obj.author=author 
        Books_obj.type=type 
        Books_obj.description=description 
        Books_obj.file= file_data
        Books_obj.subject = subject
        Books_obj.topic = topic
        Books_obj.save()
        return redirect(f'../../booksPage/{sid}/{tid}')
    
    books = Book.objects.filter(id=bid).first()
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'books':books,'topic':topic, 'subject':subject}
    return render(request, 'Student/edit-Books.html', context)

def BooksDelete(request, sid, tid,  id):
    books =Book.objects.filter(id = id).first()
    books.delete()
    return redirect(f'../../booksPage/{sid}/{tid}')


def assigmentsPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigment = Assigment.objects.all()
    user_id = request.user.id
    user_data = User.objects.filter(id = user_id).first()
    submission_ass =AssigmentSubmission.objects.filter(user=user_data)
    
    submission = []
    submission_late = []
    for ass in submission_ass:
        if ass.status == "submission":
            submission.append(ass)
        else:
            submission_late.append(ass)
    context = {'topic':topic, 'subject':subject, 'assigment':assigment, 'submission_late':submission_late, 'submission':submission}
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
        file = request.FILES['file']
        subject = Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        type_assigment = AssigmentType.objects.filter(id = Category).first()
        if file == None:
            Assigment.objects.create(name = Assigment_number, description=Description, task = task, date = date, time = time, Weight = Weight, subject = subject,  topic = topic, type= type_assigment)
        else:
            Assigment.objects.create(name = Assigment_number, description=Description, task = task, date = date, time = time, Weight = Weight, file = file, subject = subject,  topic = topic, type= type_assigment)

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

def AssigmentSubmision(request, sid, tid, aid):
    if request.method == "POST":
        file_submitted = request.FILES['file_submitted']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        assigments = Assigment.objects.filter(id=aid).first()
        
        if assigments.type.name == 'Group':
            user_id = request.user.id
            user_data = User.objects.filter(id = user_id).first()
            user_belong_group = StudentGroup.objects.filter(user=user_data, subject=subject).first()
            AssigmentSubmission.objects.create(doc = file_submitted, is_group=True, group=user_belong_group, subject=subject, topic=topic, assigniment=assigments, user=user_data)
            return redirect(f'../../../assigmentsPage/{sid}/{tid}') 
        
        else:
            user_id = request.user.id
            user_data = User.objects.filter(id = user_id).first()
            AssigmentSubmission.objects.create(doc = file_submitted, subject=subject, topic=topic, assigniment=assigments, user=user_data)
            return redirect(f'../../../assigmentsPage/{sid}/{tid}')
        
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/submit-assigniment.html', context)

def UploadAssigments(request, sid, tid, aid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    assigments = Assigment.objects.filter(id=aid).first()
    context = {'topic':topic, 'subject':subject, 'assigments':assigments}
    return render(request, 'Student/assigment-upload.html', context)

def marksAssigments(request, sid, tid, aid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    submission_ass =AssigmentSubmission.objects.all()

    context = {'topic':topic, 'subject':subject, 'submission_ass':submission_ass}
    return render(request, 'Student/assigment-marks.html', context)

def assignMarksToAssigment(request, sid, tid, aid):
    if request.method == "POST":
        marks = request.POST.get('marks')
        submission_ass =AssigmentSubmission.objects.filter(id = aid).first()
        submission_ass.marks = marks
        submission_ass.save()
        return redirect(f'../../../assigmentsPage/{sid}/{tid}')
    
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


def AddAssigmentMarks(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/add-assigmnents-marks.html', context)

def discussionsPage(request, sid, tid):
    if request.method == 'POST':
        message = request.POST.get('message')
        user_id = request.user.id
        user_data = User.objects.filter(id= user_id).first()
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        GroupDiscussionsMessage.objects.create(message=message, topic=topic, subject=subject, sender=user_data)
        return redirect(f'../../discussionsPage/{sid}/{tid}')
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    messages = GroupDiscussionsMessage.objects.all()
    context = {'topic':topic, 'subject':subject, 'messages':messages}
    return render(request, 'Student/discussions.html', context)
 
def groupsPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    groups = StudentGroup.objects.filter(subject=subject)
    context = {'topic':topic, 'subject':subject, 'groups':groups}
    return render(request, 'Student/groups.html', context)

def groupAdd(request, sid):
    if request.method == "POST":
        name = request.POST.get('name')
        logo = request.FILES['logo']
        description = request.POST.get('description')
        type_group = request.POST.get('type_group')
        participants = request.POST.get('participants')
        
        grouptype = StudentGroupType.objects.filter(id = type_group).first()
        
        if grouptype.name == 'Public':
        
            subject = Subject.objects.filter(id = sid).first()
            for user_id in participants:
                user_data = User.objects.filter(id = user_id).first()
                student_data = Student.objects.filter(user = user_data).first()
                group =StudentGroup.objects.create(name = name, description= description, file = logo, type_group= grouptype, subject = subject)
                StudentGroupManyToMany.objects.create(student = student_data, group=group)

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
            return redirect(f'../../TopicList/{sid}')
        
    
    try:
        groups_dtype = ['Public', 'Private']
        for i in groups_dtype:
            StudentGroupType.objects.create(name=i)
    except:
        pass
    
    user_id = request.user.id
    student_info = Student.objects.filter(id = user_id).first()

    subject =Subject.objects.filter(id = sid).first()
    users = Student.objects.all()
    assigment = AssigmentType.objects.all()
    Grouptype = StudentGroupType.objects.all()
    context = {'subject':subject, 'Grouptype':Grouptype, 'users':users}
    return render(request, 'Student/create-group.html', context)

def JoinToGroup(request, id):
    user_id = request.user.id
    user = User.objects.filter(id = user_id).first()
    student = Student.objects.filter(user = user).first()
    group = StudentGroup.objects.filter(id= id).first()
    group_id = group.id
    StudentGroupManyToMany.objects.create(group = group, student = student)
    return redirect(f'../groupContent/{group_id}')

def groupContent(request, id):
    if request.method == "POST":
        message = request.POST.get('message')
        user_id = request.user.id
        User_info = User.objects.filter(id = user_id).first()
        post = GroupPost.objects.filter(id = id).first()
        GroupPostComent.objects.create(message= message, post = post, sender = User_info)
        return redirect(f'../groupContent/{id}')

    group = StudentGroup.objects.filter(id= id).first()
    posts = GroupPost.objects.filter(group = group)
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
    context = {'group':group, 'users':users, 'students_data':students_data, 'post_comment':post_comment}
    return render(request, 'Student/group-content.html', context)

def groupPost(request, id):
    if request.method == "POST":
        message = request.POST.get('message')
        user_id = request.user.id
        posts = GroupPost.objects.filter(i = id)
        User_info = User.objects.filter(id = user_id).first()
        group = post.group
        group_id = group.id
        GroupPost.objects.create(message= message, has_topic = False, subject = group.subject, group= group, sender = User_info)
        return redirect(f'../groupContent/{group_id}')

    group = StudentGroup.objects.filter(id= id).first()
    context = {'group':group}
    return render(request, 'Student/add-post.html', context)

def groupPostLikes(request, id):
    user_id = request.user.id
    User_info = User.objects.filter(id = user_id).first()
    post = GroupPost.objects.filter(id = id).first()
    like = GroupPostLike.objects.filter(sender = User_info, message_liked = post)
    if like:
        print('present')
        GroupPostLike.objects.create(likes= True, message_liked = post, sender = User_info)

        # like.delete() 
        return redirect(f'../groupContent/{id}')
    else:
        print('absent')
        GroupPostLike.objects.create(likes= True, message_liked = post, sender = User_info)
        return redirect(f'../groupContent/{id}')
    return redirect(f'../groupContent/{id}')


def groupEdit(request, sid, id):
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
        return redirect(f'../../../groupPage/{sid}')
    
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject, 'group':group, }
    return render(request, 'Student/edit-group.html', context)

def groupDelete(request, sid):
    Assigment.objects.filter(id = id).first().delete()
    return redirect(f'../../TopicList/{sid}')

def RemoveStudentGroup(request, gid, sid):
    group = StudentGroup.objects.filter(id=gid).first()
    students = Student.objects.filter(id =sid).first()
    students_data = StudentGroupManyToMany.objects.filter(group = group, student= students)
    students_data.delete()
    return redirect(f'../../groupContent/{gid}')

def LeftStudentGroup(request, gid):
    group = StudentGroup.objects.filter(id=gid).first()
    user_id = request.user.id
    User_info = User.objects.filter(id = user_id).first()
    students = Student.objects.filter(user= User_info).first()
    students_data = StudentGroupManyToMany.objects.filter(group = group, student= students)
    students_data.delete()
    return redirect(f'../../groupContent/{gid}')

def AddGroupActivities(request, gid):
    group = StudentGroup.objects.filter(id=gid).first()
    students_group = StudentGroupManyToMany.objects.filter(group = group)

    context ={'students_group':students_group}
    return render(request, 'Student/Add-activity.html', context)


def anauncementPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    user_id = request.user.id
    user_info = User.objects.filter(id = user_id).first()
    anaunciment_type = AnnouncimentType.objects.filter(name= 'Inbox').first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, announcimentType=anaunciment_type, is_deleted=False)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

def anauncementSentPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    user_id = request.user.id
    user_info = User.objects.filter(id = user_id).first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, sender=user_info, is_deleted=False)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

def anauncementTrashPage(request, sid, tid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    anaunciment = Announciment.objects.filter(subject = subject, topic = topic, is_deleted=True)
    inbox_number = anaunciment.count()
    context = {'topic':topic, 'subject':subject, 'inbox_number':inbox_number, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement.html', context)

def anauncementContentPage(request, sid, tid, anid):
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    anaunciment = Announciment.objects.filter(id = anid).first()
    anaunciment.is_opened = True
    anaunciment.save()
    context = {'topic':topic, 'subject':subject, 'anaunciment':anaunciment}
    return render(request, 'Student/anauncement-content.html', context)

def anauncementSoftDeletePage(request, sid, tid, anid):
    anaunciment = Announciment.objects.filter(id = anid).first()
    if anaunciment.is_deleted == False:
        anaunciment.is_deleted= True
        anaunciment.save()
    else:
        anaunciment.delete()
    return redirect(f'../../../anauncementPage/{sid}/{tid}')

def ComposeAnaunciment(request, sid, tid):
    if request.method == 'POST':
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
        return redirect(f'../../anauncementPage/{sid}/{tid}')

    types = ['Inbox', 'Important', 'Sent', 'Draft', 'Trash']
    for i in types:
        try:
            AnnouncimentType.objects.create(name =i)
        except:
            pass
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}
    return render(request, 'Student/compose-anaunciments.html', context)

def TutorialPage(request, sid, tid):
    try:
        tutorial_id = 1
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(id = tutorial_id).first()
        context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
        return render(request, 'Student/tutorials.html', context)

    except:
        return redirect(f'../../TutorialAdd/{sid}/{tid}')


def PreviousPage(request, sid, tid, preid):
    tutorial_id = int(preid) -1
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    tutorial = Tutorial.objects.filter(id = tutorial_id).first()
    context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}

    return render(request, 'Student/tutorials.html', context)

def NextTuturial(request, sid, tid, tuid):
    tutorial_id = int(tuid)+1
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    tutorial = Tutorial.objects.filter(id = tutorial_id).first()
    context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}

    return render(request, 'Student/tutorials.html', context)

def TutorialAdd(request, sid, tid):
    if request.method == "POST":
        Tutorial_title = request.POST.get('Tutorial_title')
        Description = request.POST.get('Description')
        file_data = request.FILES['file']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        books = Tutorial.objects.create(title = Tutorial_title, description=Description, file= file_data, topic = topic, subject= subject)
        return redirect(f'../../TutorialPage/{sid}/{tid}')
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    context = {'topic':topic, 'subject':subject}

    return render(request, 'Student/add-tutorial.html', context)

def TutorialEdit(request, sid, tid, tuid):
    if request.method == "POST":
        Tutorial_title = request.POST.get('Tutorial_title')
        Description = request.POST.get('Description')
        file_data = request.FILES['file']
        subject =Subject.objects.filter(id = sid).first()
        topic = Topic.objects.filter(id = tid).first()
        tutorial = Tutorial.objects.filter(id = tuid).first()
        tutorial.title = Tutorial_title
        tutorial.description=Description
        tutorial.file= file_data
        tutorial.topic = topic
        tutorial.subject= subject
        tutorial.save()
        return redirect(f'../../../TutorialPage/{sid}/{tid}')
    
    subject =Subject.objects.filter(id = sid).first()
    topic = Topic.objects.filter(id = tid).first()
    tutorial = Tutorial.objects.filter(id = tuid).first()

    context = {'topic':topic, 'subject':subject, 'tutorial':tutorial}
    return render(request, 'Student/edit-tutorial.html', context)