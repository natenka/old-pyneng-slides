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
                result.append(' {} {}'.format(command,
                                              sw_dict['access'][intf]))
            else:
                result.append(' {}'.format(command))
    return result


print('\n'.join(generate_access_cfg(sw1_fast_int)))

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

### if __name__ == "__main__"

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

### if __name__ == "__main__"

В файле generate_sw_cfg.py импортируются шаблоны из sw_cfg_templates.py и функции из предыдущих файлов:
```python
from sw_data import sw1_fast_int
from generate_sw_int_cfg import generate_access_cfg
from sw_cfg_templates import basic_cfg, lines_cfg


print(basic_cfg)
print('\n'.join(generate_access_cfg(sw1_fast_int)))
print(lines_cfg)
```

В результате, должны отобразиться такие части конфигурации, по порядку:
шаблон basic_cfg, настройка интерфейсов, шаблон lines_cfg.

#VSLIDE

### if __name__ == "__main__"

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

### if __name__ == "__main__"

Полученный вывод не совсем правильный: перед строками шаблона basic_cfg, идет лишняя конфигурация интерфейсов.


Так получилось из-за строки print в файле generate_sw_int_cfg.py:
```python
print '\n'.join(generate_access_cfg(sw1_fast_int))
```

Когда скрипт импортирует какой-то модуль, всё, что находится в модуле, выполняется.


#VSLIDE

### if __name__ == "__main__"

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
                result.append(' {} {}'.format( command, sw_dict['access'][intf] ))
            else:
                result.append(' {}'.format( command ))
    return result

if __name__ == "__main__":
    print('\n'.join(generate_access_cfg(sw1_fast_int)))

```

#VSLIDE

### if __name__ == "__main__"

```python
if __name__ == "__main__":
    print('\n'.join(generate_access_cfg(sw1_fast_int)))
```

Переменная ```__name__``` это специальная переменная, которая выставляется равной ```"__main__"```, если если файл запускается как основная программа.
И выставляется равной имени модуля, если модуль импортируется.

Таким образом, условие ```if __name__ == "__main__"``` проверяет был ли файл запущен напрямую.

#VSLIDE

### if __name__ == "__main__"

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
### Функция subprocess.call()

Функция ```call()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* функция возращает код возврата


#VSLIDE
### Функция subprocess.call()

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
In [3]: print(result)
0
```

#VSLIDE
### Функция subprocess.call()

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
### Функция subprocess.call()

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
### Функция subprocess.call()

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
### Функция subprocess.call()

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
### Функция subprocess.call()

Функция ```call()``` подходит, если нужно:
* подождать выполнения программы, прежде чем выполнять следующие шаги
* нужно получить только код выполнения и не нужен вывод


#VSLIDE
### Функция subprocess.call()

Ещё один аспект работы функции ```call()```, она выводит результат выполнения команды, на стандартный поток вывода.

Файл subprocess_call.py:
```python
import subprocess

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'])

if reply == 0:
    print("Alive")
else:
    print("Unreachable")

```

#VSLIDE
### Функция subprocess.call()

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
### Функция subprocess.call()

Если нужно это отключить и не выводить результат выполнения, надо перенаправить stdout в devnull (файл subprocess_call_devnull.py):
```python
import subprocess
import os

DNULL = open(os.devnull, 'w')

reply = subprocess.call(['ping', '-c', '3', '-n', '8.8.8.8'], stdout=DNULL)

if reply == 0:
    print("Alive")
else:
    print("Unreachable")

```

Теперь результат выполнения будет таким:
```
$ python subprocess_call_devnull.py
Alive
```

#VSLIDE
### Функция subprocess.check_output()


Функция ```check_output()```:
* позволяет выполнить команду
 * при этом, она ожидает завершения команды.
* если команда отработала корректно (код возврата 0), функция возращает результат выполнения команды
* если возникла ошибка, при выполнении команды, функция генерирует исключение

#VSLIDE
### Функция subprocess.check_output()

Пример использования функции ```check_output()``` (файл subprocess_check_output.py):
```python
import subprocess

reply = subprocess.check_output(['ping', '-c', '3', '-n', '8.8.8.8'])

print("Result:")
print(reply.decode('utf-8'))

