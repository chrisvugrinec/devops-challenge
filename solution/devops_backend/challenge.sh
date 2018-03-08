#!/bin/bash

# TODO: rewrite into json query results


# Iterate over all buckets
aws s3 ls | while read bucket
do
   # Bucket name, Creation date, Number of files, Total size of files, Last modified date
   bucketName=$(echo $bucket | awk '{ print $3 }')
   creationDate=$(echo $bucket | awk '{ print $1 $2 }')
   echo "-----------------------"
   echo "Bucket: "$bucketName
   echo "Creation Date: "$creationDate
   summary=$(aws s3 ls s3://$bucketName --recursive --summarize |grep Total | sed 's/[^0-9]*//')
   echo "Total Number of files: "${summary[@]:0:1}
   echo "Total Size of files: "${summary[@]:1}


   # Determine and display last modified file
   lastModifiedFileAndDate=$(aws s3 ls s3://$bucketName --recursive | sort -n | tail -1)
   lastModifiedDate=$(echo $lastModifiedFileAndDate | awk '{ print $1 $2 }')
   lastModifiedFile=$(echo $lastModifiedFileAndDate | awk '{ print $4 }')
   echo "last modified file: "$lastModifiedFile" modified on: "$lastModifiedDate
done
