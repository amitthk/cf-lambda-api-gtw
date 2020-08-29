#!/bin/bash -xe
BASE_DIR=$(pwd)

source venv/Scripts/activate

source ${BASE_DIR}/deployenv.sh

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} s3 rb --force s3://${DownloadS3Bucket}

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} cloudformation delete-stack  --stack-name=${AwsCFDeployStackName}
deactivate