#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.8
#
import os.path

import logging
import boto3
import argparse
from botocore.exceptions import ClientError


def Main():

    my_parser = argparse.ArgumentParser(
        prog='upload_s3', description='Upload a file to an S3 bucket')
    my_parser.add_argument('bucket', type=str,
                           help='specify AWS S3 bucket to upload to')
    my_parser.add_argument('file', type=str,
                           help='specify the local file to upload')
    my_parser.add_argument('-o', '--object', type=str, nargs='?', default=None,
                           help='object name to upload the file as')
    args = my_parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.WARN,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    if (args.object == None):
        bucket_object = args.file
    else:
        bucket_object = args.object
    # Upload a file
    response = upload_file(args.file, args.bucket, bucket_object)
    if response:
        logging.info('File was uploaded')


def upload_file(file, bucket, object):

    logging.info('Bucket:', bucket, 'File:', file, 'Object:', object)

    if object is None:
        object = file
    if (os.path.isfile(file)):
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file, bucket, object)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    logging.info(file, ':  No such file')
    print(file, ':  No such file')
    return False


if __name__ == '__main__':
    Main()
