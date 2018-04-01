# Python для сетевых инженеров 


#HSLIDE
## Модули для работы с сетевым оборудованием

#HSLIDE
## Модуль ios_config

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
