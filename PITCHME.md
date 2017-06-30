# Python для сетевых инженеров 


#HSLIDE

# Unicode

#HSLIDE

### Зачем вообще нужна кодировка?

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


#VSLIDE

### Windows CP1252

![Windows CP1252](http://rabbit.eng.miami.edu/info/cp1252.gif)


#HSLIDE

### Unicode &#129365;


* 1,114,112 code points in the range 0x0 to 0x10FFFF
* The Unicode Standard version 10.0 (released June 2017) defines 136,690

### Unicode

&#9658;
&#128579;
&#128704;
&#128640;
&#129412;

&#129365;
&#129317;
&#129318;
&#129417;

&#9749;
&#9731;
&#128013;
&#127875;
&#127829;
&#127828;


&#128512;
&#128513;
&#128514;
&#128515;
&#128516;
&#128517;
&#128518;
&#128519;
&#128520;
&#128521;


При этом модуль может автоматически конвертировать байты.

