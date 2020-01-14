from datetime import datetime, timedelta

# Used to setup other X-Ray compatible modules
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder  # Used to send data from our code

import boto3

patch_all()

time_now = datetime.now()
days_to_delete = 200

client = boto3.client('iam')
resource = boto3.resource('iam')
segement = xray_recorder.begin_segment('Old Roles Destroyer')
# Get Roles
roles = client.list_roles()

# Loop through the roles and print it's Last Used date
for r in roles['Roles']:
    role = resource.Role(name=r['RoleName'])
    subsegment = xray_recorder.begin_subsegment(role.name)
    subsegment.put_annotation('RoleArn', role.arn)
    try:
        # Check if we have a usable usage dict
        if role.role_last_used:

            subsegment.put_annotation('RoleLastUsed', str(
                role.role_last_used['LastUsedDate']))

            # Subtract the LastUsedDate from todays date
            time_diff = time_now - \
                role.role_last_used['LastUsedDate'].replace(tzinfo=None)

            # Check diff is more than or equal to 100 days
            if time_diff.days >= days_to_delete:
                print(f"Attempting to delete Role {role.name}.")

                # Get all Managed Policies and detatch them
                print(f"Removing Managed Policies from {role.name}")
                [role.detach_policy(PolicyArn=policy.arn)
                 for policy in role.attached_policies.all()]

                # Get all Instance Profiles and detatch them
                print(f"Removing role from InstanceProfiles")
                [profile.remove_role(RoleName=role.name)
                 for profile in role.instance_profiles.all()]

                # Get all Inline Policies and delete them
                print(f"Deleting Inline Policies")
                [role_policy.delete() for role_policy in role.policies.all()]

                role.delete()
                print(f"{role.name} deleted\n")
    except Exception as e:
        print(e)
    # Finish recording for the current sub-segement for the role we are checking
    xray_recorder.end_subsegment()

xray_recorder.end_segment()  # Finish our X-Ray Segement recording
