#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.4

import boto3
import argparse
import logging
from botocore.exceptions import ClientError

#
# Vaild s3 types STANDARD, STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, GLACIER, DEEP_ARCHIVE
#
#
lifecycle_config = {
    "Rules": [
        {
            "ID": "S3 30day StandardIA 90day Glacier Transition Rule",
            "Filter": {
                "Prefix": ""
            },
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 300,
                    "StorageClass": "STANDARD_IA"
                },
                {
                    "Days": 900,
                    "StorageClass": "GLACIER"
                }
            ],
            "NoncurrentVersionTransitions": [
                {
                    "NoncurrentDays": 400,
                    "StorageClass": "STANDARD_IA"
                },
                {
                    "NoncurrentDays": 1000,
                    "StorageClass": "GLACIER"
                }
            ]
        }
    ]
}
# lifecycle_config = {
#     'Rules': [
#         {'ID': 'S3 30day StandardIA 90day Glacier Transition Rule',
#          'Filter': {'Prefix': ''},
#          'Status': 'Enabled',
#          'Transitions': [
#              {'Days': 300,
#               'StorageClass': 'STANDARD_IA'},
#              {'Days': 900,
#               'StorageClass': 'GLACIER'}
#          ]}
#     ]}


def Main():
    my_parser = argparse.ArgumentParser(
        prog='set_s3_lifecycle', description='Attempt to set the lifecycle of a S3 bucket')
    my_parser.add_argument('bucket', type=str,
                           help='specify AWS S3 bucket to modify')
    my_parser.add_argument('-v', '--verbose', help='verbose output, show lifecycle after modifying',
                           action="store_true")
    args = my_parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    #
    # Vaild s3 types STANDARD, STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, GLACIER, REDUCED_REDUNDANCY
    #
    #

    if (get_bucket_lifecycle(args.bucket) != ''):
        set_lifecycle(args.bucket, lifecycle_config)
        if (args.verbose):
            print_lifecycle(args.bucket)
    else:
        logging.info('Unable to update the lifecyle policy for', args.bucket)


def set_lifecycle(bucket, lifecycle):

    # aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://<file.json>

    s3 = boto3.client('s3')
    try:
        s3.put_bucket_lifecycle_configuration(Bucket=bucket,
                                              LifecycleConfiguration=lifecycle)
    except ClientError as e:
        # print(e.response)
        return False
    return True


def get_bucket_lifecycle(bucket):
    s3_client = boto3.client('s3')
    # aws s3api get-bucket-lifecycle-configuration --bucket <bucket>
    try:
        response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
            return response['Rules']
        else:
            e.response['Error']['Code'] == 'NoSuchBucket'
            logging.error(bucket, 'bucket does not exist')
            return None
    return response['Rules']


def print_lifecycle(bucket):
    lifecycle_config = get_bucket_lifecycle(bucket)
    if lifecycle_config is not None:
        if not lifecycle_config:
            logging.error(bucket, 'does not have a lifecycle configuration.')
        else:
            for rule in lifecycle_config:
                print(lifecycle_config)


if __name__ == '__main__':
    Main()
