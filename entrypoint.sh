#!/bin/sh

python3 manage.py makemigrations 

python3 manage.py migrate 

python3 manage.py insert_loan_types 

python3 manage.py runserver 0.0.0.0:8000  
