from flask import Flask
from flask_apscheduler import APScheduler
import requests

url = 'http://192.168.43.94:8000'
# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='send_sms', minutes=1)
def send_sms():
    print("generating an exam")
    url_exam = url+r'/generating_exam'
    response =requests.get(url_exam)

scheduler.start()
