#!/usr/bin/env python2

import os
import uuid
import subprocess

bucket = os.getenv('S3_BUCKET')
access_key = os.getenv('S3_ACCESS_KEY')
secret_key = os.getenv('S3_SECRET_KEY')
region = "eu-west-1"

cmd = ("psql",
        "-c", "select __filename__, __uuid__ from system$filedocument where hascontents or submetaobjectname = 'System.Thumbnail'",
        "-t", "-A")
proc1 = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = proc1.communicate()

if stderr != '':
    print("Error occurred while calling psql, but it is ok: %s" % stderr)

lines = stdout.split('\n')
files = []
for line in lines:
    tokens = line.split('|')
    if len(tokens) != 2:
        print("# Skipped: %s " % line)
        continue
    file_name = tokens[0]
    file_uuid = tokens[1]
    files.append((file_name, file_uuid))


def get_local_file_path(file_name, file_uuid):
    old_format = get_local_file_path_for_filename(file_name)
    if old_format:
        return old_format
    return get_local_file_path_for_uuid(file_uuid, prefix='./files')


def get_local_file_path_for_uuid(file_uuid, index=0, prefix=''):
    filename = file_uuid.strip()
    index_plus_2 = index + 2
    if index + 1 >= len(file_uuid):
        return None
    folder = filename[index:index_plus_2]
    file_path = os.path.join(prefix, folder, file_uuid)
    if os.path.isfile(file_path):
        return file_path
    else:
        return get_local_file_path_for_uuid(file_uuid, index=index_plus_2, prefix=os.path.join(prefix, folder))


def get_local_file_path_for_filename(filename):
    filename = int(filename.strip())
    folder = filename / 1000
    x = str(filename)
    folder = "%02d" % (folder,)
    file_path = os.path.join('./files', folder, x)
    if os.path.isfile(file_path):
        return file_path
    else:
        return None

for file_name, file_uuid in files:
    file_path = get_local_file_path(file_name, file_uuid)
    if file_path and os.path.isfile(file_path):
        new_file = str(uuid.uuid4())
        print 's3cmd', '--region=' + region, '--access_key=' + access_key, '--secret_key=' + secret_key, 'put', file_path, 's3://' + bucket + '/' + new_file
        print 'psql -c "update system\$filedocument set __uuid__ = \'%s\' where __filename__ = \'%s\'";' % (new_file, file_name)
    else:
        print '#error: File not found: %s (%s)' % (file_name, file_path)