
# Python для сетевых инженеров 

#HSLIDE

# Функции

#VSLIDE

### Функции

Функция - это блок кода, выполняющий определенные действия:
* у функции есть имя, с помощью которого можно запускать этот блок кода сколько угодно раз
 * запуск кода функции, называется __вызовом функции__
* при создании функции, как правило, определяются параметры функции.
 * параметры функции определяют какие аргументы функция может принимать
* функциям можно передавать аргументы
 * соответственно, код функции будет выполняться с учетом указанных аргументов


#VSLIDE

### Зачем нужны функции?

Часто получается, что есть кусок кода, который повторяется.
Конечно, его можно копировать из одного скрипта в другой.
Но это очень неудобно, так как, при внесении изменений в код, нужно будет обновить его во всех файлах, в которые он скопирован.

Гораздо проще и правильней вынести этот код в функцию (это может быть и несколько функций).

И тогда, в этом файле, или каком-то другом, эта функция просто будет использоваться.

#HSLIDE

## Создание функций

#VSLIDE
## Создание функций

Создание функции:
* функции создаются с помощью зарезервированного слова __def__
* при создании функции, могут также указываться параметры, которые функция принимает
* первой строкой, опционально, может быть комментарий, так называемая __docstring__
* в функциях может использоваться оператор __return__
 * он используется для прекращения работы функции и выхода из нее
 * чаще всего, оператор return возвращает какое-то значение

#VSLIDE
## Создание функций


Пример функции:
```python
In [1]: def open_file( filename ):
   ...:     """Documentation string"""
   ...:     with open(filename) as f:
   ...:         print f.read()
   ...:
```

Когда функция создана, она ещё ничего не выполняет. Только при вызыве функции, действия, которые в ней перечислены, будут выполняться.

#VSLIDE

### Вызов функции

При вызове функции, нужно указать её имя и передать аргументы, если нужно.
* Параметры - это переменные, которые используются, при создании функции.
* Аргументы - это фактические значения (данные), которые передаются функции, при вызове.

#VSLIDE

### Вызов функции

```python
In [1]: def open_file( filename ):
   ...:     """Documentation string"""
   ...:     with open(filename) as f:
   ...:         print f.read()
   ...:

In [2]: open_file('r1.txt')
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```
#VSLIDE

### docstring


Первая строка в определении функции - это docstring, строка документации. Это комментарий, который используется как описание функции. Его можно отобразить так:
```python
In [4]: open_file.__doc__
Out[4]: 'Documentation string'
```
#VSLIDE

### Оператор return

Оператор __return__ используется для прекращения работы функции, выхода из нее, и, как правило, возврата какого-то значения.
Функция может возвращать любой объект Python.



#VSLIDE

### Оператор return

Если присвоить вывод функции переменной result, результат будет таким:
```python
In [1]: def open_file( filename ):
   ...:     """Documentation string"""
   ...:     with open(filename) as f:
   ...:         print f.read()
   ...:

In [5]: result = open_file('ospf.txt')
router ospf 1
 router-id 10.0.0.3
 auto-cost reference-bandwidth 10000
 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.2.0 0.0.0.255 area 2
 network 10.1.1.0 0.0.0.255 area 0

In [6]: print result
None
```

#VSLIDE

### Оператор return

```python
In [7]: def open_file( filename ):
   ...:     """Documentation string"""
   ...:     with open(filename) as f:
   ...:         return f.read()
   ...:

In [8]: result = open_file('r1.txt')

In [9]: print result
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```


#VSLIDE

### Оператор return


Ещё один важный аспект работы оператора return: выражения, которые идут после return, не выполняются.

То есть, в функции ниже, строка "Done" не будет выводиться, так как она стоит после return:
```python
In [10]: def open_file( filename ):
    ...:     print "Reading file", filename
    ...:     with open(filename) as f:
    ...:         return f.read()
    ...:         print "Done"
    ...:

In [11]: result = open_file('r1.txt')
Reading file r1.txt

```

#HSLIDE

## Пространства имен. Области видимости

#VSLIDE
### Пространства имен. Области видимости


У переменных в Python есть область видимости. В зависимости от места в коде, где переменная была определена, определяется и область видимости, то есть, где переменная будет доступна.

