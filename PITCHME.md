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
sqlite> DROP table switch;
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

```python
import sqlite3

connection = sqlite3.connect('dhcp_snooping.db')
```

#VSLIDE
### Cursor

После создания соединения, надо создать объект Cursor - это основной способ работы с БД.

Создается курсор из соединения с БД:
```python
import sqlite3

connection = sqlite3.connect('dhcp_snooping.db')
cursor = connection.cursor()
```

#VSLIDE
### Выполнение команд SQL

Для выполнения команд SQL в модуле есть несколько методов:
* __```execute()```__ - метод для выполнения одного выражения SQL
* __```executemany()```__ - метод позволяет выполнить одно выражение SQL для последовательности параметров (или для итератора)
* __```executescript()```__ - метод позволяет выполнить несколько выражений SQL за один раз


#VSLIDE
#### Метод execute

Метод execute позволяет выполнить одну команду SQL.

Сначала надо создать соединение и курсор:
```python
In [1]: import sqlite3

In [2]: connection = sqlite3.connect('sw_inventory.db')

In [3]: cursor = connection.cursor()
```

#VSLIDE
#### Метод execute

Создание таблицы switch с помощью метода execute:
```python
In [4]: cursor.execute("create table switch (mac text primary key, hostname text, model text, location text)")
Out[4]: <sqlite3.Cursor at 0x1085be880>
```

#VSLIDE
#### Метод execute

Выражения SQL могут быть параметризированы - вместо данных можно подставлять специальные значения.
Засчет этого можно использовать одну и ту же команду SQL для передачи разных данных.


#VSLIDE
#### Метод execute

Например, таблицу switch нужно заполнить данными из списка data:
```python
In [5]: data = [
   ...: ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
   ...: ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
   ...: ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
```

#VSLIDE
#### Метод execute

Для этого можно использовать запрос вида:
```python
In [6]: query = "INSERT into switch values (?, ?, ?, ?)"
```

Знаки вопроса в команде используются для подстановки данных, которые будут передаваться методу execute.

#VSLIDE
#### Метод execute

Теперь можно передать данные таким образом:
```
In [7]: for row in data:
   ...:     cursor.execute(query, row)
   ...:
```

Второй аргумент, который передается методу execute, должен быть кортежем.
Если нужно передать кортеж с одним элементом, используется запись ```(value, )```.

#VSLIDE
#### Метод execute
Чтобы изменения применились, нужно выполнить commit (обратите внимание, что метод commit вызывается у соединения):
```
In [8]: connection.commit()
```

#VSLIDE
#### Метод execute

Теперь, при запросе из командной строки sqlite3, можно увидеть эти строки в таблице switch:
```
$ sqlite3 sw_inventory.db

sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3780  London, Green Str
0000.AAAA.DDDD  sw3         Cisco 2960  London, Green Str
0011.AAAA.CCCC  sw4         Cisco 3750  London, Green Str
```

#VSLIDE
#### Метод executemany

Метод executemany позволяет выполнить одну команду SQL для последовательности параметров (или для итератора).

С помощью метода executemany, в таблицу switch можно добавить аналогичный список данных одной командой.

#VSLIDE
#### Метод executemany

Например, в таблицу switch надо добавить данные из списка data2:
```python
In [9]: data2 = [
   ...: ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
   ...: ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]
```

#VSLIDE
#### Метод executemany

Для этого нужно использовать аналогичный запрос вида:
```python
In [10]: query = "INSERT into switch values (?, ?, ?, ?)"
```

Теперь можно передать данные методу executemany:
```python
In [11]: cursor.executemany(query, data2)
Out[11]: <sqlite3.Cursor at 0x10ee5e810>

In [12]: connection.commit()
```

#VSLIDE
#### Метод executemany

