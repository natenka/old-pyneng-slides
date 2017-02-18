# Python для сетевых инженеров 


#HSLIDE

## Основы Python

#HSLIDE

### Синтаксис Python

Отступы имеют значение:
* они определяют какие выражения попадают в блок кода
* когда блок кода заканчивается

Tab или пробел:
* лучше использовать пробелы (настроить редактор)
* количество пробелов должно быть одинаковым в одном блоке:
 * лучше во всем коде
 * обычно используются 2-4 пробела (в курсе используются 4 пробела)

#HSLIDE

### Синтаксис Python

```python
a = 10
b = 5

if a > b:
    print "A больше B"
    print a - b
else:
    print "B больше или равно A"
    print b - a

print "The End"

def open_file( filename ):
    print "Reading file", filename
    with open(filename) as f:
        return f.read()
        print "Done"
```

#HSLIDE

### Комментарии

Однострочный комментарий:
```python
#Очень важный комментарий
a = 10
b = 5 #Очень нужный комментарий
```

Многострочный комментарий:
```python
"""
Очень важный
и длинный комментарий
"""
a = 10
b = 5
```

#HSLIDE

### Интерпретатор IPython

```python
In [1]: 1 + 2
Out[1]: 3

In [2]: 22*45
Out[2]: 990

In [3]: 2**3
Out[3]: 8

In [4]: print 'Hello!'
Hello!
```

#HSLIDE

### Интерпретатор IPython

```python
In [5]: for i in range(5):
   ...:     print i
   ...:     
0
1
2
3
4
```

#HSLIDE

### Интерпретатор IPython

Оператор print
```python
In [6]: print 'Hello!'
Hello!

In [7]: print 5*5
25

In [8]: print 1*5, 2*5, 3*5, 4*5
5 10 15 20

In [9]: print 'one', 'two', 'three'
one two three
```

#HSLIDE

## Типы данных в Python

#HSLIDE

### Типы данных в Python

В Python есть несколько стандартных типов данных:
* Numbers (числа)
* Strings (строки)
* Lists (списки)
* Dictionary (словари)
* Tuples (кортежи)
* Sets (множества)
* Boolean

#HSLIDE

### Типы данных в Python

* Изменяемые:
 * Списки
 * Словари
 * Множества
* Неизменяемые
 * Числа
 * Строки
 * Кортежи

#HSLIDE

### Типы данных в Python

* Упорядоченные:
 * Списки
 * Кортежи
 * Строки
* Неупорядоченные:
 * Словари
 * Множества

#HSLIDE

### Числа

Пример различных типов числовых значений:
* int (40, -80)
* float (1.5, -30.7)

```python
In [1]: 1 + 2
Out[1]: 3

In [2]: 1.0 + 2
Out[2]: 3.0

In [3]: 10 - 4
Out[3]: 6

In [4]: 2**3
Out[4]: 8
```

#VSLIDE

###Числа

Отличия деления int и float:
```python
In [5]: 10/3
Out[5]: 3

In [6]: 10/3.0
Out[6]: 3.3333333333333335

In [7]: 10 / float(3)
Out[7]: 3.3333333333333335

In [8]: float(10) / 3
Out[8]: 3.3333333333333335
```

С помощью функции round можно округлять числа до нужного количества знаков:
```python
In [9]: round(10/3.0, 2)
Out[9]: 3.33

In [10]: round(10/3.0, 4)
Out[10]: 3.3333
```


#VSLIDE

###Числа


Остаток от деления:
```python
In [11]: 10 % 3
Out[11]: 1
```

Операторы сравнения
```python
In [12]: 10 > 3.0
Out[12]: True

In [13]: 10 < 3
Out[13]: False

In [14]: 10 == 3
Out[14]: False

In [15]: 10 == 10
Out[15]: True

In [16]: 10 <= 10
Out[16]: True

In [17]: 10.0 == 10
Out[17]: True
```

#VSLIDE

###Числа


Функция int() позволяет выполнять конвертацию в тип int:
```python
In [18]: a = '11'

In [19]: int(a)
Out[19]: 11
```
Во втором аргументе можно указывать систему исчисления:
```python
In [20]: int(a, 2)
Out[20]: 3
```

Конвертация в int типа float:
```python
In [21]: int(3.333)
Out[21]: 3

In [22]: int(3.9)
Out[22]: 3
```

#VSLIDE

###Числа

Функция bin позволяет получить двоичное представление числа (обратите внимание, что результат строка):
```python
In [23]: bin(8)
Out[23]: '0b1000'

In [24]: bin(255)
Out[24]: '0b11111111'
```

Аналогично, функция hex() позволяет получить шестнадцатеричное значение:
```python
In [25]: hex(10)
Out[25]: '0xa'
```

#HSLIDE

#### Python example

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

    print "Connection to device %s" % device_dict['ip']
    queue.put({device_dict['ip']: result})


def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target = function,
                                    args = (device, command, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append(queue.get())

    return results

print( conn_processes(connect_ssh, devices['routers'], COMMAND) )
```

#HSLIDE

Python example

```python
def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target = function,
                                    args = (device, command, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append(queue.get())

    return results

print( conn_processes(connect_ssh, devices['routers'], COMMAND) )
```
