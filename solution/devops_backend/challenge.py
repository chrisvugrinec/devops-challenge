import boto3
import json
from boto3.session import Session
from boto.s3.connection import S3Connection
import dateutil.parser
import os
import sys
import decimal
from enum import Enum

# enumaration used of filesize calculation
class FileSize(Enum):
   B = 1
   KB = 1024
   MB = 1024*1024
   GB = 1024*1024*1024

# init of app
ACCESS_KEY=os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
conn = S3Connection(ACCESS_KEY,SECRET_KEY)
s3 = session.resource('s3')
s3_client = boto3.client('s3')
filter = ''
size = 'KB'
selectedFileSize = FileSize.KB
get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))


# calc FileSize in desired Size
def getFileSize(sizeInBytes, FileSizeParam):
   return round(decimal.Decimal(sizeInBytes * (1./FileSizeParam.value)),3)


# create the BucketModel
def createBucketModel( bucket ):
   tmp_model = {}
   bucket_cdate = dateutil.parser.parse(bucket.creation_date)
   tmp_model["bucket_name"] = bucket.name
   tmp_model["bucket_creation_date"] = bucket_cdate.strftime('%Y-%m-%d %I:%S')

   nrOfFiles = 0
   totalBytes = 0
   unsorted_files = []

   # Get All the files; Bucket is always in 1 region
   response = s3_client.list_objects( Bucket = bucket.name, Prefix = filter )
   location = response['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']
   try:
      fileEntries = []
      for file in response['Contents']:
         nrOfFiles += 1
         unsorted_files.append(file)
         fileEntry = {}
         fileEntry["storage_class"] = file['StorageClass']
         fileEntry["filename"] = file['Key']
         fileEntries.append(fileEntry)
         totalBytes += file['Size']

      tmp_model["files"] = fileEntries

      # Determine last file
      last_added_file = [obj['Key'] for obj in sorted(unsorted_files, key=get_last_modified)][0]
      last_added_date = [obj['LastModified'] for obj in sorted(unsorted_files, key=get_last_modified)][0]
      # Print File summary
      tmp_model["location"] = location
      tmp_model["nr_of_files"] = str(nrOfFiles)
      tmp_model["total_size_of_files"] = str(getFileSize(totalBytes,selectedFileSize))+size
      tmp_model["last_added_file"] = last_added_file
      tmp_model["last_added_file_date"] = last_added_date.strftime('%Y-%m-%d %I:%S')

      return tmp_model

   # Occurs when no required Keys are found in the response
   except KeyError as error:
      print('Filter: '+filter+' does not contain files '+str(error))



# model wrapper; generates json data
def getJsonFromModel(FileSizeParam):
   selectedFileSize = FileSizeParam
   result_model = {}
   all_models = []
   all_buckets = conn.get_all_buckets()
   for bucket in all_buckets:
      model = createBucketModel(bucket)
      if model is not None:
         all_models.append(model)

   # DataDict that contains it all
   result_model["buckets"] = all_models

   # Display the complete model
   json_data_str = json.dumps(result_model, indent=3)
   json_data = json.loads(json_data_str)
   return json_data


# iterate over all buckets and create SuperModel
def showBucketInfo(FileSizeParam):
   json_data_str = getJsonFromModel(FileSizeParam)
   print(json_data_str)

# this is called by the rest wrapper
def getBucketInfo():
   return getJsonFromModel(FileSize.MB)

# Main Wrappers
def main():
    if(size == 'KB'):
       showBucketInfo(FileSize.KB)
    elif(size == 'MB'):
       showBucketInfo(FileSize.MB)
    elif(size == 'GB'):
       showBucketInfo(FileSize.GB)
    else:
       showBucketInfo(FileSize.B)

if __name__ == '__main__':
   try:
      size = sys.argv[1]
      filter = sys.argv[2]
      main()
   except IndexError:
      print('please provide one of the following params: B KB MB or GB')
   except:
      raise