После выполнения commit, данные доступны в таблице:
```
sqlite> select * from switch;
mac             hostname    model       location
--------------  ----------  ----------  -----------------
0000.AAAA.CCCC  sw1         Cisco 3750  London, Green Str
0000.BBBB.CCCC  sw2         Cisco 3780  London, Green Str
0000.AAAA.DDDD  sw3         Cisco 2960  London, Green Str
0011.AAAA.CCCC  sw4         Cisco 3750  London, Green Str
0000.1111.0001  sw5         Cisco 3750  London, Green Str
0000.1111.0002  sw6         Cisco 3750  London, Green Str
0000.1111.0003  sw7         Cisco 3750  London, Green Str
0000.1111.0004  sw8         Cisco 3750  London, Green Str
```


#VSLIDE
#### Метод executescript

Метод executescript позволяет выполнить несколько выражений SQL за один раз.

#VSLIDE
#### Метод executescript

Особенно удобно использовать этот метод при создании таблиц:
```python
In [14]: connection = sqlite3.connect('new_db.db')

In [15]: cursor = connection.cursor()

In [16]: cursor.executescript("""
    ...:     create table switches(
    ...:         hostname     text primary key,
    ...:         location     text
    ...:     );
    ...:
    ...:     create table dhcp(
    ...:         mac          text primary key,
    ...:         ip           text,
    ...:         vlan         text,
    ...:         interface    text,
    ...:         switch       text not null references switches(hostname)
    ...:     );
    ...: """)
Out[16]: <sqlite3.Cursor at 0x10efd67a0>
```

#VSLIDE
### Получение результатов запроса

#VSLIDE
### Получение результатов запроса

Для получения результатов запроса в sqlite3 есть несколько способов:
* использование методов ```fetch...()``` - в зависимости от метода возвращаются одна, несколько или все строки
* использование курсора как итератора - возвращается итератор

#VSLIDE
#### Метод fetchone

Метод fetchone возвращает одну строку данных.

Пример получения информации из базы данных sw_inventory.db:
```python
In [1]: import sqlite3

In [2]: connection = sqlite3.connect('sw_inventory.db')

In [3]: cursor = connection.cursor()

In [4]: cursor.execute('select * from switch')
Out[4]: <sqlite3.Cursor at 0x104eda810>

In [5]: cursor.fetchone()
Out[5]: (u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
```

#VSLIDE
#### Метод fetchone

Если повторно вызвать метод, он вернет следующую строку:
```python
In [6]: print cursor.fetchone()
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
```

#VSLIDE
#### Метод fetchone

Аналогичным образом метод будет возвращать следующие строки.
После обработки всех строк, метод начинает возвращать None.

#VSLIDE
#### Метод fetchone

Засчет этого, метод можно использовать в цикле, например, так:
```python
In [7]: cursor.execute('select * from switch')
Out[7]: <sqlite3.Cursor at 0x104eda810>

In [8]: while True:
   ...:     next_row = cursor.fetchone()
   ...:     if next_row:
   ...:         print next_row
   ...:     else:
   ...:         break
   ...:
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')
```

#VSLIDE
#### Метод fetchmany

Метод fetchmany возвращает возвращает список строк данных.

Синтаксис метода:
```
cursor.fetchmany([size=cursor.arraysize])
```

#VSLIDE
#### Метод fetchmany

С помощью параметра size, можно указывать какое количество строк возвращается.
По умолчанию, параметр size равен значению cursor.arraysize:
```python
In [9]: print cursor.arraysize
1
```

#VSLIDE
#### Метод fetchmany

Например, таким образом можно возвращать по три строки из запроса:
```python

In [10]: cursor.execute('select * from switch')
Out[10]: <sqlite3.Cursor at 0x104eda810>

In [11]: while True:
    ...:     three_rows = cursor.fetchmany(3)
    ...:     if three_rows:
    ...:         print three_rows
    ...:         print
    ...:     else:
    ...:         break
    ...:
[(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str'),
 (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
 (u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')]

[(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')]

[(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```


