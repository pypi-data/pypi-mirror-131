import paramiko


class SSH:
    def __init__(self, hostname: str = '192.168.18.11', port: int = 22,
                 username: str = 'zhangdapeng', password: str = 'zhangdapeng') -> None:

        # 建立一个sshclient对象
        self.ssh = paramiko.SSHClient()
        self.ssh_trans = paramiko.SSHClient()

        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

        # 调用connect方法连接服务器
        self.connect()

        # trans字典
        self.trans = {
            hostname: {  # 键是该服务器的ip地址
                "hostname": hostname,  # 主机地址
                "port": port,  # 端口号
                "username": username,  # 用户名
                "password": password  # 密码
            }
        }

    def add_trans(self, hostname:str, port:int, username: str, password: str):
        """
        添加trans服务，用于在多个ssh之间切换
        """
        self.trans[hostname] = {  # 键是该服务器的ip地址
            "hostname": hostname,  # 主机地址
            "port": port,  # 端口号
            "username": username,  # 用户名
            "password": password  # 密码
        }
    
    def __set_trans(self, hostname:str):
        """
        设置要连接的trans，用以切换不同的ssh
        """
        trans_dict = self.trans.get(hostname)
        if trans_dict is None:
            raise Exception("不存在该主机的trans配置")
        
        # 使用trans连接
        self.trans_server = paramiko.Transport((trans_dict.get("hostname"), trans_dict.get("port")))
        self.trans_server.connect(username=trans_dict.get("username"), password=trans_dict.get("password"))
        self.ssh_trans._transport = self.trans_server
    
    def execute_trans(self, hostname:str,  command:str):
        """
        使用trans的方式执行ssh命令
        """
        self.__set_trans(hostname)

        # 执行命令，和传统方法一样
        stdin, stdout, stderr = self.ssh_trans.exec_command(command)
        print(stdout.read().decode())
        
        # 关闭连接
        self.ssh_trans.close()
        

    def connect(self):
        """
        建立连接
        """
        self.ssh.connect(hostname=self.hostname, port=self.port,
                         username=self.username, password=self.password)

    def execute(self, command: str):
        """
        执行命令
        """
        self.connect()

        # 执行命令
        stdin, stdout, stderr = self.ssh.exec_command(command)

        # 结果放到stdout中，如果有错误将放到stderr中
        print(stdout.read().decode())

        # 关闭连接
        self.close()

    def close(self):
        """
        关闭连接
        """
        self.ssh.close()
