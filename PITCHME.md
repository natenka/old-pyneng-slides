# Python для сетевых инженеров 

#HSLIDE

# Ansible

#VSLIDE
### Ansible

Ansible - это система управления конфигурациями. Ansible позволяет автоматизировать и упростить настройку, обслуживание и развертывание серверов, служб, ПО и др.

Ansible активно развивается в сторону поддержки сетевого оборудования и постоянно появляются новые возможности и модули для работы с сетевым оборудованием.

#VSLIDE
### Ansible

Примеры задач, которые поможет решить Ansible:
* подключение по SSH к устройствам
 * паралелльное подключение к устройствам по SSH
* отправка команд на устройства
* удобный синтаксис описания устройств:
 * можно разбивать устройства на группы и затем отправлять какие-то команды на всю группу
* поддержка шаблонов конфигураций с Jinja2

#VSLIDE
### Установка Ansible

Ansible нужно устанавливать только на той машине, с которой будет выполняться управление устройствами.

Требования к управляющему хосту:
* поддержка Python 2.7 (или 2.6)
* Windows не может быть управляющим хостом

Ansible довольно часто обновляется, поэтому лучше установить его в виртуальном окружении.

#VSLIDE
### Установка Ansible

Установить Ansible можно [по-разному](http://docs.ansible.com/ansible/intro_installation.html#).

Например, с помощью pip:
```
$ pip install ansible==2.2.0.0
```

#VSLIDE
### Параметры оборудования

В примерах раздела используются три маршрутизатора и один коммутатор:
* пользователь: cisco
* пароль: cisco
* пароль на режим enable: cisco
* SSH версии 2
* IP-адреса:
 * R1: 192.168.100.1
 * R2: 192.168.100.2
 * R3: 192.168.100.3
 * SW1: 192.168.100.100

#HSLIDE
## Основы Ansible

#VSLIDE
### Основы Ansible

* Работает без установки агента на управляемые хосты
* Использует SSH для подключения к управляемым хостам
* Выполняет изменения, с помощью модулей Python, которые выполняются на управляемых хостах
* Может выполнять действия локально, на управляющем хосте
* Использует YAML для описания сценариев
* Содержит множество модулей (их количество постоянно растет)
* Легко писать свои модули

#VSLIDE
### Терминология

* __Control machine__ —  управляющий хост. Сервер Ansible, с которого происходит управление другими хостами
* __Manage node__ —  управляемые хосты
* __Inventory__ —  инвентарный файл. В этом файле описываются хосты, группы хостов. А также могут быть созданы переменные
* __Playbook__ — файл сценариев
* __Play__ —  сценарий (набор задач). Связывает задачи с хостами, для которых эти задачи надо выполнить
* __Task__ —  задача. Вызывает модуль с указанными параметрами и переменными
* __Module__ — модуль Ansible. Реализует определенные функции


#VSLIDE
### Quick start

Минимум, который нужен для начала работы:
* инвентарный файл - в нем описываются устройства
* изменить конфигурацию Ansible, для работы с сетевым оборудованием
* разобраться с ad-hoc командами - это возможность выполнять простые действия с устройствами из командной строки


#HSLIDE
### Инвентарный файл

#VSLIDE
### Инвентарный файл

Инвентарный файл - это файл, в котором описываются устройства, к которым Ansible будет подключаться.

В инвентарном файле устройства могут указываться используя IP-адреса или имена.
Устройства могут быть указаны по одному или разбиты на группы.

#VSLIDE
### Инвентарный файл

Файл описывается в формате INI:
```ini
r5.example.com

[cisco-routers]
192.168.255.1
192.168.255.2
192.168.255.3
192.168.255.4

[cisco-edge-routers]
192.168.255.1
192.168.255.2
```


#VSLIDE
### Инвентарный файл

По умолчанию, файл находится в ```/etc/ansible/hosts```.

Но можно создавать свой инвентарный файл и использовать его.
Для этого нужно, либо указать его при запуске Ansible, используя опцию ```-i <путь>```, либо указать файл в конфигурационном файле Ansible.


#VSLIDE
### Инвентарный файл

Пример инвентарного файла, с использованием нестандартных портов для SSH:
```ini
[cisco-routers]
192.168.255.1:22022
192.168.255.2:22022
192.168.255.3:22022

[cisco-switches]
192.168.254.1
192.168.254.2
```

Такой вариант указания порта работает только с подключениями OpenSSH и не работает с paramiko.


#VSLIDE
### Инвентарный файл

Если в группу надо добавить несколько устройств с однотипными именами, можно использовать такой вариант записи:
```ini
[cisco-routers]
192.168.255.[1-5]
```

В группу попадут устройства с адресами 192.168.255.1-192.168.255.5.

#VSLIDE
### Группа из групп

Ansible также позволяет объединять группы устройств в общую группу. Для этого используется специальный синтаксис:
```ini
[cisco-routers]
192.168.255.1
192.168.255.2
192.168.255.3

[cisco-switches]
192.168.254.1
192.168.254.2

[cisco-devices:children]
cisco-routers
cisco-switches
```


#HSLIDE
### Ad Hoc команды

#VSLIDE
### Ad Hoc команды

Ad-hoc команды - это возможность запустить какое-то действие Ansible из командной строки.

Такой вариант используется, как правило, в тех случаях, когда надо что-то проверить, например, работу модуля.
Или просто выполнить какое-то разовое действие, которое не нужно сохранять.

В любом случае, это простой и быстрый способ начать использовать Ansible.

#VSLIDE
### Ad Hoc команды

Сначала нужно создать в локальном каталоге инвентарный файл:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

#VSLIDE
### Ad Hoc команды

Пример ad-hoc команды:
```
$ ansible cisco-routers -i myhosts -m raw -a "sh ip int br" -u cisco --ask-pass
```

#VSLIDE
### Ad Hoc команды

Результат выполнения будет таким:
```
$ ansible cisco-routers -i myhosts -m raw -a "sh ip int br" -u cisco --ask-pass
```

![ad-hoc-fail](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/2_ad-hoc-fail.png)

#VSLIDE
### Ad Hoc команды

Ошибка значит, что нужно установить программу sshpass.
Эта особенность возникает только когда используется аутентификацию по паролю.

Установка sshpass:
```
$ sudo apt-get install sshpass
```

#VSLIDE
### Ad Hoc команды

Команду надо выполнить повторно:
```
$ ansible cisco-routers -i myhosts -m raw -a "sh ip int br" -u cisco --ask-pass
```

#VSLIDE

Результат выполнения команды
![ad-hoc](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/1_ad-hoc.png)


#HSLIDE

### Конфигурационный файл

#VSLIDE
### Конфигурационный файл

Настройки Ansible можно менять в конфигурационном файле.

Конфигурационный файл Ansible может хранится в разных местах:
* ANSIBLE_CONFIG (переменная окружения)
* ansible.cfg (в текущем каталоге)
* .ansible.cfg (в домашнем каталоге пользователя)
* /etc/ansible/ansible.cfg

Ansible ищет файл конфигурации в указанном порядке и использует первый найденный (конфигурация из разных файлов не совмещается).

#VSLIDE
### Конфигурационный файл

В конфигурационном файле можно менять множество параметров.
Полный список параметров и их описание, можно найти в [документации](http://docs.ansible.com/ansible/intro_configuration.html).

В текущем каталоге должен быть инвентарный файл myhosts:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

#VSLIDE
### Конфигурационный файл

Конфигурационный файл ansible.cfg:
```
[defaults]

inventory = ./myhosts
remote_user = cisco
ask_pass = True
```

#VSLIDE
### Конфигурационный файл

Настройки в конфигурационном файле:
* ```[defaults]``` - секция описывает общие параметры по умолчанию
* ```inventory = ./myhosts``` - местоположение инвентарного файла
* ```remote_user = cisco``` - от имени какого пользователя будет подключаться Ansible
* ```ask_pass = True``` - этот параметр аналогичен опции --ask-pass в командной строке

#VSLIDE
### Конфигурационный файл

Теперь вызов ad-hoc команды будет выглядеть так:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
```

Теперь не нужно указывать инвентарный файл, пользователя и опцию --ask-pass.


#VSLIDE
### gathering

По умолчанию, Ansible собирает факты об устройствах.

Факты - это информация о хостах, к которым подключается Ansible.
Эти факты можно использовать в playbook и шаблонах как переменные.

Сбором фактов, по умолчанию, занимается модуль [setup](http://docs.ansible.com/ansible/setup_module.html).

Но, для сетевого оборудования, модуль setup не подходит, поэтому сбор фактов надо отключить.
Это можно сделать в конфигурационном файле Ansible или в playbook.

#VSLIDE
### gathering

Для сетевого оборудования нужно использовать отдельные модули для сбора фактов (если они есть).

Отключение сбора фактов в конфигурационном файле:
```yml
gathering = explicit
```


#VSLIDE
### host_key_checking

Параметр host_key_checking отвечает за проверкy ключей, при подключении по SSH.
Если указать в конфигурационном файле ```host_key_checking=False```, проверка будет отключена.

Это полезно, когда с управляющего хоста Ansible надо подключиться к большому количеству устройств первый раз.

Чтобы проверить этот функционал, надо удалить сохраненные ключи для устройств Cisco, к которым уже выполнялось подкление.
В линукс они находятся в файле ~/.ssh/known_hosts.

#VSLIDE
### host_key_checking

Если выполнить ad-hoc команду, после удаления ключей, вывод будет таким:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
```

![host_key_checking](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/host_key_checking.png)


#VSLIDE
### host_key_checking

Добавляем в конфигурационный файл параметр host_key_checking:
```
[defaults]

inventory = ./myhosts

remote_user = cisco
ask_pass = True

host_key_checking=False
```

#VSLIDE
### host_key_checking

И повторим ad-hoc команду:
```
$ ansible cisco-routers -m raw -a "sh ip int br"
```

#VSLIDE
Результат выполнения команды:

![host_key_checking2](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/host_key_checking2.png)

#VSLIDE
### host_key_checking

Обратите внимание на строки:
```
 Warning: Permanently added '192.168.100.1' (RSA) to the list of known hosts.
```

Ansible сам добавил ключи устройств в файл ~/.ssh/known_hosts.
При подключении в следующий раз этого сообщения уже не будет.


Другие параметры конфигурационного файла можно посмотреть в документации.
Пример конфигурационного файла в [репозитории Ansible](https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg).

#HSLIDE

### Модули Ansible

#VSLIDE
### Модули Ansible

Вместе с установкой Ansible устанавливается также большое количество модулей (библиотека модулей).
В текущей библиотеке модулей, находится порядка 200 модулей.

Модули отвечают за действия, которые выполняет Ansible.
При этом, каждый модуль, как правило, отвечает за свою конкретную и небольшую задачу.

Модули можно выполнять отдельно, в ad-hoc командах или собирать в определенный сценарий (play), а затем в playbook.

#VSLIDE
### Модули Ansible

Как правило, при вызове модуля, ему нужно передать аргументы.
Какие-то аргументы будут управлять поведением и параметрами модуля, а какие-то передавать, например, команду, которую надо выполнить.

Например, мы уже выполняли ad-hoc команды, используя модуль raw. И передавали ему аргументы:
```
$ ansible cisco-routers -i myhosts -m raw -a "sh ip int br" -u cisco --ask-pass
```

#VSLIDE
### Модули Ansible

Выполнение такой же задачи в playbook будет выглядеть так:
```
    - name: run sh ip int br        
      raw: sh ip int br | ex unass
```

После выполнения, модуль возвращает результаты выполнения в формате JSON.

#VSLIDE
### Модули Ansible

Модули Ansible, как правило, идемпотентны.
Это означает, что модуль можно выполнять сколько угодно раз, но при этом модуль будет выполнять изменения, только если система не находится в желаемом состоянии.

#VSLIDE
### Модули Ansible

В Ansible модули разделены на две категории:
* __core__ - это модули, которые всегда устанавливаются вместе с Anible. Их поддерживает основная команда разработчиков Ansible.
* __extra__ - это модули на данный момент устанавливаются с Ansible, но нет гарантии, что они и дальше будут устанавливаться с Ansible. Возможно, в будущем, их нужно будет устанавливать отдельно. Большинство этих модулей поддерживаются сообществом.

Также в Ansible модули разделены по функциональности.
Список всех категорий находится в [документации](http://docs.ansible.com/ansible/modules_by_category.html).


#HSLIDE
## Основы playbooks

#VSLIDE
### Основы playbooks

Playbook (файл сценариев) — это файл в котором описываются действия, которые нужно выполнить на какой-то группе хостов.

Внутри playbook:
* play - это набор задач, которые нужно выполнить для группы хостов
* task - это конкретная задача. В задаче есть, как минимум:
 * описание (название задачи можно не писать, но очень рекомендуется)
 * модуль и команда (действие в модуле)


#VSLIDE
### Синтаксис playbook

Пример plabook 1_show_commands_with_raw.yml:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br        
      raw: sh ip int br | ex unass

    - name: run sh ip route
      raw: sh ip route

- name: Run show commands on switches
  hosts: cisco-switches
  gather_facts: false

  tasks:

    - name: run sh int status
      raw: sh int status

    - name: run sh vlan
      raw: show vlan
```

#VSLIDE

И тот же playbook с отображением элементов:

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook.png)

#VSLIDE
### Синтаксис playbook

Так выглядит выполнение playbook:
```
$ ansible-playbook 1_show_commands_with_raw.yml
```

#VSLIDE
Так выглядит выполнение playbook:

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook_execution.png)

#VSLIDE
### Синтаксис playbook

Запуск playbook с опцией -v (вывод сокращен):
```
$ ansible-playbook 1_show_commands_with_raw.yml -v
```

![Verbose playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook-verbose.png)


#VSLIDE
### Порядок выполнения задач и сценариев

Сценарии (play) и задачи (task) выполняются последовательно, в том порядке, в котором они описаны в playbook.

Если в сценарии, например, две задачи, то сначала первая задача должна быть выполнена для всех устройств, которые указаны в параметре hosts.
Только после того, как первая задача была выполнена для всех хостов, начинается выполнение второй задачи.

Если в ходе выполнения playbook, возникла ошибка в задаче на каком-то устройстве, это устройство исключается, и другие задачи на нем выполняться не будут.

#VSLIDE
### Порядок выполнения задач и сценариев

Например, заменим пароль пользователя cisco на cisco123 (правильный cisco) на маршрутизаторе 192.168.100.1, и запустим playbook заново:
```
$ ansible-playbook 1_show_commands_with_raw.yml
```

#VSLIDE

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook_failed_execution.png)

#VSLIDE
### Порядок выполнения задач и сценариев

Обратите внимание на ошибку в выполнении первой задачи для маршрутизатора 192.168.100.1.

Во второй задаче 'TASK [run sh ip route]', Ansible уже исключил маршрутизатор и выполняет задачу только для маршрутизаторов 192.168.100.2 и 192.168.100.3.

#VSLIDE
### Порядок выполнения задач и сценариев

Еще один важный аспект - Ansible выдал сообщение:
```
to retry, use: --limit @/home/nata/pyneng_course/chapter15/1_show_commands_with_raw.retry
```
#VSLIDE
### Порядок выполнения задач и сценариев

Если, при выполнении playbook, на каком-то устройстве возникла ошибка, Ansible создает специальный файл, который называется точно так же как playbook, но расширение меняется на retry.

В этом файле хранится имя или адрес устройства на котором возникла ошибка (файл 1_show_commands_with_raw.retry):
```
192.168.100.1
```

#VSLIDE
### Порядок выполнения задач и сценариев

После настройки правильного пароля на маршрутизаторе, перезапускаем playbook:
```
$ ansible-playbook 1_show_commands_with_raw.yml --limit @/home/nata/pyneng_course/chapter15/1_show_commands_with_raw.retry
```

![Ansible playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook-retry.png)

#VSLIDE
### Порядок выполнения задач и сценариев

Ansible взял список устройств, которые перечислены в файле retry и выполнил playbook только для них.

Можно запустить playbook и так:
```
$ ansible-playbook 1_show_commands_with_raw.yml --limit @1_show_commands_with_raw.retry
```

#VSLIDE
### Параметр --limit

Параметр --limit позволяет ограничивать, для каких хостов или групп будет выполняться playbook, при этом, не меняя сам playbook.

Например, таким образом playbook можно запустить только для маршрутизатора 192.168.100.1:
```
$ ansible-playbook 1_show_commands_with_raw.yml --limit 192.168.100.1
```

#VSLIDE

### Идемпотентность

Модули Ansible идемпотентны.
Это означает, что модуль можно выполнять сколько угодно раз, но при этом модуль будет выполнять изменения, только если система не находится в желаемом состоянии.

Но, есть исключения из такого поведения.
Например, модуль raw всегда вносит изменения.
Поэтому в выполнении playbook выше, всегда отображалось состояние changed.

#VSLIDE
### Идемпотентность

Например, если в задаче указано, что на сервер Linux надо установить пакет httpd, то он будет установлен только в том случае, если его нет.
То есть, действие не будет повторяться снова и снова, при каждом запуске.
А лишь тогда, когда пакета нет.

Аналогично, и с сетевым оборудованием.
Если задача модуля выполнить команду в конфигурационном режиме, а она уже есть на устройстве, модуль не будет вносить изменения.


#HSLIDE
### Переменные

#VSLIDE
### Переменные

Переменной может быть:
* информация об устройстве, которая собрана как факт, а затем используется в шаблоне
* в переменные можно записывать полученный вывод команды
* переменная может быть указана вручную в playbook

#VSLIDE
### Имена переменных

В Ansible есть определенные ограничения по формату имен переменных:
* Переменные могут состоять из букв, чисел и символа ```_```
* Переменные должны начинаться с буквы

#VSLIDE
### Имена переменных

Кроме того, можно создавать словари с переменными (в формате YAML):
```
R1:
  IP: 10.1.1.1/24
  DG: 10.1.1.100
```

#VSLIDE
### Имена переменных

Обращаться к переменным в словаре можно двумя вариантами:
```
R1['IP']
R1.IP
```

При использовании второго варианта, могут быть проблемы, если название ключа совпадает с зарезервированным словом (методом или атрибутом) в Python или Ansible.

#VSLIDE
### Где можно определять переменные

Переменные можно создавать:
* в инвентарном файле
* в playbook
* в специальных файлах для группы/устройства
* в отдельных файлах, которые добавляются в playbook через include (как в Jinja2)
* в ролях, которые затем используются
* можно передавать переменные при вызове playbook

Также можно использовать факты, которые были собраны про устройство, как переменные.


#VSLIDE
### Переменные в инвентарном файле

В инвентарном файле можно указывать переменные для группы:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100

[cisco-routers:vars]
ntp_server=192.168.255.100
log_server=10.255.100.1
```

#VSLIDE
### Переменные в playbook

Переменные можно задавать прямо в playbook

```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  vars:
    ntp_server: 192.168.255.100
    log_server: 10.255.100.1

  tasks:

    - name: run sh ip int br        
      raw: sh ip int br | ex unass

    - name: run sh ip route
      raw: sh ip route

```

#VSLIDE
### Переменные в специальных файлах

Ansible позволяет хранить переменные для группы/устройства в специальных файлах:
* Для групп устройств, переменные должны находится в каталоге group_vars, в файлах, которые называются, как имя группы.
 * в каталоге group_vars можно создавать файл all, в котором будут находиться переменные, которые относятся ко всем группам.
* Для конкретных устройств, переменные должны находится в каталоге host_vars, в файлах, которые соответствуют имени или адресу хоста.

#VSLIDE
### Переменные в специальных файлах

Ansible позволяет хранить переменные для группы/устройства в специальных файлах:
* Все файлы с переменными, должны быть в формате YAML. Расширение файла может быть yml, yaml, json или без расширения
* каталоги group_vars и host_vars должны находиться в том же каталоге, что и playbook. Или могут находиться внутри каталога inventory (первый вариант более распространенный).
 * если каталоги и файлы названы правильно и расположены в указанных каталогах, Ansible сам разпознает файлы и будет использовать переменные

#VSLIDE
### Переменные в специальных файлах

Например, если инвентарный файл myhosts выглядит так:
```
[cisco-routers]
192.168.100.1
192.168.100.2
192.168.100.3

[cisco-switches]
192.168.100.100
```

#VSLIDE
### Переменные в специальных файлах

Можно создать такую структуру каталогов:
```
├── group_vars                 _
│   ├── all.yml                 |
│   ├── cisco-routers.yml       |  Каталог с переменными для групп устройств
│   └── cisco-switches.yml     _|
|
├── host_vars                  _
│   ├── 192.168.100.1           |
│   ├── 192.168.100.2           |
│   ├── 192.168.100.3           |  Каталог с переменными для устройств 
│   └── 192.168.100.100        _|
|
└── myhosts                     |  Инвентарный файл
```

#VSLIDE
### Переменные в специальных файлах

Файл group_vars/all.yml:
```
cli:
  host: "{{ inventory_hostname }}"
  username: "cisco"
  password: "cisco"
  transport: cli
  authorize: yes
  auth_pass: "cisco"

```

#VSLIDE
### Переменные в специальных файлах

В файле group_vars/all.yml создан словарь cli.
В этом словаре перечислены те аргументы, которые должны задаваться для работы с сетевым оборудованием через встроенные модули Ansible

Переменная host: "{{ inventory_hostname }}":
* inventory_hostname - это специальная переменная, которая указывает на тот хост, для которого Ansible выполняет действия.
* синтаксис {{ inventory_hostname }} - это подстановка переменных. Используется формат Jinja

#VSLIDE
### Переменные в специальных файлах

group_vars/cisco-routers.yml
```
log_server: 10.255.100.1
ntp_server: 10.255.100.1
users:
  user1: pass1
  user2: pass2
  user3: pass3
```

#VSLIDE
### Переменные в специальных файлах

group_vars/cisco-switches.yml
```
vlans:
  - 10
  - 20
  - 30
```

#VSLIDE
### Переменные в специальных файлах

Файлы с переменными для хостов однотипны и в них меняются только адреса и имена.

Файл host_vars/192.168.100.1
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
### Приоритетность переменных

Чаще всего, переменная с определенным именем только одна.

Но, иногда может понадобиться создать переменную в разных местах и тогда нужно понимать, в каком порядке Ansible перезаписывает переменные.

#VSLIDE
### Приоритетность переменных

Приоритет переменных (последние значения переписывают предыдущие):
* Значения переменных в ролях
 * задачи в ролях будут видеть собственные значения. Задачи, которые определены вне роли, будут видеть последние значения переменных роли
* переменные в инвентарном файле
* переменные для группы хостов в инвентарном файле
* переменные для хостов в инвентарном файле

#VSLIDE
### Приоритетность переменных

* переменные в каталоге group_vars
* переменные в каталоге host_vars
* факты хоста
* переменные сценария (play)
* переменные сценария, которые запрашиваются через vars_prompt

#VSLIDE
### Приоритетность переменных

* переменные, которые передаются в сценарий через vars_files
* переменные полученные через параметр register
* set_facts
* переменные из роли и помещенные через include
* переменные блока (переписывают другие значения только для блока)
* переменные задачи (task) (переписывают другие значения только для задачи)
* переменные, которые передаются при вызове playbook через параметр --extra-vars (всегда наиболее приоритетные)

#HSLIDE
### Работа с результатами выполнения модуля

#VSLIDE
### verbose

Флаг verbose позволяет подробно посмотреть какие шаги выполняет Ansible.

Пример запуска playbook с флагом verbose (вывод сокращен):
```
ansible-playbook 1_show_commands_with_raw.yml -v
```

![Verbose playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/playbook-verbose.png)

#VSLIDE
### verbose

При увеличении количества букв v в флаге, вывод становится более подробным.
```
ansible-playbook 1_show_commands_with_raw.yml -vvv
```

#VSLIDE
### verbose

В выводе видны результаты выполнения задачи, они возвращаются в формате JSON:
* __changed__ - ключ, который указывает были ли внесены изменения
* __rc__ - return code. Это поле появляется в выводе тех модулей, которые выполняют какие-то команды
* __stderr__ - ошибки, при выполнении команды. Это поле появляется в выводе тех модулей, которые выполняют какие-то команды
* __stdout__ - вывод команды
* __stdout_lines__ - вывод в виде списка команд, разбитых построчно


#VSLIDE
### register

Параметр __register__ сохраняет результат выполнения модуля в переменную.
Затем эта переменная может использоваться в шаблонах, в принятии решений о ходе сценария или для отображении вывода.

#VSLIDE
### register

В playbook 2_register_vars.yml, с помощью register, вывод команды sh ip int br сохранен в переменную sh_ip_int_br_result:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int br | ex unass
      register: sh_ip_int_br_result
```

#VSLIDE
### register

Если запустить этот playbook, вывод не будет отличаться, так как вывод только записан в переменную, но с переменной не выполяется никаких действий.
Следующий шаг - отобразить результат выполнения команды, с помощью модуля debug.


#VSLIDE
### debug

Модуль debug позволяет отображать информацию на стандартный поток вывода.
Это может быть произвольная строка, переменная, факты об устройстве.

#VSLIDE
### debug

Для отображения сохраненных результатов выполнения команды, в playbook 2_register_vars.yml добавлена задача с модулем debug:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int br | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug: var=sh_ip_int_br_result.stdout_lines
```

#VSLIDE
### debug

Обратите внимание, что выводится не всё содержимое переменной sh_ip_int_br_result, а только содержимое stdout_lines.
В sh_ip_int_br_result.stdout_lines находится список строк, поэтому вывод будут структурированн.

Результат запуска playbook будет выглядит так:
```
$ ansible-playbook 2_register_vars.yml
```

#VSLIDE
### debug

![Verbose playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/2_register_vars.png)


#VSLIDE
### register, debug, when

С помощью ключевого слова __when__, можно указать условие, при выполнении которого, задача выполняется.
Если условие не выполняется, то задача пропускается.

when в Ansible используется как if в Python.


#VSLIDE
### register, debug, when

Пример playbook 3_register_debug_when.yml:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: sh ip int bri | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug:
        msg: "Error in command"
      when: "'invalid' in sh_ip_int_br_result.stdout"
```

#VSLIDE
### register, debug, when

Модуль debug отображает не содержимое сохраненной переменной, а сообщение, которое указано в переменной msg.

Задача будет выполнена только в том случае, если в выводе sh_ip_int_br_result.stdout будет найдена строка invalid
```
when: "'invalid' in sh_ip_int_br_result.stdout"
```

Модули, которые работают с сетевым оборудованием, автоматически проверяют ошибки, при выполнении команд. Тут этот пример используется для демонстрации возможностей Ansible.

#VSLIDE
### register, debug, when

Выполнение playbook:
```
$ ansible-playbook 3_register_debug_when.yml
```

![Verbose playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/3_register_debug_when_skip.png)

#VSLIDE
### register, debug, when

Выполнение того же playbook, но с ошибкой в команде:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false

  tasks:

    - name: run sh ip int br
      raw: shh ip int bri | ex unass
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug:
        msg: "Error in command"
      when: "'invalid' in sh_ip_int_br_result.stdout"
```

#VSLIDE
### register, debug, when

Теперь результат выполнения такой:
```
$ ansible-playbook 3_register_debug_when.yml
```

![Verbose playbook](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/3_register_debug_when.png)

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
### Варианты подключения

Ansible поддерживает такие типы подключений:
* __paramiko__
* __SSH__ - OpenSSH. Используется по умолчанию
* __local__ - действия выполняются локально, на управляющем хосте

> При подключении по SSH, по умолчанию используются SSH ключи, но можно переключиться на использование паролей.

#VSLIDE
### Варианты подключения

По умолчанию, Ansible загружает модуль Python на устройство, для того, чтобы выполнить действия.
Если же оборудование не поддерживает Python, как в случае с доступом к сетевому оборудованию через CLI, нужно указать, что модуль должен запускаться локально, на управляющем хосте Ansible.


#VSLIDE
### Особенности подключения к сетевому оборудованию

При  работе с сетевым оборудованием, есть несколько параметров в playbook, которые нужно менять:
* gather_facts - надо отключить, так как для сетевого оборудования используются свои модули сбора фактов
* connection - управляет тем, как именно будет происходить подключение. Для сетевого оборудования необходимо установить в local

#VSLIDE
### Особенности подключения к сетевому оборудованию

То есть, для каждого сценария (play), нужно указывать:
* gather_facts: false
* connection: local

```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

```

#VSLIDE
### Особенности подключения к сетевому оборудованию

В Ansible переменные можно указывать в разных местах, поэтому те же настройки можно указать по-другому.

Например, в конфигурационном файле:
```
[defaults]

gathering = explicit
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
ansible_connection=local
```

#VSLIDE
### Особенности подключения к сетевому оборудованию

Или в файлах переменных, например, в group_vars/all.yml:
```
ansible_connection: local
```

#VSLIDE
### Особенности подключения к сетевому оборудованию

В следующих разделах будет использоваться такой вариант:
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local
```

В реальной жизни нужно выбрать тот вариант, который наиболее удобен для работы.

#VSLIDE
### Аргумент provider

Модули, которые используются для работы с сетевым оборудованием, требуют задания нескольких аргументов.

Для каждой задачи должны быть указаны такие аргументы:
* __host__ - имя или IP-адрес удаленного устройства
* __port__ - к какому порту подключаться
* __username__ - имя пользователя
* __password__ - пароль
* __transport__ - тип подключения: CLI или API. По умолчанию - cli
* __authorize__ - нужно ли переходить в привилегированный режим (enable, для Cisco)
* __auth_pass__ - пароль для привилегированного режима

#VSLIDE
### Аргумент provider

Ansible также позволяет собрать их в один аргумент - __provider__.

```
  tasks:

    - name: run show version
      ios_command:
        commands: show version
        host: "{{ inventory_hostname }}"
        username: cisco
        password: cisco
        transport: cli
```

#VSLIDE
### Аргумент provider

Аргументы созданы как переменная ```cli``` в playbook, а затем передаются как переменная аргументу provider:
```
  vars:
    cli:
      host: "{{ inventory_hostname }}"
      username: cisco
      password: cisco
      transport: cli

  tasks:
    - name: run show version
      ios_command:
        commands: show version
        provider: "{{ cli }}"

```

#VSLIDE
### Аргумент provider

И, самый удобный вариант, задавать аргументы в каталоге group_vars.

Например, если у всех устройств одинаковые значения аргументов, можно задать их в файле group_vars/all.yml:
```
cli:
  host: "{{ inventory_hostname }}"
  username: cisco
  password: cisco
  transport: cli
  authorize: yes
  auth_pass: cisco
```

#VSLIDE
### Аргумент provider

Затем переменная используется в playbook так же, как и в случае указания переменных в playbook:
```
  tasks:
    - name: run show version
      ios_command:
        commands: show version
        provider: "{{ cli }}"
```

#VSLIDE
### Аргумент provider

Кроме того, Ansible поддерживает задание параметров в переменных окружения:
* ANSIBLE_NET_USERNAME - для переменной username
* ANSIBLE_NET_PASSWORD - password
* ANSIBLE_NET_SSH_KEYFILE - ssh_keyfile
* ANSIBLE_NET_AUTHORIZE - authorize
* ANSIBLE_NET_AUTH_PASS - auth_pass

#VSLIDE
### Аргумент provider

Приоритетность значений в порядке возрастания приоритетности:
* значения по умолчанию
* значения переменных окружения
* параметр provider
* аргументы задачи (task)

#VSLIDE
### Подготовка к работе с сетевыми модулями

В следующих разделах рассматривается работа с модулями ios_command, ios_facts и ios_config.
Для того, чтобы все примеры playbook работали, надо создать несколько файлов (проверить, что они есть).

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

remote_user = cisco
ask_pass = True
```

#VSLIDE
### Подготовка к работе с сетевыми модулями

В файле group_vars/all.yml надо создать переменную cli, чтобы не указывать каждый раз все параметры, которые нужно передать аргументу provider:
```
cli:
  host: "{{ inventory_hostname }}"
  username: "cisco"
  password: "cisco"
  transport: cli
  authorize: yes
  auth_pass: "cisco"
```

#HSLIDE
## Модуль ios_command

#VSLIDE
### Модуль ios_command

Модуль __ios_command__ - отправляет команду show на устройство под управлением IOS и возвращает результат выполнения команды.

Модуль ios_command не поддерживает отправку команд в конфигурационном режиме. Для этого используется отдельный модуль - ios_config.

#VSLIDE
### Модуль ios_command

Перед отправкой самой команды, модуль:
* выполняет аутентификацию по SSH,
* переходит в режим enable
* выполняет команду ```terminal length 0```, чтобы вывод команд show отражался полностью, а не постранично.

#VSLIDE
### Модуль ios_command

Пример использования модуля ios_command (playbook 1_ios_command.yml):
```
- name: Run show commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: run sh ip int br
      ios_command:
        commands: show ip int br
        provider: "{{ cli }}"
      register: sh_ip_int_br_result

    - name: Debug registered var
      debug: var=sh_ip_int_br_result.stdout_lines
```

#VSLIDE
### Модуль ios_command

Модуль ios_command ожидает параметры:
* commands - список команд, которые нужно отправить на устройство
* provider - словарь с параметрами подключения
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
  gather_facts: false
  connection: local

  tasks:

    - name: run show commands
      ios_command:
        commands:
          - show ip int br
          - sh ip route
        provider: "{{ cli }}"
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
    provider: "{{ cli }}"
```

#VSLIDE
### Модуль ios_facts

Собрать только подмножество interfaces:
```
- ios_facts:
    gather_subset:
      - interfaces
    provider: "{{ cli }}"
```

#VSLIDE
### Модуль ios_facts

Собрать всё, кроме hardware:
```
- ios_facts:
    gather_subset:
      - "!hardware"
    provider: "{{ cli }}"
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
  gather_facts: false
  connection: local

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
        provider: "{{ cli }}"
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
  gather_facts: false
  connection: local

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
        provider: "{{ cli }}"

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
  gather_facts: false
  connection: local

  tasks:

    - name: Facts
      ios_facts:
        gather_subset: all
        provider: "{{ cli }}"
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

В строке ```content: "{{ ios_facts_result | to_nice_json }}"```
* параметр to_nice_json - это фильтр Jinja2, который преобразует информацию переменной в формат, в котором удобней читать информацию
* переменная в формате Jinja2 должна быть заключена в двойные фигурные скобки, а также указана в двойных кавычках

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

#VSLIDE
### Изменения с опцией --diff

В Ansible можно не только увидеть, что изменения произошли, но и увидеть какие именно изменения были сделаны.
Например, в ситуации с сохранением фактов об устройстве это может быть очень полезно.

Пример запуска playbook с опцией --diff и с внесенными изменениями на одном из устройств:
```
$ ansible-playbook 3_ios_facts.yml --diff --limit=192.168.100.1
```

#VSLIDE

![5a_ios_facts](https://raw.githubusercontent.com/natenka/PyNEng/master/images/15_ansible/5a_ios_facts_diff.png)

#HSLIDE
## Модуль ios_config

Модуль ios_config - позволяет настраивать устройства под управлением IOS, а также, генерировать шаблоны конфигураций или отправлять команды на основании шаблона.

#VSLIDE
## Модуль ios_config

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
## Модуль ios_config

* __parents__ - название секции, в которой нужно применить команды. Если команда находится внутри вложенной секции, нужно указывать весь путь. Если этот параметр не указан, то считается, что команда должны быть в глобальном режиме конфигурации
* __replace__ - параметр указывает как выполнять настройку устройства
* __save__ - сохранять ли текущую конфигурацию в стартовую. По умолчанию конфигурация не сохраняется
* __src__ - параметр указывает путь к файлу, в котором находится конфигурация или шаблон конфигурации. Взаимоисключающий параметр с lines (то есть, можно указывать или lines или src). Заменяет модуль ios_template, который скоро будет удален.

#HSLIDE
## lines (commands)

Самый простой способ использовать модуль ios_config - отправлять команды глобального конфигурационного режима с параметром lines.

Для параметра lines есть alias commands, то есть, можно вместо lines писать commands.

#VSLIDE
## lines (commands)

Пример playbook 1_ios_config_lines.yml:
```yml
- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Config password encryption
      ios_config:
        lines:
          - service password-encryption
        provider: "{{ cli }}"
```

#VSLIDE
## lines (commands)

Результат выполнения playbook:
```
$ ansible-playbook 1_ios_config_lines.yml
```

#VSLIDE
## lines (commands)

![6_ios_config_lines]({{ book.ansible_img_path }}6_ios_config_lines.png)

#VSLIDE
## lines (commands)

Ansible выполняет такие команды:
* terminal length 0
* enable
* show running-config - чтобы проверить есть ли эта команда на устройстве. Если команда есть, задача выполняться не будет. Если команды нет, задача выполнится
* если команды, которая указана в задаче нет в конфигурации:
 * configure terminal
 * service password-encryption
 * end

#VSLIDE
## lines (commands)

Так как модуль каждый раз проверяет конфигурацию, прежде чем применит команду, модуль идемпотентен.
То есть, если ещё раз запустить playbook, изменения не будут выполнены:
```
$ ansible-playbook 1_ios_config_lines.yml
```

![6_ios_config_lines]({{ book.ansible_img_path }}6_ios_config_lines_2.png)

#VSLIDE
## lines (commands)

Параметр lines позволяет отправлять и несколько команд (playbook 1_ios_config_mult_lines.yml):
```
- name: Run cfg commands on routers
  hosts: cisco-routers
  gather_facts: false
  connection: local

  tasks:

    - name: Send config commands
      ios_config:
        lines:
          - service password-encryption
          - no ip http server
          - no ip http secure-server
          - no ip domain lookup
        provider: "{{ cli }}"
```

#VSLIDE
## lines (commands)

Результат выполнения:
```
$ ansible-playbook 1_ios_config_mult_lines.yml
```

![6_ios_config_mult_lines]({{ book.ansible_img_path }}6_ios_config_mult_lines.png)

