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
    'version': '0.1.0',
    'description': 'python实现ssh操作',
    'long_description': "# zdpapi_shh\npython实现ssh操作，基于paramiko二次封装\n\n安装方式：\n```shell\npip install zdpapi_ssh\n```\n\n## 一、快速入门\n\n### 1.1 建立连接\nparamiko方式\n```python\nimport paramiko\n\n# 建立一个sshclient对象\nssh = paramiko.SSHClient()\n\n# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面\nssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())\n\n# 调用connect方法连接服务器\nssh.connect(hostname='192.168.18.11', port=22,\n            username='zhangdapeng', password='zhangdapeng')\n\n# 执行命令\nstdin, stdout, stderr = ssh.exec_command('df -hl')\n\n# 结果放到stdout中，如果有错误将放到stderr中\nprint(stdout.read().decode())\n\n# 关闭连接\nssh.close()\n```\n\nzdpapi_shh方式\n```python\n\n```\n",
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
