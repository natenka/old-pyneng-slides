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

### Unicode &#129412;


#VSLIDE

### Unicode

* 1,114,112 кодов &#129318;
* диапазон 0x0 - 0x10FFFF &#129365;
* Стандарт Unicode версии 10.0 (Июнь 2017) определяет 136 690 символов  &#128519;


#VSLIDE
### Unicode

* U+1F383 JACK-O-LANTERN &#127875;
* U+2615 HOT BEVERAGE  &#9749;
* U+1f600 GRINNING FACE &#128512;

#VSLIDE
### schön

### U+0073 U+0063 U+0068 U+00f6 U+006e


#VSLIDE
### &#128579; &#8238; Unicode, ты супер!

![U+202e](https://imgs.xkcd.com/comics/rtl_2x.png)

#HSLIDE
### Кодировки

* UTF-8
* UTF-16
* UTF-32

#VSLIDE
### UTF-8

* позволяет хранить символы Юникода
* использует переменное количество байт
* символы ASCII обозначаются такими же кодами

#VSLIDE
### UTF-8

| H | i | &#128704; | &#128640; | &#9731; |
|:-:|:-:|:---------:|:---------:|:-------:|
| 48|69 | 01 f6 c0  | 01 f6 80  | 26 03   |


#HSLIDE
### Unicode в Python 3

#HSLIDE
### str

#VSLIDE
### str

Строка в Python 3 - это последовательность кодов Unicode.

```python
In [1]: s = 'привет'

In [2]: type(s)
Out[2]: str

In [3]: s.upper()
Out[3]: 'ПРИВЕТ'
```

#VSLIDE
### str

```python
In [4]: hi = '\u043f\u0440\u0438\u0432\u0435\u0442'

In [5]: print(hi)
привет

In [6]: len(hi)
Out[6]: 6
```


#VSLIDE
### ord

Функция ord возвращает значение кода Unicode для символа:
```python
In [7]: ord('п')
Out[7]: 1087

In [8]: hex(ord("a"))
Out[8]: '0x61'
```

#VSLIDE
### chr

Функция chr возвращает строку Unicode, которая символу, чем код был передан как аргумент:
```python
In [9]: chr(1087)
Out[9]: 'п'

In [10]: chr(8364)
Out[10]: '€'

In [11]: chr(9731)
Out[11]: '☃'

```


#HSLIDE
### bytes


#VSLIDE
### bytes

```python
In [12]: hi_bytes = b"Hello"

In [13]: type(hi_bytes)
Out[13]: bytes

In [14]: hi_bytes.upper()
Out[14]: b'HELLO'

In [15]: hi_bytes.find(b'l')
Out[15]: 2

In [16]: len(hi_bytes)
Out[16]: 5

```

#VSLIDE
### bytes

Можно работать с байтовыми строками, как с unicode строками:
```python
In [17]: d = {b'hi':'Hello', b'by':'Goodbye'}

In [18]: d[b'hi']
Out[18]: 'Hello'

In [19]: d['hi']
----------------------------------------------------------
KeyError                 Traceback (most recent call last)
<ipython-input-38-259732fc8381> in <module>()
----> 1 d['hi']

KeyError: 'hi'

```

#VSLIDE
### bytes

```python
In [20]: import subprocess

In [21]: result = subprocess.run('ls', stdout=subprocess.PIPE)

In [22]: output = result.stdout

In [23]: output
Out[23]: b'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'

In [24]: type(output)
Out[24]: bytes
```

#VSLIDE
### Non ASCII

```python
In [25]: test = b'привет'
  File "<ipython-input-39-e8b153ea3e66>", line 1
    test = b'привет'
          ^
SyntaxError: bytes can only contain ASCII literal characters.
```

#HSLIDE
### encode vs decode

#VSLIDE

#### unicode .encode() &#8594; bytes
#### bytes .decode() &#8594; unicode

```python
In [26]: hi_unicode = 'привет'

In [27]: hi_bytes = hi_unicode.encode('utf-8')

In [28]: hi_bytes
Out[28]: b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'

In [29]: len(hi_bytes)
Out[29]: 12

In [30]: hi_bytes.decode('utf-8')
Out[30]: 'привет'
```

#VSLIDE
### encode vs decode

```python
In [31]: import subprocess

In [32]: result = subprocess.run('ls', stdout=subprocess.PIPE)

In [33]: result.stdout
Out[33]: b'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode vs decode

```python
In [34]: output_unicode = result.stdout.decode('utf-8')

In [35]: output_unicode
Out[35]: 'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode vs decode

```python
In [36]: result = subprocess.run('ls', stdout=subprocess.PIPE, encoding='utf-8')

In [37]: result.stdout
Out[37]: 'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode vs decode


```python
import telnetlib
import time

t = telnetlib.Telnet('192.168.100.1')

t.read_until(b"Username:")
t.write(b'cisco\n')

t.read_until(b"Password:")
t.write(b'cisco\n')
t.write(b'sh ip int br')

time.sleep(5)

output = t.read_very_eager().decode('utf-8')
print(output)
```

#VSLIDE
### encode vs decode


```python
In [38]: de_hi_unicode = 'grüezi'

In [39]: bytes(de_hi_unicode, encoding='utf-8')
Out[39]: b'gr\xc3\xbcezi'

In [40]: bytes(de_hi_unicode, encoding='utf-16')
Out[40]: b'\xff\xfeg\x00r\x00\xfc\x00e\x00z\x00i\x00'

In [41]: bytes(de_hi_unicode, encoding='utf-32')
Out[41]: b'\xff\xfe\x00\x00g\x00\x00\x00r\x00\x00\x00\xfc\x00\x00\x00e\x00\x00\x00z\x00\x00\x00i\x00\x00\x00'

```


#HSLIDE
### Ошибки


#VSLIDE
### Ошибки

```python
In [42]: hi_unicode = 'привет'

In [43]: hi_unicode.encode('ascii')
------------------------------------------------------------
UnicodeEncodeError         Traceback (most recent call last)
<ipython-input-211-ec69c9fd2dae> in <module>()
----> 1 hi_unicode.encode('ascii')

UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)
```

#VSLIDE
### Ошибки

```python
In [44]: de_hi_unicode = 'grüezi'

