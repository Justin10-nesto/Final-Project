# from django.core.mail import send_mail
# from django.conf import settings
# from django.db.models import Q
# from django.dispatch import receiver
# from django.db.models.signals import pre_delete, pre_save, post_save, post_delete, post_migrate
# from django.utils.functional import SimpleLazyObject
# from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking
# from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult, Generated_exam
# from OnlineExamination.ExamsDoc import results, timetable
# from OnlineExamination.ExamGenerator.exam_generator import ExamGerator
# from schools.models import Department, Subject, SchoolLevel, StudentClass, CourseSubject
# import datetime

# # @receiver(post_save, sender='schools.UserLog')
# def generating_exam(request):
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
#                 exam_type = ExamType.objects.filter(name = st_exam.exam.name).first()
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
#     promotion = False
#     subjects_pass_arr = []
#     print('ok')
#     studentInfo = Student.objects.filter(user= kwargs['instance'].user).first()
#     classCurrent = studentInfo.classCurrent
#     exam_type = ExamType.objects.filter(studentClass = classCurrent).first()
#     subjects = StudentSubject.objects.filter(student = studentInfo)
#     grade = Grade.objects.filter(level=studentInfo.classCurrent.level)
#     if subjects.exists():
#         for subject in subjects:
#             # print(subject.subject.subject_name)
#             continue_excusion = False
#             subjects_pass_status = 0
#             exam = StudentExam.objects.filter(subject = subject.subject, exam= exam_type).order_by('date_created')
#             if exam.exists():
#                 points_exam = results.getting_points(grades=grade, marks=[exam[0].marks, exam[0].marks])
#                 marks_grade =points_exam['grade'][0]
#                 if studentInfo.classCurrent.level.name == 'A-Level':
#                     if marks_grade <= 'D':
#                         continue_excusion = True
#                 else:
#                     if marks_grade <= 'C':
#                         continue_excusion = True

#                 if continue_excusion:
#                     assigments =AssigmentSubmission.objects.filter(subject=subject.subject, user=studentInfo.user)
#                     student_group =StudentGroupManyToMany.objects.filter(student = studentInfo).first()
#                     no_group_work = 0
#                     if student_group:
#                         group_assigments =AssigmentSubmission.objects.filter(subject=subject.subject, group =student_group.group)
#                         no_group_work +=group_assigments.count()
#                     all_assigments = Assigment.objects.filter(subject=subject.subject).count()
#                     no_assigments = no_group_work + assigments.count()

#                     final_percentage = 0
#                     Tutorial_learning_pecentage = 0
#                     Tutorial_learning_arr = []
#                     tutorials = Tutorial.objects.filter(subject = subject.subject)
#                     video_tracking = TutorialTimeTacking.objects.filter(user = studentInfo.user)
#                     for tutorial in tutorials:
#                         for tr_tutorials in video_tracking:
#                             if tr_tutorials.tutorial == tutorial:
#                                 Tutorial_learning_arr.append(tr_tutorials.video_complition_percentage)
#                     try:
#                         Tutorial_learning_pecentage  = sum(Tutorial_learning_arr)/tutorials.count()
#                     except:
#                         pass

#                     try:
#                         final_percentage = (no_assigments/all_assigments)*100
#                     except ZeroDivisionError:
#                         final_percentage = 0
#                     # print(final_percentage)
#                     if final_percentage>=0:
#                         if student_group:
#                             assigment_submitted = AssigmentSubmission.objects.filter(Q(group =student_group.group) | Q(user= kwargs['instance'].user))
#                             if assigment_submitted.exists():
#                                 assigment_marks = [ass.marks*ass.assigniment.Weight for ass in assigment_submitted]
#                                 total_marks_scored = sum(assigment_marks)
#                                 all_assigments = Assigment.objects.filter(subject=subject.subject)
#                                 total_assigments = [ass.Weight**2 for ass in all_assigments]
#                                 try:
#                                     total_marks = (total_marks_scored/sum(total_assigments))*100

#                                 except:
#                                     total_marks = 0
#                                 if total_marks>80 or Tutorial_learning_pecentage >80:
#                                     subjects_pass_status = 1

#                                 if total_marks>60 and Tutorial_learning_pecentage >70:
#                                     subjects_pass_status = 1
#             subjects_pass_arr.append(subjects_pass_status)

#         passed_subject = sum(subjects_pass_arr)
#         print(subjects.count())
#         if passed_subject == subjects.count()/2:
#             promotion  = True

#         if promotion:
#             StudentClassManyToMany.objects.create(classCurrent = studentInfo.classCurrent,student = studentInfo)
#             if not classCurrent.get_final_class:
#                 next_class_id = classCurrent.id+1
#                 next_class = StudentClass.objects.filter(id = next_class_id)
#                 studentInfo.classCurrent = next_class
#                 studentInfo.save()
#                 ptint('ok')
#     return redirect('Dashboard')