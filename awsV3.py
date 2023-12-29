import boto3
import getpass
import botocore

def get_aws_session(access_key, secret_key, region):
    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

def list_ec2_instances(session, region):
    try:
        ec2 = session.client('ec2', region_name=region)
        instances = ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance Type: {instance['InstanceType']}")
                print(f"Launch Time: {instance['LaunchTime']}")
                print(f"State: {instance['State']['Name']}")
                print(f"Public IP: {instance.get('PublicIpAddress', 'N/A')}")
                print(f"Private IP: {instance.get('PrivateIpAddress', 'N/A')}")
                print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing EC2 instances: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def list_s3_buckets(session):
    try:
        s3 = session.client('s3')
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(f"Bucket Name: {bucket['Name']}")
            print(f"Creation Date: {bucket['CreationDate']}")
            location = s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
            print(f"Bucket Location: {location or 'us-east-1'}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing s3 Buckets: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def list_route53_domains(session):
    try:
        route53 = session.client('route53')
        response = route53.list_hosted_zones()
        for zone in response['HostedZones']:
            print(f"Domain Name: {zone['Name']}")
            print(f"Zone ID: {zone['Id']}")
            records = route53.list_resource_record_sets(HostedZoneId=zone['Id'])
            for record in records['ResourceRecordSets']:
                print(f"Record Name: {record['Name']} - Type: {record['Type']}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing Route 53 Domains: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_cloudfront_distributions(session):
    try:
        cloudfront = session.client('cloudfront')
        response = cloudfront.list_distributions()
        if 'DistributionList' in response and 'Items' in response['DistributionList']:
            for distribution in response['DistributionList']['Items']:
                print(f"Distribution ID: {distribution['Id']}")
                print(f"Domain Name: {distribution['DomainName']}")
                print(f"Status: {distribution['Status']}")
                print(f"Enabled: {distribution['Enabled']}")
                print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing Cloudfront Distributions: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_acm_certificates(session):
    try:
        acm = session.client('acm')
        certificates = acm.list_certificates()
        for certificate in certificates['CertificateSummaryList']:
            print(f"Certificate ARN: {certificate['CertificateArn']}")
            print(f"Domain Name: {certificate['DomainName']}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing ACM certificates: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

def list_ecr_repositories(session):
    try:
        ecr = session.client('ecr')
        repositories = ecr.describe_repositories()
        for repo in repositories['repositories']:
            print(f"Repository Name: {repo['repositoryName']}")
            print(f"Repository URI: {repo['repositoryUri']}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing ECR repositories: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

def list_eks_clusters(session):
    try:
        eks = session.client('eks')
        clusters = eks.list_clusters()
        for cluster_name in clusters['clusters']:
            print(f"Cluster Name: {cluster_name}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing EKS clusters: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

def list_iam_users_and_roles(session):
    try:
        iam = session.client('iam')
        users = iam.list_users()
        for user in users['Users']:
            print(f"IAM User: {user['UserName']}")
        roles = iam.list_roles()
        for role in roles['Roles']:
            print(f"IAM Role: {role['RoleName']}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing IAM users and roles: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

def list_elastic_ips(session):
    try:
        ec2 = session.client('ec2')
        eips = ec2.describe_addresses()
        for eip in eips['Addresses']:
            print(f"Elastic IP: {eip['PublicIp']} - Allocation ID: {eip.get('AllocationId', 'N/A')}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing Elastic IPs: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

def list_vpcs(session):
    try:
        ec2 = session.client('ec2')
        vpcs = ec2.describe_vpcs()
        for vpc in vpcs['Vpcs']:
            print(f"VPC ID: {vpc['VpcId']} - State: {vpc['State']}")
            print("-------------------------------------------------")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing VPCs: {e.response['Error']['Code']} - {e.response['Error']['Message']}")


def main():
    access_key = input("Enter your AWS Access Key ID: ")
    secret_key = getpass.getpass("Enter your AWS Secret Access Key: ")
    region = input("Enter your AWS Default Region (e.g., us-west-1): ")

    session = get_aws_session(access_key, secret_key, region)

    regions = [region]  # or a list of regions if needed
    for reg in regions:
        print(f"Listing EC2 instances in {reg}:")
        list_ec2_instances(session, reg)
    
    print("\nListing all S3 buckets:")
    list_s3_buckets(session)

    print("\nListing all Route 53 domains:")
    list_route53_domains(session)

    print("\nListing all CloudFront distributions:")
    list_cloudfront_distributions(session)

    print("\nListing ACM Certificates:")
    list_acm_certificates(session)

    print("\nListing ECR Repositories:")
    list_ecr_repositories(session)

    print("\nListing EKS Clusters:")
    list_eks_clusters(session)

    print("\nListing IAM Users and Roles:")
    list_iam_users_and_roles(session)

    print("\nListing Elastic IPs:")
    list_elastic_ips(session)

    print("\nListing VPCs:")
    list_vpcs(session)

if __name__ == "__main__":
    main()

