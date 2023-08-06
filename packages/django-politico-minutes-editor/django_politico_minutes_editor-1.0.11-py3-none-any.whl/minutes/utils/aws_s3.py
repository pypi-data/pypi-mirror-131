import boto3
import json
import uuid
from django.conf import settings


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


session = boto3.session.Session(
    region_name='us-east-1',
    aws_access_key_id=settings.MINUTES_PUBLISH_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.MINUTES_PUBLISH_AWS_SECRET_ACCESS_KEY
)

s3 = session.client('s3')


class S3Response:
    ok = None
    status_code = None
    body = None
    headers = None

    def __init__(self, resp):
        resp_payload = resp['ResponseMetadata']
        self.status_code = resp_payload['HTTPStatusCode']
        self.headers = resp_payload['HTTPHeaders']

        self.ok = self.status_code >= 200 and self.status_code < 300


def put_json(payload, path, mode="STAGING"):
    bucket = (
        "interactives.politico.com"
        if mode == "PRODUCTION"
        else "staging.interactives.politico.com"
    )

    resp = s3.put_object(
        Body=json.dumps(payload, cls=ComplexEncoder),
        Bucket=bucket,
        Key=path,
        CacheControl='max-age=300',
        ContentType='application/json',
        StorageClass='STANDARD',
    )

    return S3Response(resp)
