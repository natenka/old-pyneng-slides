# Python для сетевых инженеров 

#HSLIDE

# Сериализация данных

#VSLIDE
### Сериализация данных

Сериализация данных - это сохранение данных в каком-то формате.
Чаще всего, это сохранение в каком-то структурированном формате.

Например, это могут быть:
* файлы в формате YAML или JSON
* файлы в формате CSV
* база данных

#VSLIDE
### Сериализация данных

Для чего могут пригодится форматы YAML, JSON, CSV:
* у вас могут быть данные о IP-адресах и подобной информации, которую нужно обработать, в таблицах
 * таблицу можно экспортировать в формат CSV и обрабатывать её с помощью Python
* управляющий софт может возвращать данные в JSON. Соответственно, преобразовав эти данные в объект Python, с ними можно работать и делать, что угодно
* YAML очень удобно использовать для описания параметров
 * например, это могут быть параметры настройки различных объектов (IP-адреса, VLAN и др)

#HSLIDE

## Работа с файлами в формате CSV

#VSLIDE

### Работа с файлами в формате CSV

__CSV (comma-separated value)__ - это формат представления табличных данных (например, это могут быть данные из таблицы, или данные из БД).

В этом формате, каждая строка файла - это строка таблицы.
Несмотря на название формата, разделителем может быть не только запятая.

У форматов с другим разделителем может быть и собственное название, например, TSV (tab separated values), тем не менее под форматом CSV понимают, как правило, любые разделители.

#VSLIDE

### Работа с файлами в формате CSV

Пример файла в формате CSV (sw_data.csv):
```
hostname,vendor,model,location
sw1,Cisco,3750,London
sw2,Cisco,3850,Liverpool
sw3,Cisco,3650,Liverpool
sw4,Cisco,3650,London
```

В стандартной библиотеке Python есть модуль csv, который позволяет работать с файлами в CSV формате.

#VSLIDE

###Чтение файлов в формате CSV

Пример использования модуля csv (файл csv_read.py):
```python
import csv

with open('sw_data.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
```

Вывод будет таким:
```
$ python csv_read.py
['hostname', 'vendor', 'model', 'location']
['sw1', 'Cisco', '3750', 'London']
['sw2', 'Cisco', '3850', 'Liverpool']
['sw3', 'Cisco', '3650', 'Liverpool']
['sw4', 'Cisco', '3650', 'London']
```

#VSLIDE

###Чтение файлов в формате CSV

DictReader позволяет получить словари, в которых ключи - это названия столбцов, а значения - значения столбцов (файл csv_read_dict.py):
```python
import csv

with open('sw_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print row
```

Вывод будет таким:
```
$ python csv_read_dict.py
{'model': '3750', 'hostname': 'sw1', 'vendor': 'Cisco', 'location': 'London'}
{'model': '3850', 'hostname': 'sw2', 'vendor': 'Cisco', 'location': 'Liverpool'}
{'model': '3650', 'hostname': 'sw3', 'vendor': 'Cisco', 'location': 'Liverpool'}
{'model': '3650', 'hostname': 'sw4', 'vendor': 'Cisco', 'location': 'London'}
```
#VSLIDE

###Чтение файлов в формате CSV

reader - это итератор. Поэтому, если просто вывести reader, то вывод будет таким:
```python
In [1]: import csv

In [2]: with open('sw_data.csv') as f:
   ...:     reader = csv.reader(f)
   ...:     print reader
   ...:
<_csv.reader object at 0x10385b050>
```

Но, если нужно все объекты передать куда-то дальше, его можно превратить в список таким образом:
```python
In [3]: with open('sw_data.csv') as f:
   ...:     reader = csv.reader(f)
   ...:     print list(reader)
   ...:
[['hostname', 'vendor', 'model', 'location'], ['sw1', 'Cisco', '3750', 'London'], ['sw2', 'Cisco', '3850', 'Liverpool'], ['sw3', 'Cisco', '3650', 'Liverpool'], ['sw4', 'Cisco', '3650', 'London']]
```

#VSLIDE

###Запись файлов в формате CSV

