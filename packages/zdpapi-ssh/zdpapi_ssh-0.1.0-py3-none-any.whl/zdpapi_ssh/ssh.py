import paramiko

class SSH:
    def __init__(self, hostname:str='192.168.18.11', port:int=22,
                 username:str='zhangdapeng', password:str='zhangdapeng') -> None:

        # 建立一个sshclient对象
        self.ssh = paramiko.SSHClient()
        

        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        
        # 调用connect方法连接服务器
        self.connect()
    
    def connect(self):
        """
        建立连接
        """
        self.ssh.connect(hostname=self.hostname, port=self.port,
                         username=self.username, password=self.password)

    def execute(self, command:str):
        """
        执行命令
        """
        self.connect()

        # 执行命令
        stdin, stdout, stderr = self.ssh.exec_command('df -hl')
        
        # 结果放到stdout中，如果有错误将放到stderr中
        print(stdout.read().decode())
        
        # 关闭连接
        self.close()
    
    def close(self):
        """
        关闭连接
        """
        self.ssh.close()
