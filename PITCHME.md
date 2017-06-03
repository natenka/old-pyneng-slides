# Python для сетевых инженеров 


#HSLIDE

# Основы Python

#VSLIDE

### Синтаксис Python

Отступы имеют значение. Они определяют:
* какие выражения попадают в блок кода
* когда блок кода заканчивается

Tab или пробел:
* лучше использовать пробелы (настроить редактор)
* количество пробелов должно быть одинаковым в одном блоке:
 * лучше во всем коде
 * обычно используются 2-4 пробела (в курсе используются 4 пробела)

#VSLIDE

### Синтаксис Python

```python
a = 10
b = 5

if a > b:
    print("A больше B")
    print(a - b)
else:
    print("B больше или равно A")
    print(b - a)

print("The End")

def open_file(filename):
    print("Reading file", filename)
    with open(filename) as f:
        return f.read()
        print("Done")
```

#VSLIDE

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

#VSLIDE

### Интерпретатор IPython

#VSLIDE

### Интерпретатор IPython

```python
In [1]: 1 + 2
Out[1]: 3

In [2]: 22*45
Out[2]: 990

In [3]: 2**3
Out[3]: 8

In [4]: print('Hello!')
Hello!

In [5]: for i in range(5):
   ...:     print(i)
   ...:     
0
1
2
3
4
```

#VSLIDE

### Интерпретатор IPython

Функция print()
```python
In [6]: print('Hello!')
Hello!

In [7]: print(5*5)
25

In [8]: print(1*5, 2*5, 3*5, 4*5)
5 10 15 20

In [9]: print('one', 'two', 'three')
one two three
```

#VSLIDE

### IPython magic

История текущей сессии:
```python
In [1]: a = 10

In [2]: b = 5

In [3]: if a > b:
   ...:     print("A is bigger")
   ...:
A is bigger

In [4]: %history
a = 10
b = 5
if a > b:
    print("A is bigger")
%history
```

#VSLIDE

### IPython help

```python
In [1]: help(str)
Help on class str in module builtins:

class str(object)
 |  str(object='') -> str
 |  str(bytes_or_buffer[, encoding[, errors]]) -> str
 |
 |  Create a new string object from the given object. If encoding or
 |  errors is specified, then the object must expose a data buffer
 |  that will be decoded using the given encoding and error handler.
...

In [2]: help(str.strip)
Help on method_descriptor:

strip(...)
    S.strip([chars]) -> str

    Return a copy of the string S with leading and trailing
    whitespace removed.
    If chars is given and not None, remove characters in chars instead.
```

#VSLIDE

### IPython help

```python
In [3]: ?str
Init signature: str(self, /, *args, **kwargs)
Docstring:
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
Type:           type

In [4]: ?str.strip
Docstring:
S.strip([chars]) -> str

Return a copy of the string S with leading and trailing
whitespace removed.
If chars is given and not None, remove characters in chars instead.
Type:      method_descriptor
```

#VSLIDE

### Переменные

#VSLIDE

### Переменные

Переменные в Python:
* не требуют объявления типа переменной (Python язык с динамической типизацией)
* являются ссылками на область памяти

Имя переменной:
* может состоять только из букв, цифр и знака подчеркивания
* не может начинаться с цифры
* не может содержать специальных символов @, $, %

#VSLIDE

### Переменные

```python
In [1]: a = 3

In [2]: b = 'Hello'

In [3]: c, d = 9, 'Test'

In [4]: print(a, b, c, d)
3 Hello 9 Test
```

#VSLIDE

### Переменные

Переменные являются ссылками на область памяти:
```python
In [5]: a = b = c = 33

In [6]: id(a)
Out[6]: 31671480

In [7]: id(b)
Out[7]: 31671480

In [8]: id(c)
Out[8]: 31671480
```

#VSLIDE

### Переменные

Рекомендации по именованию функций, классов и переменных:
* имена переменных обычно пишутся полностью большими или маленькими буквами
 * DB_NAME
 * db_name
* имена функций задаются маленькими буквами, с подчеркиваниями между словами
 * get_names
* имена классов задаются словами с заглавными буквами, без пробелов
 * CiscoSwitch

#HSLIDE

