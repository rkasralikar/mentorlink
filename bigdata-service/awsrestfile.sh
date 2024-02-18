#!/bin/bash
set -x

#Constants
PATH=$PATH:/usr/local/bin; export PATH
REGION=us-west-2
REPOSITORY_NAME=bigdatarest
CLUSTER=staging
FAMILY=`sed -n 's/.*"family": "\(.*\)",/\1/p' resttaskdef.json | tr -d '\r'`
NAME=`sed -n 's/.*"name": "\(.*\)",/\1/p' resttaskdef.json | tr -d '\r'`
SERVICE_NAME=dev-test-bigdatarest
BUILD_ID=$1
env
docker pull stedolan/jq
docker run --rm -i amazon/aws-cli configure list
echo $HOME

#Store the repositoryUri as a variable
REPOSITORY_URI=`docker run --rm -i amazon/aws-cli  ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${REGION} | docker run -i stedolan/jq .repositories[].repositoryUri | tr -d '"'`


#Replace the build number and respository URI placeholders with the constants above
sed -e "s;%BUILD_ID%;${BUILD_ID};g" -e "s;%REPOSITORY_URI%;${REPOSITORY_URI};g" resttaskdef.json > ${NAME}-v_${BUILD_ID}.json

SERVICES=`docker run --rm -i amazon/aws-cli  ecs describe-services --services ${SERVICE_NAME} --cluster ${CLUSTER} --region ${REGION} | docker run -i stedolan/jq .failures[]`

TASKDEF=`docker run --rm -i amazon/aws-cli ecs describe-task-definition --task-definition $NAME --output json | grep taskDefinitionArn | awk {'print $2'} | tr ',' ' '`

REVISION=`docker run --rm -i amazon/aws-cli  ecs describe-task-definition --task-definition ${NAME} --region ${REGION} | docker run -i stedolan/jq .taskDefinition.revision`

if [ "$SERVICES" == "" ]; then
  echo "entered existing service"
  DESIRED_COUNT=`docker run --rm -i amazon/aws-cli  ecs describe-services --services ${SERVICE_NAME} --cluster ${CLUSTER} --region ${REGION} | grep desiredCount | awk {'print $2'} | tr -d ',' | head -n 1`
  if [ "${DESIRED_COUNT}" -eq "0" ]; then

    DESIRED_COUNT="1"

  fi

  docker run --rm -i amazon/aws-cli ecs update-service --cluster ${CLUSTER} --region ${REGION} --service ${SERVICE_NAME} --task-definition ${FAMILY}:${REVISION} --desired-count ${DESIRED_COUNT} --force-new-deployment

else

  echo "entered new service"
  docker run --rm -i amazon/aws-cli ecs create-service --service-name ${SERVICE_NAME} --desired-count 1 --task-definition ${FAMILY} --cluster ${CLUSTER} --region ${REGION}

fi