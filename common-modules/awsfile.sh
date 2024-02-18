#!/bin/bash
set -x

#Constants
PATH=$PATH:/usr/local/bin; export PATH
REGION=us-west-2
CLUSTER=staging

env
docker pull stedolan/jq
docker run --rm -i amazon/aws-cli configure list
echo $HOME

SERVICE_NAME=dev-test-contentstackoverflow
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-insightsservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-bigdatakafka
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-contentrss
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-bigdatayoutube
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-chatservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-userservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-contentmeetup
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-analytics
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-bigdatarest
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-feedservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-appservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-bigdatauser
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-bigdatarss
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-contentyoutube
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-recoservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment

SERVICE_NAME=dev-test-feedservice
docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --force-new-deployment


