import boto3
import getpass
import botocore
import csv

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


def get_available_regions(service):
    """ Get available regions for a given AWS service. """
    return boto3.Session().get_available_regions(service)

def get_user_region_choice():
    """ Prompt the user to choose regions. """
    print("Available AWS regions are:")
    all_regions = get_available_regions('ec2')  # Using EC2 as a reference for available regions
    for region in all_regions:
        print(region)
    user_input = input("Enter a region from the list above, 'all' for all regions, or 'multiple' to specify multiple regions: ")
    
    if user_input.lower() == 'all':
        return all_regions
    elif user_input.lower() == 'multiple':
        selected_regions = input("Enter regions separated by a comma (e.g., us-east-1,eu-west-1): ")
        return [region.strip() for region in selected_regions.split(',')]
    else:
        return [user_input.strip()]


def gather_ec2_instance_data(session, region):
    ec2_data = []
    ec2 = session.client('ec2', region_name=region)
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_data = {
                "Region": region,
                "Resource Type": "EC2 Instance",
                "ID": instance['InstanceId'],
                "Type": instance['InstanceType'],
                "State": instance['State']['Name'],
                "Public IP": instance.get('PublicIpAddress', 'N/A'),
                "Private IP": instance.get('PrivateIpAddress', 'N/A')
            }
            ec2_data.append(instance_data)
    return ec2_data

def gather_s3_bucket_data(session):
    s3_data = []
    s3 = session.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket_data = {
            "Resource Type": "S3 Bucket",
            "Name": bucket['Name'],
            "Creation Date": bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")
        }
        s3_data.append(bucket_data)
    return s3_data


def gather_route53_domain_data(session):
    route53_data = []
    route53 = session.client('route53')
    response = route53.list_hosted_zones()
    for zone in response['HostedZones']:
        domain_data = {
            "Resource Type": "Route 53 Domain",
            "Name": zone['Name'],
            "ID": zone['Id']
        }
        route53_data.append(domain_data)
    return route53_data

def gather_cloudfront_distribution_data(session):
    cloudfront_data = []
    cloudfront = session.client('cloudfront')
    response = cloudfront.list_distributions()
    if 'DistributionList' in response and 'Items' in response['DistributionList']:
        for distribution in response['DistributionList']['Items']:
            distribution_data = {
                "Resource Type": "CloudFront Distribution",
                "ID": distribution['Id'],
                "Domain Name": distribution['DomainName'],
                "Status": distribution['Status']
            }
            cloudfront_data.append(distribution_data)
    return cloudfront_data

def gather_acm_certificate_data(session):
    acm_data = []
    acm = session.client('acm')
    certificates = acm.list_certificates()
    for certificate in certificates['CertificateSummaryList']:
        certificate_data = {
            "Resource Type": "ACM Certificate",
            "ARN": certificate['CertificateArn'],
            "Domain Name": certificate['DomainName']
        }
        acm_data.append(certificate_data)
    return acm_data


def gather_ecr_repository_data(session):
    ecr_data = []
    ecr = session.client('ecr')
    repositories = ecr.describe_repositories()
    for repo in repositories['repositories']:
        repo_data = {
            "Resource Type": "ECR Repository",
            "Name": repo['repositoryName'],
            "URI": repo['repositoryUri']
        }
        ecr_data.append(repo_data)
    return ecr_data


def gather_eks_cluster_data(session):
    eks_data = []
    eks = session.client('eks')
    clusters = eks.list_clusters()
    for cluster_name in clusters['clusters']:
        cluster_data = {
            "Resource Type": "EKS Cluster",
            "Name": cluster_name
        }
        eks_data.append(cluster_data)
    return eks_data

def gather_iam_user_and_role_data(session):
    iam_data = []
    iam = session.client('iam')
    users = iam.list_users()
    for user in users['Users']:
        user_data = {
            "Resource Type": "IAM User",
            "UserName": user['UserName']
        }
        iam_data.append(user_data)
    roles = iam.list_roles()
    for role in roles['Roles']:
        role_data = {
            "Resource Type": "IAM Role",
            "RoleName": role['RoleName']
        }
        iam_data.append(role_data)
    return iam_data

def gather_elastic_ip_data(session):
    eip_data = []
    ec2 = session.client('ec2')
    eips = ec2.describe_addresses()
    for eip in eips['Addresses']:
        eip_info = {
            "Resource Type": "Elastic IP",
            "Public IP": eip['PublicIp'],
            "Allocation ID": eip.get('AllocationId', 'N/A')
        }
        eip_data.append(eip_info)
    return eip_data

def gather_vpc_data(session):
    vpc_data = []
    ec2 = session.client('ec2')
    vpcs = ec2.describe_vpcs()
    for vpc in vpcs['Vpcs']:
        vpc_info = {
            "Resource Type": "VPC",
            "VPC ID": vpc['VpcId'],
            "State": vpc['State']
        }
        vpc_data.append(vpc_info)
    return vpc_data

def write_to_csv(data, filename):
    if not data:
        return False

    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return True

def main():
    access_key = input("Enter your AWS Access Key ID: ")
    secret_key = getpass.getpass("Enter your AWS Secret Access Key: ")
    
    # Get user's choice of regions
    chosen_regions = get_user_region_choice()

    for region in chosen_regions:
        session = get_aws_session(access_key, secret_key, region)

        print(f"\n--- Listing resources in {region} ---")
        print("\nListing EC2 instances:")
        list_ec2_instances(session, region)
    
        if region == chosen_regions[0]:  # For global services, list them only once
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
    all_data = []
    for region in chosen_regions:
        session = get_aws_session(access_key, secret_key, region)

        # Gather data from each service
        all_data.extend(gather_ec2_instance_data(session, region))
        all_data.extend(gather_s3_bucket_data(session))
        all_data.extend(gather_route53_domain_data(session))
        all_data.extend(gather_cloudfront_distribution_data(session))
        all_data.extend(gather_acm_certificate_data(session))
        all_data.extend(gather_ecr_repository_data(session))
        all_data.extend(gather_eks_cluster_data(session))
        all_data.extend(gather_iam_user_and_role_data(session))
        all_data.extend(gather_elastic_ip_data(session))
        all_data.extend(gather_vpc_data(session))

    # Write data to CSV
    if write_to_csv(all_data, "aws_resource_inventory.csv"):
        print("Data exported to aws_resource_inventory.csv")
    else:
        print("No data to export.")


if __name__ == "__main__":
    main()

