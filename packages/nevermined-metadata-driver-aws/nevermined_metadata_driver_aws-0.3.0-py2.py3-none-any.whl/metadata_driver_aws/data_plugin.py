import logging
import os
import tempfile

import boto3
import botocore
from metadata_driver_interface.data_plugin import AbstractPlugin
from metadata_driver_interface.exceptions import DriverError

from metadata_driver_aws.log import setup_logging
from metadata_driver_aws.s3_client import get_s3_instance


setup_logging()


class Plugin(AbstractPlugin):
    def __init__(self, config=None):
        """Initialize a :class:`~.S3_Plugin`.

        The S3_plugin is a wrapper around the boto3 S3 client and resource API.

        Configuration of the AWS credentials is handled by boto3 according to the user's environment.

        Args:
             config(dict): Configuration options
        """
        # The S3 client object
        s3_instance = get_s3_instance(config)
        self.driver = s3_instance.s3_resource
        self.sign_client = s3_instance.s3_client
        self.logger = logging.getLogger(__name__)

    @property
    def type(self):
        """str: the type of this plugin (``'AWS'``)"""
        return "AWS"

    @staticmethod
    def validate_s3_path(path):
        """Validate a path if it represents correctly a S3 path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..DriverError`: if the file is not uploaded correctly."""
        return path.startswith("s3://")

    def parse_s3_path(self, path):
        """Validate a path if it represents correctly a S3 path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..DriverError`: if the file is not uploaded correctly."""
        if self.validate_s3_path(path):
            bucket = path[5:].split("/", 1)[0]
            try:
                path = path[5:].split("/", 1)[1]
            except IndexError:
                path = ""
            return bucket, path
        else:
            self.logger.error(
                f"Path {path} must be a s3 url (format s3://my_bucket/my_file)"
            )
            raise DriverError

    @staticmethod
    def validate_local_path(path):
        """Validate a path if it represents correctly a local path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..DriverError`: if the file is not uploaded correctly."""
        return not path.startswith("s3://")

    def upload(self, local_file, remote_file):
        """Upload file to a remote resource manager
        Args:
            local_file(str): The path of the file to upload.
            remote_file(str): The path of the resource manager where the file is going to be allocated.
        Raises:
            :exc:`~..DriverError`: if the file is not uploaded correctly.

        """
        self.copy(local_file, remote_file)
        self.logger.debug("Uploaded {} to {}".format(local_file, remote_file))

    def upload_bytes(self, content, remote_file):
        """Uploads bytes to a remote resource manager
         Args:
             content(bytes): The bytes to upload
            remote_file(str): The path of the resource manager where the file is going to be allocated.
         Raises:
             :exc:`~..DriverError`: if the file is not uploaded correctly.

        """
        f = tempfile.NamedTemporaryFile()
        f.write(content)
        f.flush()
        self.copy(f.name, remote_file)
        f.close()
        self.logger.debug("Uploaded content to {}".format(remote_file))

    def download(self, remote_file, local_file):
        """Download file from a remote resource manager
        Args:
             remote_file(str): The path in the resource manager of the file to download from.
             local_file(str): The path to the file to download to..
        Raises:
             :exc:`~..DriverError`: if the file is not downloaded correctly.
        """
        self.copy(remote_file, local_file)
        self.logger.debug("Downloaded {} to {}".format(remote_file, local_file))

    def download_bytes(self, remote_file):
        """Download a remote content and returned in the shape of bytes
        Args:
             remote_file(str): The path in the resource manager of the file to download from.
        Raises:
             :exc:`~..DriverError`: if the file is not downloaded correctly.
        """
        with tempfile.NamedTemporaryFile(delete=False) as local_file:
            self.copy(remote_file, local_file.name)
            self.logger.debug("Downloaded {} to {}".format(remote_file, local_file.name))
            f = open(local_file.name, "rb")
            content = f.read()
            os.remove(local_file.name)

            return content

    def list(self, remote_folder):
        """List all the files of a cloud directory.
        Args:
             remote_folder(str): Name of the directory to list.
        Returns:
            dict: List with the name of the file of a directory.
        Raises:
             :exc:`~..DriverError`: if the directory does not exist.
        """
        self.logger.debug("Retrieving items in {}".format(remote_folder))

        bucket, path = self.parse_s3_path(remote_folder)
        try:
            bucket_s3 = self.driver.Bucket(bucket)
            objects = bucket_s3.objects.filter(Prefix=path)
            result = [o.key for o in objects]
            return result
        except Exception as e:
            raise DriverError

    def list_buckets(self):
        bucket_iterator = self.driver.buckets.all()

        # extract only the name of the bucket
        bucket_names = [b.name for b in bucket_iterator]
        logging.debug(f"Found {bucket_names} buckets")

        return bucket_names

    def copy(self, source_path: str, dest_path: str):
        """Copy file from a path to another path.
        Args:
            source_path(str): The path of the file to be copied.
            dest_path(str): The destination path where the file is going to be allocated.
        Raises:
            :exc:`~..DriverError`: if the file is not uploaded correctly.
        """
        if not (source_path.startswith("s3://") or dest_path.startswith("s3://")):
            self.logger.error(
                "Source or destination must be a s3 url (format s3://my_bucket/my_file)"
            )
            raise DriverError
        if source_path.startswith("s3://") and dest_path.startswith("s3://"):
            self.logger.error("Source or destination must be a local directory")
            raise DriverError

        # Check if resources exists and can read
        if source_path.startswith("s3://"):
            bucket = source_path[5:].split("/", 1)[0]
            path = source_path[5:].split("/", 1)[1]
            try:
                bucket_s3 = self.driver.Bucket(bucket)
                bucket_s3.download_file(path, dest_path)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    self.logger.error(
                        f"Source file {path} in bucket {bucket} not found"
                    )
                    raise DriverError

        elif dest_path.startswith("s3://"):
            bucket = dest_path[5:].split("/", 1)[0]
            path = dest_path[5:].split("/", 1)[1]
            try:
                bucket_s3 = self.driver.Bucket(bucket)
                bucket_s3.upload_file(source_path, path)
            except botocore.exceptions.ClientError:
                self.logger.error(
                    f"There were a problem uploading local file {source_path}. Please check file exists and bucket "
                    f"{bucket} is accesible"
                )

    def generate_url(self, remote_file):
        """Generate a signed url that give access for a period of time to the resource
        Args:
            remote_file(str): The path in the resource manager of the file to give access.
        Raises:
             :exc:`~..DriverError`: if the file does not exist or if the action could not be done.
        """
        bucket, path = self.parse_s3_path(remote_file)
        url = self.sign_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": path},
            ExpiresIn=3600 * 24,  # 1day
        )
        return url

    def delete(self, remote_file):
        """Delete a file of a remote resource manager
        Args:
             remote_file(str): The path in the resource manager of the file to delete..
        Raises:
             :exc:`~..DriverError`: if the path does not exist or if the action could not be done.
        """

        bucket, path = self.parse_s3_path(remote_file)
        delete = {"Objects": [{"Key": path}]}
        try:
            bucket_s3 = self.driver.Bucket(bucket)
            bucket_s3.delete_objects(Delete=delete)
        except Exception as e:
            raise DriverError
        self.logger.debug("Deleted {} from {}".format(path, bucket))

    def get_bucket(self, bucketname):
        # TODO: add
        pass

    def create_bucket(self, bucket):
        """Create a bucket in S3
        Args:
            bucket(str): The name of the bucket
        Raises:
             :exc:`~..DriverError`
        """
        try:
            bucket = self.driver.create_bucket(Bucket=bucket)
        except Exception:
            logging.error("Error creating bucket %s", bucket)
            raise DriverError(f"Error creating bucket {bucket}")
        self.logger.debug("Created bucket {}".format(bucket))

        return bucket

    def delete_bucket(self, bucket_name):
        """Delete a bucket in S3
        Args:
            bucket_name(str): The name of the bucket
        Raises:
             :exc:`~..DriverError`
        """
        try:
            bucket = self.driver.Bucket(bucket_name)
            for key in bucket.objects.all():
                key.delete()
            bucket.delete()
        except Exception:
            logging.error(f"Error deleting bucket {bucket_name}")
            raise DriverError
        self.logger.debug("Deleted bucket {}".format(bucket_name))

    def create_directory(self, remote_folder):
        """Create a directory in S3
        Args:
            remote_folder(str): The path of the remote directory
        Raises:
             :exc:`~..DriverError`: if the directory already exists.
        """
        bucket, path = self.parse_s3_path(remote_folder)
        if bucket == "" or path == "":
            self.logger.error("Remote folder can not be empty")
            raise DriverError
        path = path + "/" if not path.endswith("/") else path
        try:
            bucket = self.create_bucket(bucket)
            bucket.put_object(Body="", Key=path)
        except Exception:
            raise DriverError

    def retrieve_availability_proof(self):
        """TBD"""
        pass
