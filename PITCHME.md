# Python для сетевых инженеров 


#HSLIDE
## Модули для работы с сетевым оборудованием



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
