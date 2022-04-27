FROM python:3.10

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . . 

EXPOSE 80

CMD ["python3", "/src/myproject/manage.py", "runserver", "0.0.0.0:80"]