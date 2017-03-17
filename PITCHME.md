# Python для сетевых инженеров 

#HSLIDE

# Работа с базами данных

#VSLIDE
### Работа с базами данных

__База данных (БД)__ - это данные, которые хранятся в соответствии с определенной схемой. В этой схеме каким-то образом описаны соотношения между данными.

__Язык БД (лингвистические средства)__ - используется для описания структуры БД, управления данными (добавление, изменение, удаление, получение), управления правами доступа к БД и ее объектам, управления транзакциями.

__Система управления базами данных (СУБД)__ - это программные средства, которые дают возможность управлять БД. СУБД должны поддерживать соответствующий язык (языки) для управления БД.

#VSLIDE
### SQL

__SQL (structured query language)__ - используется для описания структуры БД, управления данными (добавление, изменение, удаление, получение), управления правами доступа к БД и ее объектам, управления транзакциями.

Язык SQL подразделяется на такие 4 категории:
* DDL (Data Definition Language) - язык описания данных
* DML (Data Manipulation Language) - язык манипулирования данными
* DCL (Data Control Language) - язык определения доступа к данным
* TCL (Transaction Control Language) - язык управления транзакциями

#VSLIDE
### SQL

В каждой категории есть свои операторы (перечислены не все операторы):
* DDL
 * CREATE - создание новой таблицы, СУБД, схемы
 * ALTER - изменение существующей таблицы, колонки
 * DROP - удаление существующих объектов из СУБД
* DML
 * SELECT - выбор данных
 * INSERT - добавление новых данных
 * UPDATE - обновление существующих данных
 * DELETE - удаление данных

#VSLIDE
### SQL

* DCL
 * GRANT - предоставление пользователям разрешения на чтение/запись определенных объектов в СУБД
 * REVOKE - отзывает ранее предоставленые разрешения
* TCL
 * COMMIT Transaction - применение транзакции
 * ROLLBACK Transaction - откат всех изменений сделанных в текущей транзакции

#VSLIDE

### SQL и Python
Для работы с реляционной СУБД в Python можно использовать два подхода:
* работать с библиотекой, которая соответствует конкретной СУБД и использовать для работы с БД язык SQL
 * Например, для работы с SQLite используется модуль sqlite3