```

#VSLIDE
### Функция subprocess.check_output()

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
### Функция subprocess.check_output()

Если выполнить команду, которая вызовет ошибку и, соответственно, код возрата будет не 0 (файл subprocess_check_output_catch_exception.py):
```python
$ python subprocess_check_output_catch_exception.py
ping: unknown host a
Traceback (most recent call last):
  File "subprocess_check_output_catch_exception.py", line 3, in <module>
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
  File "/usr/local/lib/python3.6/subprocess.py", line 336, in check_output
    **kwargs).stdout
  File "/usr/local/lib/python3.6/subprocess.py", line 418, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['ping', '-c', '3', '-n', 'a']' returned non-zero exit status 2.

```

#VSLIDE
### Функция subprocess.check_output()

Функция ```check_output()``` всегда будет возвращать исключение ```CalledProcessError```, когда код возврата не равен 0.

Это значит, что в скрипте можно написать выражение try/except, с помощью которого будет выполняться проверка корректно ли отработала команда (дополняем файл subprocess_check_output_catch_exception.py):
```python
import subprocess

try:
    reply = subprocess.check_output(['ping', '-c', '3', '-n', 'a'])
except subprocess.CalledProcessError as e:
    print("Error occurred")
    print("Return code:", e.returncode)

```

#VSLIDE
### Функция subprocess.check_output()

Результат выполнения:
```
$ python subprocess_check_output_catch_exception.py
ping: unknown host a
Error occurred
Return code: 2

```

Теперь программа завершилась корректно и вывела сообщение об ошибке и код возврата.
И, хотя сообщение об ошибке, не выводилось, оно попало на стандартный поток вывода.

#VSLIDE
### Функция subprocess.check_output()

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
            return 0, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read().decode('utf-8')

print(ping_ip('8.8.8.8'))
print(ping_ip('a'))

```

#VSLIDE
### Функция subprocess.check_output()


Результат выполнения будет таким:
```
$ python subprocess_ping_function.py
(0, 'PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.\n64 bytes from 8.8.8.8: icmp_seq=1 ttl=43 time=53.0 ms\n64 bytes from 8.8.8.8: icmp_seq=2 ttl=43 time=57.5 ms\n64 bytes from 8.8.8.8: icmp_seq=3 ttl=43 time=54.1 ms\n\n--- 8.8.8.8 ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 2004ms\nrtt min/avg/max/mdev = 53.060/54.906/57.546/1.934 ms\n')
(2, 'ping: unknown host a\n')

```

#VSLIDE
### Модуль tempfile

Модуль tempfile входит в стандартную библиотеку Python и используется тут для того, чтобы сохранить сообщение об ошибке.
Функция TemporaryFile создает временный файл и удаляет его автоматически, после того, как файл закрывается.

На основе этой функции, можно сделать функцию, которая будет проверять список IP-адресов и возвращать, в результате выполнения, два списка: доступные и недоступные адреса.

Если количество IP-адресов, которые нужно проверить, большое, можно использовать модуль multiprocessing, чтобы ускорить проверку.

#HSLIDE

## Модуль os

#VSLIDE

### Модуль os

Модуль ```os``` позволяет работать с файловой системой, с окружением, управлять процессами.


#VSLIDE

### Модуль os

Модуль os позволяет создавать каталоги:
```python
In [1]: import os

In [2]: os.mkdir('test')

In [3]: ls -ls
total 0
0 drwxr-xr-x  2 nata  nata  68 Jan 23 18:58 test/
```
#VSLIDE

### Модуль os

Кроме того, в модуле есть соответствующие проверки на существование.
Например, если попробовать повторно создать каталог, возникнет ошибка:
```python
In [4]: os.mkdir('test')
---------------------------------------------------------------------------
FileExistsError                           Traceback (most recent call last)
<ipython-input-4-cbf3b897c095> in <module>()
----> 1 os.mkdir('test')

FileExistsError: [Errno 17] File exists: 'test'

```

В таком случае, пригодится проверка ```os.path.exists```:
```python
In [5]: os.path.exists('test')
Out[5]: True

In [6]: if not os.path.exists('test'):
   ...:     os.mkdir('test')
   ...:
```

