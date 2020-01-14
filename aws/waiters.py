
import boto3

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

# List all of the possible waiters for both clients
print("s3 waiters:")
a = s3.waiter_names
print(a)

print("ec2 waiters:")
ec2.waiter_names
b = ec2.waiter_names
print(b)
