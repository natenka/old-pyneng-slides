# Python для сетевых инженеров 

---
## Параллельные сессии

+++
### Параллельные сессии

Когда нужно опросить много устройств, выполнение подключений поочередно, будет достаточно долгим.
Конечно, это будет быстрее, чем подключение вручную.
Но, хотелось бы получать отклик как можно быстрее.

Для параллельного подключения к устройствам в курсе используются модули:
* threading
* multiprocessing
* concurrent.futures

+++
### Измерение времени выполнения скрипта

Для оценки времени выполнения скрипта есть несколько вариантов.
В курсе используются самые простые варианты:
* утилиту Linux time
* и модуль Python datetime

При оценке времени выполнения скрипта, в данном случае, не важна высокая точность. 
Главное, сравнить время выполнения скрипта в разных вариантах.

+++
### ```time```

Утилита time в Linux позволяет замерить время выполнения скрипта. Например:
```
$ time python thread_paramiko.py
...
real    0m4.712s
user    0m0.336s
sys     0m0.064s
```

Для использования утилиты time достаточно написать time перед строкой запуска скрипта.

+++
### ```datetime```

Второй вариант - модуль datetime.
Этот модуль позволяет работать с временем и датами в Python.

Пример использования:
```python
from datetime import datetime
import time

start_time = datetime.now()

#Тут выполняются действия
time.sleep(5)

print(datetime.now() - start_time)
```

+++
### ```datetime```

Результат выполнения:
```
$ python test.py
0:00:05.004949
```

---
## Процессы и потоки в Python (CPython)

* процесс (process) - это, грубо говоря, запущенная программа. Процессу выделяются отдельные ресурсы: память, процессорное время
* поток (thread) - это единица исполнения в процессе. Потоки разделяют ресурсы процесса, к которому они относятся.

+++
### Процессы и потоки в Python (CPython)

Python (а точнее, CPython - реализация, которая используется в курсе) оптимизирован для работы в однопоточном режиме. Это хорошо, если в программе используется только один поток.

И, в то же время, у Python есть определенные нюансы работы в многопоточном режиме. Связаны они с тем, что CPython использует GIL (global interpreter lock).

+++
### GIL

GIL не дает нескольким потокам исполнять одновременно код Python.
GIL можно представить как некий переходящий флаг, который разрешает потокам выполняться.
У кого флаг, тот может выполнять работу.

Флаг передается либо каждые сколько-то инструкций Python, либо, например, когда выполняются какие-то операции ввода-вывода.

Поэтому получается, что разные потоки не будут выполняться параллельно, а программа просто будет между ними переключаться, выполняя их в разное время.

+++
### IO bound task

Но не всё так плохо. Если в программе есть некое "ожидание": пакетов из сети, запроса пользователя, пауза типа sleep - то в такой программе потоки будут выполняться как будто параллельно.
А всё потому, что во время таких пауз флаг (GIL) можно передать другому потоку.

Но тут также нужно быть осторожным, так как такой результат может наблюдаться на небольшом количестве сессий, но может ухудшиться с ростом количества сессий.

Потоки отлично подходят для задач, которые связаны с операциями ввода-вывода.
Подключение к оборудованию входит в число подобных задач.


+++
### Процессы

Процессы позволяют выполнять задачи на разных ядрах компьютера.
Это важно для задач, которые не завязаны на операции ввода-вывода.

Для каждого процесса создается своя копия ресурсов, выделяется память, у каждого процесса свой GIL.
Это же делает процессы более тяжеловесными, по сравнению с потоками.

Кроме того, количество процессов, которые запускаются параллельно, зависит от количества ядер и CPU и обычно исчисляется в десятках, тогда как количество потоков для операций ввода-вывода может исчисляться в сотнях.


---

## Модуль threading

+++
### Модуль threading

Модуль threading может быть полезен для таких задач:
* фоновое выполнение каких-то задач:
 * например, отправка почты во время ожидания ответа от пользователя