#VSLIDE

### Модуль os

Метод listdir, позволяет посмотреть содержимое каталога:
```python
In [7]: os.listdir('.')
Out[7]: ['cover3.png', 'dir2', 'dir3', 'README.txt', 'test']
```

С помощью проверок ```os.path.isdir``` и ```os.path.isfile```, можно получить отдельно список файлов и список каталогов:
```python
In [8]: dirs = [ d for d in os.listdir('.') if os.path.isdir(d)]

In [9]: dirs
Out[9]: ['dir2', 'dir3', 'test']

In [10]: files = [ f for f in os.listdir('.') if os.path.isfile(f)]

In [11]: files
Out[11]: ['cover3.png', 'README.txt']

```

#VSLIDE

### Модуль os

Также в модуле есть отдельные методы для работы с путями:
```python
In [12]: os.path.basename(file)
Out[12]: 'README.md'

In [13]: os.path.dirname(file)
Out[13]: 'Programming/PyNEng/book/16_additional_info'

In [14]: os.path.split(file)
Out[14]: ('Programming/PyNEng/book/16_additional_info', 'README.md')
```

#HSLIDE
## Модуль argparse


#VSLIDE

### Модуль argparse

argparse - это модуль для обработки аргументов командной строки.

Примеры того, что позволяет делать модуль:
* создавать аргументы и опции, с которыми может вызываться скрипт
* указывать типы аргументов, значения по умолчанию
* указывать какие действия соответствуют аргументам
* выполнять вызов функции, при указании аргумента
* отображать сообщения с подсказами по использованию скрипта

#VSLIDE

### Модуль argparse


Пример скрипта ping_function.py:
```python
import subprocess
from tempfile import TemporaryFile
import argparse

def ping_ip(ip_address, count):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read().decode('utf-8')

```

#VSLIDE

### Модуль argparse


Пример скрипта ping_function.py (продолжение):
```python
parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('-a', action="store", dest="ip")
parser.add_argument('-c', action="store", dest="count", default=2, type=int)

args = parser.parse_args()
print(args)

rc, message = ping_ip( args.ip, args.count )
print(message)

```

#VSLIDE

### Модуль argparse

Создание парсера:
```
parser = argparse.ArgumentParser(description='Ping script')
```

#VSLIDE

### Модуль argparse

Добавление аргументов:
* аргумент, который передается после опции ```-a```, сохранится в переменную ```ip```
```
parser.add_argument('-a', action="store", dest="ip")
```

* аргумент, который передается после опции ```-c```, будет сохранен в переменную ```count```, но, прежде, будет конвертирован в число. Если аргумент не было указан, по умолчанию, будет значение 2
```
parser.add_argument('-c', action="store", dest="count", default=2, type=int)
```

#VSLIDE

### Модуль argparse

Строка ```args = parser.parse_args()``` указывается, после того как определены все аргументы.

После её выполнения, в переменной ```args``` содержатся все аргументы, которые были переданы скрипту.
К ним можно обращаться, используя синтаксис ```args.ip```.

#VSLIDE

### Модуль argparse

Если переданы оба аргумента:
```
$ python ping_function.py -a 8.8.8.8 -c 5
Namespace(count=5, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.673 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.902 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=48.696 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=48 time=50.040 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=48 time=48.831 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.673/49.228/50.040/0.610 ms
```

Namespace - это объект, который возвращает метод parse_args()

#VSLIDE

### Модуль argparse

Передаем только IP-адрес:
```
$ python ping_function.py -a 8.8.8.8
Namespace(count=2, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.563 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.616 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.563/49.090/49.616/0.526 ms
```

#VSLIDE

### Модуль argparse

Вызов скрипта без аргументов:
```
$ python ping_function.py
Namespace(count=2, ip=None)
Traceback (most recent call last):
  File "ping_function.py", line 31, in <module>
    rc, message = ping_ip( args.ip, args.count )
  File "ping_function.py", line 16, in ping_ip
    stderr=temp)
  File "/usr/local/lib/python3.6/subprocess.py", line 336, in check_output
    **kwargs).stdout
  File "/usr/local/lib/python3.6/subprocess.py", line 403, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/local/lib/python3.6/subprocess.py", line 707, in __init__
    restore_signals, start_new_session)
  File "/usr/local/lib/python3.6/subprocess.py", line 1260, in _execute_child
    restore_signals, start_new_session, preexec_fn)
TypeError: expected str, bytes or os.PathLike object, not NoneType

```

