import boto3
import requests

def download_url(event, context):
    try:
        s3 = boto3.resource('s3')
        client_s3 = boto3.client('s3')
        object_url = event["object_url"].upper()
        dest_bucket = event["dest_bucket"].upper()
        bucket = s3.Bucket(dest_bucket)

        for obj in bucket.objects.filter(Prefix=object_url + '/'):
            url = "https://s3-ap-southeast-1.amazonaws.com/" + obj.bucket_name + "/" + obj.key
            return ("Object URL is {0}".format(url))
        return("*** Failure to retrieve Object Url - Please check your request ***")

    except BaseException as error:
        print("*** Failure to retrieve Object Url - Please check your request ***")
        return str(error)

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
        return("*** Failure to retrieve Object Url - Please check your request ***")

    except BaseException as error:
        print("*** Failure to retrieve Object Url - Please check your request ***")
        return str(error)

