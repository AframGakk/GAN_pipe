#!/usr/bin/env bash

kubectl scale deployment test-container-1-deployment --replicas=0
kubectl scale deployment test-container-1-deployment --replicas=1

kubectl scale deployment test-container-2-deployment --replicas=0
kubectl scale deployment test-container-2-deployment --replicas=1

kubectl scale deployment test-container-3-deployment --replicas=0
kubectl scale deployment test-container-3-deployment --replicas=1