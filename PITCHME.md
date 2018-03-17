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
### Количество потоков

+++
## Одна команда

```
Количество устройств: 40
########## Последовательное выполнение ###########
0:05:03.249943
```

+++
### Тест 1. От 5 до 30 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 5 потоков ####################
0:01:03.416216
################### 10 потоков ###################
0:00:36.339131
################### 15 потоков ###################
0:00:28.748473
################### 20 потоков ###################
0:00:20.728099
################### 25 потоков ###################
0:00:20.889887
################### 30 потоков ###################
0:00:19.441675
```

+++
### Тест 2. От 20 до 40 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 20 потоков ###################
0:00:22.222185
################### 25 потоков ###################
0:00:20.248397
################### 30 потоков ###################
0:00:19.714420
################### 35 потоков ###################
0:00:18.888092
################### 40 потоков ###################
0:00:15.560998
```

+++
### Тест 3. От 20 до 50 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 20 потоков ###################
0:00:21.915024
################### 25 потоков ###################
0:00:20.560245
################### 30 потоков ###################
0:00:21.018879
################### 35 потоков ###################
0:00:18.808900
################### 40 потоков ###################
0:00:15.508909
################### 45 потоков ###################
0:00:15.561980
################### 50 потоков ###################
0:00:15.594148
```

+++
### Тест 4. От 40 до 100 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 40 потоков ###################
0:00:15.459810
################### 45 потоков ###################
0:00:15.559053
################### 50 потоков ###################
0:00:15.492092
################### 55 потоков ###################
0:00:15.535447
################### 60 потоков ###################
0:00:15.618027
################### 65 потоков ###################
0:00:15.610531
################### 70 потоков ###################
0:00:15.468397
################### 75 потоков ###################
0:00:15.520221
################### 80 потоков ###################
0:00:15.676777
################### 85 потоков ###################
0:00:15.412259
################### 90 потоков ###################
0:00:15.624427
################### 95 потоков ###################
0:00:15.460216
################## 100 потоков ###################
0:00:15.949646

```


+++
### Тест 5. От 100 до 200 потоков с шагом 10

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################## 100 потоков ###################
0:00:15.926021
################## 110 потоков ###################
0:00:15.820079
################## 120 потоков ###################
0:00:15.786823
################## 130 потоков ###################
0:00:15.810952
################## 140 потоков ###################
0:00:15.978455
################## 150 потоков ###################
0:00:15.747290
################## 160 потоков ###################
0:00:15.567023
################## 170 потоков ###################
0:00:15.731518
################## 180 потоков ###################
0:00:15.757106
################## 190 потоков ###################
0:00:16.078069
################## 200 потоков ###################
0:00:15.671120
```


+++
## Пять команд

```
Количество устройств: 40
########## Последовательное выполнение ###########
0:06:39.209494
```

+++
### Тест 1. От 1 до 5 потоков с шагом 1

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 1 потоков ####################
0:06:39.209494
################### 2 потоков ####################
0:03:20.323560
################### 3 потоков ####################
0:02:19.811905
################### 4 потоков ####################
0:01:42.125918
################### 5 потоков ####################
0:01:23.594863
```

+++
### Тест 2. От 5 до 40 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 5 потоков ####################
0:01:23.243076
################### 10 потоков ###################
0:00:45.570973
################### 15 потоков ###################
0:00:35.691461
################### 20 потоков ###################
0:00:28.726146
################### 25 потоков ###################
0:00:26.849497
################### 30 потоков ###################
0:00:25.368939
################### 35 потоков ###################
0:00:24.468013
################### 40 потоков ###################
0:00:20.721652
```

+++
### Тест 3. От 40 до 100 потоков с шагом 5

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################### 40 потоков ###################
0:00:18.520967
################### 45 потоков ###################
0:00:20.108423
################### 50 потоков ###################
0:00:18.739881
################### 55 потоков ###################
0:00:18.540936
################### 60 потоков ###################
0:00:19.505306
################### 65 потоков ###################
0:00:20.483919
################### 70 потоков ###################
0:00:19.220402
################### 75 потоков ###################
0:00:20.086475
################### 80 потоков ###################
0:00:19.838017
################### 85 потоков ###################
0:00:19.417624
################### 90 потоков ###################
0:00:19.129760
################### 95 потоков ###################
0:00:20.934856
################## 100 потоков ###################
0:00:21.002833

```


