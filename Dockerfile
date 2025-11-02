FROM python:3.12
LABEL maintainer="bokovdenys.dev@gmail.com"
ENV PYTHONUNBUFFERED 1

WORKDIR drf-app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]