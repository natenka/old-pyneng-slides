# Python для сетевых инженеров 

---
## PEP 8 - руководство по написанию кода

---

## Расположение кода

+++
## Табы или пробелы

* В качестве отступов рекомендуется использовать пробелы.
* Один уровень отступа - 4 пробела
* Python 3 запрещает одновременное использование Tab и пробелов в отступах.

> Как правило, в редакторах и IDE есть настройка, которая позволяет указать, что при нажатии клавиши Tab будет устанавливаться 4 пробела.


+++?color=rgba(143,188,143, 0.5)
### Отступы. Да

Вертикальное выравнивание по открывающейся скобке:
```python
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

Выравнивание с учетом остальных строк.
Тут параметры функции сдвинуты относительно print,
чтобы визуально разделить их:
```python
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

Висячие отступы (hanging indents) - все строки с отступом, кроме первой.
Однако, надо учитывать ситуацию выше
и отделять строки дополнительным отступом, если необходимо:
```python
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

+++?color=rgba(143,188,143, 0.5)
### Отступы. Да

При использовании висячих отступов, можно использовать не только 4 пробела
```python
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```


+++?color=rgba(240,128,128, 0.5)
### Отступы. Нет

Запрещено писать аргументы в первой строке, если не используется вертикальное выравнивание:
```python
foo = long_function_name(var_one, var_two,
    var_three, var_four)
```

В этом случае, надо добавить отступы перед параметрами функции,
чтобы они отличались от следующих строк:
```python
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

+++?color=rgba(143,188,143, 0.5)
### Отступы и перенос условия на разные строки

Иногда условие в выражении if слишком длинное, чтобы писать его в одной строке.
В таком случае, возможны такие варианты переноса выражения:

Часть выражения находится на том же уровне, что и следующие команды:
```python
if (this_is_one_thing
    and that_is_another_thing):
    do_something()
```

В варианте выше сложнее отличить часть условия от команд внутри условия.
Улучшить ситуацию можно сделав дополнительный отступ в условии:
```python
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

+++?color=rgba(143,188,143, 0.5)
### Отступы и перенос условия на разные строки

Иногда, создание дополнительной переменной перед условием, также может помочь сократить условие
```python
ignore_line = '!' in line or ignore_command(line, ignore)

if line and not ignore_line:
    do_something()
```

Python позволяет разбивать код до или после операторов, однако рекомендуется разбивать код до операторов.
Такой вариант обычно легче воспринимается
```python
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

+++?color=rgba(240,128,128, 0.5)
### Отступы и перенос условия на разные строки

```python
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

### Закрывающиеся скобки

Первый вариант закрытия скобок:
```python
port_security_template = [
    'switchport port-security maximum 2',
    'switchport port-security violation restrict',
    'switchport port-security',
    ]
```

Второй вариант закрытия скобок:
```python
port_security_template = [
    'switchport port-security maximum 2',
    'switchport port-security violation restrict',
    'switchport port-security',
]
```

+++
## Максимальная длина строки

* Максимальная длина строки кода - 79 символов.
* Максимальная длина комментариев/docstring - 72 символа.

Длинные строки предпочтительней разбивать на несколько, используя круглые скобки:
```python
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

Многие выражения в скобках можно переносить на разные строки:
```python
r1 = {'IOS': '15.4',
      'IP': '10.255.0.1',
      'hostname': 'london_r1',
      'location': '21 New Globe Walk',
      'model': '4451',
      'vendor': 'Cisco'}

lower_r1 = {str.lower(key): value
            for key, value in r1.items()}
```

+++
## Максимальная длина строки

Некоторые выражения нельзя разбить на несколько строк. В этом случае, можно использовать обратный слеш:
```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

Аналогичная ситуация будет с выражением assert:
```python
assert return_value == correct_return_value,\
       "Функция возвращает неправильное значение"
```

+++
## Пустые строки

Функции и классы должны быть отделены друг от друга двумя пустыми строками:
```python
def sum_numbers(a, b):
    return a + b


def divide_numbers(a, b):
    return a/b


class Robot:

    def __init__(self, name):
        self.name = name
```

+++
## Пустые строки

Внутри класса метода должны быть отделены друг от друга одной пустой строкой:
```python
class Robot:

    def __init__(self, name):
        self.name = name

    def hello(self):
        return f'My name is {self.name}'

    def say(self, message):
        return f'message'
```

+++
## Кодировка исходного файла

Для кода должна использоваться кодировка UTF-8.

Соглашение по именам в стандартной библиотеке:

* все идентификаторы должны состоять только из ASCII символов
* индентификаторы должны сосоять из английских слов/сокращений
* комментарии должны состоять из ASCII символов

+++
### Импорт

Импорт модулей всегда должен находиться в начале файла, сразу после docstring/комментариев модуля.
```python
# -*- coding: utf-8 -*-
"""Utilities for writing code that runs on Python 2 and 3"""

import functools
import itertools
import operator
import sys
```

+++
### Импорт

Импорт модулей должен выполняться в таком порядке
1. Модули стандартной библиотеки
2. Модули сторонних библиотек
3. Модули текущего проекта  

Каждая группа должна быть разделена пустой строкой.

+++
### Импорт

```python
import sys
import os

import tabulate
import jinja

import my_super_script
```

+++?color=rgba(143,188,143, 0.5)
### Импорт. Правильно

Импорт каждого модуля, как правило, должен находиться на отдельной строке:
```python
import os
import sys
```

При этом, можно импортировать несколько объектов из модуля в одной строке:
```python
from subprocess import run, PIPE
```

+++?color=rgba(240,128,128, 0.5)
### Импорт. Неправильно

```python
import os, sys
```

