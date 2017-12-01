#HSLIDE
## Python для сетевых инженеров

#HSLIDE

## Python package

#VSLIDE

### Python package

Пакет Python - это набор модулей, которые организованы по каталогам. Каталоги задают структуру пакета

Пакет Python и обычны набор скриптов Python отличаются тем, что в пакете, в каждом каталоге должен находиться специальный файл - ```__init__.py```

#VSLIDE

### Python package

Пример структуры пакета:
```
$ tree my_scripts/
my_scripts/
├── __init__.py
├── configs
│   ├── __init__.py
│   └── cisco.py
├── connect.py
└── parse
    ├── __init__.py
    ├── cisco.py
    └── juniper.py

```

Файлы ```__init__.py``` пустые.

#VSLIDE
### Python package

Файл connect.py:
```python
print('Import connect.py')

def connect_ssh(ip):
    print('Connect SSH to {}'.format(ip))


def connect_telnet(ip):
    print('Connect Telnet to {}'.format(ip))
```

#VSLIDE
### Python package

Файл configs/cisco.py:
```python
print('Import configs/cisco.py')

basic_cfg = """
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
"""

lines_cfg = """
!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
"""
```

#VSLIDE
### Python package

Файл parse/cisco.py:
```python
print('Import parse/cisco.py')

def parse_with_re(command):
    print('Parse command {} with regex'.format(command))


def parse_with_textfsm(command):
    print('Parse command {} with texfsm'.format(command))
```

#VSLIDE
### Python package

Файл parse/juniper.py:
```python
print('Import parse/juniper.py')

def parse_with_re(command, regex):
    print('Parse command {} with regex {}'.format(command,
                                                  regex))


def parse_with_textfsm(command, template):
    print('Parse command {} with texfsm {}'.format(command,
                                                   template))
```

#VSLIDE
### Python package

Импорт модулей/функций из пакета:
```python
In [1]: import my_scripts.connect
Import connect.py

In [2]: dir(my_scripts.connect)
Out[2]:
['__builtins__',
 '__cached__',
 '__doc__',
 '__file__',
 '__loader__',
 '__name__',
 '__package__',
 '__spec__',
 'connect_ssh',
 'connect_telnet']

```

#VSLIDE
### Python package

```python
In [3]: my_scripts.connect.connect_ssh('10.1.1.1')
Connect SSH to 10.1.1.1

In [4]: my_scripts.connect.connect_telnet('10.1.1.1')
Connect Telnet to 10.1.1.1

```

#VSLIDE
### Python package

```python
In [5]: import my_scripts.parse.cisco as parse_cisco
Import parse/cisco.py

In [6]: parse_cisco.parse_with_re
Out[6]: <function my_scripts.parse.cisco.parse_with_re>

```

#VSLIDE
### Python package

```python
In [7]: import my_scripts.configs.cisco as cfg_cisco
Import configs/cisco.py

In [8]: cfg_cisco.basic_cfg
Out[8]: '\nservice timestamps debug datetime msec localtime show-timezone year\nservice timestamps log datetime msec localtime show-timezone year\nservice password-encryption\nservice sequence-numbers\n!\nno ip domain lookup\n!\n'

```

#VSLIDE
### Python package

Можно упростить импорт, настроив ```__init__.py```:
```python
from .connect import *
from .parse import cisco
from .parse import juniper as parse_juniper
from .configs.cisco import *
```

#VSLIDE
### Python package

Теперь, если выполнить import my_scripts:
```python
In [1]: import my_scripts
Import connect.py
Import parse/cisco.py
Import parse/juniper.py
Import configs/cisco.py

```

#VSLIDE
### Python package

```python
In [4]: dir(my_scripts)
Out[4]:
[
 'basic_cfg',
 'cisco',
 'configs',
 'connect',
 'connect_ssh',
 'connect_telnet',
 'lines_cfg',
 'parse',
 'parse_juniper']
```

#VSLIDE

### Python package (глобально)

Для того чтобы можно было импортировать пакет, его необходимо разместить в одном из каталогов, в котором Python ищет модули или добавить новый путь:
```
In [1]: import sys

In [2]: sys.path
Out[2]: 
['',
 '/home/vagrant/venv/py3_convert/bin',
 '/home/vagrant/venv/py3_convert/lib/python36.zip',
 '/home/vagrant/venv/py3_convert/lib/python3.6',
 '/home/vagrant/venv/py3_convert/lib/python3.6/lib-dynload',
 '/usr/local/lib/python3.6',
 '/home/vagrant/venv/py3_convert/lib/python3.6/site-packages',
 '/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/IPython/extensions',
 '/home/vagrant/.ipython']
```


#VSLIDE

### Python package (глобально)

Для своих пакетов можно использовать каталог:
```
$ python3.6 -m site --user-site
/home/vagrant/.local/lib/python3.6/site-packages
```

После того как каталог будет создан, он автоматически будет добавлен в пути поиска модулей:
```
$ mkdir -p /home/vagrant/.local/lib/python3.6/site-packages
```

#VSLIDE
### Python package (глобально)

```
In [1]: import sys

In [2]: sys.path
Out[2]: 
['',
 '/usr/local/bin',
 '/usr/local/lib/python36.zip',
 '/usr/local/lib/python3.6',
 '/usr/local/lib/python3.6/lib-dynload',
 '/home/vagrant/.local/lib/python3.6/site-packages',
 '/usr/local/lib/python3.6/site-packages',
 '/usr/local/lib/python3.6/site-packages/IPython/extensions',
 '/home/vagrant/.ipython']

```

#VSLIDE
### Python package (в виртуальном окружении)

Для того чтобы можно было импортировать пакет, его необходимо разместить в одном из каталогов, в котором Python ищет модули или добавить новый путь:
```
['',
 '/home/vagrant/venv/py3_convert/bin',
 '/home/vagrant/venv/py3_convert/lib/python36.zip',
 '/home/vagrant/venv/py3_convert/lib/python3.6',
 '/home/vagrant/venv/py3_convert/lib/python3.6/lib-dynload',
 '/usr/local/lib/python3.6',
 '/home/vagrant/venv/py3_convert/lib/python3.6/site-packages',
 '/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/IPython/extensions',
 '/home/vagrant/.ipython']
```

#VSLIDE
### Python package (в виртуальном окружении)

В виртуальном окружении можно размещать пакеты в пути:
```
/home/vagrant/venv/py3_convert/lib/python3.6/site-packages
```
