#!/bin/bash -xe
BASE_DIR=$(pwd)

if [ ! -d "${BASE_DIR}/venv" ]
then
    echo "=== virtual environment does not exist so creating it ===> "
    python -m virtualenv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    deactivate
fi

source venv/Scripts/activate
pip install -r requirements.txt

echo "=== Packaging Lambda ===> "
cd ${BASE_DIR}/s3downloader
mkdir -p ${BASE_DIR}/dist
zip -r ${BASE_DIR}/dist/s3downloader.zip .

echo "=== Deploying stack ===> "
cd ${BASE_DIR}
source ${BASE_DIR}/deployenv.sh
aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} s3 cp ${BASE_DIR}/dist/s3downloader.zip s3://${LambdaCodeBucket}/${LambdaS3Key}

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} cloudformation create-stack --on-failure=DO_NOTHING --capabilities=CAPABILITY_NAMED_IAM --stack-name=${AwsCFDeployStackName} --template-body file://cf-template.yml --parameters file://cf-params.json
aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} cloudformation wait stack-create-complete --stack-name=${AwsCFDeployStackName}
aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} cloudformation describe-stacks  --stack-name=${AwsCFDeployStackName}
