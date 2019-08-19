#!/usr/bin/env bash

gcloud container clusters create ai-offline-pipe \
   --num-nodes 1 \
   --enable-basic-auth \
   --issue-client-certificate \
   --zone us-central1-a


gcloud container clusters get-credentials ai-offline-pipe \
    --zone europe-west3-a


