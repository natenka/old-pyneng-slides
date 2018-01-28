# Python для сетевых инженеров 

---

## Объектно-ориентированное программирование. Часть 3

---
## Named Tuple

+++
### Named Tuple

Именованные кортежи присваивают имена каждому элементу кортежа и код выглядит более понятным, так как вместо индексов используются имена.
При этом, все возможности обычных кортежей остаются.

+++
### Named Tuple

Функция namedtuple позволяет создавать новые классы, которые наследуют tuple и при этом:

* доступ к атрибутам может осуществляться по имени
* доступ к элементами по индексу
* экземпляр класса является итерируемым объектом
* атрибуты неизменяемы


```python
In [1]: from collections import namedtuple

In [2]: RouterClass = namedtuple('Router', ['hostname', 'ip', 'ios'])

In [3]: r1 = RouterClass('r1', '10.1.1.1', '15.4')
```

+++
### Named Tuple

```python
In [2]: RouterClass = namedtuple('Router', ['hostname', 'ip', 'ios'])

In [3]: r1 = RouterClass('r1', '10.1.1.1', '15.4')

In [4]: r1
Out[4]: Router(hostname='r1', ip='10.1.1.1', ios='15.4')

In [5]: r1[0]
Out[5]: 'r1'

In [6]: r1[1]
Out[6]: '10.1.1.1'

In [7]: r1.ios
Out[7]: '15.4'

In [8]: r1.ip
Out[8]: '10.1.1.1'
```

+++
### ```_as_dict```

Метод ```_as_dict``` возвращает OrderedDict:
```python
In [9]: r1._asdict()
Out[9]: OrderedDict([('hostname', 'r1'), ('ip', '10.1.1.1'), ('ios', '15.4')])
```

+++
### ```_replace```

Метод ```_replace``` возвращает новый экземпляр класса, в котором заменены указанные поля:
```python
In [18]: r1 = RouterClass('r1', '10.1.1.1', '15.4')

In [19]: r1
Out[19]: Router(hostname='r1', ip='10.1.1.1', ios='15.4')

In [20]: r1._replace(ip='10.2.2.2')
Out[20]: Router(hostname='r1', ip='10.2.2.2', ios='15.4')
```

+++
### ```_make```

Метод ```_make``` создает новый экземпляр класса из последовательности полей (это метод класса):
```python
In [22]: RouterClass._make(['r3', '10.3.3.3', '15.2'])
Out[22]: Router(hostname='r3', ip='10.3.3.3', ios='15.2')

In [23]: r3 = RouterClass._make(['r3', '10.3.3.3', '15.2'])
```

+++
### ```_make```

```python
import sqlite3
from collections import namedtuple


key = 'vlan'
value = 10
db_filename = 'dhcp_snooping.db'

keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
DhcpSnoopRecord = namedtuple('DhcpSnoopRecord', keys)

conn = sqlite3.connect(db_filename)
query = 'select {} from dhcp where {} = ?'.format(','.join(keys), key)

print('-' * 40)
for row in map(DhcpSnoopRecord._make, conn.execute(query, (value,))):
    print(row.mac, row.ip, row.interface, sep='\n')
    print('-' * 40)

```

+++
### ```_make```

```
$ python get_data.py
----------------------------------------
00:09:BB:3D:D6:58
10.1.10.2
FastEthernet0/1
----------------------------------------
00:07:BC:3F:A6:50
10.1.10.6
FastEthernet0/3
----------------------------------------
```

+++
### ```_source```

