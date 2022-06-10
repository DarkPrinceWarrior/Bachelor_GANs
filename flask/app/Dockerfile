FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

#CMD gunicorn --bind 0.0.0.0:5000 app:app
CMD ["uwsgi", "app.ini"]
