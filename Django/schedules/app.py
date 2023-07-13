from flask import Flask
from flask_apscheduler import APScheduler
import requests

# url = 'http://192.168.43.94:8000'
url = 'http://127.0.0.1:8000'
# set configuration values

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='send_sms', seconds = 30)
def send_sms():
    print("generating an exam")
    url_exam = url+r'/generatingExams_API'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='generate_questions', seconds=45)
def generate_questions():
    print("generating an questions")
    url_exam = url+r'/generatingQuestions'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='notification', minutes=1)
def notification():
    print("sending notification")
    url_exam = url+r'/ExamNotification'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='exam_generation', minutes=1)
def exam_generation():
    print("generating an exams")
    url_exam = url+r'/generatingExams'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='student_promotion', minutes=2)
def student_promotion():
    print("promoting student")
    url_exam = url+r'/StudentPromotin'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='generateResults', minutes=1)
def generateResults():
    print("generating results")
    url_exam = url+r'/GeneratingStudentResult'
    response =requests.get(url_exam)
    
@scheduler.task('interval', id='training_model', minutes=3)
def training_model():
    print("generating results")
    url_exam = url+r'/training_model_marks_prediction'
    response =requests.get(url_exam)

scheduler.start()