Метод ```_source``` показывает код, который использовался для создания класса:
```python
from builtins import property as _property, tuple as _tuple
from operator import itemgetter as _itemgetter
from collections import OrderedDict

class Router(tuple):
    'Router(hostname, ip, ios)'

    __slots__ = ()

    _fields = ('hostname', 'ip', 'ios')

    def __new__(_cls, hostname, ip, ios):
        'Create new instance of Router(hostname, ip, ios)'
        return _tuple.__new__(_cls, (hostname, ip, ios))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new Router object from a sequence or iterable'
        result = new(cls, iterable)
        if len(result) != 3:
            raise TypeError('Expected 3 arguments, got %d' % len(result))
        return result

    def _replace(_self, **kwds):
        'Return a new Router object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, ('hostname', 'ip', 'ios'), _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % list(kwds))
        return result

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '(hostname=%r, ip=%r, ios=%r)' % self

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values.'
        return OrderedDict(zip(self._fields, self))

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    hostname = _property(_itemgetter(0), doc='Alias for field number 0')

    ip = _property(_itemgetter(1), doc='Alias for field number 1')

    ios = _property(_itemgetter(2), doc='Alias for field number 2')





```

---
## staticmethod

+++
### staticmethod

staticmethod позволяет добавить в класс функцию, как метод. При этом, в метод не передается ссылка на экземпляр класса, а значит в параметрах метода не надо указывать self.

+++
### staticmethod

```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

    @staticmethod
    def parse_show(command, command_output,
                   index_file='index', templates='templates'):
        attributes = {'Command': command,
                      'Vendor': 'cisco_ios'}
        cli_table = clitable.CliTable(index_file, templates)
        cli_table.ParseCmd(command_output, attributes)
        return [dict(zip(cli_table.header, row)) for row in cli_table]
```

+++
### staticmethod

```python
In [4]: r1 = CiscoSSH(**DEVICE_PARAMS)

In [5]: sh_output = r1.ssh.send_command('sh ip int br')

In [6]: r1.parse_show('sh ip int br', sh_output)
Out[6]:
[{'ADDR': '192.168.100.1',
  'INT': 'Ethernet0/0',
  'PROTO': 'up',
  'STATUS': 'up'},
 {'ADDR': '192.168.200.1',
  'INT': 'Ethernet0/1',
  'PROTO': 'up',
  'STATUS': 'up'},
 {'ADDR': '192.168.230.1',
  'INT': 'Ethernet0/3',
  'PROTO': 'up',
  'STATUS': 'up'}]
```

---
### classmethod

+++
### classmethod


```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

    @classmethod
    def default_params(cls, ip):
        params = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco'}
        return cls(**params)
```

+++
### classmethod

```python
In [8]: r1 = CiscoSSH.default_params('192.168.100.1')

In [9]: r1.send_show_command('sh clock')
Out[9]: '*16:38:01.883 UTC Sun Jan 28 2018'
```


---
### property

+++
### property

```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()
        self.__cfg = None

    def send_show_command(self, command):
        return self.ssh.send_command(command)

    @property
    def cfg(self):
        if not self.__cfg:
            self.__cfg = self.send_show_command('sh run')
        return self.__cfg
```

+++
### property

```python
In [8]: r1 = CiscoSSH(**DEVICE_PARAMS)

In [9]: config = r1.cfg

In [10]: r1.cfg = 'test'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-10-a11a70bc6f4b> in <module>()
----> 1 r1.cfg = 'test'

AttributeError: can't set attribute
```

+++
### property setter

```python
class CiscoSSH:
    def __init__(self, **device_params):
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()
        self.__mgmt_ip = None

    @property
    def mgmt_ip(self):
        if not self.__mgmt_ip:
            loopback0 = self.ssh.send_command('sh run interface lo0')
            self.__mgmt_ip = re.search('ip address (\S+) ', loopback0).group(1)
        return self.__mgmt_ip

    @mgmt_ip.setter
    def mgmt_ip(self, new_ip):
        if self.mgmt_ip != new_ip:
            self.ssh.send_config_set(['interface lo0',
                                      'ip address {} 255.255.255.255'.format(new_ip)])
            self.__mgmt_ip = new_ip
```

+++
### property setter

```python
In [3]: r1 = CiscoSSH(**DEVICE_PARAMS)

In [4]: r1.mgmt_ip
Out[4]: '10.1.1.1'

In [5]: r1.mgmt_ip = '10.1.1.2'

In [6]: r1.mgmt_ip
Out[6]: '10.1.1.2'
```

