import ftplib
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

def set_file_modification_time(filename, mtime):
    stat = os.stat(filename)
    atime = stat.st_atime
    os.utime(filename, times=(atime, mtime.timestamp()))

def ftp_connect():
    ftp = ftplib.FTP('10.9.8.100')
    ftp.login(os.getenv('FTPUSERNAME'), os.getenv('FTPPASSWORD'))
        #print("Connected and Authenticated")
    return ftp

def pull_files(filename, mtime):
    ftp = ftp_connect()
    with open("files/" + filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, lambda data: f.write(data))
    #set_file_modification_time(filename, mtime)
    ftp.quit()

def push_files(local_file_path, ftp_file_path):
    ftp = ftp_connect()
    with open("files/" + local_file_path, 'rb') as f:
        ftp.storbinary('STOR ' + ftp_file_path, f)
    ftp.quit()

def grab_files():
    ftp = ftp_connect()
    dir_list = []
    ftp.dir(dir_list.append)
    name_list = ftp.nlst()
    file_list = []
    # Iterate over the files and print their names and dates
    for line in dir_list:
        parts = line.split()
        name = name_list[dir_list.index(line)]
        date_cmp_str = ftp.voidcmd("MDTM " + name)
        date_disp_str = ' '.join(parts[5:8])
        file_size = parts[4]
        # Do something with the file name and date
        file_list.append([name,date_disp_str,date_cmp_str[4:],file_size])

    return file_list
