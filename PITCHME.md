# Python для сетевых инженеров 


#HSLIDE

## Модули

#VSLIDE

### Модули

Модуль в Python это обычный текстовый файл с кодом Python и расширением __.py__.
Они позволяют логически упорядочить и сгруппировать код.

Разделение на модули может быть, например, по такой логике:
* разделение данных, форматирования и логики кода
* группировка функций и других объектов по функционалу

Модули хороши тем, что позволяют повторно использовать уже написанный код и не копировать его (например, не копировать когда-то написанную функцию).

#HSLIDE

## Импорт модуля

#VSLIDE

### Импорт модуля

В Python есть несколько способов импорта модуля:
* ```import module```
* ```import module as```
* ```from module import object```
* ```from module import *```

#VSLIDE
### ```import module```

```python
In [1]: dir()
Out[1]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'quit']

In [2]: import os

In [3]: dir()
Out[3]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'os',
 'quit']

In [4]: os.getlogin()
Out[4]: 'natasha'
```

#VSLIDE
### ```import module as```

Конструкция __import module as__ позволяет импортировать модуль под другим именем (как правило, более коротким):
```python
In [1]: import subprocess as sp

In [2]: sp.check_output('ping -c 2 -n  8.8.8.8', shell=True)
Out[2]: 'PING 8.8.8.8 (8.8.8.8): 56 data bytes\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.880 ms\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=46.875 ms\n\n--- 8.8.8.8 ping statistics ---\n2 packets transmitted, 2 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 46.875/48.377/49.880/1.503 ms\n'
```

#VSLIDE

### ```from module import object```
Вариант __from module import object__ удобно использовать, когда из всего модуля нужны только одна-две функции:

```python
In [1]: from os import getlogin, getcwd
```

Теперь эти функции доступны в текущем именном пространстве:
```python
In [2]: dir()
Out[2]: 
['In',
 'Out',
 ...
 'exit',
 'get_ipython',
 'getcwd',
 'getlogin',
 'quit']
```

#VSLIDE
### ```from module import object```

Их можно вызывать без имени модуля:
```python
In [3]: getlogin()
Out[3]: 'natasha'

In [4]: getcwd()
Out[4]: '/Users/natasha/Desktop/Py_net_eng/code_test'
```

#VSLIDE
### ```from module import *```

Вариант __from module import *__ импортирует все имена модуля в текущее именное пространство:
```python
In [1]: from os import *

In [2]: dir()
Out[2]: 
['EX_CANTCREAT',
 'EX_CONFIG',
 ...
 'wait',
 'wait3',
 'wait4',
 'waitpid',
 'walk',
 'write']

```

Такой вариант импорта лучше не использовать.
При таком импорте, по коду не понятно, что какая-то функция взята из модуля os, например.
Это заметно усложняет понимание кода.

#HSLIDE

## Создание своих модулей

#VSLIDE
### Создание своих модулей

Файл sw_int_templates.py:
```python
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan']

l3int_template = ['no switchport', 'ip address']
```

Файл sw_data.py:
```python
sw1_fast_int = {
                'access':{
                         '0/12':'10',
                         '0/14':'11',
                         '0/16':'17'}}
```

#VSLIDE
### Создание своих модулей

Совмещаем всё вместе в файле generate_sw_int_cfg.py:
```python
import sw_int_templates
from sw_data import sw1_fast_int


def generate_access_cfg(sw_dict):
    result = []
    for intf in sw_dict['access']:
        result.append('interface FastEthernet' + intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' %s %s' % (command, sw_dict['access'][intf]))
            else:
                result.append(' %s' % command)
    return result


print '\n'.join(generate_access_cfg(sw1_fast_int))

```

#VSLIDE
### Создание своих модулей

Результат выполнения скрипта:
```
$ python generate_sw_int_cfg.py
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable
```

#VSLIDE

### ```if __name__ == "__main__"```

Иногда, скрипт, который вы создали, может выполняться и самостоятельно, и может быть импортирован как модуль, другим скриптом.

Файл sw_cfg_templates.py с шаблонами конфигурации:
```python
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

### ```if __name__ == "__main__"```

В файле generate_sw_cfg.py импортируются шаблоны из sw_cfg_templates.py и функции из предыдущих файлов:
```python
from sw_data import sw1_fast_int
from generate_sw_int_cfg import generate_access_cfg
from sw_cfg_templates import basic_cfg, lines_cfg


