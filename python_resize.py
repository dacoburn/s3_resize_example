from __future__ import print_function
import boto3
import os
import sys
import uuid
import json
#from PIL import Image, ImageDraw
from PIL import Image
#import PIL.image

payload = os.environ.get('PAYLOAD_FILE')
print("ConfigFile: %s" % payload)

if not(payload is None):
	with open(payload) as data_file:
		options = json.load(data_file)
else:
	print("No Payload found")
	exit(2)

if "aws_access_key" in options:
	aws_access_key = options["aws_access_key"]
else:
	print("aws_access_key not specified in payload should be \"aws_access_key\"")
	exit(3)

if "aws_secret_key" in options:
	aws_secret_key = options["aws_secret_key"]
else:
	print("No aws_secret_key specified")
	exit(1)

if "endpoint_url" in options:
	endpoint_url = options["endpoint_url"]
	full_url = endpoint_url
else:
	print("endpoint_url not specified in payload should be \"endpoint_url\":\"S3ENDPOINT:PORT\"")
	exit(4)

if "region" in options:
	region = options["region"]
else:
	print("No region specified, defaulting to us-east-1, not sure this is needed")

if "aws_s3_bucket" in options:
	aws_s3_bucket = options["aws_s3_bucket"]
else:
	print("aws_s3_bucket not specified, needed in order to look in the bucket.")
	exit(1)

if "key" in options:
	key = options['key']
else:
	print("No key, don't know what file to use")
	exit(1)


print("Connecting to S3/Swift Server %s" % full_url)
# s3_client = boto3.client('s3', endpoint_url=full_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
s3 = boto3.resource(
		's3',
	    aws_access_key_id=aws_access_key,
	    aws_secret_access_key=aws_secret_key,
	    endpoint_url=full_url
	    )
print("Connected to S3/Swift Server %s" % full_url)

def resize_image(image_path, resized_path):
	with Image.open(image_path) as image:
		image.thumbnail(tuple(x / 2 for x in image.size))
		image.save(resized_path)

def handler():
	download_path = "%s" % (key)
	upload_path = 'resized-{}'.format(key)
	print("Downloading file: %s/%s/%s" % (full_url, aws_s3_bucket, key))
	print(download_path)
	s3.meta.client.download_file(aws_s3_bucket, key, download_path)
	print("File Downloaded: %s" % (key))
	print("Resizing image: %s" % (download_path))
	resize_image(download_path,upload_path)
	print("Image Resized: %s" % (upload_path))
	print("Uploading File: %s" % (upload_path))
	resized_bucket = '{}resized'.format(aws_s3_bucket)
	bucket = s3.create_bucket(Bucket=resized_bucket)
	s3.meta.client.put_bucket_acl(ACL='public-read', Bucket=resized_bucket)
	s3.meta.client.upload_file(upload_path, resized_bucket, key)
	s3.meta.client.put_object_acl(ACL='public-read', Bucket=resized_bucket, Key=key)
	print("Upload Complete: %s Url: %s/%s/%s" % (upload_path,full_url,resized_bucket,key))

handler()