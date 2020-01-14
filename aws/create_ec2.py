import boto3
ec2 = boto3.resource('ec2')

# create a new EC2 instance
instances = ec2.create_instances(
#     ImageId='ami-00b6a8a2bd28daf19',
     ImageId='ami-0c322300a1dd5dc79',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='boto3-keypair'
 )