#VSLIDE

### Модуль argparse

Если бы функция была вызвана без аргументов, когда не используется argparse, возникла ошибка, что не все аргументы указаны.

Но, из-за argparse, фактически аргумент передается, только он равен ```None```.
Это видно в строке ```Namespace(count=2, ip=None)```.

#VSLIDE

### Модуль argparse

В таком скрипте, очевидно, IP-адрес необходимо указывать всегда.
И в argparse можно указать, что аргумент является обязательным.

Надо изменить опцию ```-a```: добавить в конце ```required=True```:
```python
parser.add_argument('-a', action="store", dest="ip", required=True)
```

#VSLIDE

### Модуль argparse

Теперь, если вызвать скрипт без аргументов, вывод будет таким:
```
$ python ping_function.py
usage: ping_function.py [-h] -a IP [-c COUNT]
ping_function.py: error: the following arguments are required: -a

```

Теперь отображается понятное сообщение, что надо указать обязательный аргумент.
И подсказка usage.

#VSLIDE

### Модуль argparse

Также, благодаря argparse, доступен help:
```
$ python ping_function.py -h
usage: ping_function.py [-h] -a IP [-c COUNT]

Ping script

optional arguments:
  -h, --help  show this help message and exit
  -a IP
  -c COUNT
```

Обратите внимание, что в сообщении, все опции находятся в секции `optional arguments`.
argparse сам определяет, что указаны опцию, так как они начинаются с ```-``` и в имени только одна буква.

#VSLIDE

### Модуль argparse

Зададим IP-адрес, как позиционный аргумент.

Файл ping_function_ver2.py:
```python
import subprocess
from tempfile import TemporaryFile

import argparse

def ping_ip(ip_address, count=3):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read().decode('utf-8')

```
#VSLIDE

### Модуль argparse

Файл ping_function_ver2.py (продолжение):
```python
parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('host', action="store", help="IP or name to ping")
parser.add_argument('-c', action="store", dest="count", default=2, type=int,
                    help="Number of packets")

args = parser.parse_args()
print(args)

rc, message = ping_ip( args.host, args.count )
print(message)

```

#VSLIDE

### Модуль argparse

Теперь, вместо указания опции ```-a```, можно просто передать IP-адрес.
Он будет автоматически сохранен в переменной ```host```.
И автоматически считается обязательным.

То есть, теперь не нужно указывать ```required=True``` и ```dest="ip"```.

#VSLIDE

### Модуль argparse

Теперь вызов скрипта выглядит так:
```
$ python ping_function_ver2.py 8.8.8.8 -c 2
Namespace(host='8.8.8.8', count=2)
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.203 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=51.764 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.203/50.484/51.764/1.280 ms
```

#VSLIDE

### Модуль argparse


А сообщение help так:
```
$ python ping_function_ver2.py -h
usage: ping_function_ver2.py [-h] [-c COUNT] host

Ping script

positional arguments:
  host        IP or name to ping

optional arguments:
  -h, --help  show this help message and exit
  -c COUNT    Number of packets
```

#VSLIDE

### Вложенные парсеры

Файл parse_dhcp_snooping.py:
```python
# -*- coding: utf-8 -*-
import argparse

DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'

def create(args):
    print("Creating DB {} with DB schema {}".format((args.name, args.schema)))


def add(args):
    if args.sw_true:
        print("Adding switch data to database")
    else:
        print("Reading info from file(s) \n{}".format(', '.join(args.filename)))
        print("\nAdding data to db {}".format(args.db_file))


def get(args):
    if args.key and args.value:
        print("Geting data from DB: {}".format(args.db_file))
        print("Request data for host(s) with {} {}".format((args.key, args.value)))
    elif args.key or args.value:
        print("Please give two or zero args\n")
        print(show_subparser_help('get'))
    else:
        print("Showing {} content...".format(args.db_file))

```

#VSLIDE

### Вложенные парсеры

