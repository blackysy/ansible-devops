#!/usr/bin/python
# _*_coding:utf-8_*_
# @Time     : 2019/5/29 上午9:36
# @Author   : blackysy
# @File     : RemoteExec.py
# @Software : PyCharm

import sys
import paramiko


def ssh_connect():
    hostname = '172.28.250.2'
    username = 'jenkins'
    password = '123931'
    try:
        ssh_fd = paramiko.SSHClient()
        ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_fd.connect(hostname, username=username, password=password)
        return ssh_fd
    except Exception as e:
        print('ssh %s@%s: %s' % (username, hostname, e))
        exit()


def ssh_exec_cmd(ssh_fd, cmd):
    return ssh_fd.exec_command(cmd)


def ssh_close(ssh_fd):
    ssh_fd.close()


def app_start(ip, user, app_type):
    if app_type == 'jdk':
        cmd = "ansible %s -u %s -m shell -a 'source ~/.bash_profile && cd $BIN_HOME && sh start.sh'" \
              % (ip, user)
    elif app_type == 'tomcat':
        cmd = "ansible %s -u %s -m shell -a 'source ~/.bash_profile && cd $BIN_HOME/.. && nohup ./bin/startup.sh'" \
              % (ip, user)
    else:
        sys.exit(0)

    sshd = ssh_connect()
    stdin, stdout, stderr = ssh_exec_cmd(sshd, cmd)
    err_list = stderr.readlines()

    if len(err_list) > 0:
        print('Start failed:' + err_list[0])
        sys.exit(0)
    else:
        print('Start success.')

    # for item in stdout.readlines():
    #    print item

    ssh_close(sshd)


def app_stop(ip, user):
    cmd = """ansible %s -u %s -m shell -a 'ps x|grep java|grep -v grep|cut -d " " -f 1|xargs kill -9'""" \
          % (ip, user)
    sshd = ssh_connect()
    stdin, stdout, stderr = ssh_exec_cmd(sshd, cmd)
    err_list = stderr.readlines()

    if len(err_list) > 0:
        print('Stop failed: ' + err_list[0])
        sys.exit(0)
    else:
        print('Stop success.')

    # for item in stdout.readlines():
    #    print item

    ssh_close(sshd)


app_start(ip='172.28.250.103', user='smp_client_str', app_type='tomcat')
#app_stop(ip='172.28.250.103', user='smp_client_str')