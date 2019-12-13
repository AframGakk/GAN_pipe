#!/usr/bin/env bash

gcloud builds submit --tag gcr.io/samplergan/ingestion-service ./IngestionServices/
gcloud builds submit --tag gcr.io/samplergan/controller-service ./ControllerService/
gcloud builds submit --tag gcr.io/samplergan/training-scheduler ./TrainingScheduler/
gcloud builds submit --tag gcr.io/samplergan/gan-service ./GAN/