+++
### Тест 4. От 100 до 200 потоков с шагом 10

```
$ python netmiko_threads_submit_count.py
Количество устройств: 40
################## 100 потоков ###################
0:00:20.575740
################## 110 потоков ###################
0:00:18.942644
################## 120 потоков ###################
0:00:18.519601
################## 130 потоков ###################
0:00:19.400769
################## 140 потоков ###################
0:00:19.524433
################## 150 потоков ###################
0:00:19.242951
################## 160 потоков ###################
0:00:19.077351
################## 170 потоков ###################
0:00:20.738970
################## 180 потоков ###################
0:00:20.350205
################## 190 потоков ###################
0:00:18.588683
################## 200 потоков ###################
0:00:18.729154

```


---
## Модуль concurrent.futures

Модуль concurrent.futures предоставляет высокоуровневый интерфейс для работы с процессами и потоками.
При этом и для потоков, и для процессов используется одинаковый интерфейс, что позволяет легко переключаться между ними.

Если сравнивать этот модуль с threading или multiprocessing, то у него меньше возможностей.
Но зато с concurrent.futures работать проще и интерфейс более понятный.

+++
### Модуль concurrent.futures

Модуль concurrent.futures позволяет легко решить задачу запуска нескольких потоков/процессов и получения из них данных.

Модуль предоставляет два класса:

* **ThreadPoolExecutor** - для работы с потоками
* **ProcessPoolExecutor** - для работы с процессами


Оба класса используют одинаковый интерфейс, поэтому достаточно разобраться с одним и затем просто переключиться на другой при необходимости.

+++
## Future