Аналогичным образом, с помощью модуля csv, можно и записать файл в формате CSV (файл csv_write.py):

```python
import csv

data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

with open('sw_data_new.csv') as f:
    print f.read()
```

#VSLIDE

###Запись файлов в формате CSV

Вывод будет таким:
```
$ python csv_write.py
hostname,vendor,model,location
sw1,Cisco,3750,"London, Best str"
sw2,Cisco,3850,"Liverpool, Better str"
sw3,Cisco,3650,"Liverpool, Better str"
sw4,Cisco,3650,"London, Best str"
```

Обратите внимание на интересную особенность: последнее значение, взято в кавычки, а остальные строки - нет.
#VSLIDE

###Запись файлов в формате CSV

Для того, чтобы все строки записывались в файл csv с кавычками, надо изменить скрипт таким образом (файл csv_write_ver2.py):
```python
import csv

data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in data:
        writer.writerow(row)

with open('sw_data_new.csv') as f:
    print f.read()
```

#VSLIDE

###Запись файлов в формате CSV

Теперь вывод будет таким:
```
$ python csv_write_ver2.py
"hostname","vendor","model","location"
"sw1","Cisco","3750","London, Best str"
"sw2","Cisco","3850","Liverpool, Better str"
"sw3","Cisco","3650","Liverpool, Better str"
"sw4","Cisco","3650","London, Best str"
```

Теперь все значения с кавычками. И, так как номер модели задан как строка, в изначальном списке, тут он тоже в кавычках.

#VSLIDE

###Указание разделителя

Например, если в файле используется разделитель ```;``` (файл sw_data2.csv):
```
hostname;vendor;model;location
sw1;Cisco;3750;London
sw2;Cisco;3850;Liverpool
sw3;Cisco;3650;Liverpool
sw4;Cisco;3650;London
```

Достаточно просто указать какой разделитель используется в reader (файл csv_read_delimiter.py):
```python
import csv

with open('sw_data2.csv') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        print row
```


#HSLIDE

## Работа с файлами в формате JSON

#VSLIDE

### Работа с файлами в формате JSON

__JSON (JavaScript Object Notation)__ - это текстовый формат для хранения и обмена данными.

