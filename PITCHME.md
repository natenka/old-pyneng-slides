# Python для сетевых инженеров 

---
## Welcome to продленка :)

---

## Объектно-ориентированное программирование. Часть 2


---
### Специальные методы

+++
### `__str__`

```python
In [45]: class Switch:
    ...:     def __init__(self, hostname, model):
    ...:         self.hostname = hostname
    ...:         self.model = model
    ...:

In [46]: sw1 = Switch('sw1', 'Cisco 3850')

In [47]: print(sw1)
<__main__.Switch object at 0xb4e47d8c>
```