#VSLIDE
#### Метод fetchall

Метод fetchall возвращает все строки в виде списка:
```python
In [12]: cursor.execute('select * from switch')
Out[12]: <sqlite3.Cursor at 0x104eda810>

In [13]: cursor.fetchall()
Out[13]:
[(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str'),
 (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str'),
 (u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str'),
 (u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```

#VSLIDE
#### Метод fetchall

Важный аспект работы метода - он возвращает все оставшиеся строки.

То есть, если до метода fetchall, использовался, например, метод fetchone, то метод fetchall вернет оставшиеся строки запроса:
```python
In [14]: cursor.execute('select * from switch')
Out[14]: <sqlite3.Cursor at 0x104eda810>

In [15]: cursor.fetchone()
Out[15]: (u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')

In [16]: cursor.fetchone()
Out[16]: (u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')

In [17]: cursor.fetchall()
Out[17]:
[(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str'),
 (u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str'),
 (u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')]
```

#VSLIDE
#### Cursor как итератор

Если нужно построчно обрабатывать результирующие строки, лучше использовать курсор как итератор.
При этом не нужно использовать методы fetch.

При использовании методов execute, возвращается курсор.

#VSLIDE
#### Cursor как итератор

```python
In [18]: result = cursor.execute('select * from switch')

In [19]: for row in result:
    ...:     print row
    ...:
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0001', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0002', u'sw6', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0003', u'sw7', u'Cisco 3750', u'London, Green Str')
(u'0000.1111.0004', u'sw8', u'Cisco 3750', u'London, Green Str')
```

#VSLIDE
### Использование модуля sqlite3 без явного создания курсора

#VSLIDE
### Использование модуля sqlite3 без явного создания курсора

Методы execute доступны и в объекте Connection.
При их использовании курсор создается, но не явно.
Однако, методы fetch в Connection недоступны.

Но, если использовать курсор, который возвращают методы execute, как итератор, методы fetch могут и не понадобиться.

#VSLIDE
### Использование модуля sqlite3 без явного создания курсора

Пример итогового скрипта (файл create_sw_inventory_ver1.py):
```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('sw_inventory2.db')

con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

query = "INSERT into switch values (?, ?, ?, ?)"
con.executemany(query, data)
con.commit()

for row in con.execute("select * from switch"):
    print row

con.close()
```

#VSLIDE
### Использование модуля sqlite3 без явного создания курсора

Результат выполнения будет таким:
```
$ python create_sw_inventory_ver1.py
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
```

#VSLIDE
#### Обработка исключений

#VSLIDE
#### Обработка исключений

В таблице switch поле mac должно быть уникальным.
И, если попытаться записать пересекающийся MAC-адрес, возникнет ошибка:
```python
In [22]: con = sqlite3.connect('sw_inventory2.db')

In [23]: query = "INSERT into switch values ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str')"

In [24]: con.execute(query)
---------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
<ipython-input-56-ad34d83a8a84> in <module>()
----> 1 con.execute(query)

IntegrityError: UNIQUE constraint failed: switch.mac
```

#VSLIDE
#### Обработка исключений

Соответственно, можно перехватить исключение:
```python
In [25]: try:
    ...:     con.execute(query)
    ...: except sqlite3.IntegrityError as e:
    ...:     print "Error occured: ", e
    ...:
Error occured:  UNIQUE constraint failed: switch.mac
```

#VSLIDE
### Connection как менеджер контекста

#VSLIDE
### Connection как менеджер контекста

После выполнения операций, изменения должны быть сохранены (надо выполнить ```commit()```), а затем можно закрыть соединение, если оно больше не нужно.

Python позволяет использовать объект Connection, как менеджер контекста.
В таком случае, не нужно явно делать commit и закрывать соединение.
При этом:
* при возникновении исключения, транзакция автоматически откатывается
* если исключения не было, автоматически выполняется commit