print basic_cfg
print '\n'.join(generate_access_cfg(sw1_fast_int))
print lines_cfg
```

В результате, должны отобразиться такие части конфигурации, по порядку:
шаблон basic_cfg, настройка интерфейсов, шаблон lines_cfg.

#VSLIDE

### ```if __name__ == "__main__"```

Результат выполнения:
```
$ python generate_sw_cfg.py
interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable

service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!

interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable

!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!
```

#VSLIDE

### ```if __name__ == "__main__"```

Полученный вывод не совсем правильный: перед строками шаблона basic_cfg, идет лишняя конфигурация интерфейсов.


Так получилось из-за строки print в файле generate_sw_int_cfg.py:
```python
print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Когда скрипт импортирует какой-то модуль, всё, что находится в модуле, выполняется.


#VSLIDE

### ```if __name__ == "__main__"```

Файл generate_sw_int_cfg2.py:
```python
import sw_int_templates
from sw_data import sw1_fast_int


def generate_access_cfg(sw_dict):
    result = []
    for intf in sw_dict['access']:
        result.append('interface FastEthernet' + intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' %s %s' % (command, sw_dict['access'][intf]))
            else:
                result.append(' %s' % command)
    return result

if __name__ == "__main__":
    print '\n'.join(generate_access_cfg(sw1_fast_int))

```

#VSLIDE

### ```if __name__ == "__main__"```

```python
if __name__ == "__main__":
    print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Переменная ```__name__``` это специальная переменная, которая выставляется равной ```"__main__"```, если если файл запускается как основная программа.
И выставляется равной имени модуля, если модуль импортируется.

Таким образом, условие ```if __name__ == "__main__"``` проверяет был ли файл запущен напрямую.

#VSLIDE

### ```if __name__ == "__main__"```

```python
$ python generate_sw_cfg.py

service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!

interface FastEthernet0/12
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/14
 switchport mode access
 switchport access vlan 11
 spanning-tree portfast
 spanning-tree bpduguard enable
interface FastEthernet0/16
 switchport mode access
 switchport access vlan 17
 spanning-tree portfast
 spanning-tree bpduguard enable

!
line con 0
 logging synchronous
 history size 100
line vty 0 4
 logging synchronous
 history size 100
 transport input ssh
!

```


#HSLIDE

## Полезные модули

#HSLIDE

## Модуль subprocess

#VSLIDE

### Модуль subprocess

Модуль subprocess позволяет создавать новые процессы.
При этом, он может подключаться к [стандартным потокам ввода/вывода/ошибок](http://xgu.ru/wiki/stdin) и получать код возврата.


С помощью subprocess, можно, например, выполнять любые команды Linux из скрипта.
И, в зависимости от ситуации, получать вывод или только проверять, что команда выполнилась без ошибок.

#VSLIDE
### Функция ```subprocess.call()```

Функция ```call()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* функция возращает код возврата


#VSLIDE
### Функция ```subprocess.call()```

Пример выполнения команды ```ls```:
```python
In [1]: import subprocess

In [2]: result = subprocess.call('ls')
LICENSE.md          course_presentations        faq.md
README.md           course_presentations.zip    howto.md
SUMMARY.md          cover.jpg           images
ToDo.md             examples            resources
about.md            examples.zip            schedule.md
book                exercises
book.json           exercises.zip
```

В переменной result теперь содержится код возврата (код 0 означает, что программа выполнилась успешно):
```python
In [3]: print result
0
```

#VSLIDE
### Функция ```subprocess.call()```

