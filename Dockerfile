
FROM python:3

EXPOSE 8000

WORKDIR /app
ADD . /app

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