In [45]: de_hi_unicode.encode('ascii')
------------------------------------------------------------
UnicodeEncodeError         Traceback (most recent call last)
<ipython-input-216-31c172a5bbb1> in <module>()
----> 1 de_hi_unicode.encode('ascii')

UnicodeEncodeError: 'ascii' codec can't encode character '\xfc' in position 2: ordinal not in range(128)`:w

```


#VSLIDE
### Ошибки

```python
In [46]: hi_unicode = 'привет'

In [47]: hi_bytes = hi_unicode.encode('utf-8')

In [48]: hi_bytes.decode('ascii')
------------------------------------------------------------
UnicodeDecodeError         Traceback (most recent call last)
<ipython-input-219-aa0ada5e44e9> in <module>()
----> 1 hi_bytes.decode('ascii')

UnicodeDecodeError: 'ascii' codec can't decode byte 0xd0 in position 0: ordinal not in range(128)

```

#VSLIDE
### Ошибки

```python
In [49]: utf_16 = de_hi_unicode.encode('utf-16')

In [50]: de_hi_unicode = 'grüezi'

In [51]: utf_16 = de_hi_unicode.encode('utf-16')

In [52]: utf_16.decode('utf-8')
------------------------------------------------------------
UnicodeDecodeError         Traceback (most recent call last)
<ipython-input-226-4b4c731e69e4> in <module>()
----> 1 utf_16.decode('utf-8')

UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

```

#VSLIDE
### Надо знать какая кодировка использовалась


```python
In [53]: hi_unicode = 'привет'

In [54]: hi_bytes = hi_unicode.encode('utf-8')

In [55]: hi_bytes
Out[55]: b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'

In [56]: hi_bytes.decode('utf-16')
Out[56]: '뿐胑룐닐뗐苑'

```

#HSLIDE
### Обработка ошибок

#VSLIDE
### Обработка ошибок

```python
In [57]: de_hi_unicode = 'grüezi'

In [58]: de_hi_unicode.encode('ascii', 'replace')
Out[58]: b'gr?ezi'

In [59]: de_hi_unicode.encode('ascii', 'namereplace')
Out[59]: b'gr\\N{LATIN SMALL LETTER U WITH DIAERESIS}ezi'

In [60]: de_hi_unicode.encode('ascii', 'ignore')
Out[60]: b'grezi'

```

#VSLIDE
### Обработка ошибок

```python
In [61]: de_hi_unicode = 'grüezi'

In [62]: de_utf8 = de_hi_unicode.encode('utf-8')

In [63]: de_utf8
Out[63]: b'gr\xc3\xbcezi'

In [64]: de_utf8.decode('ascii', 'ignore')
Out[64]: 'grezi'

In [65]: de_utf8.decode('ascii', 'replace')
Out[65]: 'gr��ezi'
```

#HSLIDE
### Unicode sandwich

#VSLIDE
### Unicode sandwich

![unicode-sandwich](http://engineering.cerner.com/assets/2014-08-02-the-plain-text-is-a-lie/unicode-sandwich.png)

#VSLIDE
### Unicode sandwich

![unicode-sandwich](https://astrodsg.github.io/static/img/blog/unicode_sandwich.jpg)

#VSLIDE
### Работа с файлами

```python

In [66]: de_hi_unicode = 'grüezi'

In [67]: f = open('test_unicode.txt', 'w')

In [68]: f.write(de_hi_unicode+'\n')
Out[68]: 7

In [69]: f.close()

In [70]: open('test_unicode.txt').read()
Out[70]: 'grüezi\n'

```

#VSLIDE
### Работа с файлами

По умолчанию:
```python
In [71]: import locale

In [72]: locale.getpreferredencoding()
Out[72]: 'UTF-8'

```

#VSLIDE
### Работа с файлами

```python
In [73]: de_hi_unicode = 'grüezi'

In [74]: f = open('test_unicode.txt', 'w', encoding='utf-8')

In [75]: f.write(de_hi_unicode+'\n')
Out[75]: 7

In [76]: f.close()

In [77]: open('test_unicode.txt',  encoding='utf-8').read()
Out[77]: 'grüezi\n'

```

#VSLIDE
### Работа с файлами


```python
In [78]: file_content = open('test_unicode.txt', 'rb').read()

In [79]: file_content
Out[79]: b'gr\xc3\xbcezi\n'

In [80]: file_content.decode('utf-8')
Out[80]: 'grüezi\n'
```

#VSLIDE

# &#128561;

#VSLIDE

# &#9749; &#127829; &#127828;

#VSLIDE

### &#128123; &#129417; &#9749; &#128013; &#127829; &#127828;

### &#128512; &#128519; &#128520; &#128521; &#128564; &#128561;