## Типы данных в Python

#VSLIDE

### Типы данных в Python

В Python есть несколько стандартных типов данных:
* Numbers (числа)
* Strings (строки)
* Lists (списки)
* Dictionary (словари)
* Tuples (кортежи)
* Sets (множества)
* Boolean

#VSLIDE

### Типы данных в Python

* Изменяемые:
 * Списки
 * Словари
 * Множества
* Неизменяемые
 * Числа
 * Строки
 * Кортежи

#VSLIDE

### Типы данных в Python

* Упорядоченные:
 * Списки
 * Кортежи
 * Строки
* Неупорядоченные:
 * Словари
 * Множества

#HSLIDE

## Числа

#VSLIDE

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

Деление int и float:
```python
In [5]: 10/3
Out[5]: 3.3333333333333335

In [6]: 10/3.0
Out[6]: 3.3333333333333335

In [9]: round(10/3.0, 2)
Out[9]: 3.33

In [10]: round(10/3.0, 4)
Out[10]: 3.3333
```


#VSLIDE

###Числа

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


Конвертация в тип int:
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

Функция bin():
```python
In [23]: bin(8)
Out[23]: '0b1000'

In [24]: bin(255)
Out[24]: '0b11111111'
```

Функция hex():
```python
In [25]: hex(10)
Out[25]: '0xa'
```

#HSLIDE

## Строки

#VSLIDE

### Строки

Строка в Python:
* последовательность символов, заключенная в кавычки
* неизменяемый, упорядоченный тип данных

```python
In [1]: 'Hello'
Out[1]: 'Hello'

In [2]: "Hello"
Out[2]: 'Hello'

In [3]: tunnel = """
   ....: interface Tunnel0
   ....:  ip address 10.10.10.1 255.255.255.0
   ....:  ip mtu 1416
   ....:  ip ospf hello-interval 5
   ....:  tunnel source FastEthernet1/0
   ....:  tunnel protection ipsec profile DMVPN
   ....: """
```

#VSLIDE

#### Строки - упорядоченный тип данных

```python
In [20]: string1 = 'interface FastEthernet1/0'

In [21]: string1[0]
Out[21]: 'i'

In [22]: string1[1]
Out[22]: 'n'

In [23]: string1[-1]
Out[23]: '0'

In [24]: string1[0:9]
Out[24]: 'interface'

In [25]: string1[10:22]
Out[25]: 'FastEthernet'

In [26]:  string1[10:]
Out[26]: 'FastEthernet1/0'

In [27]: string1[-3:]
Out[27]: '1/0'
```

#VSLIDE

#### Строки - упорядоченный тип данных

```python
In [28]: a = '0123456789'

In [29]: a[::]
Out[29]: '0123456789'

In [30]: a[::-1]
Out[30]: '9876543210'

In [31]: a[::2]
Out[31]: '02468'

In [32]: a[1::2]
Out[32]: '13579'
```

#VSLIDE

### Методы работы со строками

#VSLIDE

Методы ```upper(), lower(), swapcase(), capitalize()```
```python
In [25]: string1 = 'FastEthernet'

In [26]: string1.upper()
Out[26]: 'FASTETHERNET'

In [27]: string1.lower()
Out[27]: 'fastethernet'

In [28]: string1.swapcase()
Out[28]: 'fASTeTHERNET'

In [29]: string2 = 'tunnel 0'

In [30]: string2.capitalize()
Out[30]: 'Tunnel 0'
```

#VSLIDE

Метод __```count()```__ используется для подсчета того, сколько раз символ или подстрока, встречаются в строке:
```python
In [33]: string1 = 'Hello, hello, hello, hello'

In [34]: string1.count('hello')
Out[34]: 3

In [35]: string1.count('ello')
Out[35]: 4
```

Методу __```find()```__ можно передать подстроку или символ и он покажет на какой позиции находится первый символ подстроки (для первого совпадения):
```python
In [36]: string1 = 'interface FastEthernet0/1'

In [37]: string1.find('Fast')
Out[37]: 10

In [38]: string1[string1.find('Fast')::]
Out[38]: 'FastEthernet0/1'
```

#VSLIDE

