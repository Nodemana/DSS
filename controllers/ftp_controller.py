from ftplib import FTP
import os
import sys
import datetime as dt
import threading

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the 'models' directory to the system path
models_dir = os.path.join(current_dir, '..', 'models')
sys.path.append(models_dir)

# Import the ftp_model module
from ftp_model import *

def convert_time(unix_timestamp):
    # Convert the Unix timestamp to a datetime object
    unix_timestamp = dt.datetime.fromtimestamp(unix_timestamp)

    gmt_time = unix_timestamp - dt.timedelta(hours = 10)
    gmt_time = gmt_time.strftime('%Y%m%d%H%M%S.%f')[:-3]
    return float(gmt_time)

def cmp_files(local, remote):
    if remote[0] != local:
        #print("Name Discrepancy")
        return False
    else:
        local_timestamp = convert_time(os.path.getmtime("files/" + local))
        #print(local_timestamp)
        remote_timestamp = remote[2]
        #print(remote_timestamp)
        if float(remote_timestamp) > float(local_timestamp):
            #print("Timestamp Discrepancy")
            return False
        else:
            local_size = os.path.getsize("files/" + local)
            if int(local_size) != int(remote[-1]):
                #print("Filesize Discrepancy")
                return False
            else:
                #print("File Accounted For")
                return True

def cmp_dir():
    flag = False
    remote_files = grab_files()
    local_files = os.listdir("files/")
    for file in remote_files:
        for lfile in local_files:
            flag = cmp_files(lfile, file)
            if flag:
                break
        if not flag:
            pull_files(file[0], file[2])
            print("Downloading File " + file[0])
    print("Directories Compared")

def sync():
    print("Syncing...")
    cmp_dir()
    timer = threading.Timer(300, lambda: sync())
    timer.start()

