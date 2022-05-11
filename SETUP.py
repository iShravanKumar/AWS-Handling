import boto3


def create_ec2():
    client = boto3.client('ec2')
    client.run_instances(
        ImageId='ami-0bd6906508e74f692',
        InstanceType='t2.micro',
        KeyName='EC2Key',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=['sg-00fb1c31cfc37abc7'],
        SubnetId='subnet-0d11b270c746edf52',
        IamInstanceProfile={
            'Arn': 'arn:aws:iam::634171635162:instance-profile/EC2-S3'
        }
    )


# create_ec2()


def create_s3():
    s3_client = boto3.client('s3', region_name='ap-southeast-1')
    location = {'LocationConstraint': 'ap-southeast-1'}
    s3_client.create_bucket(Bucket='s3shravanb01', CreateBucketConfiguration=location)


# create_s3()
