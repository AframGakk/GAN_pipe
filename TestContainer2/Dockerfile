FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["python", "./TestControler2.py"]