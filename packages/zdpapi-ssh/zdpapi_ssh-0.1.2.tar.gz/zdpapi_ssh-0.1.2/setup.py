# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdpapi_ssh']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'zdpapi-ssh',
    'version': '0.1.2',
    'description': 'python实现ssh操作',
    'long_description': "# zdpapi_shh\npython实现ssh操作，基于paramiko二次封装\n\n安装方式：\n```shell\npip install zdpapi_ssh\n```\n\n## 一、快速入门\n\n### 1.1 建立连接\nparamiko方式\n```python\nimport paramiko\n\n# 建立一个sshclient对象\nssh = paramiko.SSHClient()\n\n# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面\nssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())\n\n# 调用connect方法连接服务器\nssh.connect(hostname='192.168.18.11', port=22,\n            username='zhangdapeng', password='zhangdapeng')\n\n# 执行命令\nstdin, stdout, stderr = ssh.exec_command('df -hl')\n\n# 结果放到stdout中，如果有错误将放到stderr中\nprint(stdout.read().decode())\n\n# 关闭连接\nssh.close()\n```\n\nzdpapi_shh方式\n```python\nfrom zdpapi_ssh import SSH\n\nssh = SSH(hostname='192.168.18.11', port=22,\n          username='zhangdapeng', password='zhangdapeng')\nssh.execute('df -hl')\n```\n\n### 1.2 建立多个ssh连接\n方法1是传统的连接服务器、执行命令、关闭的一个操作，有时候需要登录上服务器执行多个操作，比如执行命令、上传/下载文件，方法1则无法实现，可以通过如下方式来操作\n\nparamiko的方式\n```python\nimport paramiko\n\n# 实例化一个transport对象\ntrans = paramiko.Transport(('192.168.18.11', 22))\n\n# 建立连接\ntrans.connect(username='zhangdapeng', password='zhangdapeng')\n\n# 将sshclient的对象的transport指定为以上的trans\nssh = paramiko.SSHClient()\nssh._transport = trans\n\n# 执行命令，和传统方法一样\nstdin, stdout, stderr = ssh.exec_command('df -hl')\nprint(stdout.read().decode())\n\n# 关闭连接\ntrans.close()\n```\n\nzdpapi_ssh的方式\n```python\nfrom zdpapi_ssh import SSH\n\nssh = SSH(hostname='192.168.18.11', port=22,\n          username='zhangdapeng', password='zhangdapeng')\nssh.execute_trans('192.168.18.11', 'df -hl')\n```\n\n## 二、FTP操作\n\n### 2.1 上传和下载\nparamiko实现\n```python\nimport paramiko\n\n# 实例化一个trans对象# 实例化一个transport对象\ntrans = paramiko.Transport(('192.168.18.11', 22))\n\n# 建立连接\ntrans.connect(username='zhangdapeng', password='zhangdapeng')\n\n# 实例化一个 sftp对象,指定连接的通道\nsftp = paramiko.SFTPClient.from_transport(trans)\n\n# 发送文件\nsftp.put(localpath='README.md', remotepath='/home/zhangdapeng/README.md')\n\n# 下载文件\n# sftp.get(remotepath, localpath)\ntrans.close()\n```\n\nzdpapi_ssh实现\n```python\nfrom zdpapi_ssh import SSH\n\nssh = SSH(hostname='192.168.18.11', port=22,\n          username='zhangdapeng', password='zhangdapeng')\n\n# 上传\nssh.ftp_upload('192.168.18.11', 'README.md', '/home/zhangdapeng/README1.md')\n\n# 下载\nssh.ftp_download('192.168.18.11', 'README1.md', '/home/zhangdapeng/README1.md')\n```\n",
    'author': '张大鹏',
    'author_email': 'lxgzhw@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhangdapeng520/zdpapi_ssh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
