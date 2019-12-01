#!/usr/bin/env bash

#kubectl delete deployment test-container-1-deployment
#kubectl delete service test-container-1-service

#kubectl delete deployment test-container-2-deployment
#kubectl delete service test-container-2-service

#kubectl delete deployment test-container-3-deployment
#kubectl delete service test-container-3-service

kubectl delete deployment ingestion-service
kubectl delete deployment controller-service
kubectl delete deployment training-scheduler
kubectl delete deployment gan-service
