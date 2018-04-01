# Python для сетевых инженеров 


#HSLIDE
## Модули для работы с сетевым оборудованием

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
