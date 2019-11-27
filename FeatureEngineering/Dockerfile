FROM python:3.7

RUN apt-get update
RUN apt-get install -y libsndfile1-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./FeatureController.py" ]