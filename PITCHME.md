# Python для сетевых инженеров 

---
## Welcome to продленка :)

---

## Модуль logging


---
### Базовый пример

+++?code=code/logging_basic_1.py&lang=python&title=logging_basic_1.py

@[1]
@[3]
@[5-7]

+++
### Log-файл

```
DEBUG:root:Сообщение уровня debug
INFO:root:Сообщение уровня info
WARNING:root:Сообщение уровня warning
```

+++?code=code/logging_basic_2.py&lang=python&title=logging_basic_2.py

+++
### Log-файл

```
DEBUG:root:Сообщение уровня debug:
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0xb72a57ac>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'logging_basic_2.py', '__cached__': None, 'logging': <module 'logging' from '/usr/local/lib/python3.6/logging/__init__.py'>}
INFO:root:Сообщение уровня info
WARNING:root:Сообщение уровня warning
```


