#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.4

import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Call S3 to get bucket tagging
bucket_tagging = s3.get_bucket_tagging(Bucket='mentaljolt.com')

# Get a list of all tags
tag_set = bucket_tagging['TagSet']

print(tag_set[1])
