import boto3
import getpass

def get_aws_session(access_key, secret_key, region):
    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

def list_ec2_instances(session, region):
    ec2 = session.client('ec2', region_name=region)
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"Instance Type: {instance['InstanceType']}")
            print(f"Launch Time: {instance['LaunchTime']}")
            print(f"Public DNS: {instance.get('PublicDnsName', 'N/A')}")
            print("-------------------------------------------------")

def list_s3_buckets(session):
    s3 = session.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"Bucket Name: {bucket['Name']}")
        print(f"Creation Date: {bucket['CreationDate']}")
        location = s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
        print(f"Bucket Location: {location or 'us-east-1'}")
        print("-------------------------------------------------")

def list_route53_domains(session):
    route53 = session.client('route53')
    response = route53.list_hosted_zones()
    for zone in response['HostedZones']:
        print(f"Domain Name: {zone['Name']}")
        print(f"Zone ID: {zone['Id']}")
        records = route53.list_resource_record_sets(HostedZoneId=zone['Id'])
        for record in records['ResourceRecordSets']:
            print(f"Record Name: {record['Name']} - Type: {record['Type']}")
        print("-------------------------------------------------")

def list_cloudfront_distributions(session):
    cloudfront = session.client('cloudfront')
    response = cloudfront.list_distributions()
    if 'DistributionList' in response and 'Items' in response['DistributionList']:
        for distribution in response['DistributionList']['Items']:
            print(f"Distribution ID: {distribution['Id']}")
            print(f"Domain Name: {distribution['DomainName']}")
            print(f"Status: {distribution['Status']}")
            print(f"Enabled: {distribution['Enabled']}")
            print("-------------------------------------------------")

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

if __name__ == "__main__":
    main()