Файл parse_dhcp_snooping.py:
```python

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='description')


create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
create_parser.set_defaults( func=create )
```

#VSLIDE

### Вложенные парсеры

Файл parse_dhcp_snooping.py:
```python
add_parser = subparsers.add_parser('add', help='add data to db')
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
add_parser.add_argument('-s', dest='sw_true', action='store_true',
                        help='add switch data if set, else add normal data')
add_parser.set_defaults( func=add )


get_parser = subparsers.add_parser('get', help='get data from db')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
get_parser.add_argument('-k', dest="key",
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
get_parser.add_argument('-v', dest="value", help='value of key')
get_parser.add_argument('-a', action='store_true', help='show db content')
get_parser.set_defaults( func=get )

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

#VSLIDE

### Вложенные парсеры

Вложенные парсеры будут отображаться как команды.
Но, фактически, они будут использоваться как обязательные аргументы.

С помощью вложенных парсеров, создается иерархия аргументов и опций.
Аргументы, которые добавлены во вложенный парсер, будут доступны как аргументы этого парсера.


Например, в этой части, создан вложенный парсер create_db и к нему добавлена опция ```-n```:
```python
create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', dest='name', default=DFLT_DB_NAME,
                           help='db filename')
```

#VSLIDE

### Вложенные парсеры

Синтаксис создания вложенных парсеров и добавления к ним аргументов, одинаков:
```python
create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
create_parser.set_defaults( func=create )
```

Метод ```add_argument``` добавляет аргумент.
Тут синтаксис точно такой же, как и без использования вложенных парсеров.

#VSLIDE

### Вложенные парсеры

В строке указывается, что, при вызове парсера ```create_parser```, будет вызвана функция create.
```
create_parser.set_defaults( func=create )
```

Функция create получает как аргумент, все аргументы, которые были переданы.
И, внутри функции, можно обращаться к нужным:
```python
def create(args):
    print("Creating DB {} with DB schema {}".format((args.name, args.schema)))

```

#VSLIDE

### Вложенные парсеры

Если вызвать help для этого скрипта, вывод будет таким:
```
$ python parse_dhcp_snooping.py -h
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} ...

optional arguments:
  -h, --help           show this help message and exit

subcommands:
  valid subcommands

  {create_db,add,get}  description
    create_db          create new db
    add                add data to db
    get                get data from db
```

#VSLIDE

### Вложенные парсеры

Обратите внимание, что каждый вложенный парсер, который создан в скрипте, отображается как команда в подсказке usage:
```
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} ...
```

У каждого вложенного парсера теперь есть свой help:
```
$ python parse_dhcp_snooping.py create_db -h
usage: parse_dhcp_snooping.py create_db [-h] [-n db-filename] [-s SCHEMA]

optional arguments:
  -h, --help      show this help message and exit
  -n db-filename  db filename
  -s SCHEMA       db schema filename
```

Кроме вложенных парсеров, в этом примере также есть несколько новых возможностей argparse.

#VSLIDE

#### metavar

В парсере create_parser используется новый аргумент - ```metavar```:
```python
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
```

#VSLIDE

#### metavar

Аргумент ```metavar``` позволяет указывать имя аргумента для вывода в сообщении usage и help:
```
$ python parse_dhcp_snooping.py create_db -h
usage: parse_dhcp_snooping.py create_db [-h] [-n db-filename] [-s SCHEMA]

optional arguments:
  -h, --help      show this help message and exit
  -n db-filename  db filename
  -s SCHEMA       db schema filename
```

Посмотрите на разницу между опциями ```-n``` и ```-s```:
* после опции ```-n```, и в usage, и в help, указывается имя, которое указано в параметре metavar
* после опции ```-s``` указывается имя переменной, в которую сохраняется значение

#VSLIDE

#### nargs

В парсере add_parser используется ```nargs```:
```python
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
```

```nargs``` позволяет указать, что в этот аргумент должно попасть определенное количество элементов.
В этом случае, все аргументы, которые были переданы скрипту, после имени аргумента ```filename```,
попадут в список nargs.
Но должен быть передан хотя бы один аргумент.

#VSLIDE

#### nargs
Сообщение help, в таком случае, выглядит так:
```
$ python parse_dhcp_snooping.py add -h
usage: parse_dhcp_snooping.py add [-h] [--db DB_FILE] [-s]
                                  filename [filename ...]

