#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.8


import boto3

# Let's use Amazon S3
s3 = boto3.client('s3')

response = s3.get_bucket_location(Bucket='mentaljolt.com')
print(response)
