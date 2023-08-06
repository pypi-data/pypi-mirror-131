# xmlrpcutils

xmlrpc服务器简化工具。

## 安装

```
pip install xmlrpcutils
```

## TestServer测试服务器

```
from xmlrpcutils.server import SimpleXmlRpcServer
from xmlrpcutils.service import ServiceBase

class SayHelloService(ServiceBase):

    def hello(self, name):
        return f"Hello {name}, how are you!"

class TestServer(SimpleXmlRpcServer):
    
    def register_services(self):
        super().register_services()
        SayHelloService(namespace="debug").register_to(self.server)

app =  TestServer()
app_ctrl = app.get_controller()

if __name__ == "__main__":
    app_ctrl()

```

## 启动测试服务器

```
python test_server.py
```

## 远程调用xmlrpc测试服务器

```
In [9]: from xmlrpc.client import ServerProxy

In [10]: server = ServerProxy('http://127.0.0.1:8381')

In [11]: server.system.listMethods()
Out[11]:
['debug.counter',
 'debug.echo',
 'debug.false',
 'debug.hello',
 'debug.hostname',
 'debug.null',
 'debug.ping',
 'debug.sleep',
 'debug.sum',
 'debug.timestamp',
 'debug.true',
 'debug.uname',
 'debug.urandom',
 'debug.uuid4',
 'system.listMethods',
 'system.methodHelp',
 'system.methodSignature',
 'system.multicall']

In [12]: server.debug.hello('zencore')
Out[12]: 'Hello zencore, how are you!'
```

## 版本

### v0.1.1 2021/12/15

- 初始版本。