#VSLIDE
### Connection как менеджер контекста

Пример использования соединения с базой, как менеджера контекстов (create_sw_inventory_ver2.py): 
```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]


con = sqlite3.connect('sw_inventory3.db')
con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

try:
    with con:
        query = "INSERT into switch values (?, ?, ?, ?)"
        con.executemany(query, data)
except sqlite3.IntegrityError as e:
    print "Error occured: ", e

for row in con.execute("select * from switch"):
    print row
```

#VSLIDE
### Connection как менеджер контекста

```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('sw_inventory3.db')
con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

try:
    with con:
        query = "INSERT into switch values (?, ?, ?, ?)"
        con.executemany(query, data)
except sqlite3.IntegrityError as e:
    print "Error occured: ", e

for row in con.execute("select * from switch"):
    print row

print '-'*30

#MAC-адрес sw7 совпадает с MAC-адресом существующего коммутатора - sw3
data2 = [('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
         ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
         ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
         ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]

try:
    with con:
        query = "INSERT into switch values (?, ?, ?, ?)"
        con.executemany(query, data2)
except sqlite3.IntegrityError as e:
    print "Error occured: ", e

for row in con.execute("select * from switch"):
    print row
```

#VSLIDE
### Connection как менеджер контекста

Результат выполнения скрипта:
```
$ python create_sw_inventory_ver3.py
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
------------------------------
Error occured:  UNIQUE constraint failed: switch.mac
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
```

#VSLIDE
### Connection как менеджер контекста

Обратите внимание, что содержимое таблицы switch до и после второго добавления информации - одинаково.
Это значит, что не записалась ни одна строка из списка data2.

Так получилось из-за того, что используется метод executemany и
в пределах одной транзакции мы пытаемся записать все 4 строки.
Если возникает ошибка с одной из них - откатываются все изменения.

#VSLIDE
### Connection как менеджер контекста

```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('sw_inventory3.db')
con.execute("create table switch (mac text primary key, hostname text, model text, location text)")

try:
    with con:
        query = "INSERT into switch values (?, ?, ?, ?)"
        con.executemany(query, data)
except sqlite3.IntegrityError as e:
    print "Error occured: ", e

for row in con.execute("select * from switch"):
    print row

print '-'*30

#MAC-адрес sw7 совпадает с MAC-адресом существующего коммутатора - sw3
data2 = [('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
         ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
         ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
         ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]

for row in data2:
    try:
        with con:
            query = "INSERT into switch values (?, ?, ?, ?)"
            con.execute(query, row)
    except sqlite3.IntegrityError as e:
        print "Error occured: ", e

for row in con.execute("select * from switch"):
    print row
```

#VSLIDE
### Connection как менеджер контекста

```
$ python create_sw_inventory_ver4.py
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
------------------------------
Error occured:  UNIQUE constraint failed: switch.mac
(u'0000.AAAA.CCCC', u'sw1', u'Cisco 3750', u'London, Green Str')
(u'0000.BBBB.CCCC', u'sw2', u'Cisco 3780', u'London, Green Str')
(u'0000.AAAA.DDDD', u'sw3', u'Cisco 2960', u'London, Green Str')
(u'0011.AAAA.CCCC', u'sw4', u'Cisco 3750', u'London, Green Str')
(u'0055.AAAA.CCCC', u'sw5', u'Cisco 3750', u'London, Green Str')
(u'0066.BBBB.CCCC', u'sw6', u'Cisco 3780', u'London, Green Str')
(u'0088.AAAA.CCCC', u'sw8', u'Cisco 3750', u'London, Green Str')
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
* ```conn.row_factory = sqlite3.Row``` 
 * позволяет далее обращаться к данным в колонках, по имени колонки
* ```cursor.execute("select * from dhcp where %s = ?" % key, (value,))```
 * из БД выбираются те строки, в которых ключ равен указанному значению
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
