```commandline
aws iam create-user --user-name CLIuser
aws iam create-group --group-name CLIgroup
aws iam add-user-to-group --user-name CLIuser --group-name CLIgroup
aws iam create-access-key --user-name CLIuser

aws iam list-policies
aws iam create-role --role-name CLIrole --assume-role-policy-document file://Role.json
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess --role-name CLIrole
```

```commandline
aws ec2 describe-vpcs 
// vpc-0127a6e04d973a411

aws ec2 describe-key-pairs
aws ec2 create-key-pair --key-name CLIEC2Key --query 'KeyMaterial' --output text > CLIEC2Key.pem

aws ec2 create-security-group --group-name CLISecurityGroup --description "CLISecurityGroup"

aws ec2 run-instances --image-id ami-0bd6906508e74f692 --count 1 --instance-type t2.micro --key-name CLIEC2Key --security-group-ids sg-0e627b70fb0a73d09 --subnet-id subnet-0d11b270c746edf52
```

```commandline
aws s3api create-bucket --bucket shravanclibucket --region ap-southeast-1 --create-bucket-configuration LocationConstraint=ap-southeast-1
```