import boto
import boto.s3.connection
from config import *
from boto.s3.key import Key

boto.config.add_section('s3')
boto.config.set('s3', 'use-sigv4', 'True')

def get_connection():
    return boto.connect_s3(aws_access_key_id=AWS_ACCESS_KEY,
                           aws_secret_access_key=AWS_SECRET_KEY,
                           host=S3_HOST,
                           port=S3_PORT,
                           is_secure=S3_IS_SECURE)

def get_presigned_url(key):
    conn = get_connection()
    b = conn.get_bucket(S3_BUCKET)
    b.new_key(key)
    url = conn.generate_url(
        expires_in=long(86400),
        method='PUT',
        bucket=S3_BUCKET,
        key=key,
        query_auth=False
    )
    return url


def upload_to_s3(file, key_name):
    conn = get_connection()
    b = conn.get_bucket(S3_BUCKET)
    key = Key(b)
    key.key = key_name
    key.set_contents_from_filename(file)

if __name__ == '__main__':

    print get_presigned_url('test222')
    # upload_to_s3('./docker-compose.yml', 'docker-compose')
