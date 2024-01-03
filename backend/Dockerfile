FROM python:3

WORKDIR /backend/

COPY requirements.txt /backend/

RUN pip install -r requirements.txt 

COPY . /backend/

CMD python manage.py runserver 0.0.0.0:8000