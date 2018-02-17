# Python для сетевых инженеров 

---
## Welcome to продленка :)

---

## Модуль logging


+++
### Базовый пример

---?code=code/logging_basic.py&lang=python&title=Базовый пример

+++
### Базовый пример

Файл logging_basic.py:
```python
import logging

logging.basicConfig(filename='mylog.log', level=logging.DEBUG)

logging.debug('Сообщение уровня debug')
logging.info('Сообщение уровня info')
logging.warning('Сообщение уровня warning')
```

+++
### Log-файл

```
DEBUG:root:Сообщение уровня debug
INFO:root:Сообщение уровня info
WARNING:root:Сообщение уровня warning
```
