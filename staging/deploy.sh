#!/bin/bash

#gcloud config set project samplergan
#gcloud config set compute/zone europe-west3-a

# RabbitMQ depoloyment
#kubectl apply -f ./staging/rabbitmq-dpl.yaml
#kubectl apply -f ./staging/rabbitmq-srv.yaml

# TaskRecommendFeatureService deployment
#kubectl apply -f ./staging/TestContainer1-dpl.yaml
#kubectl apply -f ./staging/TestContainer1-srv.yaml

# TrainingScheduler deploymebt
#kubectl apply -f ./staging/TestContainer2-dpl.yaml
#kubectl apply -f ./staging/TestContainer2-srv.yaml

# TrainingScheduler deploymebt
#kubectl apply -f ./staging/TestContainer3-dpl.yaml
#kubectl apply -f ./staging/TestContainer3-srv.yaml

# Ingestion service deployment
kubectl apply -f ./staging/IngestionService-dpl.yaml