Проверка на то начинается (или заканчивается) ли строка на определенные символы (методы __```startswith()```__, __```endswith()```__):
```python
In [40]: string1 = 'FastEthernet0/1'

In [41]: string1.startswith('Fast')
Out[41]: True

In [42]: string1.startswith('fast')
Out[42]: False

In [43]: string1.endswith('0/1')
Out[43]: True

In [44]: string1.endswith('0/2')
Out[44]: False
```

#VSLIDE

Замена последовательности символов в строке, на другую последовательность (метод __```replace()```__):
```python
In [45]: string1 = 'FastEthernet0/1'

In [46]: string1.replace('Fast', 'Gigabit')
Out[46]: 'GigabitEthernet0/1'
```

Метод __```strip()```__:
```python
In [47]: string1 = '\n\tinterface FastEthernet0/1\n'

In [48]: print(string1)

    interface FastEthernet0/1


In [49]: string1
Out[49]: '\n\tinterface FastEthernet0/1\n'

In [50]: string1.strip()
Out[50]: 'interface FastEthernet0/1'
```


#VSLIDE

Метод __```split()```__:
```python
In [51]: string1 = 'switchport trunk allowed vlan 10,20,30,100-200'

In [52]: string1.split()
Out[52]: ['switchport', 'trunk', 'allowed', 'vlan', '10,20,30,100-200']

In [53]: string1 = ' switchport trunk allowed vlan 10,20,30,100-200\n'

In [54]: commands = string1.strip().split()

In [55]: print(commands)
['switchport', 'trunk', 'allowed', 'vlan', '10,20,30,100-200']

In [56]: vlans = commands[-1].split(',')

In [57]: print(vlans)
['10', '20', '30', '100-200']
```


#VSLIDE

### Форматирование строк

#VSLIDE
### Форматирование строк

Существует два варианта форматирования строк:
* с оператором ```%``` (более старый вариант)
* методом ```format()``` (новый вариант)

Пример использования метода format:
```python
In [1]: "interface FastEthernet0/{}".format('1')
Out[1]: 'interface FastEthernet0/1'
```

Аналогичный пример с оператором %:
```python
In [2]: "interface FastEthernet0/%s" % '1'
Out[2]: 'interface FastEthernet0/1'
```


#VSLIDE
### Форматирование строк

Выравнивание по правой стороне:
```python
In [3]: vlan, mac, intf = ['100', 'aabb.cc80.7000', 'Gi0/1']

In [4]: print("%15s %15s %15s" % (vlan, mac, intf))
            100  aabb.cc80.7000           Gi0/1

In [5]: print("{:>15} {:>15} {:>15}".format(vlan, mac, intf))
            100  aabb.cc80.7000           Gi0/1
```

Выравнивание по левой стороне:
```python
In [6]: print("%-15s %-15s %-15s" % (vlan, mac, intf))
100             aabb.cc80.7000  Gi0/1

In [7]: print("{:15} {:15} {:15}".format(vlan, mac, intf))
100             aabb.cc80.7000  Gi0/1

```
#VSLIDE
### Форматирование строк
С помощью форматирования строк, можно также влиять на отображение чисел.

Например, можно указать сколько цифр после запятой выводить:
```python
In [8]: print("%.3f" % (10.0/3))
3.333

In [9]: print("{:.3f}".format(10.0/3))
3.333
```

Конвертировать в двоичный формат, указать сколько цифр должно быть в отображении числа и дополнить недостающее нулями:
```python
In [10]: '{:08b}'.format(10)
Out[10]: '00001010'
```


#HSLIDE

## Списки

#VSLIDE

### Список (List)

Список - это изменяемый упорядоченный тип данных.

Список в Python - это последовательность элементов, разделенных между собой запятой и заключенных в квадратные скобки.

Примеры списков:
```python
In [1]: list1 = [10,20,30,77]

In [2]: list2 = ['one', 'dog', 'seven']

In [3]: list3 = [1, 20, 4.0, 'word']
```

#VSLIDE

Список - упорядоченный тип данных:
```python
In [4]: list3 = [1, 20, 4.0, 'word']

In [5]: list3[1]
Out[5]: 20

In [6]: list3[1::]
Out[6]: [20, 4.0, 'word']

In [7]: list3[-1]
Out[7]: 'word'

In [8]: list3[::-1]
Out[8]: ['word', 4.0, 20, 1]
```

