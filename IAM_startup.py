import boto3
import json

with open('Role.json') as f:
    role_policy = json.load(f)
role_policy_string = json.dumps(role_policy)

client = boto3.client('iam')
user = 'BOTO3user'
client.create_user(UserName=user)
arn = 'arn:aws:iam::aws:policy/PowerUserAccess'
client.attach_user_policy(UserName=user, PolicyArn=arn)
client.create_access_key(UserName=user)
role = 'BOTO3role'
client.create_role(RoleName=role, AssumeRolePolicyDocument=role_policy_string)
client.attach_role_policy(RoleName=role, PolicyArn=arn)
group = 'BOTO3group'
client.create_group(GroupName=group)
client.add_user_to_group(GroupName=group, UserName=user)
