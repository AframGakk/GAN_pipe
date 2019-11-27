#!/usr/bin/env bash

#gcloud builds submit --tag gcr.io/samplergan/test-app-1 ./TestContainer1/
#gcloud builds submit --tag gcr.io/samplergan/test-app-2 ./TestContainer2/
#gcloud builds submit --tag gcr.io/samplergan/test-app-3 ./TestContainer3/

gcloud builds submit --tag gcr.io/samplergan/ingestion-service ./IngestionServices/
gcloud builds submit --tag gcr.io/samplergan/controller-service ./ControllerService/
gcloud builds submit --tag gcr.io/samplergan/training-scheduler ./TrainingScheduler/
gcloud builds submit --tag gcr.io/samplergan/feature-engineering ./FeatureEngineering/