#VSLIDE

Так как списки изменяемые, элементы списка можно менять:
```python
In [13]: list3
Out[13]: [1, 20, 4.0, 'word']

In [14]: list3[0] = 'test'

In [15]: list3
Out[15]: ['test', 20, 4.0, 'word']
```

#VSLIDE

Можно создавать и список списков. И, как и в обычном списке, можно обращаться к элементам во вложенных списках:
```python
In [16]: interfaces = [['FastEthernet0/0', '15.0.15.1', 'YES', 'manual', 'up', 'up'],
   ....: ['FastEthernet0/1', '10.0.1.1', 'YES', 'manual', 'up', 'up'],
   ....: ['FastEthernet0/2', '10.0.2.1', 'YES', 'manual', 'up', 'down']]

In [17]: interfaces[0][0]
Out[17]: 'FastEthernet0/0'

In [18]: interfaces[2][0]
Out[18]: 'FastEthernet0/2'

In [19]: interfaces[2][1]
Out[19]: '10.0.2.1'
```

#VSLIDE

### Методы для работы со списками

#VSLIDE

Метод __join()__ собирает список строк в одну строку с разделителем, который указан в join():
```python
In [16]: vlans = ['10', '20', '30', '100-200']

In [17]: ','.join(vlans[:-1])
Out[17]: '10,20,30'
```

Метод __append()__ добавляет в конец списка указанный элемент:
```python
In [18]: vlans = ['10', '20', '30', '100-200']

In [19]: vlans.append('300')

In [20]: vlans
Out[20]: ['10', '20', '30', '100-200', '300']
```

#VSLIDE

Если нужно объединить два списка, то можно использовать два способа. Метод __extend()__ и операцию сложения:
```python
In [21]: vlans = ['10', '20', '30', '100-200']

In [22]: vlans2 = ['300', '400', '500']

In [23]: vlans.extend(vlans2)

In [24]: vlans
Out[24]: ['10', '20', '30', '100-200', '300', '400', '500']

In [25]: vlans + vlans2
Out[25]: ['10', '20', '30', '100-200', '300', '400', '500', '300', '400', '500']

In [26]: vlans
Out[26]: ['10', '20', '30', '100-200', '300', '400', '500']
```

При этом метод extend() расширяет список "на месте", а при операции сложения выводится итоговый суммарный список, но исходные списки не меняются.


#VSLIDE

Метод __pop()__ удаляет элемент, который соответствует указанному номеру. Но, что важно, при этом метод возвращает этот элемент:
```python
In [28]: vlans = ['10', '20', '30', '100-200']

In [29]: vlans.pop(-1)
Out[29]: '100-200'

In [30]: vlans
Out[30]: ['10', '20', '30']
```

Метод __remove()__ удаляет указанный элемент.
remove() не возвращает удаленный элемент:
```python
In [31]: vlans = ['10', '20', '30', '100-200']

In [32]: vlans.remove('20')

In [33]: vlans
Out[33]: ['10', '30', '100-200']
```


#VSLIDE

Метод __index()__ используется для того, чтобы проверить под каким номером в списке хранится элемент:
```python
In [35]: vlans = ['10', '20', '30', '100-200']

In [36]: vlans.index('30')
Out[36]: 2
```

Метод __insert()__ позволяет вставить элемент на определенное место в списке:
```python
In [37]: vlans = ['10', '20', '30', '100-200']

In [38]: vlans.insert(1,'15')

In [39]: vlans
Out[39]: ['10', '15', '20', '30', '100-200']
```


#VSLIDE

### Варианты создания списка

Создание списка с помощью литерала:
```python
In [1]: vlans = [10, 20, 30, 50]
```

Создание списка с помощью функции __list()__:
```python
In [2]: list1 = list('router')

In [3]: print(list1)
['r', 'o', 'u', 't', 'e', 'r']
```

__Генераторы списков__:
```python
In [4]: list2 = ['FastEthernet0/'+ str(i) for i in range(3)]

In [5]: list2
Out[6]:
['FastEthernet0/0',
 'FastEthernet0/1',
 'FastEthernet0/2']
```