При использовании имен переменных в программе, Python каждый раз, ищет, создает или изменяет эти имена в соответствующем пространстве имен.
Пространство имен, которое доступно в каждый момент, зависит от области в которой находится код.

#VSLIDE
### Пространства имен. Области видимости

У Python есть правило LEGB, которым он пользуется при поиске переменных.

Например, если внутри функции, выполняется обращение к имени переменной, Python ищет переменную в таком порядке по областям видимости (до первого совпадения):
* L (local) - в локальной (внутри функции)
* E (enclosing) - в локальной области объемлющих функций (это те функции, внутри которых находится наша функция)
* G (global) - в глобальной (в скрипте)
* B (built-in) - в встроенной (зарезервированные значения Python)

#VSLIDE
### Пространства имен. Области видимости

Соответственно есть локальные и глобальные переменные:
* локальные переменные:
 * переменные, которые определены внутри функции
 * эти переменные становятся недоступными после выхода из функции
* глобальные переменные
 * переменные, которые определены вне функции
 * эти переменные 'глобальны' только в пределах модуля
   * например, чтобы они были доступны в другом модуле, их надо импортировать

#VSLIDE
### Пространства имен. Области видимости

Пример локальной и глобальной переменной result:
```python
In [1]: result = 'test string'

In [2]: def open_file( filename ):
   ...:     with open(filename) as f:
   ...:         result = f.read()
   ...:         return result
   ...:

In [3]: open_file('r1.txt')
Out[3]: '!\nservice timestamps debug datetime msec localtime show-timezone year\nservice timestamps log datetime msec localtime show-timezone year\nservice password-encryption\nservice sequence-numbers\n!\nno ip domain lookup\n!\nip ssh version 2\n!\n'

In [4]: result
Out[4]: 'test string'
```

#HSLIDE

## Параметры и аргументы функций

#VSLIDE
### Параметры и аргументы функций

Цель создания функции, как правило, заключается в том, чтобы вынести кусок кода, который выполняет определенную задачу, в отдельный объект.
Это позволяет использовать этот кусок кода многократно, не создавая его заново в программе.

Как правило, функция должна выполнять какие-то действия с входящими значениями и на выходе выдавать результат.

При работе с функциями, важно различать:
* __параметры__ - это переменные, которые используются, при создании функции.
* __аргументы__ - это фактические значения (данные), которые передаются функции, при вызове.

#VSLIDE
### Параметры и аргументы функций

Для того чтобы функция могла принимать входящие значения, ее нужно создать с параметрами:
```python
In [1]: def delete_exclamation_from_cfg( in_cfg, out_cfg ):
   ...:     with open(in_cfg) as in_file:
   ...:         result = in_file.readlines()
   ...:     with open(out_cfg, 'w') as out_file:
   ...:         for line in result:
   ...:             if not line.startswith('!'):
   ...:                 out_file.write(line)
   ...:
```

#VSLIDE
### Параметры и аргументы функций

Файл r1.txt будет использоваться как первый аргумент (in_cfg):
```python
In [2]: cat r1.txt
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
```

#VSLIDE
### Параметры и аргументы функций

Пример использования функции delete_exclamation_from_cfg:
```python
In [3]: delete_exclamation_from_cfg('r1.txt', 'result.txt')
```

Файл result.txt выглядит так:
```python
In [4]: cat result.txt
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
no ip domain lookup
ip ssh version 2

```

#VSLIDE
### Параметры и аргументы функций


При таком определении функции, надо обязательно передать оба аргумента.
Если передать только один аргумент, возникнет ошибка. Аналогично, возникнет ошибка, если передать три и больше аргументов:
```python
In [5]: delete_exclamation_from_cfg('r1.txt')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-7-66ae381f1c4f> in <module>()
----> 1 delete_exclamation_from_cfg('r1.txt')

TypeError: delete_exclamation_from_cfg() takes exactly 2 arguments (1 given)
```

#HSLIDE

## Типы параметров функции

#VSLIDE

### Типы параметров функции

При создании функции, можно указать, какие аргументы нужно передавать обязательно, а какие нет.

Соответственно, функция может быть создана с параметрами:
* __обязательными__
* __необязательными__ (опциональными, параметрами со значением по умолчанию)

#VSLIDE

### Обязательные параметры

__Обязательные параметры__ - определяют какие аргументы нужно передать функции обязательно.
При этом, их нужно передать ровно сколько, сколько указано параметров функции (нельзя указать большее или меньшее количество аргументов)

