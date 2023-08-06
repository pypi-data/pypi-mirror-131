import os
import time
import uuid
import platform
import socket

import magic_import

class ServiceBase(object):

    def __init__(self, config=None, namespace=None):
        self.config = config or {}
        if namespace:
            self.namespace = namespace

    def get_config(self, path, default=None):
        return magic_import.select(self.config, path, default)

    def get_ignroe_methods(self):
        return [
            "get_config",
            "get_ignroe_methods",
            "register_to",
            "get_server_service",
            "get_namespace",
            "get_methods",
        ]

    def register_to(self, server):
        if hasattr(self, "_server"):
            raise Exception("service is already registered...")
        for name, method in self.get_methods():
            server.register_function(method, name)
        if not hasattr(server, "_services"):
            setattr(server, "_services", {})
        services = getattr(server, "_services")
        services[self.get_namespace()] = self
        self._server = server
    
    def get_server_service(self, name):
        if not self._server:
            raise Exception("service is not register to any server...")
        if not hasattr(self._server, "_services"):
            setattr(self._server, "_services", {})
        return self._server._services.get(name, None)

    def get_namespace(self):
        namespace = getattr(self, "namespace", None)
        if not namespace:
            namespace = str(self.__class__.__name__).lower()
            if namespace.endswith("service"):
                namespace = namespace[:-7]
        return namespace

    def get_methods(self):
        methods = []
        base_names = dir(ServiceBase)
        for name in dir(self):
            if name in base_names:
                continue
            method = getattr(self, name)
            if not name.startswith("_") and callable(method):
                name = self.get_namespace() + "." + name
                methods.append((name, method))
        return methods


class DebugService(ServiceBase):

    namespace = "debug"

    def __init__(self, *args, **kwargs):
        self._counter = 0

    def ping(self):
        self._counter += 1
        return "pong"
    
    def echo(self, msg):
        self._counter += 1
        return msg
    
    def timestamp(self):
        self._counter += 1
        return time.time()
    
    def hostname(self):
        self._counter += 1
        return socket.gethostname()

    def uuid4(self):
        self._counter += 1
        return str(uuid.uuid4())

    def urandom(self, length=32):
        self._counter += 1
        return os.urandom(length)

    def uname(self):
        self._counter += 1
        info = platform.uname()
        uname = {}
        for name in dir(info):
            if name.startswith("_"):
                continue
            value = getattr(info, name)
            if callable(value):
                continue
            uname[name] = value
        return uname

    def true(self):
        self._counter += 1
        return True
    
    def false(self):
        self._counter += 1
        return False

    def null(self):
        self._counter += 1
        return None
    
    def sum(self, *args):
        self._counter += 1
        return sum(args)

    def counter(self):
        self._counter += 1
        return self._counter

    def sleep(self, seconds=30):
        time.sleep(seconds)
        return True

