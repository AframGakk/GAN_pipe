#!/bin/bash

#gcloud config set project samplergan
#gcloud config set compute/zone europe-west3-a

# RabbitMQ depoloyment
kubectl apply -f ./staging/rabbitmq-dpl.yaml
kubectl apply -f ./staging/rabbitmq-srv.yaml

# Ingestion service deployment
kubectl apply -f ./staging/IngestionService-dpl.yaml

# Ingestion service deployment
kubectl apply -f ./staging/TrainingScheduler-dpl.yaml
kubectl apply -f ./staging/TrainingScheduler-srv.yaml

# Ingestion service deployment
kubectl apply -f ./staging/ControllerService-dpl.yaml

# Feature engineering deployment
kubectl apply -f ./staging/GanService-dpl.yaml

# Ingress
kubectl apply -f ./staging/ingress.yaml