#HSLIDE

## Словари

#VSLIDE

### Словарь (Dictionary)

Словари - это изменяемый, неупорядоченный тип данных

Словарь (ассоциативный массив, хеш-таблица):
* данные в словаре - это пары ```ключ: значение```
* доступ к значениям осуществляется по ключу, а не по номеру, как в списках
* ключ должен быть объектом неизменяемого типа:
 * число
 * строка
 * кортеж
* значение может быть данными любого типа


#VSLIDE

Пример словаря:
```python
london = {'name': 'London1', 'location': 'London Str', 
'vendor': 'Cisco', 'model': '4451', 'IOS': '15.4'}
```

Можно записывать и так:
```python
london = {
        'id': 1,
        'name':'London',
        'IT_VLAN':320,
        'User_VLAN':1010,
        'Mngmt_VLAN':99,
        'to_name': None,
        'to_id': None,
        'port':'G1/0/11'
}
```


#VSLIDE

Для того, чтобы получить значение из словаря, надо обратиться по ключу, таким же образом, как это было в списках, только вместо номера, будет использоваться ключ:
```python
In [1]: london = {'name': 'London1', 'location': 'London Str'}

In [2]: london['name']
Out[2]: 'London1'

In [3]: london['location']
Out[3]: 'London Str'
```

Аналогичным образом можно добавить новую пару "ключ:значение":
```python
In [4]: london['vendor'] = 'Cisco'

In [5]: print(london)
{'vendor': 'Cisco', 'name': 'London1', 'location': 'London Str'}
```


#VSLIDE

В словаре в качестве значения можно использовать словарь:
```python
london_co = {
    'r1' : {
    'hostname': 'london_r1',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'IOS': '15.4',
    'IP': '10.255.0.1'
    },
    'sw1' : {
    'hostname': 'london_sw1',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '3850',
    'IOS': '3.6.XE',
    'IP': '10.255.0.101'
    }
}
```

#VSLIDE

Получить значения из вложенного словаря можно так:
```python
In [7]: london_co['r1']['IOS']
Out[7]: '15.4'

In [8]: london_co['r1']['model']
Out[8]: '4451'

In [9]: london_co['sw1']['IP']
Out[9]: '10.255.0.101'
```

#VSLIDE

### Методы для работы со словарями

#VSLIDE

Методы __keys()__, __values()__, __items()__:
```python
In [24]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [25]: london.keys()
Out[25]: dict_keys(['name', 'location', 'vendor'])

In [26]: london.values()
Out[26]: dict_values(['London1', 'London Str', 'Cisco'])

In [27]: london.items()
Out[27]: dict_items([('name', 'London1'), ('location', 'London Str'), ('vendor', 'Cisco')])

```

#VSLIDE

```python
In [28]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [29]: keys = london.keys()

In [30]: print(keys)
dict_keys(['name', 'location', 'vendor'])

In [31]: london['ip'] = '10.1.1.1'

In [32]: keys
Out[32]: dict_keys(['name', 'location', 'vendor', 'ip'])
```

#VSLIDE

Метод __clear()__ позволяет очистить словарь:
```python
In [1]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco', 'model': '4451', 'IOS': '15.4'}

In [2]: london.clear()

In [3]: london
Out[3]: {}
```

Удалить ключ и значение:
```python
In [28]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [29]: del(london['name'])

In [30]: london
Out[30]: {'location': 'London Str', 'vendor': 'Cisco'}
```


#VSLIDE

Метод __copy()__ позволяет создать полную копию словаря.
```python
In [10]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [11]: london2 = london.copy()

In [12]: id(london)
Out[12]: 25524512

In [13]: id(london2)
Out[13]: 25563296

In [14]: london['vendor'] = 'Juniper'

In [15]: london2['vendor']
Out[15]: 'Cisco'
```

#VSLIDE

Если при обращении к словарю указывается ключ, которого нет в словаре, возникает ошибка:
```python
In [16]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [17]: london['IOS']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-17-b4fae8480b21> in <module>()
----> 1 london['IOS']

KeyError: 'IOS'
```

