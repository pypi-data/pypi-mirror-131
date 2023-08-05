import logging
import boto3
logger = logging.getLogger(__name__)


def get_available_regions_for_service(service: str):
    """AWS exposes their list of regions as an API. Gather the list."""
    regions = boto3.session.Session().get_available_regions(service)
    logger.debug("The service %s does not have available regions. Returning us-east-1 as default")
    if not regions:
        regions = ["us-east-1"]
    return regions
