# Python для сетевых инженеров 

---
## Welcome to продленка :)

---

## Объектно-ориентированное программирование

---
## Наследование


+++
### Наследование

Базовый пример наследования:
```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

class CiscoRouter(CiscoSSH):
    pass

In [7]: r1 = CiscoRouter(**DEVICE_PARAMS)

In [8]: r1.send_show_command('sh clock')
Out[8]: '*12:20:52.788 UTC Sun Jan 21 2018'
```


+++
### Добавление метода в дочернем классе

```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

class CiscoRouter(CiscoSSH):
    def say_hello(self):
        print("Hello from {}".format(self.ssh.ip))

In [10]: r1 = CiscoRouter(**DEVICE_PARAMS)

In [11]: r1.say_hello()
Hello from 192.168.100.1
```

+++
### Переопределение родительского метода

```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

class CiscoRouter(CiscoSSH):
    def say_hello(self):
        print("Hello from {}".format(self.ssh.ip))

    def send_show_command(self, command):
        print('У меня тут командочка')
        command_result = CiscoSSH.send_show_command(self, command)
        return command_result

In [13]: r1 = CiscoRouter(**DEVICE_PARAMS)

In [14]: r1.send_show_command('sh ip int  br')
У меня тут командочка
Out[14]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '
```


