import paramiko
import os
from postbook.send_files import send_files
def write_conf():
    nginx_conf_string = """
    events {}
    http{
    gzip on;
gzip_disable "msie6";
gzip_vary on;
gzip_proxied any;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
        server {
        location / {
            root /root/blog ;

        }

    }
    }
    """

    with open("nginx.conf","w") as f:
        f.write(nginx_conf_string)
    cwd = os.getcwd()
    send_files('nginx.conf','/etc/nginx/nginx.conf')
def host_setup(ip_address,username,password):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip_address,22,username=username,password=password)
    get_pwd_command = 'pwd'
    nginx_install_command = 'apt update && apt --assume-yes install nginx'
    print("Getting the working directory...")
    (stdin, stdout, stderr) = s.exec_command(get_pwd_command)
    for working_dir in stdout.readlines():
        print (working_dir)
    print("Installing nginx on host....")
    (stdin, stdout, stderr) = s.exec_command(nginx_install_command)
    for line in stdout.readlines():
        print (line)
    print("Setting up permissions...")
    print(working_dir)
    permission_command = f'mkdir blog && chmod +x {working_dir} chmod +x blog'
    (stdin, stdout, stderr) = s.exec_command(permission_command)
    for line in stdout.readlines():
        print (line)
    write_conf()
    nginx_command = 'nginx -s reload'
    (stdin, stdout, stderr) = s.exec_command(nginx_command)
    for line in stdout.readlines():
        print (line)
    
    s.close()