positional arguments:
  filename      file(s) to add to db

optional arguments:
  -h, --help    show this help message and exit
  --db DB_FILE  db name
  -s            add switch data if set, else add normal data
```

#VSLIDE

#### nargs

Если передать несколько файлов, они попадут в список.
А, так как функция add, просто выводит имена файлов, вывод получится таким:
```
$ python parse_dhcp_snooping.py add filename test1.txt test2.txt
Reading info from file(s)
filename, test1.txt, test2.txt

Adding data to db dhcp_snooping.db
```

#VSLIDE

#### nargs

```nargs``` поддерживает такие значения:
* ```N``` - должно быть указанное количество аргументов. Аргументы будут в списке (даже, если указан 1)
* ```?``` - 0 или 1 аргумент
* ```*``` - все аргументы попадут в список 
* ```+``` - все аргумнеты попадут в список, но должен быть передан, хотя бы, один аргумент

#VSLIDE

#### choices

В парсере get_parser используется ```choices```:
```python
get_parser.add_argument('-k', dest="key",
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
```

Для некоторых аргументов, важно, чтобы значение было выбрано только из определенных вариантов.
Для таких случаев, можно указывать ```choices```.

#VSLIDE

#### choices

Для этого парсера, help выглядит так:
```
$ python parse_dhcp_snooping.py get -h
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --db DB_FILE          db name
  -k {mac,ip,vlan,interface,switch}
                        host key (parameter) to search
  -v VALUE              value of key
  -a                    show db content
```

#VSLIDE

#### choices

А, если выбрать неправильный вариант:
```
$ python parse_dhcp_snooping.py get -k test
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]
parse_dhcp_snooping.py get: error: argument -k: invalid choice: 'test' (choose from 'mac', 'ip', 'vlan', 'interface', 'switch')
```

#VSLIDE

#### Импорт парсера

В файле parse_dhcp_snooping.py, последние две строки будут выполняться только в том случае, если скрипт был вызван как основной.
```python
if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

А значит, если импортировать файл, эти строки не будут вызваны.

#VSLIDE

#### Импорт парсера

Попробуем импортировать парсер в другой файл (файл call_pds.py):
```python
from parse_dhcp_snooping import parser

args = parser.parse_args()
args.func(args)
```

#VSLIDE

#### Импорт парсера

Вызов сообщения help:
```
$ python call_pds.py -h
usage: call_pds.py [-h] {create_db,add,get} ...

optional arguments:
  -h, --help           show this help message and exit

subcommands:
  valid subcommands

  {create_db,add,get}  description
    create_db          create new db
    add                add data to db
    get                get data from db
```

#VSLIDE

#### Импорт парсера

Вызов аргумента:
```
$ python call_pds.py add test.txt test2.txt
Reading info from file(s)
test.txt, test2.txt

Adding data to db dhcp_snooping.db
```

Всё работает без проблем.

#VSLIDE

#### Передача аргументов вручную

И, последняя особенность argparse - возможность передавать аргументы вручную.

Аргументы можно передать как список, при вызове метода ```parse_args()``` (файл call_pds2.py):
```python
from parse_dhcp_snooping import parser, get

args = parser.parse_args('add test.txt test2.txt'.split())
args.func(args)
```

Необходимо использовать метод split(), так как метод ```parse_args```, ожидает список аргументов.

#VSLIDE

#### Передача аргументов вручную

Результат будет таким, как если бы скрипт был вызван с аргументами:
```
$ python call_pds2.py
Reading info from file(s)
test.txt, test2.txt

Adding data to db dhcp_snooping.db
```

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
$ tree ~/.local/lib/python2.7/site-packages/my_app
├── __init__.py
├── cfg.py
└── switches
    ├── __init__.py
    ├── access.py
    └── sw_cfg_templates.py
```

#VSLIDE

### Python package

Для того чтобы можно было импортировать пакет, его необходимо разместить в одном из каталогов, в котором Python ищет модули или добавить новый путь:
```
In [1]: import sys

