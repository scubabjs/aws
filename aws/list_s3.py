#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.8


import boto3
import argparse
import logging
from botocore.exceptions import ClientError


def Main():
    my_parser = argparse.ArgumentParser(
        prog='list_s3', description='List the S3 buckets in an AWS account')
    group = my_parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all',
                       help='list all buckets', action='store_true')
    group.add_argument('-n', '--name',
                       help='specify that bucket names should be used for the search')
    group.add_argument('-t', '--tag',
                       help='specify that tags on the bucket should be used for the search')
    args = my_parser.parse_args()
    if (args.all):
        list_buckets(None)
    elif (args.name != None):
        list_buckets(args.name)
    elif (args.tag != None):
        list_tagged_buckets(args.tag)


def list_buckets(string):

    s3 = boto3.client('s3')
    try:
        # Call S3 to list current buckets
        response = s3.list_buckets()
        # Output the bucket names
        for bucket in response["Buckets"]:
            if (string == None):
                print(f'{bucket["Name"]}')
            elif (string in bucket["Name"]):
                print(f'{bucket["Name"]}')
    except ClientError as e:
        logging.info('No buckets in account?')


def list_tagged_buckets(string):

    s3 = boto3.client('s3')
    try:
        # Call S3 to list current buckets
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            (bucket['Name'])
            try:
                tags = s3.get_bucket_tagging(Bucket=(bucket['Name']))
                tag = tags['TagSet']
                t = str(tag)
                if (string in t):
                    print(bucket['Name'])
            except ClientError as e:
                logging.info('Pretty sure there are no tags on this bucket')
    except ClientError as e:
        logging.info(
            'The bucket does not exist, how we even got here is a question, raise the exception:')
    return


if __name__ == '__main__':
    Main()
