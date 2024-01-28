# -*- coding: utf-8 -*-
import sys
from parser import Parser
from minio import Minio
from datetime import datetime

file = "rss.xml"
minio_host="play.min.io:9443"
minio_connection_secure=True
minio_access_key="Q3AM3UQ867SPQQA43P2F"
minio_secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
minio_bucket = "test"
minio_dest_file = "tldr/rss.xml"
 
parser = Parser(datetime.now().strftime("%Y-%m-%d"))
print("Downloading page ...")
error = parser.getPage()
if error != None:
    print("Download failed: " + error)
    sys.exit(1)
print("Parsing page ...")
error = parser.parseArticles()
if error != None:
    print("Parse failed: " + error)
    sys.exit(1)
print("Generating feed ...")
parser.generateFeed(file)
if error != None:
    print("Generate failed: " + error)
    sys.exit(1)

# upload to minio
print("Uploading feed ...")
client = Minio(minio_host,access_key=minio_access_key,secret_key=minio_secret_key, secure=minio_connection_secure)

# check that bucket exists
found = client.bucket_exists(minio_bucket)
if not found:
    print("Upload failed! Target bucket does not exists.")
    sys.exit(1)

# Upload the file, renaming it in the process
client.fput_object(minio_bucket, minio_dest_file, file)
print("Done")