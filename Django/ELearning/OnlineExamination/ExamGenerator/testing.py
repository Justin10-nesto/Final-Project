from exam_generator import ExamGerator
path = r'C:\Users\CTS\Downloads\ELearning\static\media\Books\Entrepreneurship3.pdf'
# path = r'C:\Users\CTS\Downloads\ELearning\static\models\Qns Generation\new.txt'
hist = ExamGerator('history', [path])
doc =hist.doc_opening()
taging = hist.chicking_doc_tags()
print('essay questions')
questions, answers= hist.generate_exams('Essay', 10)
print('fill the blanks')
questions, answers= hist.generate_exams('fill the blanks', 10)
print('Short Note')
questions, answers= hist.generate_exams('fill the blanks', 10)
print(questions)
