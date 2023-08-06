import boto3
import os
import datetime
import pandas as pd

def get_date_from_filename(filename):
    base_name = os.path.basename(filename)
    if base_name != "":
        split_name = base_name.split("_")
        year = int(split_name[0])
        month = int(split_name[1])
        day = int(split_name[2])
        hour = int(split_name[3])
        minute = int(split_name[4])
        time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    else:
        time = datetime.datetime(1950, 1, 1)
    return time

def get_latest_files(bucket_path, prefix):
    s3 = boto3.client('s3')

    objs = s3.list_objects_v2(Bucket=bucket_path, Prefix=prefix)['Contents']
    files = [obj['Key'] for obj in objs]
    files = sorted(files, key=get_date_from_filename, reverse=True)
    return files

def read_from_s3(s3url,curr_filename):
    output_file = s3url.format(curr_filename)
    df = pd.read_csv(output_file)
    return df