Функция с обязательными параметрами:
```python
In [1]: def cfg_to_list(cfg_file, delete_exclamation):
  ....:     result = []
  ....:     with open( cfg_file ) as f:
  ....:         for line in f:
  ....:             if delete_exclamation and line.startswith('!'):
  ....:                 pass
  ....:             else:
  ....:                 result.append(line.rstrip())
  ....:     return result
```

#VSLIDE
### Обязательные параметры

Пример вызова функции:
```python
In [2]: cfg_to_list('r1.txt', True)
Out[2]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

Так как аргументу delete_exclamation передано значение True, в итоговом словаре нет строк с восклицательными знаками.

#VSLIDE
### Обязательные параметры

Вызов функции, со значением False для аргумента delete_exclamation:
```python
In [3]: cfg_to_list('r1.txt', False)
Out[3]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 'ip ssh version 2',
 '!']
```
#VSLIDE

### Необязательные параметры (параметры со значением по умолчанию)

При создании функции, можно указывать значение по умолчанию для параметра:
```python
In [4]: def cfg_to_list(cfg_file, delete_exclamation=True):
  ....:     result = []
  ....:     with open( cfg_file ) as f:
  ....:         for line in f:
  ....:             if delete_exclamation and line.startswith('!'):
  ....:                 pass
  ....:             else:
  ....:                 result.append(line.rstrip())
  ....:     return result
  ....:

```

#VSLIDE

### Необязательные параметры (параметры со значением по умолчанию)

Так как теперь у параметра delete_exclamation значение по умолчанию равно True,
соответствующий аргумент можно не указывать при вызове функции, если значение по умолчанию подходит:
```python
In [5]: cfg_to_list('r1.txt')
Out[5]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

#VSLIDE

### Необязательные параметры (параметры со значением по умолчанию)

Но, можно и указать, если нужно поменять значение по умолчанию:
```python
In [6]: cfg_to_list('r1.txt', False)
Out[6]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 'ip ssh version 2',
 '!']

```

#HSLIDE

## Типы аргументов функции

#VSLIDE

### Типы аргументов функции

При вызове функции аргументы можно передавать двумя способами:
* как __позиционные__ - передаются в том же порядке, в котором они определены, при создании функции. То есть, порядок передачи аргументов, определяет какое значение получит каждый
* как __ключевые__ - передаются с указанием имени аргумента и его значения. В таком случае, аргументы могут быть указаны в любом порядке, так как их имя указывается явно.

#VSLIDE

### Типы аргументов функции

Позицонные и ключевые аргументы могут быть смешаны, при вызове функции.
То есть, можно использовать оба способа, при передаче аргументов одной и той же функции.
При этом, сначала должны идти позиционные аргументы, а только потом - ключевые.

#VSLIDE

### Типы аргументов функции

```python
In [1]: def cfg_to_list(cfg_file, delete_exclamation):
  ....:     result = []
  ....:     with open( cfg_file ) as f:
  ....:         for line in f:
  ....:             if delete_exclamation and line.startswith('!'):
  ....:                 pass
  ....:             else:
  ....:                 result.append(line.rstrip())
  ....:     return result
  ....:
```

#VSLIDE

### Позиционные аргументы

Позиционные аргументы, при вызове функции, надо передать в правильном порядке (поэтому они и называются позиционные)

```python
In [2]: cfg_to_list('r1.txt', False)
Out[2]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 '',
 '',
 'ip ssh version 2',
 '!']
```

#VSLIDE

Если при вызове функции поменять аргументы местами, скорее всего, возникнет ошибка, в зависимости от конкретной функции.

В случае с функцией cfg_to_list, получится такой результат:
```python
In [3]: cfg_to_list(False, 'r1.txt')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-18-e6da7e2657eb> in <module>()
----> 1 cfg_to_list(False, 'r1.txt')

<ipython-input-15-21a013e5e92c> in cfg_to_list(cfg_file, delete_exclamation)
      1 def cfg_to_list(cfg_file, delete_exclamation):
      2     result = []
----> 3     with open( cfg_file ) as f:
      4         for line in f:
      5             if delete_exclamation and line.startswith('!'):

TypeError: coercing to Unicode: need string or buffer, bool found
```

#VSLIDE

