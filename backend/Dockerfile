FROM python:3.10

WORKDIR /backend/

COPY requirements.txt /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

COPY . /backend/

# Gunicorn 설치
RUN pip install gunicorn

CMD ["gunicorn", "backend.wsgi:application", "-b", "0.0.0.0:8000"]