#!/bin/bash -xe
BASE_DIR=$(pwd)

if [ -f "${BASE_DIR}/venv/Scripts/activate" ]
then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

source ${BASE_DIR}/deployenv.sh

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} s3 rb --force s3://${DownloadS3Bucket}

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} cloudformation delete-stack  --stack-name=${AwsCFDeployStackName}
deactivate