### Ключевые аргументы
__Ключевые аргументы__:
* передаются с указанием имени аргумента
* засчет этого, они могут передаваться в любом порядке

Если передать оба аргумента, как ключевые, можно передавать их в любом порядке:
```python
In [4]: cfg_to_list(delete_exclamation=False, cfg_file='r1.txt')
Out[4]:
['!',
 'service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 '!',
 'no ip domain lookup',
 '!',
 'ip ssh version 2',
 '!']
```
#VSLIDE
### Ключевые аргументы

__Сначала должны идти позиционные аргументы, а затем ключевые.__

Если сделать наоборот, возникнет ошибка:
```python
In [5]: cfg_to_list(delete_exclamation=False, 'r1.txt')
  File "<ipython-input-19-5efdee7ce6dd>", line 1
    cfg_to_list(delete_exclamation=False, 'r1.txt')
SyntaxError: non-keyword arg after keyword arg

```

#VSLIDE
### Ключевые аргументы

Но в такой комбинации можно:
```python
In [6]: cfg_to_list('r1.txt', delete_exclamation=True)
Out[6]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']

```

#HSLIDE

## Аргументы переменной длины

#VSLIDE

### Аргументы переменной длины

Иногда, необходимо сделать так, чтобы функция принимала не фиксированное количество аргументов, а любое.
Для такого случая, в Python можно создавать функцию со специальным параметром, который принимает аргументы переменной длины.
Такой параметр может быть, как ключевым, так и позиционным.


#VSLIDE

#### Позиционные аргументы переменной длины

Параметр, который принимает позиционные аргументы переменной длины, создается добавлением перед именем параметра звездочки.
Имя параметра может быть любым, но, по договоренности, чаще всего, используют имя ```*args```

Пример функции:
```python
In [1]: def sum_arg(a,*args):
  ....:     print a, args
  ....:     return a + sum(args)
  ....:
```

#VSLIDE
#### Позиционные аргументы переменной длины

Вызов функции с разным количеством аргументов:
```python
In [2]: sum_arg(1,10,20,30)
1 (10, 20, 30)
Out[2]: 61

In [3]: sum_arg(1,10)
1 (10,)
Out[3]: 11

In [4]: sum_arg(1)
1 ()
Out[4]: 1
```

#VSLIDE
#### Позиционные аргументы переменной длины

```python
In [5]: def sum_arg(*args):
  ....:     print arg
  ....:     return sum(arg)
  ....:

In [6]: sum_arg(1, 10, 20, 30)
(1, 10, 20, 30)
Out[6]: 61

In [7]: sum_arg()
()
Out[7]: 0
```

#VSLIDE

### Ключевые аргументы переменной длины

Параметр, который принимает ключевые аргументы переменной длины, создается добавлением перед именем параметра двух звездочек.
Имя параметра может быть любым, но, по договоренности, чаще всего, используют имя ```**kwargs``` (от keyword arguments).

```python
In [8]: def sum_arg(a,**kwargs):
  ....:     print a, kwargs
  ....:     return a + sum(kwargs.values())
  ....:
```

#VSLIDE
### Ключевые аргументы переменной длины

Вызов функцию с разным количеством ключевых аргументов:
```python
In [9]: sum_arg(a=10,b=10,c=20,d=30)
10 {'c': 20, 'b': 10, 'd': 30}
Out[9]: 70

In [10]: sum_arg(b=10,c=20,d=30,a=10)
10 {'c': 20, 'b': 10, 'd': 30}
Out[10]: 70
```

#VSLIDE
### Ключевые аргументы переменной длины

Обратите внимание, что, хотя ```a``` можно указывать как позиционный аргумент, нельзя указывать позиционный аргумент после ключевого:
```python
In [11]: sum_arg(10,b=10,c=20,d=30)
10 {'c': 20, 'b': 10, 'd': 30}
Out[11]: 70

In [12]: sum_arg(b=10,c=20,d=30,10)
  File "<ipython-input-6-71c121dc2cf7>", line 1
    sum_arg(b=10,c=20,d=30,10)
SyntaxError: non-keyword arg after keyword arg
```



#HSLIDE

## Распаковка аргументов

#VSLIDE

### Распаковка аргументов

В Python, выражения ```*args``` и ```**kwargs``` позволяют выполнять ещё одну задачу - __распаковку аргументов__.