Модуль использует понятие future.
[Future](https://en.wikipedia.org/wiki/Futures_and_promises) - это объект, который представляет отложенное вычисление.
Этот объект можно запрашивать о состоянии (завершена работа или нет), можно получать результаты или исключения, которые возникли в процессе работы, по мере возникновения.

При этом нет необходимости создавать их вручную.
Эти объекты создаются ThreadPoolExecutor и ProcessPoolExecutor.

+++
### Метод map

Метод map - это самый простой вариант работы с concurrent.futures.

Пример использования функции map с ThreadPoolExecutor (файл netmiko_threads_map_ver1.py):
```python
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

import yaml
from netmiko import ConnectHandler


def connect_ssh(device_dict, command='sh clock'):
    print('Connection to device: {}'.format(device_dict['ip']))
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return {device_dict['ip']: result}


def threads_conn(function, devices, limit=2):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
    return list(f_result)


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh, devices['routers'])
    pprint(all_done)

```


+++
### Метод map

```python
def threads_conn(function, devices, limit=2):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
    return list(f_result)
```

Обратите внимание, что функция занимает всего 4 строки, и для получения данных не надо создавать очередь и передавать ее в функцию connect_ssh.

+++
### Метод map

* ```with ThreadPoolExecutor(max_workers=limit) as executor:``` - класс ThreadPoolExecutor инициируется в блоке with с указанием количества потоков
* ```f_result = executor.map(function, devices)``` - метод map похож на функцию map, но тут функция function вызывается в разных потоках. При этом в разных потоках функция будет вызываться с разными аргументами - элементами итерируемого объекта devices.
* метод map возвращает генератор. В этом генераторе содержатся результаты выполнения функций

+++
### Метод map

Результат выполнения:
```
$ python netmiko_threads_map_ver1.py
Connection to device: 192.168.100.1
Connection to device: 192.168.100.2
Connection to device: 192.168.100.3
[{'192.168.100.1': '*04:43:01.629 UTC Mon Aug 28 2017'},
 {'192.168.100.2': '*04:43:01.648 UTC Mon Aug 28 2017'},
 {'192.168.100.3': '*04:43:07.291 UTC Mon Aug 28 2017'}]

```

+++
### Метод map

Важная особенность метода map - он возвращает результаты в том же порядке, в котором они указаны в итерируемом объекте.

Для демонстрации этой особенности в функции connect_ssh добавлены сообщения с выводом информации о том, когда функция начала работать и когда закончила.

+++
### Метод map

Файл netmiko_threads_map_ver2.py:
```python
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from datetime import datetime
import time

import yaml
from netmiko import ConnectHandler


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'
```

+++
### Метод map

```python
def connect_ssh(device_dict, command='sh clock'):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}


def threads_conn(function, devices, limit=2):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
    return list(f_result)


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh, devices['routers'])
    pprint(all_done)

```

+++
### Метод map

Результат выполнения:
```
$ python netmiko_threads_map_ver2.py
===> 04:50:50.175076 Connection to device: 192.168.100.1
===> 04:50:50.175553 Connection to device: 192.168.100.2
<=== 04:50:55.582707 Received result from device: 192.168.100.2
===> 04:50:55.689248 Connection to device: 192.168.100.3
<=== 04:51:01.135640 Received result from device: 192.168.100.3
<=== 04:51:05.568037 Received result from device: 192.168.100.1
[{'192.168.100.1': '*04:51:05.395 UTC Mon Aug 28 2017'},
 {'192.168.100.2': '*04:50:55.411 UTC Mon Aug 28 2017'},
 {'192.168.100.3': '*04:51:00.964 UTC Mon Aug 28 2017'}]
```

+++
### Метод map

Обратите внимание на фактический порядок выполнения задач: 192.168.100.2, 192.168.100.3, 192.168.100.1.
Но в итоговом списке все равно соблюдается порядок на основе списка devices['routers'].

+++
### Метод map

Еще один момент, который тут хорошо заметен, это то, что как только одна задача выполнилась, сразу берется следующая.
То есть, ограничение в два потока влияет на количество потоков, которые выполняются одновременно.

+++
### Метод map

Осталось изменить функцию таким образом, чтобы ей можно было передавать команду как аргумент.

Для этого мы воспользуемся функцией repeat из модуля itertools.
Функция repeat тут нужна для того, чтобы команда передавалась при каждом вызове функции connect_ssh.

+++
### Метод map

Файл netmiko_threads_map_final.py

```python
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'
```

+++
### Метод map

Файл netmiko_threads_map_final.py
```python
def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}



def threads_conn(function, devices, limit=2, command=''):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(command))
    return list(f_result)


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

```

+++
### Метод map

Результат выполнения:
```
$ python netmiko_threads_map_final.py
===> 05:01:08.314962 Connection to device: 192.168.100.1
===> 05:01:08.315114 Connection to device: 192.168.100.2
<=== 05:01:13.693083 Received result from device: 192.168.100.2
===> 05:01:13.799002 Connection to device: 192.168.100.3
<=== 05:01:19.363250 Received result from device: 192.168.100.3
<=== 05:01:23.685859 Received result from device: 192.168.100.1
[{'192.168.100.1': '*05:01:23.513 UTC Mon Aug 28 2017'},
 {'192.168.100.2': '*05:01:13.522 UTC Mon Aug 28 2017'},
 {'192.168.100.3': '*05:01:19.189 UTC Mon Aug 28 2017'}]
```

+++
### Использование ProcessPoolExecutor с map

Для того чтобы предыдущий пример использовал процессы вместо потоков, достаточно сменить ThreadPoolExecutor на ProcessPoolExecutor:
```python
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'
```

+++
### Использование ProcessPoolExecutor с map

```python
def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}



def threads_conn(function, devices, limit=2, command=''):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(command))
    return list(f_result)


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

```

+++
### Использование ProcessPoolExecutor с map

Результат выполнения:
```
$ python netmiko_processes_map_final.py
===> 05:26:42.974505 Connection to device: 192.168.100.1
===> 05:26:42.975733 Connection to device: 192.168.100.2
<=== 05:26:48.389420 Received result from device: 192.168.100.2
===> 05:26:48.495598 Connection to device: 192.168.100.3
<=== 05:26:54.104585 Received result from device: 192.168.100.3
<=== 05:26:58.367981 Received result from device: 192.168.100.1
[{'192.168.100.1': '*05:26:58.195 UTC Mon Aug 28 2017'},
 {'192.168.100.2': '*05:26:48.218 UTC Mon Aug 28 2017'},
 {'192.168.100.3': '*05:26:53.932 UTC Mon Aug 28 2017'}]
```

---
## Метод submit и работа с futures


+++
### Метод submit и работа с futures

При использовании метода map объект future использовался внутри, но в итоге мы получали уже готовый результат функции.

Метод submit позволяет запускать future, а функция as_completed, которая ожидает как аргумент итерируемый объект с futures и возвращает future по мере завершения.
В этом случае порядок не будет соблюдаться, как с map.

+++
### Метод submit и работа с futures

Файл netmiko_threads_submit.py:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'
```

+++
### Метод submit и работа с futures

```python
def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}
```

+++
### Метод submit и работа с futures

Теперь функция threads_conn выглядит немного по-другому:
```python
def threads_conn(function, devices, limit=2, command=''):
    all_results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            all_results.append(f.result())
    return all_results


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)
```

+++
### Метод submit и работа с futures

Остальной код не изменился, поэтому разобраться надо только с функцией threads_conn:
```python
def threads_conn(function, devices, limit=2, command=''):
    all_results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            all_results.append(f.result())
    return all_results
