
import paramiko
import pickle
import os
def send_files(from_file_path,to_file_path):
    current_directory = os.getcwd()
    with open(f"{current_directory}/.plog","rb") as f:
        meta_data = pickle.load(f)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(meta_data['ip_address'],22,username=meta_data['username'],password=meta_data['password'],timeout=4)
    sftp = s.open_sftp()
    #sftp.put(file_path, '/root/blog/test.html')
    sftp.put(from_file_path, to_file_path)