#VSLIDE

Метод __get()__ запрашивает ключ и, если его нет, вместо ошибки возвращает ```None```.
```python
In [18]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [19]: print(london.get('IOS'))
None
```

Метод get() позволяет указывать другое значение, вместо ```None```:
```python
In [20]: print(london.get('IOS', 'Ooops'))
Ooops
```
#VSLIDE

Метод __setdefault()__ ищет ключ и, если его нет, вместо ошибки, создает ключ со значением ```None```.
```python
In [21]: london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}

In [22]: IOS = london.setdefault('IOS')

In [23]: print(IOS)
None

In [24]: london
Out[24]: {'IOS': None, 'location': 'London Str', 'name': 'London1', 'vendor': 'Cisco'}
```

#VSLIDE

Второй аргумент позволяет указать, какое значение должно соответствовать ключу:
```python
In [25]: Model = london.setdefault('Model', 'Cisco3580')

In [26]: print(Model)
Cisco3580

In [27]: london
Out[27]:
{'IOS': None,
 'Model': 'Cisco3580',
 'location': 'London Str',
 'name': 'London1',
 'vendor': 'Cisco'}
```

#VSLIDE

### Варианты создания словаря

#VSLIDE

Словарь можно создать с помощью литерала:
```python
In [1]: r1 = {'model': '4451', 'IOS': '15.4'}
```

#VSLIDE


Конструктор __dict__ позволяет создавать словарь несколькими способами.

Если в роли ключей используются строки, можно использовать такой вариант создания словаря:
```python
In [2]: r1 = dict(model='4451', IOS='15.4')

In [3]: r1
Out[3]: {'IOS': '15.4', 'model': '4451'}
```

Второй вариант создания словаря с помощью dict:
```python
In [4]: r1 = dict([('model','4451'), ('IOS','15.4')])

In [5]: r1
Out[5]: {'IOS': '15.4', 'model': '4451'}
```

#VSLIDE

В ситуации, когда надо создать словарь с известными ключами, но, пока что, пустыми значениями (или одинаковыми значениями), очень удобен метод __fromkeys()__:
```python
In [5]: d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']

In [6]: r1 = dict.fromkeys(d_keys, None)

In [7]: r1
Out[7]:
{'IOS': None,
 'IP': None,
 'hostname': None,
 'location': None,
 'model': None,
 'vendor': None}
```

#VSLIDE

Генераторы словарей:
```python
In [16]: d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']

In [17]: d = {x: None for x in d_keys}

In [18]: d
Out[18]:
{'IOS': None,
 'IP': None,
 'hostname': None,
 'location': None,
 'model': None,
 'vendor': None}
```

#HSLIDE

## Кортеж

#VSLIDE

### Кортеж (Tuple)

Кортеж это неизменяемый упорядоченный тип данных.

Кортеж в Python - это последовательность элементов, которые разделены между собой запятой и заключены в скобки.


Создать пустой кортеж:
```python
In [1]: tuple1 = tuple()

In [2]: print(tuple1)
()
```

#VSLIDE

Кортеж из одного элемента (обратите внимание на запятую):
```python
In [3]: tuple2 = ('password',)
```

Кортеж из списка:
```python
In [4]: list_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']

In [5]: tuple_keys = tuple(list_keys)

In [6]: tuple_keys
Out[6]: ('hostname', 'location', 'vendor', 'model', 'IOS', 'IP')
```

#HSLIDE

## Множество

#VSLIDE

### Множество (Set)

Множество - это изменяемый неупорядоченный тип данных. В множестве всегда содержатся только уникальные элементы.

Множество в Python - это последовательность элементов, которые разделены между собой запятой и заключены в фигурные скобки.

С помощью множества можно легко убрать повторяющиеся элементы:
```python
In [1]: vlans = [10, 20, 30, 40, 100, 10]

In [2]: set(vlans)
Out[2]: {10, 20, 30, 40, 100}

In [3]: set1 = set(vlans)

In [4]: print(set1)
set([40, 100, 10, 20, 30])
```

#VSLIDE

### Методы работы с множествами

#VSLIDE

