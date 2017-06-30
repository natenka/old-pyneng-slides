# Python для сетевых инженеров 


#HSLIDE

# Unicode

#VSLIDE

### Компьютеры работают с байтами

Мы получаем байты при работе с:

* сетью
* файлами


#VSLIDE

### Компьютеры работают с байтами

Для записи символов в байты, нужна определенная договоренность как они будут выглядеть:

* A - 0x41
* F - 0x46


#VSLIDE

### Стандарт ASCII

ASCII (American standard code for information interchange) - описывает соответствие между символом и его числовым кодом. Изначально описывал только 127 символов:

* коды от 32 до 127 описывали печатные символы
* коды до 32 описывали специальные управляющие символы

#VSLIDE

### Стандарт ASCII

![ascii](https://upload.wikimedia.org/wikipedia/commons/4/4f/ASCII_Code_Chart.svg)


#VSLIDE

### ISO Latin 1 (ISO 8859-1)

![ISO-8859-1](http://rabbit.eng.miami.edu/info/asciiiso.gif)
![Windows CP1252](http://rabbit.eng.miami.edu/info/cp1252.gif)


#VSLIDE

### Windows CP1252

![Windows CP1252](http://rabbit.eng.miami.edu/info/cp1252.gif)


При этом модуль может автоматически конвертировать байты.

