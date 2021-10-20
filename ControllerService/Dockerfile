FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

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