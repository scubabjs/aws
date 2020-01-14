#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.8

import logging
import boto3
import argparse
from botocore.exceptions import ClientError


def Main():
    my_parser = argparse.ArgumentParser(
        prog='get-s3-lifecycle', description='Attempt to retrevie the lifecycle of a S3 bucket')
    my_parser.add_argument('bucket', type=str,
                           help='specify AWS S3 bucket to query')
    args = my_parser.parse_args()
    test_bucket_name = args.bucket
    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    # Retrieve the lifecycle configuration
    lifecycle_config = get_bucket_lifecycle(test_bucket_name)
    if lifecycle_config is not None:
        if not lifecycle_config:
            logging.info(
                f'{test_bucket_name} does not have a lifecycle configuration.')
        else:
            for rule in lifecycle_config:
                logging.info(lifecycle_config)


def get_bucket_lifecycle(bucket_name):
    # Retrieve the configuration
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
            return []
        else:
            # e.response['Error']['Code'] == 'NoSuchBucket', etc.
            logging.error(e)
            return None
    #print(response)
    return response['Rules']


if __name__ == '__main__':
    Main()