```

+++
### Метод submit и работа с futures

В блоке with два цикла:
* ```future_ssh``` - это список объектов future, который создается с помощью list comprehensions
* для создания future используется функция submit
  * ей как аргументы передаются: имя функции, которую надо выполнить, и ее аргументы
* следующий цикл проходится по списку future с помощью функции as_completed. Эта функция возвращает future только когда они завершили работу или были отменены. При этом future возвращаются по мере завершения работы

+++
### Метод submit и работа с futures

Результат выполнения:
```
$ python netmiko_threads_submit.py
===> 06:02:14.582011 Connection to device: 192.168.100.1
===> 06:02:14.582155 Connection to device: 192.168.100.2
<=== 06:02:20.155865 Received result from device: 192.168.100.2
===> 06:02:20.262584 Connection to device: 192.168.100.3
<=== 06:02:25.864270 Received result from device: 192.168.100.3
<=== 06:02:29.962225 Received result from device: 192.168.100.1
[{'192.168.100.2': '*06:02:19.983 UTC Mon Aug 28 2017'},
 {'192.168.100.3': '*06:02:25.691 UTC Mon Aug 28 2017'},
 {'192.168.100.1': '*06:02:29.789 UTC Mon Aug 28 2017'}]

```

Обратите внимание, что порядок не сохраняется и зависит от того, какие функции раньше завершили работу.


---
### Обработка исключений

+++
### Обработка исключений

Если при выполнении функции возникло исключение, оно будет сгенерировано при получении результата

Например, в файле devices.yaml пароль для устройства 192.168.100.2 изменен на неправильный:
```
$ python netmiko_threads_submit.py
===> 06:29:40.871851 Connection to device: 192.168.100.1
===> 06:29:40.872888 Connection to device: 192.168.100.2
===> 06:29:43.571296 Connection to device: 192.168.100.3
<=== 06:29:48.921702 Received result from device: 192.168.100.3
<=== 06:29:56.269284 Received result from device: 192.168.100.1
Traceback (most recent call last):
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/netmiko/base_connection.py", line 491, in establish_connection
    self.remote_conn_pre.connect(**ssh_connect_params)
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/paramiko/client.py", line 394, in connect
    look_for_keys, gss_auth, gss_kex, gss_deleg_creds, gss_host)
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/paramiko/client.py", line 649, in _auth
    raise saved_exception
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/paramiko/client.py", line 636, in _auth
    self._transport.auth_password(username, password)
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/paramiko/transport.py", line 1329, in auth_password
    return self.auth_handler.wait_for_response(my_event)
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/paramiko/auth_handler.py", line 217, in wait_for_response
    raise e
