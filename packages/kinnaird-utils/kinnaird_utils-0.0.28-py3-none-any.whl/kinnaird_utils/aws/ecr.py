from kinnaird_utils.aws.login import get_boto3_client


def get_latest_ecr_image_tag(repository_name: str, region: str, profile: str = None) -> str:
    """aws ecr describe-images --profile personal --region us-east-1 --output json --repository-name zap --query 'sort_by(imageDetails,& imagePushedAt)[-1].imageTags[0]'"""
    client = get_boto3_client(service="ecr", region=region, profile=profile)
    response = client.describe_images(repositoryName=repository_name, filter={"tagStatus": "TAGGED"})
    adjusted = sorted(response["imageDetails"], key=lambda i: int(i['imagePushedAt']))
    latest_image_tag = adjusted[-1]["imageTags"][0]
    return latest_image_tag