* работать с [ORM](http://xgu.ru/wiki/ORM), которая использует объектно-ориентированный подход для работы с БД
 * Например, SQLAlchemy


#HSLIDE

## SQLite

#VSLIDE

### SQLite

[SQLite](http://xgu.ru/wiki/SQLite) — встраиваемая в процесс реализация SQL-машины.

На практике, SQLite часто используется как встроенная СУБД в приложениях.

#VSLIDE

### SQLite CLI

В комплекте поставки SQLite идёт также утилита для работы с SQLite в командной строке.
Утилита представлена в виде исполняемого файла sqlite3 (sqlite3.exe для Windows) и с ее помощью можно вручную выполнять команды SQL.

В помощью этой утилиты очень удобно проверять правильность команд SQL, а также в целом знакомится с языком SQL.

#VSLIDE

### SQLite CLI

Для того чтобы создать БД (или открыть уже созданную) надо просто вызвать sqlite3 таким образом:
```
$ sqlite3 testDB.db
SQLite version 3.7.13 2012-06-11 02:05:22
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> 
```

Внутри sqlite3 можно выполнять команды SQL или, так называемые, метакоманды (или dot-команды).

#VSLIDE

#### Метакоманды
К метакомандам относятся несколько специальных команд, для работы с SQLite.
Они относятся только к утилите sqlite3, а не к SQL языку. В конце этих команд ```;``` ставить не нужно.

Примеры метакоманд:
* ```.help``` - подсказка со списком всех метакоманд
* ```.exit``` или ```.quit``` - выход из сессии sqlite3
* ```.databases``` - показывает присоединенные БД
* ```.tables``` - показывает доступные таблицы

#VSLIDE

#### Метакоманды

Примеры выполнения:
```
sqlite> .help
.backup ?DB? FILE      Backup DB (default "main") to FILE
.bail ON|OFF           Stop after hitting an error.  Default OFF
.databases             List names and files of attached databases
...

sqlite> .databases
seq  name      file                                   
---  --------  ----------------------------------
0    main      /home/nata/py_for_ne/db/db_article/testDB.db              
```

#HSLIDE

## Основы SQL (в sqlite3 CLI)

#VSLIDE

### CREATE

Оператор create позволяет создавать таблицы.

Создадим таблицу switch, в которой хранится информация о коммутаторах:
```sql
sqlite> CREATE table switch (
   ...>     mac          text primary key,
   ...>     hostname     text,
   ...>     model        text,
   ...>     location     text
   ...> );
```

#VSLIDE

### CREATE

Аналогично можно было создать таблицу и таким образом:
```sql
sqlite> create table switch (mac text primary key, hostname text, model text, location text);
```

Поле mac является первичным ключом. Это автоматически значит, что:
* поле должно быть уникальным
* в нем не может находиться значение NULL

В этом примере это вполне логично, так как MAC-адрес должен быть уникальным.


#VSLIDE

### CREATE

На данный момент записей в таблице нет, есть только ее определение.
Просмотреть определение можно такой командой:
```sql
sqlite> .schema switch
CREATE TABLE switch (
mac          text primary key,
hostname     text,
model        text,
location     text
);
```

#VSLIDE

### DROP

Оператор drop удаляет таблицу вместе со схемой и всеми данными.

Удалить таблицу можно так:
```sql
sqlite> DROP table switch
```

#VSLIDE

### INSERT

Оператор insert используется для добавления данных в таблицу.

Если указываются значения для всех полей, добавить запись можно таким образом (порядок полей должен соблюдаться):
```sql
sqlite> INSERT into switch values ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str');
```

Если нужно указать не все поля, или указать их в произвольном порядке, используется такая запись:
```sql
sqlite> INSERT into switch (mac, model, location, hostname)
   ...> values ('0000.BBBB.CCCC', 'Cisco 3850', 'London, Green Str', 'sw5');
```

#VSLIDE

### SELECT

Оператор select позволяет запрашивать информацию в таблице.

Например:
```sql
sqlite> SELECT * from switch;
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

#VSLIDE

### SELECT

Включить отображение названия полей можно с помощью команды ```.headers ON```.
```sql
sqlite> .headers ON
sqlite> SELECT * from switch;
mac|hostname|model|location
0000.AAAA.CCCC|sw1|Cisco 3750|London, Green Str
0000.BBBB.CCCC|sw5|Cisco 3850|London, Green Str
```

#VSLIDE

### SELECT

За форматирование вывода отвечает команда ```.mode```.

Режим ```.mode column``` включает отображение в виде колонок:
```sql
sqlite> .mode column
sqlite> SELECT * from switch;
mac             hostname    model       location         
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str
```

#VSLIDE

### WHERE

Оператор WHERE используется для уточнения запроса.
С помощью этого оператора можно указывать определенные условия, по которым отбираются данные.
Если условие выполнено, возвращается соответствующее значение из таблицы, если нет, не возвращается.

Например, таблица switch выглядит так:
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

#VSLIDE

### WHERE
Показать только те коммутаторы, модель которых 3750:
```sql
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         Cisco 3750  London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

#VSLIDE

### WHERE
Оператор where позволяет указывать не только конкретное значение поля.
Если добавить к нему оператор like, можно указывать шаблон поля.

LIKE с помощью символов ```_``` и ```%``` указывает на что должно быть похоже значение:
* ```_``` - обозначает один символ или число
* ```%``` - обозначает ноль, один или много символов

Например, если поле model записано в разном формате, с помощью предыдущего запроса, не получится вывести нужные коммутаторы.

#VSLIDE

### WHERE
Например, если в таблице поле model записано в разном формате:
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.4444.CCCC  sw4         Cisco 3650  London, Green Str  10.255.0.4  255         MNGMT      
```

#VSLIDE

### WHERE
В таком варианте предыдущий запрос с оператором WHERE не поможет:
```sql
sqlite> SELECT * from switch WHERE model = 'Cisco 3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

Но, если вместе с оператором WHERE использовать оператор ```LIKE```:
```sql
sqlite> SELECT * from switch WHERE model LIKE '%3750';
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
```

#VSLIDE

### ALTER

Оператор alter позволяет менять существующую таблицу: добавлять новые колонки или переименовывать таблицу.


Новые поля:
* mngmt_ip - IP-адрес коммутатора в менеджмент VLAN
* mngmt_vid - VLAN ID (номер VLAN) для менеджмент VLAN
* mngmt_vname - Имя VLAN, который используется для менеджмента

Добавление записей с помощью команды ALTER:
```sql
sqlite> ALTER table switch ADD COLUMN mngmt_ip text;
sqlite> ALTER table switch ADD COLUMN mngmt_vid varchar(10);
sqlite> ALTER table switch ADD COLUMN mngmt_vname  text;
```

#VSLIDE

### ALTER

Теперь таблица выглядит так (новые поля установлены в значение NULL):
```sql
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str                                     
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str                                    
```

#VSLIDE

### UPDATE

Оператор update используется для изменения существующей записи таблицы.

Обычно, update используется вместе с оператором where, чтобы уточнить какую именно запись необходимо изменить.

```sql
sqlite> UPDATE switch set model = 'Cisco 3850' where hostname = 'sw1';
sqlite> UPDATE switch set mac = '0000.DDDD.DDDD' where hostname = 'sw1';
```

#VSLIDE

### UPDATE
Результат будет таким:
```
sqlite> SELECT * from switch;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
```

#VSLIDE

### DELETE

Оператор delete используется для удаления записей.

Как правило, он используется вместе с оператором where.

Например:
```sql
sqlite> DELETE from switch where hostname = 'sw4';
```

#VSLIDE

### ORDER BY

Оператор ORDER BY используется для сортировки вывода по определенному полю, по возрастанию или убыванию.

Например, выведем все записи в таблице switch и отсортируем их по имени коммутаторов (по умолчанию выполняется сортировка по умолчанию, поэтому параметр ASC можно не указывать):
```sql
sqlite> SELECT * from switch ORDER BY hostname ASC;
mac             hostname    model       location           mngmt_ip    mngmt_vid   mngmt_vname
--------------  ----------  ----------  -----------------  ----------  ----------  -----------
0000.DDDD.DDDD  sw1         Cisco 3850  London, Green Str  10.255.0.1  255         MNGMT      
0000.2222.CCCC  sw2         C3750       London, Green Str  10.255.0.2  255         MNGMT      
0000.3333.CCCC  sw3         Cisco 3750  London, Green Str  10.255.0.3  255         MNGMT      
0000.BBBB.CCCC  sw5         Cisco 3850  London, Green Str  10.255.0.5  255         MNGMT      
```

#HSLIDE

## Модуль sqlite3

#VSLIDE
### Модуль sqlite3

Для работы с SQLite в Python используется модуль sqlite3.

Рассмотрим основные объекты и методы, которые модуль использует для работы с SQLite.

#VSLIDE
### Connection

Объект __Connection__ - это подключение к конкретной БД. Можно сказать, что этот объект представляет БД.

Пример создания подключения:
```
conn = sqlite3.connect('dhcp_snooping.db')
```

#VSLIDE
### Connection

У объекта Connection есть несколько методов, с помощью которых, можно выполнять команды SQL:
* __```execute()```__ - метод для выполнения одного выражения SQL
* __```executemany()```__ - метод позволяет выполнить выражение SQL для последовательности параметров (или для итератора) 
* __```executescript()```__ - метод позволяет выполнить несколько выражений SQL за один раз


#VSLIDE
### Cursor

Для чтения данных из БД, используется объект Cursor - это основной способ работы с БД.

Создается курсор из соединения с БД:
```
cursor = sqlite3.connect('dhcp_snooping.db').cursor()
```


#VSLIDE
### Cursor

При обращении к БД, сначала нужно выполнить выражение SQL, используя один из методов:
* __```execute()```__
* __```executemany()```__
* __```executescript()```__

А затем, с помощью метода ```fetch...()```, обрабатать полученные данные, и вернуть их:
* __```fetchone()```__ - возвращает одну строку данных
* __```fetchmany()```__ - возвращает список строк данных. С помощью параметра size, можно указывать какое количество строк возвращается
* __```fetchall()```__ - возвращает все строки в виде списка

#VSLIDE
### Connection как менеджер контекста

После выполнения операций, изменения должны быть сохранены (надо выполнить ```commit()```), а затем можно закрыть курсор, если он больше не нужен.

Python позволяет использовать объект Connection, как менеджер контекста.
В таком случае, не нужно явно делать commit и закрывать соединение.

При этом:
* при возникновении исключения, транзакция автоматически откатывается
* если исключения не было, автоматически выполняется commit

Пример использования соединения с базой, как менеджера контекстов: 
```python
with sqlite3.connect('test.db') as conn
```

#HSLIDE
## Пример использования SQLite

#VSLIDE
### Пример использования SQLite

Запишем информацию полученную из вывода sh ip dhcp snooping binding в SQLite.
Это позволит делать запросы по любому параметру и получать недостающие.

Для этого примера, достаточно создать одну таблицу, где будет храниться информация.

#VSLIDE

Определение таблицы прописано в отдельном файле dhcp_snooping_schema.sql и выглядит так:
```sql
create table dhcp (
    mac          text primary key,
    ip           text,
    vlan         text,
    interface    text
);
```

#VSLIDE

Теперь надо создать файл БД, подключиться к базе данных и создать таблицу (файл create_sqlite_ver1.py):
```python
import sqlite3

with sqlite3.connect('dhcp_snooping.db') as conn:
    print 'Creating schema...'
    with open('dhcp_snooping_schema.sql', 'r') as f:
        schema = f.read()
        conn.executescript(schema)
    print "Done"
```

#VSLIDE

Комментарии к файлу:
* используется менеджер контекста ```with```
* при выполнении строки ```with sqlite3.connect('dhcp_snooping.db') as conn```:
 * создается файл dhcp_snooping.db, если его нет
 * создается объект Connection
* в БД создается таблица, на основании команд, которые указаны в файле dhcp_snooping_schema.sql:
 * открываем файл dhcp_snooping_schema.sql
 * ```schema = f.read()``` - считываем весь файл как одну строку
 * ```conn.executescript(schema)``` - метод executescript позволяет выполнять команды SQL, которые прописаны в файле

#VSLIDE

Выполняем скрипт:
```
$ python create_sqlite_ver1.py
Creating schema...
Done
```

В результате должен быть создан файл БД и таблица dhcp.

#VSLIDE

Проверить, что таблица создалась, можно с помощью утилиты sqlite3, которая позволяет выполнять запросы прямо в командной строке.

Выведем список созданных таблиц (запрос такого вида позволяет проверить какие таблицы созданы в DB):
```
$ sqlite3 dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"
dhcp
```

#VSLIDE

Теперь нужно записать информацию из вывода команды sh ip dhcp snooping binding в таблицу (файл dhcp_snooping.txt):
```
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1
00:04:A3:3E:5B:69   10.1.5.2         63951       dhcp-snooping   5     FastEthernet0/10
00:05:B3:7E:9B:60   10.1.5.4         63253       dhcp-snooping   5     FastEthernet0/9
00:09:BC:3F:A6:50   10.1.10.6        76260       dhcp-snooping   10    FastEthernet0/3
Total number of bindings: 4
```

#VSLIDE

Во второй версии скрипта, сначала вывод в файле dhcp_snooping.txt обрабатывается регулярными выражениями, а затем, добавляются записи в БД (файл create_sqlite3_ver2.py):
```python
import sqlite3
import re

regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')
result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        if line[0].isdigit():
            result.append(regex.search(line).groups())

with sqlite3.connect('dhcp_snooping.db') as conn:
    print 'Creating schema...'
    with open('dhcp_snooping_schema.sql', 'r') as f:
        schema = f.read()
        conn.executescript(schema)
    print "Done"

    print 'Inserting DHCP Snooping data'

    for row in result:
        query = """insert into dhcp (mac, ip, vlan, interface)
        values (?, ?, ?, ?)""" 
        conn.execute(query, row)
```

#VSLIDE


Комментарии к скрипту:
* в регулярном выражении, которое проходится по выводу команды sh ip dhcp snooping binding, используются не именованные группы, как в примере раздела [Регулярные выражения](../09_regex/4a_group_example.md)
 * группы созданы только для тех элементов, которые нас интересуют
* result - это список, в котором хранится результат обработки вывода команды
 * но теперь тут не словари, а кортежи с результатами
 * это нужно для того, чтобы их можно было сразу передавать на запись в БД
* Перебираем в полученном списке кортежей, элементы
* В этом скрипте используется еще один вариант записи в БД
 * строка query описывает запрос. Но, вместо значений указываются знаки вопроса. Такой вариант записи запроса, позволяет динамически подставлять значение полей
 * затем, методу execute, передается строка запроса и кортеж row, где находятся значения

#VSLIDE

Выполняем скрипт:
```
$ python create_sqlite_ver2.py
Creating schema...
Done
Inserting DHCP Snooping data
```

Проверим, что данные записались:
```
$ sqlite3 dhcp_snooping.db "select * from dhcp"
00:09:BB:3D:D6:58|10.1.10.2|10|FastEthernet0/1
00:04:A3:3E:5B:69|10.1.5.2|5|FastEthernet0/10
00:05:B3:7E:9B:60|10.1.5.4|5|FastEthernet0/9
00:07:BC:3F:A6:50|10.1.10.6|10|FastEthernet0/3
```

#VSLIDE

Теперь попробуем запросить по определенному параметру:
```
$ sqlite3 dhcp_snooping.db "select * from dhcp where ip = '10.1.5.2'"
00:04:A3:3E:5B:69|10.1.5.2|5|FastEthernet0/10
```

То есть, теперь на основании одного параметра, можно получать остальные.

#VSLIDE

Переделаем наш скрипт таким образом, чтобы в нём была проверка на наличие файла dhcp_snooping.db.
Если файл БД есть, то не надо создавать таблицу, считаем, что она уже создана.

Файл create_sqlite_ver3.py:
```python
import os
import sqlite3
import re

data_filename = 'dhcp_snooping.txt'
db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')

with open(data_filename) as data:
    result = [regex.search(line).groups() for line in data if line[0].isdigit()]

db_exists = os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if not db_exists:
        print 'Creating schema...'
        with open(schema_filename, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print 'Done'

        print 'Inserting DHCP Snooping data'
        for val in result:
            query = """insert into dhcp (mac, ip, vlan, interface)
            values (?, ?, ?, ?)"""
            conn.execute(query, val)
    else:
        print 'Database exists, assume dhcp table does, too.'
```

#VSLIDE

Проверим. В случае если файл уже есть:
```
$ python create_sqlite_ver3.py 
Database exists, assume dhcp table does, too.
```

Если файла нет (предварительно его удалить):
```
$ rm dhcp_snooping.db
$ python create_sqlite_ver3.py
Creating schema...
Done
Inserting DHCP Snooping data
```

#VSLIDE

Теперь делаем отдельный скрипт, который занимается отправкой запросов в БД и выводом результатов. Он должен:
* ожидать от пользователя ввода параметров:
 * имя параметра
 * значение параметра
* делать нормальный вывод данных по запросу

#VSLIDE

Файл get_data_ver1.py:
```python
# -*- coding: utf-8 -*-
import sqlite3
import sys

db_filename = 'dhcp_snooping.db'


key, value = sys.argv[1:]
keys = ['mac', 'ip', 'vlan', 'interface']
keys.remove(key)

with sqlite3.connect(db_filename) as conn:
    #Позволяет далее обращаться к данным в колонках, по имени колонки
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("select * from dhcp where %s = ?" % key, (value,))

    print "\nDetailed information for host(s) with", key, value
    print '-' * 40
    for row in cursor.fetchall():
        for k in keys:
            print "%-12s: %s" % (k, row[k])
        print '-' * 40
```

#VSLIDE


Комментарии к скрипту:
* из аргументов, которые передали скрипту, считываются параметры key, value 
 * из списка keys, удаляется выбранный ключ. Таким образом в списке остаются только те параметры, , которые нужно вывести
* подключаемся к БД
 * ```conn.row_factory = sqlite3.Row``` - позволяет далее обращаться к данным в колонках, по имени колонки
* из БД выбираются те строки, в которых ключ равен указанному значению
 * ```cursor.execute("select * from dhcp where %s = ?" % key, (value,))```
  * в SQL значения можно подставлять через знак вопроса, но нельзя подставлять имя столбца. Поэтому, имя столбца подставляется через форматирование строк, а значение - штатным средством SQL.
    * Обратите внимание на ```(value,)``` таким образом передается кортеж с одним элементом
* Полученная информацию выводится на стандартный поток вывода:
 * перебираем полученные результаты и выводим только те поля, названия которых находятся в списке keys

#VSLIDE

Показать параметры хоста с IP 10.1.10.2:
```
$ python get_data_ver1.py ip 10.1.10.2

Detailed information for host(s) with ip 10.1.10.2
----------------------------------------
mac         : 00:09:BB:3D:D6:58
vlan        : 10
interface   : FastEthernet0/1
----------------------------------------
```

#VSLIDE

Показать хосты в VLAN 10:
```
$ python get_data_ver1.py vlan 10

Detailed information for host(s) with vlan 10
----------------------------------------
mac         : 00:09:BB:3D:D6:58
ip          : 10.1.10.2
interface   : FastEthernet0/1
----------------------------------------
mac         : 00:07:BC:3F:A6:50
ip          : 10.1.10.6
interface   : FastEthernet0/3
----------------------------------------
```

#VSLIDE

В этом скрипте есть несколько недостатков:
* не проверяется количество аргументов, которые передаются скрипту
* не проверяется правильность аргументов
* хотелось бы собирать информацию с разных коммутаторов. А для этого надо добавить поле, которое указывает на каком коммутаторе была найдена запись


Кроме того, многое нужно доработать в скрипте, который создает БД и записывает данные.

Все доработки будут выполняться в упражнениях к этому разделу.
