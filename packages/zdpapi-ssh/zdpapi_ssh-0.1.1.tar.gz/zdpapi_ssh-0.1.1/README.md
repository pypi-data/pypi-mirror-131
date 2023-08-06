# zdpapi_shh
python实现ssh操作，基于paramiko二次封装

安装方式：
```shell
pip install zdpapi_ssh
```

## 一、快速入门

### 1.1 建立连接
paramiko方式
```python
import paramiko

# 建立一个sshclient对象
ssh = paramiko.SSHClient()

# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 调用connect方法连接服务器
ssh.connect(hostname='192.168.18.11', port=22,
            username='zhangdapeng', password='zhangdapeng')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df -hl')

# 结果放到stdout中，如果有错误将放到stderr中
print(stdout.read().decode())

# 关闭连接
ssh.close()
```

zdpapi_shh方式
```python
from zdpapi_ssh import SSH

ssh = SSH(hostname='192.168.18.11', port=22,
          username='zhangdapeng', password='zhangdapeng')
ssh.execute('df -hl')
```

### 1.2 建立多个ssh连接
paramiko的方式
```python
import paramiko

# 实例化一个transport对象
trans = paramiko.Transport(('192.168.18.11', 22))

# 建立连接
trans.connect(username='zhangdapeng', password='zhangdapeng')

# 将sshclient的对象的transport指定为以上的trans
ssh = paramiko.SSHClient()
ssh._transport = trans

# 执行命令，和传统方法一样
stdin, stdout, stderr = ssh.exec_command('df -hl')
print(stdout.read().decode())

# 关闭连接
trans.close()
```

zdpapi_ssh的方式
```python
from zdpapi_ssh import SSH

ssh = SSH(hostname='192.168.18.11', port=22,
          username='zhangdapeng', password='zhangdapeng')
ssh.execute_trans('192.168.18.11', 'df -hl')
```
