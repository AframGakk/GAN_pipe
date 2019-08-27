#!/usr/bin/env bash

gcloud container clusters create wisebeat-staging \
   --num-nodes 1 \
   --enable-basic-auth \
   --issue-client-certificate \
   --zone europe-west3-a