# Python для сетевых инженеров 


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
