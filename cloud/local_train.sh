#!/bin/bash
echo "Submitting a Cloud ML Engine job..."

REGION="us-east1"
TIER="BASIC_GPU" # BASIC | BASIC_GPU | STANDARD_1 | PREMIUM_1
BUCKET="onset_detect" # change to your bucket name

MODEL_NAME="onset_detector" # change to your model name

PACKAGE_PATH=trainer # this can be a gcs location to a zipped and uploaded package
TRAIN_FILES=gs://${BUCKET}/data/train120.pkl

CURRENT_DATE=`date +%Y%m%d_%H%M%S`
JOB_NAME=train_${MODEL_NAME}_${TIER}_${CURRENT_DATE}
JOB_DIR=gs://$BUCKET_NAME/$JOB_NAME
#JOB_NAME=tune_${MODEL_NAME}_${CURRENT_DATE} # for hyper-parameter tuning jobs

gcloud ml-engine local train \
        --job-dir ${MODEL_DIR} \
        --module-name trainer.onset_detector \
        --package-path ${PACKAGE_PATH} \
        -- \
        --data-file ./data/train120.pkl
        --epochs 1