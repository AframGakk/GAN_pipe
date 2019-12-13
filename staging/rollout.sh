#!/usr/bin/env bash

kubectl scale deployment rabbit-mq --replicas=0
kubectl scale deployment rabbit-mq --replicas=1

kubectl scale deployment ingestion-service-v1 --replicas=0
kubectl scale deployment ingestion-service-v1 --replicas=1

kubectl scale deployment controller-service-v1 --replicas=0
kubectl scale deployment controller-service-v1 --replicas=1

kubectl scale deployment training-scheduler-v1 --replicas=0
kubectl scale deployment training-scheduler-v1 --replicas=1

kubectl scale deployment gan-service-v1 --replicas=0
kubectl scale deployment gan-service-v1 --replicas=1

