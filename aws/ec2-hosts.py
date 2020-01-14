#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.2
#
#  This code assumes that you have a vaild set of AWS keys and the AWS CLI package is installed.
#
#  Buy default this will only list 'running' instances, if you want all instances in the AWS
#  accout you will need to set the '--all' flag, which will show all ec2 instances running or stopped.

import argparse
import boto3
from botocore import exceptions


def Main():
    my_parser = argparse.ArgumentParser(
        prog='create-hosts-ec2', description='Generates a /etc/hosts type file for ec2 instances')
    my_parser.add_argument('-a', '--all',
                           help='specify all ec2 instances (running & stopped)', action="store_true")
    args = my_parser.parse_args()

    ec2 = boto3.client('ec2')

    try:
        if args.all:
            instances = ec2.describe_instances()
        else:
            instances = ec2.describe_instances(
                Filters=[{
                    'Name': 'instance-state-name',
                    'Values': ['running']
                },
                ])
    except exceptions.ClientError:
        exit(1)
    for instance in instances['Reservations']:
        print(instance['Instances'][0]['PrivateIpAddress'] + '\t'
              + instance['Instances'][0]['Tags'][0]['Value'] + '\t # '
              + instance['Instances'][0]['InstanceId'] + ' '
              + instance['Instances'][0]['State']['Name'] + ' '
              + instance['Instances'][0]['InstanceType'])
        # 172.31.40.151	splunk-1	 # i-012043f7fb5f94397 running t2.micro


if __name__ == '__main__':
    Main()
