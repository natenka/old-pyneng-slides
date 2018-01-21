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


---
### Пример наследования класса CiscoIosBase из netmiko

---
### Определение нужного класса

+++
### Определение нужного класса

В netmiko используется динамический выбор нужного класса, в зависимости от значения, которое указано в device_type.
Мы не можем наследовать ConnectHandler, так как это функция:
```python
In [1]: import netmiko

In [2]: type(netmiko.ConnectHandler)
Out[2]: function
```

+++
### Определение нужного класса

Если создать объект с помощью функции ConnectHandler, мы получим экземпляр класса, по которому можно определить класс и его родительские классы:
```python
DEVICE_PARAMS = {
        'device_type': 'cisco_ios',
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}

In [3]: r1 = netmiko.ConnectHandler(**DEVICE_PARAMS)

In [4]: type(r1)
Out[4]: netmiko.cisco.cisco_ios.CiscoIosBase

In [5]: netmiko.cisco.cisco_ios.CiscoIosBase.mro()
Out[5]:
[netmiko.cisco.cisco_ios.CiscoIosBase,
 netmiko.cisco_base_connection.CiscoBaseConnection,
 netmiko.base_connection.BaseConnection,
 object]
```

+++
### mro - Method Resolution Order

```python
In [12]: type([1,2,3])
Out[12]: list

In [13]: type([1,2,3]).mro()
Out[13]: [list, object]

In [18]: from netmiko import ConnectHandler

In [19]: r1 = ConnectHandler(**DEVICE_PARAMS)

In [20]: type(r1)
Out[20]: netmiko.cisco.cisco_ios.CiscoIosBase

In [21]: type(r1).mro()
Out[21]:
[netmiko.cisco.cisco_ios.CiscoIosBase,
 netmiko.cisco_base_connection.CiscoBaseConnection,
 netmiko.base_connection.BaseConnection,
 object]
```

---
### Пример наследования

+++
### Базовый пример наследования

```python
device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

from netmiko.cisco.cisco_ios import CiscoIosBase

class MyNetmiko(CiscoIosBase):
    pass

In [4]: r1 = MyNetmiko(**device_params)

In [5]: r1.send_command('sh clock')
Out[5]: '*12:59:08.659 UTC Sun Jan 21 2018'
```

+++
### Добавление метода

```python
class MyNetmiko(CiscoIosBase):
    def say_hello(self):
        print('Hello from', self.ip)

In [7]: r1 = MyNetmiko(**device_params)

In [8]: r1.send_command('sh clock')
Out[8]: '*13:00:25.782 UTC Sun Jan 21 2018'

In [9]: r1.say_hello()
Hello from 192.168.100.1
```

+++
### Переопределение родительского метода

```python
class MyNetmiko(CiscoIosBase):
    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        print('Вывод команды:')
        return command_output

    def say_hello(self):
        print('Hello from', self.ip)

In [11]: r1 = MyNetmiko(**device_params)

In [12]: r1.send_command('sh clock')
Вывод команды:
Out[12]: '*13:03:46.341 UTC Sun Jan 21 2018'

```


+++
### Добавление дополнительного функционала

```python
class ErrorInCommand(Exception):
    pass

class MyNetmiko(CiscoIosBase):
    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        if 'Invalid input' in command_output:
            raise ErrorInCommand('Ошибка в команде {}'.format(command))
        return command_output

In [14]: r1 = MyNetmiko(**device_params)

In [15]: r1.send_command('sh clck')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-15-8d71a272499a> in <module>()
----> 1 r1.send_command('sh clck')

<ipython-input-13-8c1a511ae6bf> in send_command(self, command, *args, **kwargs)
      6         command_output = super().send_command(command, *args, **kwargs)
      7         if 'Invalid input' in command_output:
----> 8             raise ErrorInCommand('Ошибка в команде {}'.format(command))
      9         return command_output
     10

ErrorInCommand: Ошибка в команде sh clck
```



