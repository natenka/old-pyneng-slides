# Python для сетевых инженеров 


#HSLIDE
## Модули для работы с сетевым оборудованием

#VSLIDE
### Модули для работы с сетевым оборудованием

Модули для работы с сетевым оборудованием, можно разделить на две части:
* модули для оборудования с поддержкой API
* модули для оборудования, которое работает только через CLI

Если оборудование поддерживает API, как например, [NXOS](http://docs.ansible.com/ansible/list_of_network_modules.html#nxos), то для него создано большое количество модулей, которые выполняют конкретные действия, по настройке функционала (например, для NXOS создано более 60 модулей).

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
Это можно указывать в инвентарном файле, файлах с перемеными и т.д.


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
* ansible_become - нужно ли переходить в привилегированный режим (enable, для Cisco)
* ansible_become_method - каким образом надод переходить в привилегированный режим
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

Если модулю передаются несколько команд, результат выполнения команд находится в переменных stdout и stdout_lines в списке. Вывод будет в том порядке, в котором команды описаны в задаче.

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

![ios_command](https://raw.githubusercontent.com/natenka/PyNEng/python3.6/images/15_ansible/3_ios_command_waitfor.png)


#HSLIDE
## Модуль ios_facts

#VSLIDE
### Модуль ios_facts

Модуль ios_facts - собирает информацию с устройств под управлением IOS.

Информация берется из таких команд:
* dir
* show version
* show memory statistics
* show interfaces
* show ipv6 interface
* show lldp
* show lldp neighbors detail
* show running-config

#VSLIDE
### Модуль ios_facts

В модуле можно указывать какие параметры собирать - можно собирать всю информацию, а можно только подмножество.
По умолчанию, модуль собирает всю информацию, кроме конфигурационного файла.

Какую информацию собирать, указывается в параметре __gather_subset__.

#VSLIDE
### Модуль ios_facts
Поддерживаются такие варианты (указаны также команды, которые будут выполняться на устройстве):
* __all__
* __hardware__
 * dir
 * show version
 * show memory statistics
* __config__
 * show version
 * show running-config

#VSLIDE
### Модуль ios_facts

* __interfaces__
 * dir
 * show version
 * show interfaces
 * show ipv6 interface
 * show lldp
 * show lldp neighbors detail

#VSLIDE
### Модуль ios_facts

Собрать все факты:
```
- ios_facts:
    gather_subset: all
```

#VSLIDE
### Модуль ios_facts

Собрать только подмножество interfaces:
```
- ios_facts:
    gather_subset:
      - interfaces
```

#VSLIDE
### Модуль ios_facts

Собрать всё, кроме hardware:
```
- ios_facts:
    gather_subset:
      - "!hardware"
```

#VSLIDE
### Модуль ios_facts

Ansible собирает такие факты:
* ansible_net_all_ipv4_addresses - список IPv4 адресов на устройстве
* ansible_net_all_ipv6_addresses - список IPv6 адресов на устройстве
* ansible_net_config - конфигурация (для Cisco sh run)
* ansible_net_filesystems - файловая система устройства
* ansible_net_gather_subset - какая информация собирается (hardware, default, interfaces, config)
* ansible_net_hostname - имя устройства

#VSLIDE
### Модуль ios_facts

* ansible_net_image - имя и путь ОС
* ansible_net_interfaces - словарь со всеми интерфейсами устройства. Имена интерфейсов - ключи, а данные - параметры каждого интерфейса
* ansible_net_memfree_mb - сколько свободной памяти на устройстве
* ansible_net_memtotal_mb - сколько памяти на устройстве
* ansible_net_model - модель устройства
* ansible_net_serialnum - серийный номер
* ansible_net_version - версия IOS

#VSLIDE
### Использование модуля

Пример playbook 1_ios_facts.yml с использованием модуля ios_facts (собираются все факты):
```
- name: Collect IOS facts
  hosts: cisco-routers

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
```

#VSLIDE
### Использование модуля

```
$ ansible-playbook 1_ios_facts.yml
```

![5_ios_facts](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5_ios_facts.png)


#VSLIDE
### Использование модуля

Для того, чтобы посмотреть, какие именно факты собираются с устройства, можно добавить флаг -v (информация сокращена):
```
$ ansible-playbook 1_ios_facts.yml -v
Using /home/nata/pyneng_course/chapter15/ansible.cfg as config file
```

![5_ios_facts](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5_ios_facts_verbose.png)

#VSLIDE
### Использование модуля

После того, как Ansible собрал факты с устройства, все факты доступны как переменные в playbook, шаблонах и т.д.


#VSLIDE
### Использование модуля

Например, можно отобразить содержимое факта с помощью debug (playbook 2_ios_facts_debug.yml):
```yml
- name: Collect IOS facts
  hosts: 192.168.100.1

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all

    - name: Show ansible_net_all_ipv4_addresses fact
      debug: var=ansible_net_all_ipv4_addresses

    - name: Show ansible_net_interfaces fact
      debug: var=ansible_net_interfaces['Ethernet0/0']
```

#VSLIDE
### Использование модуля

Результат выполнения playbook:
```
$ ansible-playbook 2_ios_facts_debug.yml
```

#VSLIDE

![5_ios_facts_debug](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5_ios_facts_debug.png)

#VSLIDE
### Сохранение фактов

В том виде, в котором информация отображается в режиме verbose, довольно сложно понять какая информация собирается об устройствах.
Для того, чтобы лучше понять какая информация собирается об устройствах, в каком формате, скопируем полученную информацию в файл.

Для этого будет использоваться модуль copy.

#VSLIDE
### Сохранение фактов

Playbook 3_ios_facts.yml:
```
- name: Collect IOS facts
  hosts: cisco-routers

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
      register: ios_facts_result

    #- name: Create all_facts dir
    #  file:
    #    path: ./all_facts/
    #    state: directory
    #    mode: 0755

    - name: Copy facts to files
      copy:
        content: "{{ ios_facts_result | to_nice_json }}"
        dest: "all_facts/{{inventory_hostname}}_facts.json"
```

#VSLIDE
### Сохранение фактов

Модуль copy позволяет копировать файлы с управляющего хоста (на котором установлен Ansible) на удаленный хост.
Но, так как в этом случае, указан параметр ```connection: local```, файлы будут скопированы на локальный хост.

Чаще всего, модуль copy используется таким образом:
```
- copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
```

#VSLIDE
### Сохранение фактов

Но, в данном случае, нет исходного файла, содержимое которого нужно скопировать.
Вместо этого, есть содержимое переменной ios_facts_result, которое нужно перенести в файл all_facts/{{inventory_hostname}}_facts.json.

Для того чтобы перенести содержимое переменной в файл, в модуле copy, вместо src, используется параметр content.

#VSLIDE
### Сохранение фактов

```
content: "{{ ios_facts_result | to_nice_json }}"
```
Параметр to_nice_json - это фильтр Jinja2, который преобразует информацию переменной в формат, в котором удобней читать информацию.
Переменная в формате Jinja2 должна быть заключена в двойные фигурные скобки, а также указана в двойных кавычках.

Так как в пути dest используются имена устройств, будут сгенерированы уникальные файлы для каждого устройства.


#VSLIDE

Результат выполнения playbook:
```
$ ansible-playbook 3_ios_facts.yml
```

![5a_ios_facts](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5a_ios_facts.png)

#VSLIDE
### Сохранение фактов

После этого, в каталоге all_facts находятся такие файлы:
```
192.168.100.1_facts.json
192.168.100.2_facts.json
192.168.100.3_facts.json
```

#VSLIDE
### Сохранение фактов

Содержимое файла all_facts/192.168.100.1_facts.json:
```
{
    "ansible_facts": {
        "ansible_net_all_ipv4_addresses": [
            "192.168.200.1",
            "192.168.100.1",
            "10.1.1.1"
        ],
        "ansible_net_all_ipv6_addresses": [],
        "ansible_net_config": "Building configuration...\n\nCurrent configuration :
...
```

#VSLIDE
### Сохранение фактов

Сохранение информации об устройствах, не только поможет разобраться, какая информация собирается, но и может быть полезным для дальнейшего использования информации.
Например, можно использовать факты об устройстве в шаблоне.


При повторном выполнении playbook, Ansible не будет изменять информацию в файлах, если факты об устройстве не изменились

#VSLIDE
### Сохранение фактов

Если информация изменилась, для соответствующего устройства, будет выставлен статус changed.
Таким образом, по выполнению playbook всегда понятно, когда какая-то информация изменилась.

#VSLIDE

Повторный запуск playbook (без изменений):
```
$ ansible-playbook 3_ios_facts.yml
```

#VSLIDE

![5a_ios_facts](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5a_ios_facts_no_change.png)


#HSLIDE
## Модуль ios_config

#VSLIDE
### Модуль ios_config

Модуль ios_config - позволяет настраивать устройства под управлением IOS, а также, генерировать шаблоны конфигураций или отправлять команды на основании шаблона.

#VSLIDE
### Модуль ios_config

Параметры модуля:
* __after__ - какие действия выполнить после команд
* __before__ - какие действия выполнить до команд
* __backup__ - параметр, который указывает нужно ли делать резервную копию текущей конфигурации устройства перед внесением изменений. Файл будет копироваться в каталог backup, относительно каталога в котором находится playbook
* __config__ - параметр, который позволяет указать базовый файл конфигурации, с которым будут сравниваться изменения. Если он указан, модуль не будет скачивать конфигурацию с устройства.

#VSLIDE
## Модуль ios_config

* __defaults__ - параметр указывает нужно ли собирать всю информацию с устройства, в том числе, и значения по умолчанию. Если включить этот параметр, то модуль будет собирать текущую кофигурацию с помощью команды sh run all. По умолчанию этот параметр отключен и конфигурация проверяется командой sh run
* __lines (commands)__ - список команд, которые должны быть настроены. Команды нужно указывать без сокращений и ровно в том виде, в котором они будут в конфигурации.
* __match__ - параметр указывает как именно нужно сравнивать команды

#VSLIDE
### Модуль ios_config

* __parents__ - название секции, в которой нужно применить команды. Если команда находится внутри вложенной секции, нужно указывать весь путь. Если этот параметр не указан, то считается, что команда должны быть в глобальном режиме конфигурации
* __replace__ - параметр указывает как выполнять настройку устройства
* __save__ - сохранять ли текущую конфигурацию в стартовую. По умолчанию конфигурация не сохраняется
* __src__ - параметр указывает путь к файлу, в котором находится конфигурация или шаблон конфигурации. Взаимоисключающий параметр с lines (то есть, можно указывать или lines или src). Заменяет модуль ios_template, который скоро будет удален.

#HSLIDE
### Модуль ios_config
### Параметр lines (commands)

#VSLIDE
### lines (commands)

Самый простой способ использовать модуль ios_config - отправлять команды глобального конфигурационного режима с параметром lines.

Для параметра lines есть alias commands, то есть, можно вместо lines писать commands.

#VSLIDE
### lines (commands)

Пример playbook 1_ios_config_lines.yml:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config password encryption
      ios_config:
        lines:
          - service password-encryption
```

#VSLIDE
### lines (commands)

Результат выполнения playbook:
```
$ ansible-playbook 1_ios_config_lines.yml
```

![6_ios_config_lines](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6_ios_config_lines.png)

#VSLIDE
### lines (commands)

Ansible выполняет такие команды:
* terminal length 0
* enable
* show running-config - чтобы проверить есть ли эта команда на устройстве. Если команда есть, задача выполняться не будет. Если команды нет, задача выполнится
* если команды, которая указана в задаче нет в конфигурации:
 * configure terminal
 * service password-encryption
 * end

#VSLIDE
### lines (commands)

Так как модуль каждый раз проверяет конфигурацию, прежде чем применит команду, модуль идемпотентен.
То есть, если ещё раз запустить playbook, изменения не будут выполнены:
```
$ ansible-playbook 1_ios_config_lines.yml
```

![6_ios_config_lines](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6_ios_config_lines_2.png)

#VSLIDE
### lines (commands)

Параметр lines позволяет отправлять и несколько команд (playbook 1_ios_config_mult_lines.yml):
```
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Send config commands
      ios_config:
        lines:
          - service password-encryption
          - no ip http server
          - no ip http secure-server
          - no ip domain lookup
```

#VSLIDE
### lines (commands)

Результат выполнения:
```
$ ansible-playbook 1_ios_config_mult_lines.yml
```

![6_ios_config_mult_lines](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6_ios_config_mult_lines.png)

#HSLIDE
### Модуль ios_config
### Параметр parents

#VSLIDE
### parents

Параметр parents используется, чтобы указать в каком подрежиме применить команды.

Например, необходимо применить такие команды:
```
line vty 0 4
 login local
 transport input ssh
```

#VSLIDE
### parents

В таком случае, playbook 2_ios_config_parents_basic.yml будет выглядеть так:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh

```

#VSLIDE
### parents

Запуск будет выполняться аналогично предыдущим playbook:
```
$ ansible-playbook 2_ios_config_parents_basic.yml
```

![6a_ios_config_parents_basic](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6a_ios_config_parents_basic.png)

#VSLIDE
### parents

Если команда находится в нескольких вложенных режимах, подрежимы указываются в списке parents.

Например, необходимо выполнить такие команды:
```
policy-map OUT_QOS
 class class-default
  shape average 100000000 1000000
```

#VSLIDE
### parents

Тогда playbook 2_ios_config_parents_mult.yml будет выглядеть так:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config QoS policy
      ios_config:
        parents:
          - policy-map OUT_QOS
          - class class-default
        lines:
          - shape average 100000000 1000000
```

#HSLIDE
### Модуль ios_config
### Отображение обновлений

#VSLIDE
### Отображение обновлений

Playbook 2_ios_config_parents_basic.yml:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh

```

#VSLIDE
### Отображение обновлений

Например, можно выполнить playbook с флагом verbose:
```
$ ansible-playbook 2_ios_config_parents_basic.yml -v
```

![6a_ios_config_parents_basic](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6a_ios_config_parents_basic_verbose.png)

#VSLIDE
### Отображение обновлений

В выводе, в поле updates видно, какие именно команды Ansible отправил на устройство.
Изменения были выполнены только на маршрутизаторе 192.168.100.1.

Обратите внимание, что команда login local не отправлялась, так как она настроена.

Поле updates в выводе есть только в том случае, когда есть изменения.

#VSLIDE
### Отображение обновлений

В режиме verbose, информация видна обо всех устройствах.
Но, было бы удобней, чтобы информация отображалась только для тех устройств, для которых произошли изменения.

#VSLIDE
### Отображение обновлений

Новый playbook 3_ios_config_debug.yml на основе 2_ios_config_parents_basic.yml:
```
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
      register: cfg

    - name: Show config updates
      debug: var=cfg.updates
      when: cfg.changed

```

#VSLIDE
### Отображение обновлений

Изменения в playbook:
* результат работы первой задачи сохраняется в переменную __cfg__.
* в следующей задаче модуль __debug__ выводит содержимое поля __updates__.
 * но так как поле updates в выводе есть только в том случае, когда есть изменения, ставится условие when, которое проверяет были ли изменения
 * задача будет выполняться только если на устройстве были внесены изменения.
 * вместо ```when: cfg.changed``` можно написать ```when: cfg.changed == true```

#VSLIDE
### Отображение обновлений

Если запустить повторно playbook, когда изменений не было, задача Show config updates, пропускается:
```
$ ansible-playbook 3_ios_config_debug.yml
```

![6b_ios_config_debug_skipping](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6b_ios_config_debug_skipping.png)

#VSLIDE
### Отображение обновлений

Если внести изменения в конфигурацию маршрутизатора 192.168.100.1 (изменить transport input ssh на transport input all):
```
$ ansible-playbook 3_ios_config_debug.yml
```

![6b_ios_config_debug_update](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6b_ios_config_debug_update.png)

Теперь второе задание отображает информацию о том, какие именно изменения были внесены на маршрутизаторе.

#HSLIDE
### Модуль ios_config
### save_when

#VSLIDE
### save_when

Параметр __save_when__ позволяет указать нужно ли сохранять текущую конфигурацию в стартовую.

Доступные варианты значений:
* always - всегда сохранять конфигурацию (в этом случае флаг modified будет равен True)
* never (по умолчанию) - не сохранять конфигурацию
* modified - в этом случае конфигурация сохраняется только при наличии изменений

#VSLIDE
### save_when

К сожалению, на данный момент (версия ansible 2.4), этот параметр не отрабатывает корректно, так как на устройство отправляется команда copy running-config startup-config, но, при этом, не отправляется подтверждение на сохранение.
Из-за этого, при запуске playbook с параметром save_when выставленным в always или modified, появляется такая ошибка:
```
fatal: [192.168.100.2]: FAILED! => {"changed": false, "failed": true,
"msg": "timeout trying to send command: b'copy running-config startup-config'", "rc": 1}
```

#VSLIDE
### save_when

Исправить это достаточно легко, настроив в IOS:
```
file prompt quiet
```

По умолчанию настроено ```file prompt alert```


#VSLIDE
### save_when

Playbook 4_ios_config_save_when.yml
```
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        save_when: modified
```

#VSLIDE
### save_when

Вариант самостоятельного сохранения 4_ios_config_save.yml:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
      register: cfg

    - name: Save config
      ios_command:
        commands:
          - write
      when: cfg.changed
```

#VSLIDE
### save_when


#HSLIDE
### Модуль ios_config
### Параметр backup

#VSLIDE
### backup

Параметр __backup__ указывает нужно ли делать резервную копию текущей конфигурации устройства перед внесением изменений.
Файл будет копироваться в каталог backup, относительно каталога в котором находится playbook (если каталог не существует, он будет создан).

#VSLIDE
### backup

Playbook 5_ios_config_backup.yml:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        backup: yes
```

#VSLIDE
### backup

Теперь, каждый раз, когда выполняется playbook (даже если не нужно вносить изменения в конфигурацию), в каталог backup будет копироваться текущая конфигурация:
```
$ ansible-playbook 5_ios_config_backup.yml -v
```

![6d_ios_config_backup](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6d_ios_config_backup.png)

#VSLIDE
### backup

В каталоге backup теперь находятся файлы такого вида (при каждом запуске playbook они перезаписываются):
```
192.168.100.1_config.2016-12-10@10:42:34
192.168.100.2_config.2016-12-10@10:42:34
192.168.100.3_config.2016-12-10@10:42:34
```

#HSLIDE
### Модуль ios_config
### Параметр defaults

#VSLIDE
### defaults

Параметр __defaults__ указывает нужно ли собирать всю информацию с устройства, в том числе и значения по умолчанию.
Если включить этот параметр, модуль будет собирать текущую кофигурацию с помощью команды sh run all.
По умолчанию этот параметр отключен и конфигурация проверяется командой sh run.

Этот параметр полезен в том случае, если в настройках указывается команда, которая не видна в конфигурации.
Например, такое может быть, когда указан параметр, который и так используется по умолчанию.

#VSLIDE
### defaults

Если не использовать параметр defaults, и указать команду, которая настроена по умолчанию, то  при каждом запуске playbook, будут вноситься изменения.

Присходит это потому, что Ansible каждый раз вначале проверяет наличие команд в соответствующем режиме.
Если команд нет, то соответствующая задача выполняется.

#VSLIDE
### defaults

Например, в таком playbook, каждый раз будут вноситься изменения (попробуйте запустить его самостоятельно):
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/2
        lines:
          - ip address 192.168.200.1 255.255.255.0
          - ip mtu 1500
```

#VSLIDE
### defaults

Если добавить параметр ```defaults: yes```, изменения уже не будут внесены, если не хватало только команды ip mtu 1500 (playbook 6_ios_config_defaults.yml):
```
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/2
        lines:
          - ip address 192.168.200.1 255.255.255.0
          - ip mtu 1500
        defaults: yes
```

#VSLIDE
### defaults

Запуск playbook:
```
$ ansible-playbook 6_ios_config_defaults.yml
```

![6e_ios_config_default](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6e_ios_config_defaults.png)

#HSLIDE
### Модуль ios_config
### Параметр after

#VSLIDE
### after

Параметр __after__ указывает какие команды выполнить после команд в списке lines (или commands).

Команды, которые указаны в параметре after:
* выполняются только если должны быть внесены изменения.
* при этом они будут выполнены, независимо от того есть они в конфигурации или нет.

#VSLIDE
### after

Параметр after очень полезен в ситуациях, когда необходимо выполнить команду, которая не сохраняется в конфигурации.

Например, команда no shutdown не сохраняется в конфигурации маршрутизатора.
И, если добавить её в список lines, изменения будут вноситься каждый раз, при выполнении playbook. 

Но, если написать команду no shutdown в списке after, то она будет применена только в том случае, если нужно вносить изменения (согласно списка lines).

#VSLIDE
### after

Пример использования параметра after в playbook 7_ios_config_after.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config interface
      ios_config:
        parents:
          - interface Ethernet0/3
        lines:
          - ip address 192.168.230.1 255.255.255.0
        after:
          - no shutdown
```

#VSLIDE
### after

Первый запуск playbook, с внесением изменений:
```
$ ansible-playbook 7_ios_config_after.yml -v
```

![6f_ios_config_after.png](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6f_ios_config_after.png)

#VSLIDE
### after

Второй запуск playbook (изменений нет, поэтому команда no shutdown не выполняется):
```
$ ansible-playbook 7_ios_config_after.yml -v
```
![6f_ios_config_after_no_change](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6f_ios_config_after_no_change.png)

#VSLIDE
### after

С помощью after можно сохранять конфигурацию устройства (playbook 7_ios_config_after_save.yml):
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers

  tasks:

    - name: Config line vty
      ios_config:
        parents:
          - line vty 0 4
        lines:
          - login local
          - transport input ssh
        after:
          - end
          - write
```

#VSLIDE
### after

Результат выполнения playbook (изменения только на маршрутизаторе 192.168.100.1):
```
$ ansible-playbook 7_ios_config_after_save.yml -v
```
![6f_ios_config_after_save](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6f_ios_config_after_save.png)


#HSLIDE
### Модуль ios_config
### Параметр before

#VSLIDE
### before

Параметр __before__ указывает какие действия выполнить до команд в списке lines.

Команды, которые указаны в параметре before:
* выполняются только если должны быть внесены изменения.
* при этом они будут выполнены, независимо от того есть они в конфигурации или нет.

#VSLIDE
### before

Параметр before полезен в ситуациях, когда какие-то действия необходимо выполнить перед выполнением команд в списке lines.

При этом, как и after, параметр before не влияет на то, какие команды сравниваются с конфигурацией.
То есть, по-прежнему, сравниваются только команды в списке lines.

#VSLIDE
### before

Playbook 8_ios_config_before.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
```

#VSLIDE
### before

В playbook 8_ios_config_before.yml ACL IN_to_OUT сначала удалятся, с помощью параметра before, а затем создается заново.

Таким образом в ACL всегда находятся только те строки, которые заданы в списке lines.

#VSLIDE
### before

Запуск playbook с изменениями:
```
$ ansible-playbook 8_ios_config_before.yml -v
```
![6g_ios_config_before](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6g_ios_config_before.png)

#VSLIDE
### before

Запуск playbook без изменений (команда в списке before не выполняется):
```
$ ansible-playbook 8_ios_config_before.yml -v
```
![6g_ios_config_before_no_updates](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6g_ios_config_before_no_updates.png)


#HSLIDE
### Модуль ios_config
### Параметр match

#VSLIDE
### match

Параметр __match__  указывает как именно нужно сравнивать команды (что считается изменением):
* __line__ - команды проверяются построчно. Этот режим используется по умолчанию
* __strict__ - должны совпасть не только сами команды, но их положение относительно друг друга
* __exact__ - команды должны в точности сопадать с конфигурацией и не должно быть никаких лишних строк
* __none__ - модуль не будет сравнивать команды с текущей конфигурацией

#VSLIDE
### match: line

Режим ```match: line``` используется по умолчанию.

В этом режиме, модуль проверяет только наличие строк, перечисленных в списке lines в соответствующем режиме.
При этом, не проверяется порядок строк.

#VSLIDE
### match: line

На маршрутизаторе 192.168.100.1 настроен такой ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
```

#VSLIDE
### match: line

Пример использования playbook 9_ios_config_match_line.yml в режиме line:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
```

#VSLIDE
### match: line

Результат выполнения playbook:
```
$ ansible-playbook 9_ios_config_match_line.yml -v
```
![6h_ios_config_match_line](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_line.png)


#VSLIDE
### match: line

Обратите внимание, что в списке updates только две из трёх строк ACL.
Так как в режиме lines модуль сравнивает команды независимо друг от друга, он обнаружил, что не хватает только двух команд из трех.

#VSLIDE
### match: line

В итоге конфигурация на маршрутизаторе выглядит так:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit icmp any any
```

То есть, порядок команд поменялся.
И, хотя в этом случае, это не важно, иногда это может привести совсем не к тем результатам, которые ожидались.

Если повторно запустить playbook, при такой конфигурации, он не будет выполнять изменения, так как все строки были найдены.

#VSLIDE
### match: exact
Пример, в котором порядок команд важен.

ACL на маршрутизаторе:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 deny   ip any any
```

#VSLIDE
### match: exact

Playbook 9_ios_config_match_exact.yml (будет постепенно дополняться):
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
```

#VSLIDE
### match: exact

Если запустить playbook, результат будет таким:
```
$ ansible-playbook 9_ios_config_match_exact.yml -v
```
![6h_ios_config_match_exact](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_exact_1.png)

#VSLIDE
### match: exact

Теперь ACL выглядит так:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 deny   ip any any
 permit icmp any any
```

Конечно же, в таком случае, последнее правило никогда не сработает.


#VSLIDE
### match: exact

Можно добавить к этому playbook параметр before и сначала удалить ACL, а затем применять команды:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
```

Если применить playbook к последнему состоянию маршрутизатора, то изменений не будет никаких, так как все строки уже есть.

#VSLIDE
### match: exact

Попробуем начать с такого состояния ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 deny   ip any any
```

#VSLIDE
### match: exact

Результат будет таким:
```
$ ansible-playbook 9_ios_config_match_exact.yml -v
```
![6h_ios_config_match_exact](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_exact_2.png)

#VSLIDE
### match: exact

И, соответственно, на маршрутизаторе:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit icmp any any
```

#VSLIDE
### match: exact

Теперь в ACL осталась только одна строка:
* Модуль проверил каких команд не хватает в ACL (так как режим по умолчанию match: line),
* обнаружил, что не хватает команды ```permit icmp any any``` и добавил её

Но, так как в playbook ACL сначала удаляется, а затем применяется список команд lines, получилось, что в итоге в ACL одна строка.

#VSLIDE
### match: exact

Поможет, в такой ситуации, вариант ```match: exact```:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
        match: exact
```

#VSLIDE
### match: exact

Применение playbook 9_ios_config_match_exact.yml к текущему состоянию маршрутизатора (в ACL одна строка):
```
$ ansible-playbook 9_ios_config_match_exact.yml -v
```
![6h_ios_config_match_exact](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_exact_final.png)

#VSLIDE
### match: exact

Теперь результат такой:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

То есть, теперь ACL выглядит точно так же, как и строки в списке lines и в том же порядке.

#VSLIDE
### match: exact

Закомментируем в playbook строки с удалением ACL:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        #before:
        #  - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
        match: exact
```

#VSLIDE
### match: exact

В начало ACL добавлена строка:
```
ip access-list extended IN_to_OUT
 permit udp any any
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

#VSLIDE
### match: exact

То есть, последние 4 строки выглядят так, как нужно, и в том порядке, котором нужно.
Но, при этом, есть лишняя строка.
Для варианта match: exact - это уже несовпадение.

#VSLIDE
### match: exact

В таком варианте, playbook будет выполняться каждый раз и пытаться применить все команды из списка lines, что не будет влиять на содержимое ACL:
```
$ ansible-playbook 9_ios_config_match_exact.yml -v
```
![6h_ios_config_match_exact](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_exact_final_2.png)

#VSLIDE
### match: exact

Это значит, что при использовании ```match:exact```, важно, чтобы был какой-то способ удалить конфигурацию, если она не соответствует тому, что должно быть (или чтобы команды перезаписывались).
Иначе, эта задача будет выполняться каждый раз, при запуске playbook.

#VSLIDE
### match: strict

Вариант ```match: strict``` не требует, чтобы объект был в точности как указано в задаче, но, команды, которые указаны в списке lines, должны быть в том же порядке.

Если указан список parents, команды в списке lines должны идти сразу за командами parents.

#VSLIDE
### match: strict

На маршрутиазаторе такой ACL:
```
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

#VSLIDE
### match: strict

Playbook 9_ios_config_match_strict.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
        match: strict
```

#VSLIDE
### match: strict

Выполнение playbook:
```
$ ansible-playbook 9_ios_config_match_strict.yml -v
```
![6h_ios_config_match_strict](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_strict.png)

#VSLIDE
### match: strict
Так как изменений не было, ACL остался таким же.

В такой же ситуации, при использовании ```match: exact```, было бы обнаружено изменение и ACL бы состоял только из строк в списке lines.


#VSLIDE
### match: none

Использование ```match: none``` отключает идемпотентность задачи: каждый раз при выполнении playbook, будут отправляться команды, которые указаны в задаче.


#VSLIDE
### match: none

Пример playbook 9_ios_config_match_none.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
        match: none
```

#VSLIDE
### match: none

Каждый раз при запуске playbook результат будет таким:
```
$ ansible-playbook 9_ios_config_match_none.yml -v
```
![6h_ios_config_match_none](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6h_ios_config_match_none.png)


Использование ```match: none``` подходит в тех случаях, когда, независимо от текущей конфигурации, нужно отправить все команды.



#HSLIDE
### Модуль ios_config
### Параметр replace

#VSLIDE
### replace

Параметр replace указывает как именно нужно заменять конфигурацию:
* __line__ - в этом режиме отправляются только те команды, которых нет в конфигурации. Этот режим используется по умолчанию
* __block__ - в этом режиме отправляются все команды, если хотя бы одной команды нет

#VSLIDE
### replace: line

Режим ```replace: line``` - это режим работы по умолчанию.
В этом режиме, если были обнаружены изменения, отправляются только недостающие строки.

Например, на маршрутизаторе такой ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
```

#VSLIDE
### replace: line

Попробуем запустить такой playbook 10_ios_config_replace_line.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
```

#VSLIDE
### replace: line

Выполнение playbook:
```
$ ansible-playbook 10_ios_config_replace_line.yml -v
```
![6i_ios_config_replace_line](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6i_ios_config_replace_line.png)

#VSLIDE
### replace: line

После этого на маршрутизаторе такой ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 deny   ip any any
```

#VSLIDE
### replace: line

В данном случае, модуль проверил каких команд не хватает в ACL (так как режим по умолчанию match: line), обнаружил, что не хватает команды ```deny ip any any``` и добавил её.
Но, так как ACL сначала удаляется, а затем применяется список команд lines, получилось, что у теперь ACL с одной строкой.

В таких ситуациях  подходит режим ```replace: block```.

#VSLIDE
### replace: block

В режиме ```replace: block``` отправляются все команды из списка lines (и parents), если на устройстве нет хотя бы одной из этих команд.

Повторим предыдущий пример.

#VSLIDE
### replace: block

ACL на маршрутизаторе:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
```

#VSLIDE
### replace: block

Playbook 10_ios_config_replace_block.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        before:
          - no ip access-list extended IN_to_OUT
        parents:
          - ip access-list extended IN_to_OUT
        lines:
          - permit tcp 10.0.1.0 0.0.0.255 any eq www
          - permit tcp 10.0.1.0 0.0.0.255 any eq 22
          - permit icmp any any
          - deny   ip any any
        replace: block
```

#VSLIDE
### replace: block

Выполнение playbook:
```
$ ansible-playbook 10_ios_config_replace_block.yml -v
```
![6i_ios_config_replace_block](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6i_ios_config_replace_block.png)

#VSLIDE
### replace: block

В результате на маршрутизаторе такой ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

#HSLIDE
### Модуль ios_config
### Параметр src

#VSLIDE
### src

Параметр __src__ позволяет указывать путь к файлу конфигурации или шаблону конфигурации, которую нужно загрузить на устройство.

Этот параметр взаимоисключающий с lines (то есть, можно указывать или lines или src). Он заменяет модуль ios_template, который скоро будет удален.

#VSLIDE
### Конфигурация

Пример playbook 11_ios_config_src.yml:
```yml
- name: Run cfg commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Config ACL
      ios_config:
        src: templates/acl_cfg.txt
```

#VSLIDE
### src

В файле templates/acl_cfg.txt находится такая конфигурация:
```
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

#VSLIDE
### src

Удаляем на маршрутизаторе этот ACL, если он остался с прошлых разделов, и запускаем playbook:
```
$ ansible-playbook 11_ios_config_src.yml -v
```
![6j_ios_config_src](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6j_ios_config_src.png)

#VSLIDE
### src

Неприятная особенность параметра src в том, что не видно какие изменения были внесены.
Но, возможно, в следующих версиях Ansible это будет исправлено.

#VSLIDE
### src

Теперь на маршрутизаторе настроен ACL:
```
R1#sh run | s access
ip access-list extended IN_to_OUT
 permit tcp 10.0.1.0 0.0.0.255 any eq www
 permit tcp 10.0.1.0 0.0.0.255 any eq 22
 permit icmp any any
 deny   ip any any
```

#VSLIDE
### src

Если запустить playbook ещё раз, но никаких изменений не будет, так как этот параметр также идемпотентен:
```
$ ansible-playbook 11_ios_config_src.yml -v
```
![6j_ios_config_src_2](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6j_ios_config_src_2.png)


#VSLIDE
### Шаблон Jinja2

В параметре src можно указывать шаблон Jinja2.

Пример шаблона (файл templates/ospf.j2):
```j2
router ospf 1
 router-id {{ mgmnt_ip }}
 ispf
 auto-cost reference-bandwidth 10000
{% for ip in ospf_ints %}
 network {{ ip }} 0.0.0.0 area 0
{% endfor %}
```

#VSLIDE
### Шаблон Jinja2

В шаблоне используются две переменные:
* mgmnt_ip - IP-адрес, который будет использоваться как router-id
* ospf_ints - список IP-адресов интерфейсов, на которых нужно включить OSPF

Для настройки OSPF на трёх маршрутизаторах, нужно иметь возможность использовать разные значения этих переменных для разных устройств.
Для таких задач используются файлы с переменными в каталоге host_vars.

В каталоге host_vars нужно создать такие файлы (если они ещё не созданы):

#VSLIDE
### src

Файл host_vars/192.168.100.1:
```
hostname: london_r1
mgmnt_loopback: 100
mgmnt_ip: 10.0.0.1
ospf_ints:
  - 192.168.100.1
  - 10.0.0.1
  - 10.255.1.1
```

#VSLIDE
### src

Файл host_vars/192.168.100.2:
```
hostname: london_r2
mgmnt_loopback: 100
mgmnt_ip: 10.0.0.2
ospf_ints:
  - 192.168.100.2
  - 10.0.0.2
  - 10.255.2.2
```

#VSLIDE
### src

Файл host_vars/192.168.100.3:
```
hostname: london_r3
mgmnt_loopback: 100
mgmnt_ip: 10.0.0.3
ospf_ints:
  - 192.168.100.3
  - 10.0.0.3
  - 10.255.3.3
```

#VSLIDE
### src

Теперь можно создавать playbook 11_ios_config_src_jinja.yml:
```yml
- name: Run cfg commands on router
  hosts: cisco-routers

  tasks:

    - name: Config OSPF
      ios_config:
        src: templates/ospf.j2
```

#VSLIDE
### src

Так как Ansible сам найдет переменные в каталоге host_vars, их не нужно указывать.
Можно сразу запускать playbook:
```
$ ansible-playbook 11_ios_config_src_jinja.yml -v
```
![6j_ios_config_src_jinja](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6j_ios_config_src_jinja.png)


#VSLIDE
### src

Теперь на всех маршрутизаторах настроен OSPF:
```
R1#sh run | s ospf
router ospf 1
 router-id 10.0.0.1
 ispf
 auto-cost reference-bandwidth 10000
 network 10.0.0.1 0.0.0.0 area 0
 network 10.255.1.1 0.0.0.0 area 0
 network 192.168.100.1 0.0.0.0 area 0

R2#sh run | s ospf
router ospf 1
 router-id 10.0.0.2
 ispf
 auto-cost reference-bandwidth 10000
 network 10.0.0.2 0.0.0.0 area 0
 network 10.255.2.2 0.0.0.0 area 0
 network 192.168.100.2 0.0.0.0 area 0

router ospf 1
 router-id 10.0.0.3
 ispf
 auto-cost reference-bandwidth 10000
 network 10.0.0.3 0.0.0.0 area 0
 network 10.255.3.3 0.0.0.0 area 0
 network 192.168.100.3 0.0.0.0 area 0
```

#VSLIDE
### src

Если запустить playbook ещё раз, но никаких изменений не будет:
```
$ ansible-playbook 11_ios_config_src_jinja.yml -v
```
![6j_ios_config_src_jinja_2](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/6j_ios_config_src_jinja_2.png)

#VSLIDE
### Совмещение с другими параметрами

Параметр __src__ совместим с такими параметрами:
* backup
* config
* defaults
* save (но у самого save в Ansible 2.2 проблемы с работой) 

#HSLIDE
### Модуль ntc-ansible

#VSLIDE
### ntc-ansible

__ntc-ansible__ - это модуль для работы с сетевым оборудованием, который не только выполняет команды на оборудовании, но и обрабатывает вывод команд и преобразует с помощью TextFSM

Этот модуль не входит в число core модулей Ansible, поэтому его нужно установить.

#VSLIDE
### ntc-ansible

Но прежде нужно указать Ansible, где искать сторонние модули.
Указывается путь в файле ansible.cfg:
```
[defaults]

inventory = ./myhosts

remote_user = cisco
ask_pass = True

library = ./library
```

#VSLIDE
### ntc-ansible

После этого, нужно клонировать репозиторий ntc-ansible, находясь в каталоге library:
```
[~/pyneng_course/chapter15/library]
$ git clone https://github.com/networktocode/ntc-ansible --recursive
Cloning into 'ntc-ansible'...
remote: Counting objects: 2063, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 2063 (delta 1), reused 0 (delta 0), pack-reused 2058
Receiving objects: 100% (2063/2063), 332.15 KiB | 334.00 KiB/s, done.
Resolving deltas: 100% (1157/1157), done.
Checking connectivity... done.
Submodule 'ntc-templates' (https://github.com/networktocode/ntc-templates) registered for path 'ntc-templates'
Cloning into 'ntc-templates'...
remote: Counting objects: 902, done.
remote: Compressing objects: 100% (34/34), done.
remote: Total 902 (delta 16), reused 0 (delta 0), pack-reused 868
Receiving objects: 100% (902/902), 161.11 KiB | 0 bytes/s, done.
Resolving deltas: 100% (362/362), done.
Checking connectivity... done.
Submodule path 'ntc-templates': checked out '89c57342b47c9990f0708226fb3f268c6b8c1549'
```

#VSLIDE
### ntc-ansible

А затем установить зависимости модуля:
```
pip install ntc-ansible
```

#VSLIDE
### ntc-ansible

Так как в текущей версии Ansible уже есть модули, которые работают с сетевым оборудованием и позволяют выполнять команды, из всех возможностей ntc-ansible, наиболее полезной будет отправка команд show и получение структурированного вывода.
За это отвечает модуль ntc_show_command.

#VSLIDE
### ntc_show_command

Модуль использует netmiko для подключения к оборудованию (netmiko должен быть установлен) и, после выполнения команды, преобразует вывод команды show с помощью TextFSM в структурированный вывод (список словарей).

Преобразование будет выполняться в том случае, если в файле index была найдена команда и для команды был найден шаблон.

#VSLIDE
### ntc_show_command

Параметры для подключения:
* __connection__ - тут возможны два варианта: ssh (подключение netmiko) или offline (чтение из файла для тестовых целей)
* __platform__ - платформа, которая существует в index файле (library/ntc-ansible/ntc-templates/templates/index)
* __command__ - команда, которую нужно выполнить на устройстве
* __host__ - IP-адрес или имя устройства
* __username__ - имя пользователя
* __password__ - пароль
* __template_dir__ - путь к каталогу с шаблонами (library/ntc-ansible/ntc-templates/templates

#VSLIDE
### ntc_show_command

Пример playbook 1_ntc_ansible.yml:
```
- name: Run show commands on router
  hosts: 192.168.100.1

  tasks:

    - name: Run sh ip int br
      ntc_show_command:
        connection: ssh
        platform: "cisco_ios"
        command: "sh ip int br"
        host: "{{ inventory_hostname }}"
        username: "cisco"
        password: "cisco"
        template_dir: "library/ntc-ansible/ntc-templates/templates"
      register: result

    - debug: var=result
```

#VSLIDE
### ntc_show_command

Результат выполнения playbook:
```
$ ansible-playbook 1_ntc-ansible.yml
```

#VSLIDE

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/7_ntc_ansible.png)


#VSLIDE
### ntc_show_command

В переменной response находится структурированный вывод в виде списка словарей.
Ключи в словарях получены на основании переменных, которые описаны в шаблоне library/ntc-ansible/ntc-templates/templates/cisco_ios_show_ip_int_brief.template (единственное отличие - регистр):
```
Value INTF (\S+)
Value IPADDR (\S+)
Value STATUS (up|down|administratively down)
Value PROTO (up|down)

Start
  ^${INTF}\s+${IPADDR}\s+\w+\s+\w+\s+${STATUS}\s+${PROTO} -> Record
```

#VSLIDE
### ntc_show_command

Для того, чтобы получить вывод про первый интерфейс, можно поменять вывод модуля debug, таким образом:
```
    - debug: var=result.response[0]
```

#VSLIDE

Пример playbook 2_ntc_ansible_save.yml с сохранением результатов команды:
```
- name: Run show commands on routers
  hosts: cisco-routers

  tasks:

    - name: Run sh ip int br
      ntc_show_command:
        connection: ssh
        platform: "cisco_ios"
        command: "sh ip int br"
        host: "{{ inventory_hostname }}"
        username: "cisco"
        password: "cisco"
        template_dir: "library/ntc-ansible/ntc-templates/templates"
      register: result

    - name: Copy facts to files
      copy:
        content: "{{ result.response | to_nice_json }}"
        dest: "all_facts/{{inventory_hostname}}_sh_ip_int_br.json"
```

#VSLIDE
### Сохранение результатов выполнения команды

Результат выполнения:
```
$ ansible-playbook 2_ntc-ansible_save.yml
```

#VSLIDE
### Сохранение результатов выполнения команды

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/7a_ntc_ansible_save.png)

#VSLIDE
### Сохранение результатов выполнения команды

В результате, в каталоге all_facts появляются соответствующие файлы для каждого маршрутизатора.
Пример файла all_facts/192.168.100.1_sh_ip_int_br.json:
```
[
    {
        "intf": "Ethernet0/0",
        "ipaddr": "192.168.100.1",
        "proto": "up",
        "status": "up"
    },
    {
        "intf": "Ethernet0/1",
        "ipaddr": "192.168.200.1",
        "proto": "up",
        "status": "up"
    },
    {
        "intf": "Ethernet0/2",
        "ipaddr": "unassigned",
        "proto": "down",
        "status": "administratively down"
    },
...
```

#VSLIDE
### Шаблоны Jinja2

Для Cisco IOS в ntc-ansible есть такие шаблоны:
```
cisco_ios_dir.template
cisco_ios_show_access-list.template
cisco_ios_show_aliases.template
cisco_ios_show_archive.template
cisco_ios_show_capability_feature_routing.template
cisco_ios_show_cdp_neighbors_detail.template
cisco_ios_show_cdp_neighbors.template
cisco_ios_show_clock.template
...
```

#VSLIDE
### Шаблоны Jinja2

Список всех шаблонов можно посмотреть локально, если ntc-ansible установлен:
```
ls -ls library/ntc-ansible/ntc-templates/templates/
```

Или в [репозитории проекта](https://github.com/networktocode/ntc-templates/tree/master/templates).

#VSLIDE
### Шаблоны Jinja2

Используя TextFSM можно самостоятельно создавать дополнительные шаблоны.

И, для того, чтобы ntc-ansible их использовал автоматически, добавить их в файл index (library/ntc-ansible/ntc-templates/templates/index)
