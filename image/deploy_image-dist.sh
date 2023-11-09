#!/bin/bash
REGION=
AWS_ID=
REPO_NAME=
LAMBDA_FUNCTION_NAME=
ARN_ROLE=

# environment variables
OPEN_WEATHER_API=
OPEN_WEATHER_KEY=
AERO_DATA_KEY=
RD_HOST=
RD_SCHEMA=
RD_USER=
RD_KEY=
RD_PORT=

# authorization
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ID}.dkr.ecr.${REGION}.amazonaws.com

# create repository if not exist already
aws ecr describe-repositories \
    --repository-names ${REPO_NAME}  || aws ecr create-repository \
    --repository-name ${REPO_NAME} \
    --region ${REGION} \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE

# build image
docker build --platform linux/amd64 -t docker-image:test .

# add tag to aws repo
docker tag docker-image:test ${AWS_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:latest

# push image to repo
docker push ${AWS_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:latest

# create lambda function
aws lambda create-function \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --package-type Image \
    --code ImageUri=${AWS_ID}.dkr.ecr.${REGION}.amazonaws.com/gans:latest \
    --role ${ARN_ROLE} \
    --environment Variables="{OPEN_WEATHER_API=${OPEN_WEATHER_API},OPEN_WEATHER_KEY=${OPEN_WEATHER_KEY},AERO_DATA_KEY=${AERO_DATA_KEY},RD_HOST=${RD_HOST},RD_SCHEMA=${RD_SCHEMA},RD_USER=${RD_USER},RD_KEY=${RD_KEY},RD_PORT=${RD_PORT}}"

# invoke function for check
aws lambda invoke --function-name ${LAMBDA_FUNCTION_NAME} response.json