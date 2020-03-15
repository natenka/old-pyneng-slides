# What’s New In Python 3.8

---
### Assignment expressions

+++
### Walrus operator

Было:
```
n = len(a)
if n > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

Стало:
```
if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

+++
### Walrus operator

Было:

```python
import re

regex = "vlan (\d+) is flapping between port (\S+) and port (\S+)"

ports = set()

with open("log.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:
            vlan, port1, port2 = match.groups()
            ports.update({port1, port2})

print(f"Петля между портами {', '.join(ports)}")
```

Стало:

```python
with open("log.txt") as f:
    for line in f:
        if (match := re.search(regex, line)):
            vlan, port1, port2 = match.groups()
            ports.update({port1, port2})
```

+++
### Walrus operator

Было:

```
def create_user(db):
    username = input("Введите имя пользователя: ")
    while True:
        password = input("Введите пароль: ")
        check = check_password(username, password)
        if check:
            break
    with open(db, 'a') as f:
        f.write(f"{username},{password}\n")
```

Стало:

```
def create_user(db):
    username = input("Введите имя пользователя: ")
    while not check_password(
        username, password := input("Введите пароль: ")
    ):
        pass
    with open(db, 'a') as f:
        f.write(f"{username},{password}\n")
```


---
### Positional-only arguments

```
In [8]: data = [1, 2, 3]

In [9]: data.append?
Signature: data.append(object, /)
Docstring: Append object to the end of the list.
Type:      builtin_function_or_method

```

+++
### Keyword-only arguments

```
In [2]: sorted?
Signature: sorted(iterable, /, *, key=None, reverse=False)
Docstring:
Return a new list containing all items from the iterable in ascending order.

A custom key function can be supplied to customize the sort order, and the
reverse flag can be set to request the result in descending order.
Type:      builtin_function_or_method
```

---
### f-strings support = for self-documenting expressions and debugging

+++

```
In [23]: ip = "10.1.1.1"

In [24]: mask = 24

In [25]: f"{ip} {mask}"
Out[25]: '10.1.1.1 24'

In [26]: f"{ip=} {mask=}"
Out[26]: "ip='10.1.1.1' mask=24"
```


---
### Модуль typing

+++
### Аннотация типов

Пример аннотации функции:
```
import ipaddress


def check_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError as err:
        return False
```

Пример аннотации функции со значениями по умолчанию:
```
def check_passwd(username: str, password: str,
                 min_length: int = 8, check_username: bool = True) -> bool:
    if len(password) < min_length:
        print('Пароль слишком короткий')
        return False
    elif check_username and username in password:
        print('Пароль содержит имя пользователя')
        return False
    else:
        print(f'Пароль для пользователя {username} прошел все проверки')
        return True
```

+++
### Аннотация типов


```
from typing import Union, List


class BaseSSH:
    def __init__(self, ip: str, username: str, password: str) -> None:
        self.ip = ip
        self.username = username
        self.password = password

    def send_config_commands(self, commands: Union[str, List[str]]) -> str:
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
```

+++
### TypedDict

```
from netmiko import ConnectHandler
from typing import List, Dict, Any


def send_show(device_dict: Dict[str, Any], command: str) -> str:
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return result


device_dict = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
    'port': 20020,
    }
```

+++
### TypedDict

```
from typing import TypedDict, NamedTuple


class IPAddress(NamedTuple):
    ip: str
    mask: int = 24


ip1 = IPAddress('10.1.1.1', 28)

#IPAddress(ip='10.1.1.1', mask=28)


class IPAddress(TypedDict):
    ipaddress: str
    mask: int

ip1 = IPAddress(ipaddress="8.8.8.8", mask=26)

```

+++
### TypedDict

```
from netmiko import ConnectHandler
from typing import List, TypedDict, NamedTuple


class DeviceParams(TypedDict, total=False):
    device_type: str
    host: str
    username: str
    password: str
    secret: str
    port: int


def send_show(device_dict: DeviceParams, command: str) -> str:
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return result


if __name__ == "__main__":
    r1 = DeviceParams(
        device_type="cisco_ios",
        host="192.168.100.1",
        username="cisco",
        password="cisco",
        secret="cisco",
        port=20020,
    )
    print(send_show(r1, "sh clock"))

```

+++
### Literal

```
from typing import Literal


def get_data_by_key_value(
    db_name: str, key: Literal["mac", "ip", "vlan", "interface"], value: str
) -> str:
    return "line"


print(get_data_by_key_value("database.db", "ip", "8.8.8.8"))
```

+++
### Final


```
import sqlite3
from typing import Final, final

DATABASE: Final[str] = "dhcp_snooping.db"


def create_db(db_name: str, schema: str) -> None:
    with open(schema) as f:
        schema_f = f.read()
        connection = sqlite3.connect(db_name)
        connection.executescript(schema_f)
        connection.close()


if __name__ == "__main__":
    DATABASE = "mydb.db"
    schema_filename = "dhcp_snooping_schema.sql"
    create_db(DATABASE, schema_filename)
```

Ошибка:
```
$ mypy typing_final.py
typing_final.py:19: error: Cannot assign to final name "DATABASE"
Found 1 error in 1 file (checked 1 source file)

```

+++
### Final

```
from typing import Final


class BaseSSH:
    TIMEOUT: Final[int] = 10

class CiscoSSH(BaseSSH):
    TIMEOUT = 1

```

+++
### final

Декоратор final указывает, что метод не может быть переписан

```
from typing import final


class BaseSSH:
    @final
    def done(self) -> None:
        pass


class CiscoSSH(BaseSSH):
    def done(self) -> None:
        pass

```

+++
### final

Декоратор final указывает, что класс не может наследоваться

```
from typing import final

@final
class CiscoIosSSH:
    pass


class Other(CiscoIosSSH):
    pass

```

+++
### Protocol

```
class ConnectSSH(Protocol):
    def send_command(self, command: str) -> str:
        ...

    def send_config_commands(self, commands: str) -> str:
        ...


class CiscoSSH:

    def send_command(self, command: str) -> str:
        result = self._ssh.send_command(command)
        return result

    def send_config_commands(self, commands: str) -> str:
        result = self._ssh.send_config_set(commands)
        return result


def func(connection: ConnectSSH, command: str) -> str:
    return connection.send_command(command)


if __name__ == "__main__":
    r1 = CiscoSSH("192.168.100.1", "cisco", "cisco", "cisco")
    print(func(r1, "sh clock"))

```

---
### iterable unpacking in yield and return

До Python 3.8 можно было так:
```
In [27]: data = [1, 2, 3]

In [28]: result = 1, 2, *data

In [29]: result
Out[29]: (1, 2, 1, 2, 3)
```

После можно еще и так:
```
In [30]: def func():
    ...:     data = [1, 2, 3]
    ...:     return 1, 2, *data
    ...:

In [31]: func()
Out[31]: (1, 2, 1, 2, 3)

```

---
### SyntaxWarning

---
### asyncio REPL

---
### collections, csv - dict

---
### logging

---
### pprint