* параллельное выполнение задач связанных с вводом/выводом
 * ожидание ввода от пользователя
 * чтение/запись файлов
* задачи, где присутствуют паузы:
 * например, паузы с помощью sleep

+++
### Модуль threading

Следует учитывать, что в ситуациях, когда требуется повышение производительности, засчет использования нескольких процессоров или ядер, нужно использовать модуль multiprocessing, а не модуль threading.

Рассмотрим пример использования модуля threading вместе с последним примером с netmiko.

Так как для работы с threading, удобнее использовать функции, код изменен:
* код подключения по SSH перенесен в функцию
* параметры устройств перенесены в отдельный файл в формате YAML

+++
### Модуль threading

Файл netmiko_function.py:
```python
from netmiko import ConnectHandler
import sys
import yaml

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command):

    print("Connection to device {}".format( device_dict['ip'] ))

    ssh = ConnectHandler(**device_dict)
    ssh.enable()

    result = ssh.send_command(command)
    print(result)

for router in devices['routers']:
    connect_ssh(router, COMMAND)
```

+++
### Модуль threading

Файл devices.yaml с параметрами подключения к устройствам:
```yaml
routers:
- device_type: cisco_ios
  ip: 192.168.100.1
  username: cisco
  password: cisco
  secret: cisco
- device_type: cisco_ios
  ip: 192.168.100.2
  username: cisco
  password: cisco
  secret: cisco
- device_type: cisco_ios
  ip: 192.168.100.3
  username: cisco
  password: cisco
  secret: cisco
```

+++
### Модуль threading

Время выполнения скрипта (вывод скрипта удален):
```
$ time python netmiko_function.py "sh ip int br"
...
real    0m6.189s
user    0m0.336s
sys     0m0.080s
```

+++
### Модуль threading

Пример использования модуля threading для подключения по SSH с помощью netmiko (файл netmiko_threading.py):
```python
from netmiko import ConnectHandler
import sys
import yaml
import threading

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)

    print("Connection to device {}".format( device_dict['ip'] ))
    print(result)
```

+++
### Модуль threading

Файл netmiko_threading.py:
```python

def conn_threads(function, devices, command):
    threads = []
    for device in devices:
        th = threading.Thread(target = function, args = (device, command))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

conn_threads(connect_ssh, devices['routers'], COMMAND)
```

+++
### Модуль threading

Время выполнения кода:
```
$ time python netmiko_function_threading.py "sh ip int br"

...
real    0m2.229s
user    0m0.408s
sys     0m0.068s
```

Время почти в три раза меньше.
Но, надо учесть, что такая ситуация не будет повторяться при большом количестве подключений.

+++
### Модуль threading

* ```threading.Thread``` - класс, который создает поток. Ему передается функция, которую надо выполнить, и её аргументы
* ```th.start()``` - запуск потока
* ```threads.append(th)``` - поток добавляется в список
* ```th.join()``` - метод ожидает завершения работы потока. Метод join выполняется для каждого потока в списке. Таким образом основная программа завершится только когда завершат работу все потоки
 * по умолчанию, ```join``` ждет завершения работы потока бесконечно. Но, можно ограничить время ожидания передав ```join``` время в секундах. В таком случае, ```join``` завершится после указанного количества секунд.


+++
### Получение данных из потоков

В предыдущем примере, данные выводились на стандартный поток вывода.
Для полноценной работы с потоками, необходимо также научиться получать данные из потоков.
Чаще всего, для этого используется очередь.

Очередь - это структура данных, которая используется и в работе с сетевым оборудованием. Объект queue.Queue() - это FIFO очередь.

+++
### Получение данных из потоков

В Python есть модуль queue, который позволяет создавать разные типы очередей.

Очередь передается как аргумент в функцию connect_ssh, которая подключается к устройству по SSH. Результат выполнения команды добавляется в очередь.

+++
### Получение данных из потоков

