#!/bin/bash -xe
BASE_DIR=$(pwd)

if [ ! -d "${BASE_DIR}/venv" ]
then
    echo "=== virtual environment does not exist so creating it ===> "
    python -m virtualenv venv
    if [ -f "${BASE_DIR}/venv/Scripts/activate" ]
    then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    pip install -r requirements.txt
    deactivate
fi

if [ -f "${BASE_DIR}/venv/Scripts/activate" ]
then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
pip install -r requirements.txt


echo "=== Repackaging lambda code ===> "
cd ${BASE_DIR}/s3downloader
mkdir -p ${BASE_DIR}/dist
zip -r ${BASE_DIR}/dist/s3downloader.zip .

echo "=== Updating lambda code ===> "
cd ${BASE_DIR}
source ${BASE_DIR}/deployenv.sh
aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} s3 cp ${BASE_DIR}/dist/s3downloader.zip s3://${LambdaCodeBucket}/${LambdaS3Key}

aws --region=${AWS_DEFAULT_REGION} --profile=${AwsIAMDeploymentProfile} lambda update-function-code \
    --function-name  ${LambdaFunctionName} \
    --s3-bucket=${LambdaCodeBucket} --s3-key=${LambdaS3Key}
