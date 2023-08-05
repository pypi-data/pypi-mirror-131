from boto3 import client
from pandas import read_csv, DataFrame, concat
from sagemaker import get_execution_role
from tqdm import tqdm
from typing import List

get_execution_role()


def _fix_folder(folder: str) -> str:
    """
    Fix a '/'-separated folder path so there are no '/'s at the start or end.
    """
    folder_path = folder.split('/')
    folder = '/'.join([f for f in folder_path if f != ''])
    return folder


def list_bucket(bucket: str, folder: str = '') -> List[str]:
    """
    Return a list of the contents of an s3 bucket.

    :param bucket: Name of the S3 bucket.
    :param folder: Name of optional sub-folder in the bucket.
                   Can provide deep sub-folder
                   e.g. 'temp/tmp1/customer_segments'
    """
    connection = client('s3')
    folder = _fix_folder(folder)
    contents = connection.list_objects(Bucket=bucket, Prefix=folder)['Contents']
    return [f['Key'] for f in contents]


def s3_bucket_path(bucket: str) -> str:
    """
    Return the path to the s3 bucket.

    :param bucket: Name of the S3 bucket.
    """
    return f's3://{bucket}/'


def s3_folder_path(bucket: str, folder: str) -> str:
    """
    Return the path to the folder in S3.

    :param bucket: Name of the S3 bucket.
    :param folder: Name of optional sub-folder in the bucket.
                   Can provide deep sub-folder
                   e.g. 'temp/tmp1/customer_segments'
    """
    folder_path = s3_bucket_path(bucket)
    if folder != '':
        folder_path += _fix_folder(folder) + '/'
    return folder_path


def s3_file_path(file_name: str, bucket: str, folder: str = '') -> str:
    """
    Return the path to the file in S3.

    :param file_name: Name of the file to check for.
    :param bucket: Name of the S3 bucket.
    :param folder: Name of optional sub-folder in the bucket.
                   Can provide deep sub-folder
                   e.g. 'temp/tmp1/customer_segments'.
    """
    return s3_folder_path(folder=folder, bucket=bucket) + file_name


def file_exists(bucket: str, file_name: str, folder: str = '') -> bool:
    """
    Check if a file exists in the given bucket (and folder).

    :param bucket: Name of the S3 bucket.
    :param file_name: Name of the file to check for.
        :param folder: Name of optional sub-folder in the bucket.
                   Can provide deep sub-folder
                   e.g. 'temp/tmp1/customer_segments'.
    """
    files = list_bucket(bucket=bucket, folder=folder)
    if f'{_fix_folder(folder)}/{file_name}' in files:
        return True
    else:
        return False


def read_s3_csv(bucket: str, file_name: str, folder: str = '',
                **read_csv_kwargs) -> DataFrame:
    """
    Read a csv file stored in S3 into a pandas DataFrame.

    :param file_name: Name of the csv file to read.
    :param folder: Name of optional sub-folder in the bucket.
    :param bucket: Name of the S3 bucket.
    :param read_csv_kwargs: KwArgs to pass to pandas read_csv.
    """
    file_path = s3_file_path(bucket=bucket, file_name=file_name, folder=folder)
    return read_csv(file_path, **read_csv_kwargs)


def get_s3_folder_size(bucket: str, folder: str = '', ) -> int:
    """
    Return the size of the contents of the given s3 bucket or sub-folder.

    :param bucket: Name of the S3 bucket.
    :param folder: Name of optional sub-folder in the bucket.
    """
    connection = client('s3')
    contents = connection.list_objects(Bucket=bucket)['Contents']
    total_size = 0
    for content in contents:
        total_size += content['Size']
    return total_size


def read_s3_csvs(bucket: str, folder: str = '', num_files: int = None,
                 **read_csv_kwargs) -> DataFrame:
    """
    Read all (or a fixed number) of csv files from an s3 bucket.

    :param bucket: Name of the S3 bucket.
    :param folder: Name of optional sub-folder in the bucket.
    :param num_files: Optional number of files to read. Leave as None to read all.
    :param read_csv_kwargs: KwArgs to pass to pandas read_csv.
    """
    file_names = list_bucket(folder=folder, bucket=bucket)
    if num_files is not None:
        file_names = file_names[: num_files]
    csvs = []
    for file_name in tqdm(file_names):
        csvs.append(read_s3_csv(file_name, **read_csv_kwargs))
    data = concat(csvs)
    return data
