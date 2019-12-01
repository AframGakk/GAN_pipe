#!/usr/bin/env bash

#kubectl scale deployment rabbit-mq --replicas=0
#kubectl scale deployment rabbit-mq --replicas=1

#kubectl scale deployment test-container-1-deployment --replicas=0
#kubectl scale deployment test-container-1-deployment --replicas=1

#kubectl scale deployment test-container-2-deployment --replicas=0
#kubectl scale deployment test-container-2-deployment --replicas=1

#kubectl scale deployment test-container-3-deployment --replicas=0
#kubectl scale deployment test-container-3-deployment --replicas=1

kubectl scale deployment ingestion-service --replicas=0
kubectl scale deployment ingestion-service --replicas=1

kubectl scale deployment controller-service --replicas=0
kubectl scale deployment controller-service --replicas=1

kubectl scale deployment training-scheduler --replicas=0
kubectl scale deployment training-scheduler --replicas=1

kubectl scale deployment gan-service --replicas=0
kubectl scale deployment gan-service --replicas=1

