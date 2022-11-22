FROM python:3.8-buster

RUN mkdir /app  
WORKDIR /app  
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt  
ADD . .
 
ENTRYPOINT ["python", "-u", "main.py"]