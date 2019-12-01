FROM datmo/tensorflow:cpu

WORKDIR /usr/src/app

#COPY ./Models ./Models
#COPY ./Repositories ./Repositories
#COPY ./Services ./Services
#COPY ./tmp ./tmp
#COPY ./Controller.py ./Controller.py
#COPY ./requirements.txt ./requirements.txt
RUN pip install virtualenv
RUN virtualenv venv
COPY requirements.txt ./
RUN source venv/bin/activate
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV RHOST=localhost
ENV RUSER=guest
ENV RPASS=guest
ENV RVHOST=/
#ENV TRAINER=153671080191723390
#ENV ZONE=us-west1-b
#ENV PROJECT_ID=samplergan
ENV PGHOST=34.89.28.185
ENV PGDATABASE=ml-pipe-database
ENV PGUSER=villi
ENV PGPASSWORD=aframgakk19

COPY . .

CMD [ "python", "./Controller.py" ]