paramiko.ssh_exception.AuthenticationException: Authentication failed.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "netmiko_threads_submit.py", line 40, in <module>
    command='sh clock')
  File "netmiko_threads_submit.py", line 32, in threads_conn
    all_results.append(f.result())
  File "/usr/local/lib/python3.6/concurrent/futures/_base.py", line 398, in result
    return self.__get_result()
  File "/usr/local/lib/python3.6/concurrent/futures/_base.py", line 357, in __get_result
    raise self._exception
  File "/usr/local/lib/python3.6/concurrent/futures/thread.py", line 55, in run
    result = self.fn(*self.args, **self.kwargs)
  File "netmiko_threads_submit.py", line 19, in connect_ssh
    with ConnectHandler(**device_dict) as ssh:
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/netmiko/ssh_dispatcher.py", line 122, in ConnectHandler
    return ConnectionClass(*args, **kwargs)
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/netmiko/base_connection.py", line 145, in __init__
    self.establish_connection()
  File "/home/vagrant/venv/py3_convert/lib/python3.6/site-packages/netmiko/base_connection.py", line 500, in establish_connection
    raise NetMikoAuthenticationException(msg)
netmiko.ssh_exception.NetMikoAuthenticationException: Authentication failure: unable to connect cisco_ios 192.168.100.2:22
Authentication failed.
```

+++
### Обработка исключений

Так как исключение возникает при получении результата, легко добавить обработку исключений (файл netmiko_threads_submit_exception.py):
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'


def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}
```

+++
### Обработка исключений

```python
def threads_conn(function, devices, limit=2, command=''):
    all_results = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            try:
                result = f.result()
            except NetMikoAuthenticationException as e:
                print(e)
            else:
                all_results.update(result)
    return all_results


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = threads_conn(connect_ssh,
                            devices['routers'],
                            command='sh clock')
    pprint(all_done)

```

+++
### Обработка исключений

Результат выполнения:
```
$ python netmiko_threads_submit_exception.py
===> 06:45:56.327892 Connection to device: 192.168.100.1
===> 06:45:56.328190 Connection to device: 192.168.100.2
===> 06:45:58.964806 Connection to device: 192.168.100.3
Authentication failure: unable to connect cisco_ios 192.168.100.2:22
Authentication failed.
<=== 06:46:04.325812 Received result from device: 192.168.100.3
<=== 06:46:11.731541 Received result from device: 192.168.100.1
{'192.168.100.1': '*06:46:11.556 UTC Mon Aug 28 2017',
 '192.168.100.3': '*06:46:04.154 UTC Mon Aug 28 2017'}
```


+++
### ProcessPoolExecutor

Так как все работает аналогичным образом и для процессов, тут приведет последний вариант (файл netmiko_processes_submit_exception.py):
```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException


start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'


def connect_ssh(device_dict, command):
    print(start_msg.format(datetime.now().time(), device_dict['ip']))
    if device_dict['ip'] == '192.168.100.1':
        time.sleep(10)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        print(received_msg.format(datetime.now().time(), device_dict['ip']))
    return {device_dict['ip']: result}
```

+++
### ProcessPoolExecutor

```python
def processes_conn(function, devices, limit=2, command=''):
    all_results = {}
    with ProcessPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            try:
                result = f.result()
            except NetMikoAuthenticationException as e:
                print(e)
            else:
                all_results.update(result)
    return all_results


if __name__ == '__main__':
    devices = yaml.load(open('devices.yaml'))
    all_done = processes_conn(connect_ssh,
                              devices['routers'],
                              command='sh clock')
    pprint(all_done)

```

+++
### ProcessPoolExecutor

Результат выполнения:
```
$ python netmiko_processes_submit_exception.py
===> 06:40:43.828249 Connection to device: 192.168.100.1
===> 06:40:43.828664 Connection to device: 192.168.100.2
Authentication failure: unable to connect cisco_ios 192.168.100.2:22
Authentication failed.
===> 06:40:46.292613 Connection to device: 192.168.100.3
<=== 06:40:51.890816 Received result from device: 192.168.100.3
<=== 06:40:59.231330 Received result from device: 192.168.100.1
{'192.168.100.1': '*06:40:59.056 UTC Mon Aug 28 2017',
 '192.168.100.3': '*06:40:51.719 UTC Mon Aug 28 2017'}
```