[JSON](https://ru.wikipedia.org/wiki/JSON) по синтаксису очень похож на словари в Python. И достаточно удобен для восприятия.

Как и в случае с CSV, в Python есть модуль, который позволяет легко записывать и читать данные в формате JSON.


#VSLIDE

### Чтение

Файл sw_templates.json:
```json
{
  "access": [
    "switchport mode access", 
    "switchport access vlan", 
    "switchport nonegotiate", 
    "spanning-tree portfast", 
    "spanning-tree bpduguard enable"
  ], 
  "trunk": [
    "switchport trunk encapsulation dot1q", 
    "switchport mode trunk", 
    "switchport trunk native vlan 999", 
    "switchport trunk allowed vlan"
  ]
}
```

#VSLIDE

### Чтение. json.load()
Чтение файла в объект Python:
```python
In [1]: import json

In [2]: with open('sw_templates.json') as f:
   ...:     templates = json.load(f)
   ...:

In [3]: templates
Out[3]:
{u'access': [u'switchport mode access',
  u'switchport access vlan',
  u'switchport nonegotiate',
  u'spanning-tree portfast',
  u'spanning-tree bpduguard enable'],
 u'trunk': [u'switchport trunk encapsulation dot1q',
  u'switchport mode trunk',
  u'switchport trunk native vlan 999',
  u'switchport trunk allowed vlan']}
```

#VSLIDE

### Чтение. json.loads()

Считывание строки в формате JSON в объект Python:
```python

In [4]: with open('sw_templates.json') as f:
   ...:     templates = json.loads(f.read())
   ...:

In [5]: templates
Out[5]:
{u'access': [u'switchport mode access',
  u'switchport access vlan',
  u'switchport nonegotiate',
  u'spanning-tree portfast',
  u'spanning-tree bpduguard enable'],
 u'trunk': [u'switchport trunk encapsulation dot1q',
  u'switchport mode trunk',
  u'switchport trunk native vlan 999',
  u'switchport trunk allowed vlan']}
```


#VSLIDE
###Запись

```python
In [1]: import json

In [2]: trunk_template = ['switchport trunk encapsulation dot1q',
   ...:                   'switchport mode trunk',
   ...:                   'switchport trunk native vlan 999',
   ...:                   'switchport trunk allowed vlan']
   ...:
   ...:
   ...: access_template = ['switchport mode access',
   ...:                    'switchport access vlan',
   ...:                    'switchport nonegotiate',
   ...:                    'spanning-tree portfast',
   ...:                    'spanning-tree bpduguard enable']
   ...:
   ...: to_json = {'trunk':trunk_template, 'access':access_template}
   ...:
```

#VSLIDE
###Запись. json.dump()

Запись объекта в файл:
```python
In [3]: with open('sw_templates.json', 'w') as f:
   ...:     json.dump(to_json, f)
   ...:

In [4]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"], "trunk": ["switchport trunk encapsulation dot1q", "switchport mode trunk", "switchport trunk native vlan 999", "switchport trunk allowed vlan"]}
```

#VSLIDE
###Запись. json.dumps()

Преобразование объекта в строку в формате JSON:
```python
In [5]: with open('sw_templates.json', 'w') as f:
   ...:     f.write(json.dumps(to_json))
   ...:
   ...:

In [6]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate", "spanning-tree portfast", "spanning-tree bpduguard enable"], "trunk": ["switchport trunk encapsulation dot1q", "switchport mode trunk", "switchport trunk native vlan 999", "switchport trunk allowed vlan"]}
```


#VSLIDE
###Запись

Более удобный для чтения вывод (файл json_write_ver2.py):
```python
import json


trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(to_json, sort_keys=True, indent=2))

with open('sw_templates.json') as f:
    print f.read()
``` 

#VSLIDE
###Запись
Теперь содержимое файла sw_templates.json выглядит так:
```json
{
  "access": [
    "switchport mode access",
    "switchport access vlan",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable"
  ],
  "trunk": [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan"
  ]
}
```

#VSLIDE
###Запись
При работе с форамтом json, данные не всегда будут того же типа, что исходные данные в Python.

Например, строки преобразуются в формат unicode, а кортежи - в списки.

```python

In [1]: import json

In [2]: trunk_template = ('switchport trunk encapsulation dot1q',
   ...:                   'switchport mode trunk',
   ...:                   'switchport trunk native vlan 999',
   ...:                   'switchport trunk allowed vlan')

In [3]: print type(trunk_template)
<type 'tuple'>

In [4]: with open('trunk_template.json', 'w') as f:
   ...:     f.write(json.dumps(trunk_template, sort_keys=True, indent=2))
   ...:
```

#VSLIDE
###Запись
```python

In [5]: cat trunk_template.json
[
  "switchport trunk encapsulation dot1q",
  "switchport mode trunk",
  "switchport trunk native vlan 999",
  "switchport trunk allowed vlan"
]
In [6]: templates = json.load(open('trunk_template.json'))

In [7]: type(templates)
Out[7]: list

In [8]: print templates
[u'switchport trunk encapsulation dot1q', u'switchport mode trunk', u'switchport trunk native vlan 999', u'switchport trunk allowed vlan']
```

#VSLIDE
### Ключи словарей

В формат JSON нельзя записать словарь у котрого ключи - кортежи:
```python
In [9]: to_json = {('trunk', 'cisco'):trunk_template, 'access':access_template}

In [10]: with open('sw_templates.json', 'w') as f:
    ...:     json.dump(to_json, f)
    ...:
...
TypeError: key ('trunk', 'cisco') is not a string
```

#VSLIDE
### Ключи словарей

Специальный параметр позволяет игнорировать такие ключи:
```python
In [11]: with open('sw_templates.json', 'w') as f:
    ...:     json.dump(to_json, f, skipkeys=True)
    ...:
    ...:

In [12]: cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate",
"spanning-tree portfast", "spanning-tree bpduguard enable"]}
```

#HSLIDE

##Работа с файлами в формате YAML

#VSLIDE

##Работа с файлами в формате YAML

__YAML (YAML Ain't Markup Language)__ - еще один текстовый формат для записи данных.

YAML более приятен для восприятия человеком, чем JSON, поэтому его часто используют для описания сценариев в ПО.
Например, в Ansible.

#HSLIDE

###Синтаксис YAML

#VSLIDE
###Синтаксис YAML

Как и Python, YAML использует отступы для указания структуры документа.
Но в YAML можно использовать только пробелы и нельзя использовать знаки табуляции.

Еще одна схожесть с Python: комментарии начинаются с символа # и продолжаются до конца строки.

#VSLIDE

####Список

Список может быть записан в одну строку:
```yaml
[switchport mode access, switchport access vlan, switchport nonegotiate, spanning-tree portfast, spanning-tree bpduguard enable]
```

Или каждый элемент списка в своей строке:
```yaml
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable
```

Когда список записан таким блоком, каждая строка должна начинаться с ```- ``` (минуса и пробела). И все строки в списке должны быть на одном уровне отступа.

#VSLIDE

####Словарь

Словарь также может быть записан в одну строку:
```yaml
{ vlan: 100, name: IT }
```

Или блоком:
```yaml
vlan: 100
name: IT
```
#VSLIDE

####Строки

Строки в YAML не обязательно брать в кавычки.
Это удобно, но иногда всё же следует использовать кавычки.
Например, когда в строке используется какой-то специальный символ (специальный для YAML).

Такую строку, например, нужно взять в кавычки, чтобы она была корректно воспринята YAML:
```yaml
command: "sh interface | include Queueing strategy:"
```
#VSLIDE

####Комбинация элементов

Словарь, в котором есть два ключа: access и trunk.
Значения, которые соответствуют этим ключам - списки команд:
```yaml
access:
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable

trunk:
- switchport trunk encapsulation dot1q
- switchport mode trunk
- switchport trunk native vlan 999
- switchport trunk allowed vlan
```

#VSLIDE

####Комбинация элементов

Список словарей:
```yaml
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
```

#HSLIDE

### Модуль PyYAML

#VSLIDE

### Модуль PyYAML
Для работы с YAML в Python используется модуль PyYAML.
Он не входит в стандартную библиотеку модулей, поэтому его нужно установить:
```
pip install pyyaml
```

Работа с ним аналогична модулям csv и json.

#VSLIDE

####Чтение из YAML

Файл info.yaml:
```yaml
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
```

#VSLIDE

####Чтение из YAML

```python
In [1]: import yaml

In [2]: templates = yaml.load(open('info.yaml'))

In [3]: templates
Out[3]:
[{'BS': 1550,
  'IT': 791,
  'id': 11,
  'name': 'Liverpool',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1510,
  'IT': 793,
  'id': 12,
  'name': 'Bristol',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1650,
  'IT': 892,
  'id': 14,
  'name': 'Coventry',
  'to_id': 2,
  'to_name': 'Manchester'}]
```

#VSLIDE

####Запись в YAML

Запись объектов Python в YAML (файл yaml_write.py):
```python
import yaml

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    f.write(yaml.dump(to_yaml))

with open('sw_templates.yaml') as f:
    print f.read()

```

#VSLIDE

####Запись в YAML

Файл sw_templates.yaml выглядит таким образом:
```yaml
access: [switchport mode access, switchport access vlan, switchport nonegotiate, spanning-tree
    portfast, spanning-tree bpduguard enable]
trunk: [switchport trunk encapsulation dot1q, switchport mode trunk, switchport trunk
    native vlan 999, switchport trunk allowed vlan]
```

#VSLIDE

####Запись в YAML

Параметр ```default_flow_style=False``` (файл yaml_write_ver2.py):
```python
import yaml

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']


access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    f.write(yaml.dump(to_yaml, default_flow_style=False))

with open('sw_templates.yaml') as f:
    print f.read()
```

#VSLIDE

####Запись в YAML

Теперь содержимое файла sw_templates.yaml выглядит таким образом:
```yaml
access:
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable
trunk:
- switchport trunk encapsulation dot1q
- switchport mode trunk
- switchport trunk native vlan 999
- switchport trunk allowed vlan
```

