import boto3
from metadatadb_driver_interface.utils import get_value
from metadata_driver_interface.exceptions import DriverError


_S3_INSTANCE = None


def get_s3_instance(config=None):
    global _S3_INSTANCE
    if _S3_INSTANCE is None:
        _S3_INSTANCE = S3Instance(config)

    return _S3_INSTANCE


class S3Instance:
    def __init__(self, config=None):
        aws_access_key = get_value("aws.access_key", "AWS_ACCESS_KEY_ID", None, config)
        aws_secret_access_key = get_value(
            "aws.secret_access_key", "AWS_SECRET_ACCESS_KEY", None, config
        )
        default_region = get_value(
            "aws.default_region", "AWS_DEFAULT_REGION", None, config
        )
        endpoint_url = get_value("aws.endpoint_url", "AWS_ENDPOINT_URL", None, config)

        if aws_access_key is None:
            raise DriverError(
                "Config value `access_key` or env variable `AWS_ACCESS_KEY_ID` not set"
            )
        if aws_secret_access_key is None:
            raise DriverError(
                "Config value `secret_access_key` or env variable `AWS_SECRET_ACCESS_KEY` not set"
            )
        if default_region is None:
            raise DriverError(
                "Config value `default_region` or env variable `AWS_DEFAULT_REGION` not set"
            )
        if endpoint_url is None:
            raise DriverError(
                "Config value `endpoint_url` or env variable `AWS_ENDPOINT_URL` not set"
            )

        try:
            self.s3_resource = boto3.resource(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                region_name=default_region,
            )
            self.s3_client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                region_name=default_region,
            )
        except Exception as e:
            raise DriverError(f"Error creating and s3 instance: {str(e)}")
