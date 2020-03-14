# What’s New In Python 3.8

---
### Assignment expressions

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

Было

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

Стало

```python
def create_user(db):
    username = input("Введите имя пользователя: ")
    while not check_password(
        username, password := input("Введите пароль: ")
    ):
        pass
    with open(db, 'a') as f:
        f.write(f"{username},{password}\n")
```

+++

```python
if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

---
### Positional-only parameters

---
### f-strings support = for self-documenting expressions and debugging

---
### iterable unpacking in yield and return

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

