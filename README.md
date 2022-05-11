# AWS-Handling

- Cloud computing is a model for enabling convenient and on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.
- On-demand self-service, Broad network access, Resource pooling, Rapid elasticity, Measured service - Pay as you use

## Infrastructure as a service (IaaS)
A vendor provides clients pay-as-you-go access to storage, networking, servers, and other computing resources in the cloud.
## Platform as a service (PaaS)
A service provider offers access to a cloud-based environment in which users can build and deliver applications. The provider supplies underlying infrastructure.
## Software as a service (SaaS)
A service provider delivers software and applications through the internet. Users subscribe to the software and access it via the web or vendor APIs.

# AWS
- Regions divided into Availability Zones
    - Connected Via Edge Locations and Fiber Optics

**Set up AWS CLI after installation** 
```commandline
aws configure

aws iam create-group --group-name MyIamGroup
aws iam create-user --user-name MyUser
aws iam add-user-to-group --user-name MyUser --group-name MyIamGroup
aws iam get-group --group-name MyIamGroup
```
**Install boto3**
```Python
import boto3

client = boto3.client('iam')
```