До сих пор, мы вызывали все функции вручную.
И, соответственно, передавали все нужные аргументы.

Но, в реальной жизни, как правило, данные необходимо передавать в функцию программно.
И часто данные идут в виде какого-то объекта Python.

#VSLIDE

### Распаковка позиционных аргументов

Функция config_interface (файл func_args_var_unpacking.py):
```python
def config_interface(intf_name, ip_address, cidr_mask):
    interface = 'interface %s'
    no_shut = 'no shutdown'
    ip_addr = 'ip address %s %s'
    result = []
    result.append(interface % intf_name)
    result.append(no_shut)

    mask_bits = int(cidr_mask.split('/')[-1])
    bin_mask = '1'*mask_bits + '0'*(32-mask_bits)
    dec_mask = '.'.join([ str(int(bin_mask[i:i+8], 2)) for i in [0,8,16,24] ])

    result.append(ip_addr % (ip_address, dec_mask))
    return result
```

#VSLIDE
### Распаковка позиционных аргументов

```python
In [1]: config_interface('Fa0/1', '10.0.1.1', '/25')
Out[1]: ['interface Fa0/1', 'no shutdown', 'ip address 10.0.1.1 255.255.255.128']

In [2]: config_interface('Fa0/3', '10.0.0.1', '/18')
Out[2]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.192.0']

In [3]: config_interface('Fa0/3', '10.0.0.1', '/32')
Out[3]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.255']

In [4]: config_interface('Fa0/3', '10.0.0.1', '/30')
Out[4]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.252']

In [5]: config_interface('Fa0/3', '10.0.0.1', '30')
Out[5]: ['interface Fa0/3', 'no shutdown', 'ip address 10.0.0.1 255.255.255.252']
```

#VSLIDE
### Распаковка позиционных аргументов

Например, список interfaces_info, в котором находятся параметры для настройки интерфейсов:
```python
In [6]: interfaces_info = [['Fa0/1', '10.0.1.1', '/24'],
   ....:                    ['Fa0/2', '10.0.2.1', '/24'],
   ....:                    ['Fa0/3', '10.0.3.1', '/24'],
   ....:                    ['Fa0/4', '10.0.4.1', '/24'],
   ....:                    ['Lo0', '10.0.0.1', '/32']]
```

#VSLIDE
### Распаковка позиционных аргументов

Если пройтись по списку в цикле и передавать вложенный список, как аргумент функции, возникнет ошибка:
```python
In [7]: for info in interfaces_info:
   ....:     print config_interface(info)
   ....:
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-32-fb83ecc1fbcf> in <module>()
      1 for info in interfaces_info:
----> 2     print config_interface(info)
      3

TypeError: config_interface() takes exactly 3 arguments (1 given)
```

Ошибка вполне логичная: функция ожидает три аргумента, а ей передан 1 аргумент - список.

#VSLIDE
### Распаковка позиционных аргументов

В такой ситуации, пригодится распаковка аргументов.
Достаточно добавить ```*``` перед передачей списка, как аргумента, и ошибки уже не будет:
```python
In [8]: for info in interfaces_info:
  ....:     print config_interface(*info)
  ....:
['interface Fa0/1', 'no shutdown', 'ip address 10.0.1.1 255.255.255.0']
['interface Fa0/2', 'no shutdown', 'ip address 10.0.2.1 255.255.255.0']
['interface Fa0/3', 'no shutdown', 'ip address 10.0.3.1 255.255.255.0']
['interface Fa0/4', 'no shutdown', 'ip address 10.0.4.1 255.255.255.0']
['interface Lo0', 'no shutdown', 'ip address 10.0.0.1 255.255.255.255']
```

Python сам 'распакует' список info и передаст в функцию элементы списка, как аргументы.


#VSLIDE

### Распаковка ключевых аргументов

Аналогичным образом, можно распаковывать словарь, чтобы передать его как ключевые аргументы.

Функция config_to_list:
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
```

#VSLIDE

### Распаковка ключевых аргументов

Пример использования:
```python
In [9]: config_to_list('r1.txt')
Out[9]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

#VSLIDE

### Распаковка ключевых аргументов

