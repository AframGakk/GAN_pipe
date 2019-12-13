FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

ENV RUSER=guest
ENV RPASS=guest
ENV RHOST=localhost
ENV RVHOST=/
ENV TOKEN=34fwe43ff4ogfkm5!
ENV PGHOST=34.89.28.185
ENV PGDATABASE=ml-pipe-database
ENV PGUSER=villi
ENV PGPASSWORD=aframgakk19


EXPOSE 5007

CMD [ "python", "./SchedulingController.py" ]