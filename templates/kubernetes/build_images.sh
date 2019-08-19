#!/usr/bin/env bash

gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-1 ./app/
gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-2 ./app2/
gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-3 ./app3/