In [2]: sys.path
Out[2]: 
['',
 '/usr/local/bin',
 '/usr/lib/python2.7',
 '/usr/lib/python2.7/plat-i386-linux-gnu',
 '/usr/lib/python2.7/lib-tk',
 '/usr/lib/python2.7/lib-old',
 '/usr/lib/python2.7/lib-dynload',
 '/usr/local/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages/gst-0.10',
 '/usr/lib/python2.7/dist-packages/gtk-2.0',
 '/usr/lib/pymodules/python2.7',
 '/usr/local/lib/python2.7/dist-packages/IPython/extensions',
 '/home/nata/.ipython']
```


#VSLIDE

### Python package

Для своих пакетов можно использовать каталог:
```
$ python -m site --user-site
/home/nata/.local/lib/python2.7/site-packages
```

После того как каталог будет создан, он автоматически будет добавлен в пути поиска модулей:
```
$ mkdir -p /home/nata/.local/lib/python2.7/site-packages
```

#VSLIDE
### Python package

```
In [1]: import sys

In [2]: sys.path
Out[2]: 
['',
 '/usr/local/bin',
 '/usr/lib/python2.7',
 '/usr/lib/python2.7/plat-i386-linux-gnu',
 '/usr/lib/python2.7/lib-tk',
 '/usr/lib/python2.7/lib-old',
 '/usr/lib/python2.7/lib-dynload',
 '/home/nata/.local/lib/python2.7/site-packages',
 '/usr/local/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages/gst-0.10',
 '/usr/lib/python2.7/dist-packages/gtk-2.0',
 '/usr/lib/pymodules/python2.7',
 '/usr/local/lib/python2.7/dist-packages/IPython/extensions',
 '/home/nata/.ipython']
```

#VSLIDE

### Python package

Структура пакета my_app:
```
$ tree ~/.local/lib/python2.7/site-packages/my_app
├── __init__.py
├── cfg.py
└── switches
    ├── __init__.py
    ├── access.py
    └── sw_cfg_templates.py
```

Файлы __init__.py пустые.

#VSLIDE

### Python package

Файл cfg.py:
```python
def config_to_list(cfg_file, delete_excl=True,
                   delete_empty=True, strip_end=True):
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if strip_end:
                line = line.rstrip()
            if delete_empty and not line:
                pass
            elif delete_excl and line.startswith('!'):
                pass
            else:
                result.append(line)
    return result

def clear_cfg_and_write_to_file(cfg, to_file, **kwargs):
    cfg_as_list = config_to_list(cfg, **kwargs)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))
```

#VSLIDE

### Python package

Файл switches/access.py:
```python
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']


def generate_access_cfg(sw_dict):
    result = []
    for intf in sw_dict['access']:
        result.append('interface FastEthernet %s' % intf)
        for command in sw_int_templates.access_template:
            if command.endswith('access vlan'):
                result.append(' %s %s' % (command, sw_dict['access'][intf]))
            else:
                result.append(' %s' % command)
    return result
```

#VSLIDE

### Python package

Файл switches/sw_cfg_templates.py:
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

### Python package

Импорт модулей/функций из пакета:
```python
In [5]: import my_app.cfg

In [6]: dir(my_app.cfg)
Out[6]: 
['__builtins__',
 '__doc__',
 '__file__',
 '__name__',
 '__package__',
 'clear_cfg_and_write_to_file',
 'config_to_list']
```


#VSLIDE

### Python package

```
In [5]: import my_app.cfg

In [6]: dir(my_app.cfg)
Out[6]: 
['__builtins__',
 '__doc__',
 '__file__',
 '__name__',
 '__package__',
 'clear_cfg_and_write_to_file',
 'config_to_list']

In [7]: my_app.cfg.config_to_list
Out[7]: <function my_app.cfg.config_to_list>
```

#VSLIDE

### Python package

```
In [13]: import my_app.switches.access as sw_access

In [14]: sw_access.access_template
Out[14]: 
['switchport mode access',
 'switchport access vlan',
 'spanning-tree portfast',
 'spanning-tree bpduguard enable']

In [15]: sw_access.generate_access_cfg
Out[15]: <function my_app.switches.access.generate_access_cfg>
```