Метод __```add()```__ добавляет элемент во множество:
```python
In [1]: set1 = {10,20,30,40}

In [2]: set1.add(50)

In [3]: set1
Out[3]: {10, 20, 30, 40, 50}
```

Метод __```clear()```__ очищает множество:
```python
In [8]: set1 = {10,20,30,40}

In [9]: set1.clear()

In [10]: set1
Out[10]: set()
```

#VSLIDE

Метод __```discard()```__ позволяет удалять элементы, не выдавая ошибку, если элемента в множестве нет:
```python
In [3]: set1
Out[3]: {10, 20, 30, 40, 50}

In [4]: set1.discard(55)

In [5]: set1
Out[5]: {10, 20, 30, 40, 50}

In [6]: set1.discard(50)

In [7]: set1
Out[7]: {10, 20, 30, 40}
```

#VSLIDE

### Операции с множествами

Объединение множеств можно получить с помощью метода __```union()```__ или оператора __```|```__:
```python
In [1]: vlans1 = {10,20,30,50,100}
In [2]: vlans2 = {100,101,102,102,200}

In [3]: vlans1.union(vlans2)
Out[3]: {10, 20, 30, 50, 100, 101, 102, 200}

In [4]: vlans1 | vlans2
Out[4]: {10, 20, 30, 50, 100, 101, 102, 200}
```

#VSLIDE

### Операции с множествами

Пересечение множеств можно получить с помощью метода __```intersection()```__ или оператора __```&```__:
```python
In [5]: vlans1 = {10,20,30,50,100}
In [6]: vlans2 = {100,101,102,102,200}

In [7]: vlans1.intersection(vlans2)
Out[7]: {100}

In [8]: vlans1 & vlans2
Out[8]: {100}
```

#VSLIDE

### Варианты создания множества

Нельзя создать пустое множество с помощью литерала (так как в таком случае это будет не множество, а словарь):
```python
In [1]: set1 = {}

In [2]: type(set1)
Out[2]: dict
```

Но пустое множество можно создать таким образом:
```python
In [3]: set2 = set()

In [4]: type(set2)
Out[4]: set
```

#VSLIDE

Множество из строки:
```python
In [5]: set('long long long long string')
Out[5]: {' ', 'g', 'i', 'l', 'n', 'o', 'r', 's', 't'}
```

Множество из списка:
```python
In [6]: set([10,20,30,10,10,30])
Out[6]: {10, 20, 30}
```


#VSLIDE

Генератор множеств:
```python
In [7]: set2 = {i + 100 for i in range(10)}

In [8]: set2
Out[8]: {100, 101, 102, 103, 104, 105, 106, 107, 108, 109}

In [9]: print(set2)
{100, 101, 102, 103, 104, 105, 106, 107, 108, 109}
```

#HSLIDE

## Преобразование типов

#VSLIDE

```int()``` - преобразует строку в int:
```python
In [1]: int("10")
Out[1]: 10
```

С помощью функции int можно преобразовать и число в двоичной записи в десятичную (двоичная запись должна быть в виде строки)
```python
In [2]: int("11111111", 2)
Out[2]: 255
```

#VSLIDE

Преобразовать десятичное число в двоичный формат можно с помощью ```bin()```:
```python
In [3]: bin(10)
Out[3]: '0b1010'

In [4]: bin(255)
Out[4]: '0b11111111'
```

Аналогичная функция есть и для преобразования в шестнадцатиричный формат:
```python
In [5]: hex(10)
Out[5]: '0xa'

In [6]: hex(255)
Out[6]: '0xff'
```

#VSLIDE


Функция ```list()``` преобразует аргумент в список:
```python
In [7]: list("string")
Out[7]: ['s', 't', 'r', 'i', 'n', 'g']

In [8]: list({1,2,3})
Out[8]: [1, 2, 3]

In [9]: list((1,2,3,4))
Out[9]: [1, 2, 3, 4]
```

#VSLIDE


Функция ```set()``` преобразует аргумент в множество:
```python
In [10]: set([1,2,3,3,4,4,4,4])
Out[10]: {1, 2, 3, 4}

In [11]: set((1,2,3,3,4,4,4,4))
Out[11]: {1, 2, 3, 4}

In [12]: set("string string")
Out[12]: {' ', 'g', 'i', 'n', 'r', 's', 't'}
```

