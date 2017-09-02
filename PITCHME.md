# Python для сетевых инженеров 


#HSLIDE
## Инструменты курса

* [Slack](https://pyneng.slack.com) - общение, вопросы
* [Git, GitHub](https://github.com/pyneng) - хранение заданий, проверка заданий
* [Cloud 9](https://c9.io/) - виртуальная среда для выполнения заданий

#HSLIDE
### Git

#VSLIDE
### Система контроля версий

Система контроля версий (Version Control System, VCS):
* отслеживает изменения в файлах
* хранит несколько версий одного файла
* позволяет откатить изменения
* знает кто и когда сделал изменения

#VSLIDE
### Git

* распределенная система контроля версий
* широко используется
* выпущен под лицензией GNU GPL v2

#VSLIDE
### Git

![stream of snapshots](https://git-scm.com/figures/18333fig0105-tn.png)

#VSLIDE
### Git

Файл в Git может быть в таких состояниях:

* committed - файл сохранен в локальной базе
* modified - файл был изменен, но еще не сохранен в локальной базе
* staged - файл отмечен на добавление в следующий commit

#VSLIDE
### Git

![git areas](https://git-scm.com/book/en/v2/images/areas.png)

#VSLIDE
### Git


Три основные части проекта Git:

* каталог Git (.git) - тут хранятся метаданные и база данных объектов проект
* рабочий каталог -  копия определённой версии проекта
* область подготовленных файлов (staging area) - информация о том, что должно попасть в следующий commit

#VSLIDE
### Установка Git

Установка Git
```
$ sudo apt-get install git
```

#HSLIDE
### Основы Git

#VSLIDE
### Первичная настройка Git

Для начала работы с Git необходимо указать имя и email пользователя, которые будут использоваться в commit:

```
$ git config --global user.name "pyneng"
$ git config --global user.email "pyneng.course@gmail.com"
```

Посмотреть настройки можно таким образом:
```
$ git config --list
```

#VSLIDE
### Инициализация репозитория

Для начала, надо создать каталог, в котором будет находиться репозиторий:
```
[~/tools]
$ mkdir first_repo
```

И перейти в него:
```
[~/tools]
$ cd first_repo
```

#VSLIDE
### Инициализация репозитория

Теперь, в новом каталоге необходимо дать команду git init:
```
[~/tools/first_repo]
$ git init
Initialized empty Git repository in /home/vagrant/tools/first_repo/.git/
```

После этой команды, в каталоге создается каталог .git, в котором содержится вся информация, которая необходима для работы Git.

#HSLIDE
### Отображение статуса репозитория в командной строке

При работе с Git, очень удобно, когда вы сразу знаете находитесь вы в обычном каталоге или в репозитории Git.
И, кроме того, было бы хорошо понимать статус текущего репозитория.

Для этого нужно установить [специальную утилиту](https://github.com/magicmonty/bash-git-prompt), которая будет показывать статус репозитория.

#VSLIDE
### Отображение статуса репозитория в командной строке

Процесс установки достаточно прост.
Надо скопировать репозиторий в домашний каталог пользователя, под которым вы работаете:
```
cd ~
git clone https://github.com/magicmonty/bash-git-prompt.git .bash-git-prompt --depth=1
```

#VSLIDE
### Отображение статуса репозитория в командной строке

А затем добавить в конец файла ```~/.bashrc``` такие строки:
```
GIT_PROMPT_ONLY_IN_REPO=1
source ~/.bash-git-prompt/gitprompt.sh
```

Для того чтобы изменения применились, перезапустить bash:
```
exec bash
```

#VSLIDE
### Отображение статуса репозитория в командной строке


Теперь, если вы находитесь в обычном каталоге, приглашение выглядит так:
```
[~]
vagrant@jessie-i386:
$ 
```

Если же перейти в репозиторий Git:

![alt](https://pyneng.github.io/assets/images/setup_prompt.png)


#HSLIDE
### Работа с Git

Прежде чем мы начнем добавлять файлы в репозиторий, посмотрим информацию о текущем состоянии репозитория.

__git status__

Для этого в Git есть команда git status:

![alt](https://pyneng.github.io/assets/images/git_status_0.png)

#VSLIDE
### Работа с Git

Git сообщает, что мы находимся в ветке master (эта ветка создается сама и используется по умолчанию) и что ему нечего добавлять в commit.
Кроме этого, git предлагает создать или скопировать файлы и после этого воспользоваться командой git add, чтобы git начал за ними следить.

#VSLIDE
### Работа с Git

Создадим первый файл README и добавим в него пару произвольных строк текста:

![alt](https://pyneng.github.io/assets/images/vi_readme.png)

#VSLIDE
### Работа с Git

После этого приглашение выглядит таким образом:

![alt](https://pyneng.github.io/assets/images/bash_prompt.png)

#VSLIDE
### Работа с Git

Почему-то в приглашении показано, что есть два файла, за которыми git еще не следит.
Посмотрим в git status откуда взялся второй файл:

![alt](https://pyneng.github.io/assets/images/git_status_1.png)

Git сообщает, что есть файлы за которыми он не следит, подсказывает какой командой это сделать.

#VSLIDE
### Работа с Git

Два файла получились из-за того, что у меня настроены undo файлы для vim.
Это специальные файлы, благодаря которым, можно отменять изменения не только в текущем открытии файла, но и прошлые.

#VSLIDE
### .gitignore

.README.un~ - это служебный файл, который не нужно добавлять в репозиторий.

В git есть возможность сказать, что какие-то файлы или каталоги нужно игнорировать.
Для этого, надо указать соответствующие шаблоны в файле .gitignore в текущем каталоге:

Для того чтобы git игнорировал undo файлы vim, можно добавить, например, такую строку в файл .gitignore:
```
*.un~
```

Это значит, что Git должен игнорировать все файлы, которые заканчиваются на ```.un~```.

#VSLIDE
### .gitignore

После этого, git status показывает:

![alt](https://pyneng.github.io/assets/images/git_status_2.png)


#VSLIDE
### .gitignore


Обратите внимание, что теперь в выводе нет файла .README.un~.
Как только в репозитории добавлен файл .gitignore, файлы, которые указаны в нем, игнорируются.

#HSLIDE
### git add

Для того чтобы Git начал следить за файлами, используется команда git add.

Можно указать, что надо следить за конкретным файлом:

![alt](https://pyneng.github.io/assets/images/git_add_readme.png)

#VSLIDE
### git add

Или за всеми файлами:

![alt](https://pyneng.github.io/assets/images/git_add_all.png)

#VSLIDE
### git add

Проверим как теперь выглядит вывод git status:

![alt](https://pyneng.github.io/assets/images/git_status_3.png)


Теперь файлы находятся в секции "Changes to be committed".

#VSLIDE
### git commit

После того как все нужные файлы были добавлены в staging, можно закоммитить изменения.

У команды git commit есть только один обязательный параметр - флаг ```-m```.
Он позволяет указать сообщение для этого коммита:

![alt](https://pyneng.github.io/assets/images/git_commit_1.png)

#VSLIDE
### git commit


После этого, git status отображает:

![alt](https://pyneng.github.io/assets/images/git_status_4.png)


Фраза "working directory clean" обозначает, что нет изменений, которые нужно добавить в Git или закоммитить.


#HSLIDE
### Дополнительные возможности git

#VSLIDE
### git diff

Команда git diff позволяет просмотреть разницу между различными состояниями.

Например, внесем изменения в файл README и .gitignore, но не будем добавлять их в репозиторий.
Команда git status показывает, что оба файла изменены:

![alt](https://pyneng.github.io/assets/images/git_status_5.png)

#VSLIDE
### git diff

Если дать команду git diff, она покажет внесенные изменения:

![alt](https://pyneng.github.io/assets/images/git_diff.png)

То есть, команда git diff показывает какие изменения были внесены с последнего коммита.

#VSLIDE
### git diff

Если теперь добавить изменения в файлах, и ещё раз выполнить команду git diff, она ничего не покажет:

![alt](https://pyneng.github.io/assets/images/git_add_git_diff.png)

#VSLIDE
### git diff

Чтобы показать отличия между staging и последним коммитом, надо добавить параметр --staged:

![alt](https://pyneng.github.io/assets/images/git_diff_staged.png)

#VSLIDE
### git diff

Закоммитим изменения:

![alt](https://pyneng.github.io/assets/images/git_commit_2.png)


#VSLIDE
### git log

Иногда нужно посмотреть когда были выполнены последние изменения.
В этом поможет команда git log:

![alt](https://pyneng.github.io/assets/images/git_log.png)

По умолчанию команда показывает все коммиты, начиная с самого свежего.

#VSLIDE
### git log

С помощью дополнительных параметров, можно не только посмотреть информацию о коммитах, но и какие изменения были внесены.
Флаг -p позволяет отобразить отличия, которые были внесены каждым коммитом:

![alt](https://pyneng.github.io/assets/images/git_log_p.png)

#VSLIDE
### git log

Более короткий вариант вывода можно вывести с флагом ```--stat```:

![alt](https://pyneng.github.io/assets/images/git_log_stat.png)


