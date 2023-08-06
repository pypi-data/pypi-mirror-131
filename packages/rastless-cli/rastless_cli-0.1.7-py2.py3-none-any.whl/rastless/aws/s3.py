import boto3
import os
from rastless.schemas.db import StepModel


class S3Bucket:
    def __init__(self, bucket_name, region="eu-central-1"):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3', region_name=region)
        self.s3_client = boto3.client('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def create_bucket(self):
        self.bucket.create()

    def delete_object(self, object_name):
        self.s3.Object(self.bucket_name, object_name).delete()

    def upload_object(self, file_name, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)

        self.s3_client.upload_file(file_name, self.bucket_name, object_name)

    def list_bucket_entries(self, prefix=None):
        bucket = self.s3.Bucket(self.bucket_name)
        if prefix:
            files = bucket.objects.filter(Prefix=prefix)
        else:
            files = bucket.objects.all()

        return list(files)


def s3_path_to_filepath(bucket_name, s3_base_path):
    return s3_base_path.replace(f"s3://{bucket_name}/", "")


def delete_layer_step(s3_bucket: S3Bucket, step: StepModel):
    s3_bucket.delete_object(step.cog_filepath)
