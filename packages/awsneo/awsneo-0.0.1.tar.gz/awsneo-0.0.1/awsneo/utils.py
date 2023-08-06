from json import loads
from contextlib import suppress
from re import sub, MULTILINE
import boto3
from botocore.exceptions import ClientError
from .extras import SecretManagerException, BucketReadFileException


with suppress(Exception):
    scm_client = boto3.client('secretsmanager', region_name="us-east-1")
    s3_client = boto3.client('s3')


def get_connection_data(secret_id: str) -> dict:
    
    """
    Retrieves the secret value stored through secrets Manager (AWS) with the connection to the different database
    sources.

        :type secret_id: string
        :param secret_id: Arn from the Secrets Manager resource
            You must first make sure that you have the permissions on the resource to invoke

        :raises
                SecretManagerException: If bucket is None ad file is None or query is None.
                Exception: normal exception

        :return: Secrets manager data dumped
    """
    try:
        data = scm_client.get_secret_value(
            SecretId=secret_id
        )
        if isinstance(data, str):
            data = loads(data)
        return data['SecretString']
    except ClientError as e:
        raise SecretManagerException(str(e))
    except Exception as e:
        raise e


def get_script_content(bucket: str, file_name: str):
    """
        Retrieves the script stored in an s3 bucket (AWS)

        :param bucket: Bucket name from which the script will be retrieved
        :type bucket: string

        :type file_name: string
        :param file_name: file name with extension
            You must first make sure that you have the permissions on the resource to invoke
                :py:meth:`file_name.sql`.

        :raises
                BucketReadFileException: If bucket is None ad file is None or query is None.
                Exception: normal exception

        :return: Script file content
    """
    try:
        bucket = sub(r".*:(.*?)", '', bucket, 0, MULTILINE)
        data = s3_client.get_object(Bucket=bucket, Key=file_name)
        return data['Body'].read().decode('utf-8')
    except ClientError as e:
        raise BucketReadFileException(str(e))
    except Exception as e:
        raise e