Если необходимо вызвать команду с аргументами, её нужно передавать таким образом (как список):
```
In [4]: result = subprocess.call(['ls', '-ls'])
total 3624
   8 -rw-r--r--   1 nata  nata      372 Dec 10 21:34 LICENSE.md
  16 -rw-r--r--   1 nata  nata     4528 Jan 12 09:16 README.md
  32 -rw-r--r--   1 nata  nata    12480 Jan 23 11:15 SUMMARY.md
   8 -rw-r--r--   1 nata  nata     2196 Jan 23 09:16 ToDo.md
   8 -rw-r--r--   1 nata  nata       70 Dec 10 21:34 about.md
   0 drwxr-xr-x  19 nata  nata      646 Jan 23 11:05 book
   8 -rw-r--r--   1 nata  nata      355 Jan 12 09:16 book.json
   0 drwxr-xr-x  16 nata  nata      544 Dec 10 21:34 course_presentations
2176 -rw-r--r--   1 nata  nata  1111234 Dec 10 21:34 course_presentations.zip
 528 -rw-r--r--@  1 nata  nata   267824 Dec 11 08:25 cover.jpg
   0 drwxr-xr-x  20 nata  nata      680 Jan 23 13:05 examples
 360 -rw-r--r--   1 nata  nata   181075 Jan 21 14:10 examples.zip
   0 drwxr-xr-x  19 nata  nata      646 Jan 17 10:24 exercises
 416 -rw-r--r--   1 nata  nata   210621 Jan 21 14:10 exercises.zip
  32 -rw-r--r--   1 nata  nata    14684 Jan 18 05:33 faq.md
  16 -rw-r--r--   1 nata  nata     7043 Jan 17 10:28 howto.md
   0 drwxr-xr-x   4 nata  nata      136 Jan 14 11:01 images
   0 drwxr-xr-x  10 nata  nata      340 Jan 17 08:44 resources
  16 -rw-r--r--@  1 nata  nata     6219 Jan 17 11:37 schedule.md
```

#VSLIDE
### Функция ```subprocess.call()```

Все файлы, с расширением md:
```python
In [5]: result = subprocess.call(['ls', '-ls', '*md'])
ls: *md: No such file or directory
```

Чтобы вызывать команды, в которых используются регулярные выражения, нужно добавлять параметр shell:
```python
In [6]: result = subprocess.call(['ls', '-ls', '*md'], shell=True)
LICENSE.md          course_presentations        faq.md
README.md           course_presentations.zip    howto.md
SUMMARY.md          cover.jpg           images
ToDo.md             examples            resources
about.md            examples.zip            schedule.md
book                exercises
book.json           exercises.zip
```

#VSLIDE
### Функция ```subprocess.call()```

Если устанавлен аргумент ```shell=True```, указанная команда выполняется через shell.
В таком случае, команду можно указывать так:
```python
In [7]: result = subprocess.call('ls -ls *md', shell=True)
 8 -rw-r--r--  1 nata  nata    372 Dec 10 21:34 LICENSE.md
16 -rw-r--r--  1 nata  nata   4528 Jan 12 09:16 README.md
32 -rw-r--r--  1 nata  nata  12480 Jan 23 11:15 SUMMARY.md
 8 -rw-r--r--  1 nata  nata   2196 Jan 23 09:16 ToDo.md
 8 -rw-r--r--  1 nata  nata     70 Dec 10 21:34 about.md
32 -rw-r--r--  1 nata  nata  14684 Jan 18 05:33 faq.md
16 -rw-r--r--  1 nata  nata   7043 Jan 17 10:28 howto.md
16 -rw-r--r--@ 1 nata  nata   6219 Jan 17 11:37 schedule.md
```

#VSLIDE
### Функция ```subprocess.call()```

Ещё одна особенность функции ```call()``` - она ожидает завершения выполнения команды.
Если попробовать, например, запустить команду ping, то этот аспект будет заметен:
```python
In [8]: reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.868 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.243 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=50.029 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.243/49.713/50.029/0.339 ms
```

Особенно, если попробовать пингануть какой-то недоступный IP-адрес.

#VSLIDE
### Функция ```subprocess.call()```

Функция ```call()``` подходит, если нужно:
* подождать выполнения программы, прежде чем выполнять следующие шаги
* нужно получить только код выполнения и не нужен вывод


#VSLIDE
### Функция ```subprocess.call()```

Ещё один аспект работы функции ```call()```, она выводит результат выполнения команды, на стандартный поток вывода.

Файл subprocess_call.py:
```python
import subprocess

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])

if reply == 0:
    print "Alive"
else:
    print "Unreachable"
```

#VSLIDE
### Функция ```subprocess.call()```

Результат выполнения будет таким:
```
$ python subprocess_call.py
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.930 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=48.981 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=48.360 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.360/49.090/49.930/0.646 ms
Alive
```

То есть, результат выполнения команды, выводится на стандартный поток вывода.

#VSLIDE
### Функция ```subprocess.call()```

