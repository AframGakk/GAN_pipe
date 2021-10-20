FROM tensorflow/tensorflow

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y libsndfile1-dev python3 python3-pip

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

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
ENV GOOGLE_APPLICATION_CREDENTIALS=./bucket.json

COPY . .

CMD [ "python3", "./Controller.py" ]