Список словарей ```cfg```, в которых указано имя файла и все аргументы:
```python
In [10]: cfg = [dict(cfg_file='r1.txt', delete_excl=True, delete_empty=True, strip_end=True),
   ....:        dict(cfg_file='r2.txt', delete_excl=False, delete_empty=True, strip_end=True),
   ....:        dict(cfg_file='r3.txt', delete_excl=True, delete_empty=False, strip_end=True),
   ....:        dict(cfg_file='r4.txt', delete_excl=True, delete_empty=True, strip_end=False)]
```

#VSLIDE

### Распаковка ключевых аргументов

Если передать словарь функции config_to_list, возникнет ошибка:
```python
In [11]: for d in cfg:
   ....:     print config_to_list(d)
   ....:
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-40-1affbd99c2f5> in <module>()
      1 for d in cfg:
----> 2     print config_to_list(d)
      3

<ipython-input-35-6337ba2bfe7a> in config_to_list(cfg_file, delete_excl, delete_empty, strip_end)
      2                    delete_empty=True, strip_end=True):
      3     result = []
----> 4     with open( cfg_file ) as f:
      5         for line in f:
      6             if strip_end:

TypeError: coercing to Unicode: need string or buffer, dict found
```

Ошибка такая, так как все параметры, кроме имени файла, опциональны.
И на стадии открытия файла, возникает ошибка, так как вместо файла, передан словарь.

#VSLIDE

### Распаковка ключевых аргументов


Если добавить ```**``` перед передачей словаря функции, функция нормально отработает:
```python
In [12]: for d in cfg:
    ...:     print config_to_list(**d)
    ...:
['service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', 'no ip domain lookup', 'ip ssh version 2']
['!', 'service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', '!', 'no ip domain lookup', '!', 'ip ssh version 2', '!']
['service timestamps debug datetime msec localtime show-timezone year', 'service timestamps log datetime msec localtime show-timezone year', 'service password-encryption', 'service sequence-numbers', '', '', '', 'ip ssh version 2', '']
['service timestamps debug datetime msec localtime show-timezone year\n', 'service timestamps log datetime msec localtime show-timezone year\n', 'service password-encryption\n', 'service sequence-numbers\n', 'no ip domain lookup\n', 'ip ssh version 2\n']
```

Python распаковывает словарь и передает его в функцию как ключевые аргументы.

#HSLIDE

## Пример использования ключевых аргументов переменной длины и распаковки аргументов

#VSLIDE

С помощью аргументов переменной длины и распаковки аргументов,
можно передавать аргументы между функциями.

Функция config_to_list (файл kwargs_example.py):
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
```

#VSLIDE

Функция берет файл с конфигурацией, убирает часть строк и возвращает остальные строки как список.

Вызов функции в ipython:
```python
In [1]: config_to_list('r1.txt')
Out[1]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 'ip ssh version 2']
```

По умолчанию, из конфигурации убираются пустые строки, перевод строки в конце строк и строки, которые начинаются на знак восклицания.

#VSLIDE

Вызов функции со значением ```delete_empty=False```:
```python
In [2]: config_to_list('r1.txt', delete_empty=False)
Out[2]:
['service timestamps debug datetime msec localtime show-timezone year',
 'service timestamps log datetime msec localtime show-timezone year',
 'service password-encryption',
 'service sequence-numbers',
 'no ip domain lookup',
 '',
 '',
 'ip ssh version 2']

```


#VSLIDE

Задача:
* Создать функцию clear_cfg_and_write_to_file, которая с помощью функции config_to_list, удаляет лишние строки из конфигурации, а затем записывает строки в указанный файл.
 * при этом, надо не потерять возможность управлять тем, какие строки будут отброшены.
 * то есть, необходимо чтобы функция clear_cfg_and_write_to_file поддерживала те же параметры, что и функция config_to_list.

#VSLIDE

Можно просто продублировать все параметры функции и передавать их в функцию config_to_list:
```python
def clear_cfg_and_write_to_file(cfg, to_file, delete_excl=True,
                                delete_empty=True, strip_end=True):

    cfg_as_list = config_to_list(cfg, delete_excl=delete_excl,
                    delete_empty=delete_empty, strip_end=strip_end)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))
```

#VSLIDE


Но, если воспользоваться возможностью Python принимать аргументы переменной длины, можно сделать функцию clear_cfg_and_write_to_file такой:
```
def clear_cfg_and_write_to_file(cfg, to_file, **kwargs):
    cfg_as_list = config_to_list(cfg, **kwargs)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))
```
