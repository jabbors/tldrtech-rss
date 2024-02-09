# -*- coding: utf-8 -*-
import argparse
import os
import sys
from parser import Parser
from minio import Minio
from datetime import datetime
from distutils.util import strtobool

file = "rss.xml"
minio_host = os.getenv("MINIO_HOST","play.min.io:443")
minio_connection_secure = strtobool(os.getenv("MINIO_CONNECTION_SECURE", "True"))
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "Q3AM3UQ867SPQQA43P2F")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG")
minio_bucket = os.getenv("MINIO_BUCKET", "test")
minio_dest_file = os.getenv("MINIO_DEST_FILE", "tldr/rss.xml")

def print_help():
    print(
'''
This application is configured via the environment. The following environment
variables can be used:
KEY                     TYPE    DEFAULT                                     REQUIRED    DESCRIPTION
MINIO_HOST              String  play.min.io:443                                         host to connect to
MINIO_CONNECTION_SECURE Boolean True                                                    connect using SSL
MINIO_ACCESS_KEY        String  Q3AM3UQ867SPQQA43P2F                                    access key used when connecting
MINIO_SECRET_KEY        String  zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG                secret key used when connecting
MINIO_BUCKET            String  test                                                    bucket to put file in
MINIO_DEST_FILE         String  tldr/rss.xml                                            destination of the file
'''
    )
    sys.exit(0)

try:
    argparser = argparse.ArgumentParser()
    options = argparser.parse_args()
except:
    print_help()
    sys.exit(0)

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