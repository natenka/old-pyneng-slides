# What’s New In Python 3.8

---
### Assignment expressions

+++
### Walrus operator

Было:
```
n = len(a)
if n > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

Стало:
```
if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

+++

Было:

```python
import re

regex = "vlan (\d+) is flapping between port (\S+) and port (\S+)"

ports = set()

with open("log.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:
            vlan, port1, port2 = match.groups()
            ports.update({port1, port2})

print(f"Петля между портами {', '.join(ports)}")
```

Стало:

```python
with open("log.txt") as f:
    for line in f:
        if (match := re.search(regex, line)):
            vlan, port1, port2 = match.groups()
            ports.update({port1, port2})
```

+++

Было:

```
def create_user(db):
    username = input("Введите имя пользователя: ")
    while True:
        password = input("Введите пароль: ")
        check = check_password(username, password)
        if check:
            break
    with open(db, 'a') as f:
        f.write(f"{username},{password}\n")
```

Стало:

```
def create_user(db):
    username = input("Введите имя пользователя: ")
    while not check_password(
        username, password := input("Введите пароль: ")
    ):
        pass
    with open(db, 'a') as f:
        f.write(f"{username},{password}\n")
```


---
### Positional-only arguments

```
In [8]: data = [1, 2, 3]

In [9]: data.append?
Signature: data.append(object, /)
Docstring: Append object to the end of the list.
Type:      builtin_function_or_method

```

+++
### Keyword-only arguments

```
In [2]: sorted?
Signature: sorted(iterable, /, *, key=None, reverse=False)
Docstring:
Return a new list containing all items from the iterable in ascending order.

A custom key function can be supplied to customize the sort order, and the
reverse flag can be set to request the result in descending order.
Type:      builtin_function_or_method
```

---
### f-strings support = for self-documenting expressions and debugging

+++

```
In [23]: ip = "10.1.1.1"

In [24]: mask = 24

In [25]: f"{ip} {mask}"
Out[25]: '10.1.1.1 24'

In [26]: f"{ip=} {mask=}"
Out[26]: "ip='10.1.1.1' mask=24"
```

---
### iterable unpacking in yield and return

```
>>> def parse(family):
        lastname, *members = family.split()
        return lastname.upper(), *members

>>> parse('simpsons homer marge bart lisa sally')
('SIMPSONS', 'homer', 'marge', 'bart', 'lisa', 'sally')
```

---
### SyntaxWarning

---
### asyncio REPL

---
### collections, csv - dict

---
### logging

---
### pprint

---

### typing

+++
### TypedDict

+++
### Literal

+++
### Final

+++
### final

+++
### Protocol

---
###

