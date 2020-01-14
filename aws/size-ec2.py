#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.8
#
#  This code assumes that you have a vaild set of AWS keys and the AWS CLI package is installed.
#


import boto3
import argparse


def Main():
    my_parser = argparse.ArgumentParser(
        prog='size-ec2', description='Stop, Resize, Start an existing EC instance')
    my_parser.add_argument('instance', type=str,
                           help='specify AWS instance to resize')
    my_parser.add_argument('type', type=str,
                           help='specify AWS machine type')
    my_parser.add_argument('-y', '--yes', help='do not ask for confirmation to execute',
                           action="store_true")
    args = my_parser.parse_args()

    if (check_ec2(args.instance) and check_type(args.type)):
        if not args.yes:
            print('This will STOP the AWS instance',
                  args.instance, 'type "yes" to procede: ', end='')
            if (input() == 'yes'):
                # print('took input')
                do_aws_stuff(args.instance, args.type)
            else:
                # print('got bad input')
                exit
        else:
            # print('did not take input')
            do_aws_stuff(args.instance, args.type)
    else:
        exit


def do_aws_stuff(instance, type):
    #
    # There can be timing issues, if you stop and stop the same instance rapidly
    # the size change will not take effect, wait 5 secs and re-run.
    #

    client = boto3.client('ec2')
    # Stop AWS Instance
    client.stop_instances(InstanceIds=[instance])
    # Wait until is down
    waiter = client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance])
    # Change the machine type to a vaild type
    client.modify_instance_attribute(
        InstanceId=instance, Attribute='instanceType', Value=type)
    # Start the updated instance
    client.start_instances(InstanceIds=[instance])
    # Should add code here to optionally print out the IP of the new box.
    return(0)


def check_type(type):
    vaild_types = ('t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 'm4.large', 't2.xlarge', 't2.x2large',
                   'm4.10xlarge', 'm4.xlarge', 'm4.16xlarge', 'm4.4xlarge', 'm4.2xlarge', 'm4.large',
                   'r4.10xlarge', 'r4.xlarge', 'r4.16xlarge', 'r4.4xlarge', 'r4.2xlarge', 'r4.large')
    if type in vaild_types:
        # print('Vaild machine type', type)
        return(True)
    else:
        print('Invaild machine type', type)
        print('Vaild types: ', list(vaild_types))
        return(False)


def check_ec2(instance):
    instance_prefix = 'i-'
    if instance_prefix == instance[0:2]:
        # print('Vaild instance name', instance)
        return(True)
    else:
        print('Invaild instance name, instance name must start with i-', instance)
        return(False)


if __name__ == '__main__':
    Main()
