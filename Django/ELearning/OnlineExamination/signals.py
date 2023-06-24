from django.core.mail import send_mail
from django.conf import settings
from OnlineLearning.models import Student,AnnouncimentType ,StudentGroupManyToMany,GroupPost,GroupPostComent,GroupPostLike,StudentSubject,Announciment,Notes,DefaultUsers,Tutorial,GroupDiscussionsMessage,GroupDiscussionReply,Book,Assigment,StudentGroup,StudentGroupType,AssigmentType,Topic, AssigmentSubmission,StudentClassManyToMany,GroupWorkDivision,StudentTask, TutorialTimeTacking
from OnlineExamination.ExamGenerator.exam_generator import ExamGerator
from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult, Generated_exam
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

# @receiver(post_save, sender = 'OnlineExamination.StudentExam')
def generating_exam(sender, **kwargs):
    exist_status = False
    print(kwargs['instance'])
    exam_present = Generated_exam.objects.filter(exam_type=kwargs['instance'].exam)
    if exam_present.exists():
        for exam in exam_present:
            if exam.getting_academic_Year == datetime.datetime().now().year:
                exist_status = True

    if not exist_status:
        exam_generated = []
        st_exam = StudentExam.objects.filter(id = kwargs['instance'].id).first()
        exam_type = ExamType.objects.filter(name = st_exam.exam.name).first()
        format_exam =ExamFormat.objects.filter(exam_type = exam_type, subject=st_exam.subject)

        for forma in format_exam:
            sections = {'questions':[],'format':'', 'answers':[] }
            notes_paths = []
            books = Book.objects.filter(subject = forma.subject)
            notes = Notes.objects.filter(subject = forma.subject)
            for book in books:
                notes_paths.append(book.file.url)
            for note in notes:
                notes_paths.append(note.file.url)
            for incomplete_path in notes_paths:
                path = settings.STATICFILES_DIRS[0] + incomplete_path
                hist = ExamGerator(forma.subject.subject_name, path)
                doc =hist.doc_opening()
                taging = hist.chicking_doc_tags()
                questions, answers= hist.generate_exams(forma.type_questions.name, forma.type_questions.number_of_questions)
                sections['format']= forma
                for index, qust in enumerate(questions):
                    sections['questions'].append(qust)
                    sections['answers'].append(answers[index])
            sections['questions']= list(set(sections['questions']))[:forma.type_questions.number_of_questions]
            exam_generated.append(sections)
        for exm in exam_generated:
            exam_format =exm['format']
            for index, quest in enumerate(exm['questions']):
                question = quest
                answer = ''
                try:
                    answer = exm['answers'][index]
                except:
                    answer = ''
                Generated_exam.objects.create(question= question, answers =answer, exam_format=exam_format, exam_type=exam_type )
