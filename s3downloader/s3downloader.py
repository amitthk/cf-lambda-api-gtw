import boto3
import requests
import sys, time
from io import BytesIO
from pathlib import Path
try:
    from urlparse import urlparse
except ImportError as er:
    from urllib.parse import urlparse
import wget

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context



CONST_RETRY_COUNT = 5
error_message = "*** ERROR: Failure to retrieve Object Url ***"

def write_to_file(file_name,f_output):
    with open(file_name,'w') as f:
        f.write(f_output)


def download_url(event, context):
    try:
        # resource_s3 = boto3.resource('s3')
        client_s3 = boto3.client('s3')
        object_url = event["object_url"]

        if event["dest_bucket"] is not None:
            dest_bucket = event["dest_bucket"]
        else:
            dest_bucket = "lambda.atksv.mywire.org"

        # bucket = resource_s3.Bucket(dest_bucket)

        parsed_url = urlparse(object_url)
        dest_path = parsed_url.path
        dest_suffix = dest_path.split('/')[-1]
        tmp_path = "/tmp/{0}".format(dest_suffix)
        
        print(tmp_path)

        retry_count = CONST_RETRY_COUNT

        while retry_count >= 0:
            time.sleep(3) # wait 3 seconds then try again
            try:
                print("=====Saving {0} to {1}=====>".format(object_url,tmp_path))
                wget.download(object_url,tmp_path)
                print("=====Uploading {0} to {1}=====>".format(tmp_path,dest_bucket))
                with open(tmp_path, mode='rb') as upl_file:
                    obj = upl_file.read()
                    client_s3.put_object(Body=obj,Bucket=dest_bucket, Key=dest_path)
                break
            except BaseException as e:
                retry_count-=1
                print(error_message)
                print ("File {} not ready, trying again. Retry count: {}".format(tmp_path, retry_count))
                raise e

    except BaseException as error:
        print(error_message)
        raise error

def get_url(event, context):
    try:
        s3 = boto3.resource('s3')
        client_s3 = boto3.client('s3')
        object_key = event["object_key"].upper()
        src_bucket = event["src_bucket"].upper()
        bucket = s3.Bucket(src_bucket)

        for obj in bucket.objects.filter(Prefix=object_key + '/'):
            url = "https://s3-ap-southeast-1.amazonaws.com/" + obj.bucket_name + "/" + obj.key
            return ("Url URL is {0}".format(url))
        return(error_message)

    except BaseException as error:
        print(error_message)
        raise error

if __name__ == "__main__":
    event = {}
    context = []
    object_url = sys.argv[1]
    dest_bucket = sys.argv[2]
    event["object_url"]=object_url
    event["dest_bucket"]=dest_bucket
    download_url(event, context)