Эта функция очень полезна, когда нужно получить уникальные элементы в последовательности.

#VSLIDE


Функция ```tuple()``` преобразует аргумент в кортеж:
```python
In [13]: tuple([1,2,3,4])
Out[13]: (1, 2, 3, 4)

In [14]: tuple({1,2,3,4})
Out[14]: (1, 2, 3, 4)

In [15]: tuple("string")
Out[15]: ('s', 't', 'r', 'i', 'n', 'g')
```

Это может пригодится в том случае, если нужно получить неизменяемый объект.


#VSLIDE


Функция ```str()``` преобразует аргумент в строку:
```python
In [16]: str(10)
Out[16]: '10'
```

list comprehensions:
```python
In [17]: vlans = [10, 20, 30, 40]

In [18]: ','.join([ str(vlan) for vlan in vlans ])
Out[18]: '10,20,30,40'
```


#HSLIDE

## Проверка типов

#VSLIDE

Чтобы проверить состоит ли строка из одних цифр, можно использовать метод ```isdigit()```:
```python
In [2]: "a".isdigit()
Out[2]: False

In [3]: "a10".isdigit()
Out[3]: False

In [4]: "10".isdigit()
Out[4]: True
```

Пример использования метода:
```python
In [5]: vlans = ['10', '20', '30', '40', '100-200']

In [6]: [ int(vlan) for vlan in vlans if vlan.isdigit() ]
Out[6]: [10, 20, 30, 40]
```

#VSLIDE

Метод ```isalpha()``` позволяет проверить состоит ли строка из одних букв:
```python
In [7]: "a".isalpha()
Out[7]: True

In [8]: "a100".isalpha()
Out[8]: False

In [9]: "a--  ".isalpha()
Out[9]: False

In [10]: "a ".isalpha()
Out[10]: False
```

Метод ```isalnum()``` позволяет проверить состоит ли строка из  букв и цифр:
```python
In [11]: "a".isalnum()
Out[1]: True

In [12]: "a10".isalnum()
Out[12]: True
```


#VSLIDE

####type()

Иногда, в зависимости от результата, библиотека или функция может выводить разные типы объектов. Например, если объект один, возращается строка, если несколько, то возвращается кортеж.

Нам же надо построить ход программы по-разному, в зависимости от того, была ли возвращена строка или кортеж.

В этом может помочь функция ```type()```:
```python
In [13]: type("string")
Out[13]: str

In [14]: type("string") is str
Out[14]: True
```

#VSLIDE

Аналогично с кортежем (и другими типами данных):
```python
In [15]: type((1,2,3))
Out[15]: tuple

In [16]: type((1,2,3)) is tuple
Out[16]: True

In [17]: type((1,2,3)) is list
Out[17]: False
```


#HSLIDE

## Создание базовых скриптов

#VSLIDE

### Кодировка

```python
# -*- coding: utf-8 -*-

access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

print("Конфигурация интерфейса в режиме access:")
print('\n'.join(access_template).format(5))
```

#VSLIDE

### Передача аргументов скрипту

Файл access_template_argv.py:
```python
from sys import argv

interface, vlan = argv[1:]

access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

print('interface {}'.format(interface))
print('\n'.join(access_template).format(vlan))
```

#VSLIDE

### Передача аргументов скрипту

```
$ python access_template_argv.py Gi0/7 4
interface Gi0/7
switchport mode access
switchport access vlan 4
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
```

В данном случае, в списке argv находятся такие элементы:
```
['access_template_argv.py', 'Gi0/7', '4']
```

#VSLIDE

### Ввод информации пользователем

Файл access_template_raw_input.py:
```python

interface = input('Enter interface type and number: ')
vlan = int(input('Enter VLAN number: '))

access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

print('\n' + '-' * 30)
print('interface {}'.format(interface))
print('\n'.join(access_template).format(vlan))
```

#VSLIDE

### Ввод информации пользователем

```
$ python access_template_raw_input.py
Enter interface type and number: Gi0/3
Enter VLAN number: 55

------------------------------
interface Gi0/3
switchport mode access
switchport access vlan 55
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
```