Если нужно это отключить и не выводить результат выполнения, надо перенаправить stdout в devnull (файл subprocess_call_devnull.py):
```python
import subprocess
import os

DNULL = open(os.devnull, 'w')

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'], stdout=DNULL)

if reply == 0:
    print "Alive"
else:
    print "Unreachable"
```

Теперь результат выполнения будет таким:
```
$ python subprocess_call_devnull.py
Alive
```

#VSLIDE
### Функция ```subprocess.check_output()```

Функция ```check_output()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* если команда отработала корректно (код возврата 0), функция возращает результат выполнения команды
* если возникла ошибка, при выполнении команды, функция генерирует исключение

#VSLIDE
### Функция ```subprocess.check_output()```

Пример использования функции ```check_output()``` (файл subprocess_check_output.py):
```python
import subprocess

reply = subprocess.check_output(['ping', '-c', '3', '-n', '8.8.8.8'])

print "Result:"
print reply
```

#VSLIDE
### Функция ```subprocess.check_output()```

Результат выполнения (если убрать строку ```print reply```, на стандартный поток вывода ничего не будет выведено):
```
$ python subprocess_check_output.py
Result:
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.785 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=57.231 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=51.071 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.785/52.696/57.231/3.250 ms
```

#VSLIDE
### Функция ```subprocess.check_output()```

Если выполнить команду, которая вызовет ошибку и, соответственно, код возрата будет не 0 (файл subprocess_check_output_catch_exception.py):
```python
$ python subprocess_check_output_catch_exception.py
ping: cannot resolve a: Unknown host
Traceback (most recent call last):
  File "subprocess_check_output_catch_exception.py", line 3, in <module>
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 573, in check_output
    raise CalledProcessError(retcode, cmd, output=output)
subprocess.CalledProcessError: Command '['ping', '-c', '3', '-n', 'a']' returned non-zero exit status 68
```

#VSLIDE
### Функция ```subprocess.check_output()```

Функция ```check_output()``` всегда будет возвращать исключение ```CalledProcessError```, когда код возврата не равен 0.

Это значит, что в скрипте можно написать выражение try/except, с помощью которого будет выполняться проверка корректно ли отработала команда (дополняем файл subprocess_check_output_catch_exception.py):
```python
import subprocess

try:
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
except subprocess.CalledProcessError as e:
    print "Error occurred"
    print "Return code:", e.returncode
```

#VSLIDE
### Функция ```subprocess.check_output()```

Результат выполнения:
```
$ python subprocess_check_output_catch_exception.py
ping: cannot resolve a: Unknown host
Error occurred
Return code: 68
```

Теперь программа завершилась корректно и вывела сообщение об ошибке и код возврата.
И, хотя сообщение об ошибке, не выводилось, оно попало на стандартный поток вывода.

#VSLIDE
### Функция ```subprocess.check_output()```

Попробуем собрать всё в финальную функцию и добавим перехват сообщения об ошибке:
```python
import subprocess
from tempfile import TemporaryFile


def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * return code = 0
        * command output
    On failure:
        * return code
        * error output (stderr)
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', '3', '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()

print ping_ip('8.8.8.8')
print ping_ip('a')
```

#VSLIDE
### Функция ```subprocess.check_output()```


Результат выполнения будет таким:
```
$ python subprocess_ping_function.py
(0, 'PING 8.8.8.8 (8.8.8.8): 56 data bytes\n64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=46.106 ms\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=46.114 ms\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=47.390 ms\n\n--- 8.8.8.8 ping statistics ---\n3 packets transmitted, 3 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 46.106/46.537/47.390/0.603 ms\n')

(68, 'ping: cannot resolve a: Unknown host\n')
```

#VSLIDE
### Функция ```subprocess.check_output()```

Модуль tempfile входит в стандартную библиотеку Python и используется тут для того, чтобы сохранить сообщение об ошибке.
Функция TemporaryFile создает временный файл и удаляет его автоматически, после того, как файл закрывается.

> Подробнее о модуле tempfile можно почитать на сайте [PyMOTW](https://pymotw.com/2/tempfile/).

На основе этой функции, можно сделать функцию, которая будет проверять список IP-адресов и возвращать, в результате выполнения, два списка: доступные и недоступные адреса.

Если количество IP-адресов, которые нужно проверить, большое, можно использовать модуль multiprocessing, чтобы ускорить проверку.


