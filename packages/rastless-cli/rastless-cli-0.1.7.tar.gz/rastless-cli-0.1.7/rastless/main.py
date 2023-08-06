import os
from rastless.aws.db import Database
from rastless.aws.s3 import S3Bucket


class RastlessCfg:
    def __init__(self, debug=False):
        self.db_table_name = os.getenv("RASTLESS_TABLE_NAME", "rastless")
        self.db = Database(self.db_table_name)
        self.s3_bucket_name = os.getenv("RASTLESS_BUCKET_NAME", "rastless")
        self.s3_bucket = S3Bucket(self.s3_bucket_name)
        self.debug = debug
