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

In [15]: r1.send_show_command('sh clock')
У меня тут командочка
Out[15]: '*12:27:27.279 UTC Sun Jan 21 2018'
```

+++
### Варианты вызова родительского метода

```python
class CiscoRouter(CiscoSSH):
    def say_hello(self):
        print("Hello from {}".format(self.ssh.ip))

    def send_show_command(self, command):
        print('У меня тут командочка')
        command_result = super().send_show_command(command)
        #command_result = super(CiscoRouter, self).send_show_command(command)
        #command_result = CiscoSSH.send_show_command(self, command)
        return command_result
```

+++
### `__init__` в дочернем классе

```python
class CiscoRouter(CiscoSSH):
    def __init__(self, hostname, **device_params):
        self.hostname = hostname
        super().__init__(**device_params)

    def say_hello(self):
        print("Hello from {}".format(self.ssh.ip))

    def send_show_command(self, command):
        print('У меня тут командочка')
        command_result = super().send_show_command(command)
        return command_result

In [18]: r1 = CiscoRouter('r1', **DEVICE_PARAMS)

In [19]: r1.send_show_command('sh clock')
У меня тут командочка
Out[19]: '*12:31:13.603 UTC Sun Jan 21 2018'

In [20]: r1.hostname
Out[20]: 'r1'
```