Пример использования потоков с получением данных (файл netmiko_threading_data.py):
```python
# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
import sys
import yaml
import threading
from queue import Queue

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)
    print("Connection to device {}".format( device_dict['ip'] ))

    #Добавляем словарь в очередь
    queue.put({ device_dict['ip']: result })
```

+++
### Получение данных из потоков

Файл netmiko_threading_data.py:
```python

def conn_threads(function, devices, command):
    threads = []
    q = Queue()

    for device in devices:
        # Передаем очередь как аргумент, функции
        th = threading.Thread(target = function, args = (device, command, q))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    results = []
    # Берем результаты из очереди и добавляем их в список results
    for t in threads:
        results.append(q.get())

    return results

print(conn_threads(connect_ssh, devices['routers'], COMMAND))
```

+++
### Получение данных из потоков

Обратите внимание, что в функции connect_ssh добавился аргумент queue.

Очередь вполне можно воспринимать как список:
* метод ```queue.put()``` равнозначен ```list.append()```
* метод ```queue.get()``` равнозначен ```list.pop(0)```

Для работы с потоками и модулем threading, лучше использовать очередь.
Но, конкретно в данном примере, можно было бы использовать и список.

+++
### Получение данных из потоков

Пример со списком, скорее всего, будет проще понять. Поэтому ниже аналогичный код, но с использованием обычного списка, вместо очереди (файл netmiko_threading_data_list.py):
```python
# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
import sys
import yaml
import threading

COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)
    print("Connection to device {}".format( device_dict['ip'] ))

    #Добавляем словарь в список
    queue.append({ device_dict['ip']: result })
```

+++
### Получение данных из потоков

Файл netmiko_threading_data_list.py:
```python

def conn_threads(function, devices, command):
    threads = []
    q = []

    for device in devices:
        # Передаем список как аргумент, функции
        th = threading.Thread(target = function, args = (device, command, q))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # Эта часть нам не нужна, так как, при использовании списка,
    # мы просто можем вернуть его
    #results = []
    #for t in threads:
    #    results.append(q.get())

    return q

print(conn_threads(connect_ssh, devices['routers'], COMMAND))
```

---
## Модуль multiprocessing

+++
### Модуль multiprocessing

Модуль multiprocessing использует интерфейс подобный модулю threading.
Поэтому перенести код с использования потоков на использование процессов, обычно, достаточно легко.

Каждому процессу выделяются свои ресурсы.
Кроме того, у каждого процесса свой GIL, а значит, нет тех проблем, которые были с потоками и код может выполняться параллельно и задействовать ядра/процессоры компьютера.

+++
### Модуль multiprocessing

Пример использования модуля multiprocessing (файл netmiko_multiprocessing.py):
```python
import multiprocessing
from netmiko import ConnectHandler
import sys
import yaml


COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, command, queue):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)

    print("Connection to device {}".format( device_dict['ip'] ))
    queue.put({device_dict['ip']: result})
```

+++
### Модуль multiprocessing

Файл netmiko_multiprocessing.py:
```python

def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target = function, args = (device, command, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append(queue.get())

    return results

print(( conn_processes(connect_ssh, devices['routers'], COMMAND) ))
```

+++
### Модуль multiprocessing

Обратите внимание, что этот пример аналогичен последнему примеру, который использовался с модулем threading.
Единственное отличие в том, что в модуле multiprocessing есть своя реализация очереди, поэтому нет необходимости использовать модуль queue.

+++
### Модуль multiprocessing

Если проверить время исполнения этого скрипта, аналогичного для модуля threading и последовательного подключения, то получаем такую картину:
```
последовательное: 5.833s
threading:        2.225s
multiprocessing:  2.365s
```

+++
### Модуль multiprocessing

Время выполнения для модуля multiprocessing немного больше.
Но это связано с тем, что на создание процессов уходит больше времени, чем на создание потоков.
Если бы скрипт был сложнее и выполнялось больше задач, или было бы больше подключений, тогда бы multiprocessing начал бы существенно выигрывать у модуля threading.



