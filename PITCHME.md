# Python для сетевых инженеров 


#HSLIDE
## Модули для работы с сетевым оборудованием

#VSLIDE
### Модули для работы с сетевым оборудованием

Модули для работы с сетевым оборудованием, можно разделить на две части:
* модули для оборудования с поддержкой API
* модули для оборудования, которое работает только через CLI

Если оборудование поддерживает API, как например, [NXOS](http://docs.ansible.com/ansible/list_of_network_modules.html#nxos), то для него, скорее всего, создано большое количество модулей, которые выполняют конкретные действия, по настройке функционала (например, для NXOS создано более 60 модулей).

#VSLIDE
### Модули для работы с сетевым оборудованием

Для оборудования, которое работает только через CLI, Ansible поддерживает такие три типа модулей:
* os_command - выполняет команды show
* os_facts - собирает факты об устройствах
* os_config - выполняет команды конфигурации

#VSLIDE
### Модули для работы с сетевым оборудованием

Соответственно, для разных операционных систем, будут разные модули. Например, для Cisco IOS, модули будут называться:
* ios_command
* ios_config
* ios_facts

#VSLIDE
### Модули для работы с сетевым оборудованием

Аналогичные три модуля доступны для таких ОС:
* Dellos10
* Dellos6
* Dellos9
* EOS
* IOS
* IOS XR
* JUNOS
* SR OS
* VyOS


#VSLIDE
### Особенности подключения к сетевому оборудованию

При  работе с сетевым оборудованием надо указать, что должно использоваться подключение типа network_cli.
Это можно указывать в инвентарном файле, файлах с переменными и т.д.


Пример настройки для сценария (play):
```
- name: Run show commands on routers
  hosts: cisco-routers
  connection: network_cli

```

#VSLIDE
### Особенности подключения к сетевому оборудованию

В Ansible переменные можно указывать в разных местах, поэтому те же настройки можно указать по-другому.


Например, в инвентарном файле:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100

[cisco-routers:vars]
ansible_connection=network_cli
```

#VSLIDE
### Особенности подключения к сетевому оборудованию

Такой вариант подходит в том случае, когда Ansible используется больше для подключение к сетевым устройствам (или, локальные playbook используются для подключения к сетевому оборудованию).

В таком случае, нужно будет наоборот явно включать сбор фактов, если он нужен.


#VSLIDE
### Особенности подключения к сетевому оборудованию
Указать, что нужно использовать локальное подключение, также можно по-разному.

В инвентарном файле:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100

[cisco-routers:vars]
ansible_connection=network_cli
```

#VSLIDE
### Особенности подключения к сетевому оборудованию

Или в файлах переменных, например, в group_vars/all.yml:
```
ansible_connection: network_cli
```


#VSLIDE

Модули, которые используются для работы с сетевым оборудованием, требуют задания нескольких параметров.

* ansible_network_os - например, ios, eos
* ansible_user - имя пользователя
* ansible_password - пароль
* ansible_become - нужно ли переходить в привилегированный режим
* ansible_become_method - каким образом надод переходить в привилегированный режим (enable, для Cisco)
* ansible_become_pass - пароль для привилегированного режима




#VSLIDE

Пример указания всех параметров в group_vars/all.yml:
```
ansible_connection: network_cli
ansible_network_os: ios
ansible_user: cisco
ansible_password: cisco
ansible_become: yes
ansible_become_method: enable
ansible_become_pass: cisco
```

#VSLIDE
### Подготовка к работе с сетевыми модулями

Инвентарный файл myhosts:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

#VSLIDE
### Подготовка к работе с сетевыми модулями

Конфигурационный файл ansible.cfg:
```
[defaults]

inventory = ./myhosts
```

#VSLIDE
### Подготовка к работе с сетевыми модулями

В файле group_vars/all.yml надо создать параметры для подключения к оборудованию:
```
ansible_connection: network_cli
ansible_network_os: ios
ansible_user: cisco
ansible_password: cisco
ansible_become: yes
ansible_become_method: enable
ansible_become_pass: cisco
```

#HSLIDE
## Модуль ios_command

#VSLIDE
### Модуль ios_command

Модуль __ios_command__ - отправляет команду show на устройство под управлением IOS и возвращает результат выполнения команды.

Модуль ios_command не поддерживает отправку команд в конфигурационном режиме. Для этого используется отдельный модуль - ios_config.

#VSLIDE
### Модуль ios_command

Модуль ios_command поддерживает такие параметры:
* commands - список команд, которые надо отправить на устройство
* wait_for (или waitfor) - список условий на которые надо проверить вывод команды. Задача ожидает выполнения всех условий. Если после указанного количества попыток выполнения команды условия не выполняются, будет считаться, что задача выполнена неудачно.

#VSLIDE
### Модуль ios_command

Модуль ios_command поддерживает такие параметры:
* match - этот параметр используется вместе с wait_for для указания политики совпадения. Если параметр match установлен в all, должны выполниться все условия в wait_for. Если параметр равен any, достаточно чтобы выполнилось одно из условий. 
* retries - указывает количество попыток выполнить команду, прежде чем она будет считаться невыполненной. По умолчанию - 10 попыток.
* interval - интервал в секундах между повторными попытками выполнить команду. По умолчанию - 1 секунда.

#VSLIDE
### Модуль ios_command

Перед отправкой самой команды, модуль:
* выполняет аутентификацию по SSH,
* переходит в режим enable
* выполняет команду ```terminal length 0```, чтобы вывод команд show отражался полностью, а не постранично.
* выполняет команду ```terminal width 512```

#VSLIDE
### Модуль ios_command

Пример использования модуля ios_command (playbook 1_ios_command.yml):
```
- name: Run show commands on routers
  hosts: cisco-routers

  tasks:

    - name: run sh ip int br
      ios_command:
        commands: show ip int br
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug: var=sh_ip_int_br_result.stdout_lines
```

#VSLIDE
### Модуль ios_command

Модуль ios_command ожидает параметры:
* commands - список команд, которые нужно отправить на устройство
 * в нашем случае, он указан в файле group_vars/all.yml

Обратите внимание, что параметр register находится на одном уровне с именем задачи и модулем, а не на уровне параметров модуля ios_command.

Результат выполнения playbook:
```
$ ansible-playbook 1_ios_command.yml
```

#VSLIDE

![ios_command](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/2_ios_command.png)


#VSLIDE
### Выполнение нескольких команд

Playbook 2_ios_command.yml выполняет несколько команд и получает их вывод:
```
- name: Run show commands on routers
  hosts: cisco-routers

  tasks:

    - name: run show commands
      ios_command:
        commands:
          - show ip int br
          - sh ip route
      register: show_result

    - name: Debug registered var
      debug: var=show_result.stdout_lines
```

#VSLIDE
### Выполнение нескольких команд

Результат выполнения playbook (вывод сокращен):
```
$ ansible-playbook 2_ios_command.yml
```

#VSLIDE

![ios_command](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/2a_ios_command.png)


#VSLIDE
### Выполнение нескольких команд

Если модулю передаются несколько команд, результат выполнения команд находится в переменных show_result.stdout и show_result.stdout_lines в списке. Вывод будет в том порядке, в котором команды описаны в задаче.

Засчет этого, например, можно вывести результат выполнения первой команды, указав:
```
    - name: Debug registered var
      debug: var=show_result.stdout_lines[0]
```

#VSLIDE
### Обработка ошибок

В модуле встроено распознание ошибок.
Поэтому, если команда выполнена с ошибкой, модуль отобразит, что возникла ошибка.

Например, если сделать ошибку в команде, и запустить playbook еще раз
```
$ ansible-playbook 2_ios_command.yml
```

#VSLIDE
### Обработка ошибок

![ios_command](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/2_ios_command-fail.png)

#VSLIDE
### Обработка ошибок

Ansible обнаружил ошибку и возвращает сообщение ошибки.
В данном случае - 'Invalid input'.

Аналогичным образом модуль обнаруживает ошибки:
* Ambiguous command
* Incomplete command

#VSLIDE
### wait_for

Пример playbook (файл 3_ios_command_wait_for.yml):
```
- name: Run show commands on routers
  hosts: cisco-routers

  tasks:

    - name: run show commands
      ios_command:
        commands: ping 192.168.100.100
        wait_for:
          - result[0] contains 'Success rate is 100 percent'
```

#VSLIDE
### wait_for

В playbook всего одна задача, которая отправляет команду ping 192.168.100.100 и проверяет есть ли в выводе команды фраза 'Success rate is 100 percent'.

Если в выводе команды содержится эта фраза, задача считается корректно выполненой.

Запуск playbook:
```
$ ansible-playbook 3_ios_command_wait_for.yml -v
```

#VSLIDE
### wait_for

![ios_command](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/3_ios_command_waitfor.png)

