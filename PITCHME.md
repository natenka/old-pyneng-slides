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

In [4]: type(s)
Out[4]: str

In [6]: s.upper()
Out[6]: 'ПРИВЕТ'
```

#VSLIDE
### str

```python
In [188]: hi = '\u043f\u0440\u0438\u0432\u0435\u0442'

In [189]: print(hi)
привет

In [190]: len(hi)
Out[190]: 6
```


#VSLIDE
### ord

Функция ord возвращает значение кода Unicode для символа:
```python
In [8]: ord('п')
Out[8]: 1087

In [1]: hex(ord("a"))
Out[1]: '0x61'
```

#VSLIDE
### chr

Функция chr возвращает строку Unicode, которая символу, чем код был передан как аргумент:
```python
In [156]: chr(1087)
Out[156]: 'п'

In [160]: chr(8364)
Out[160]: '€'

In [161]: chr(9731)
Out[161]: '☃'

```


#HSLIDE
### bytes


#VSLIDE
### bytes

```python
In [20]: hi_bytes = b"Hello"

In [25]: type(hi_bytes)
Out[25]: bytes

In [22]: hi_bytes.upper()
Out[22]: b'HELLO'

In [23]: hi_bytes.find(b'l')
Out[23]: 2

In [24]: len(hi_bytes)
Out[24]: 5

```

#VSLIDE
### bytes

Можно работать с байтовыми строками, как с unicode строками:
```python
In [36]: d = {b'hi':'Hello', b'by':'Goodbye'}

In [37]: d[b'hi']
Out[37]: 'Hello'

In [38]: d['hi']
----------------------------------------------------------
KeyError                 Traceback (most recent call last)
<ipython-input-38-259732fc8381> in <module>()
----> 1 d['hi']

KeyError: 'hi'

```

#VSLIDE
### bytes

```python
In [1]: import subprocess

In [2]: result = subprocess.run('ls', stdout=subprocess.PIPE)

In [3]: output = result.stdout

In [4]: output
Out[4]: b'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'

In [5]: type(output)
Out[5]: bytes
```

#VSLIDE
### Non ASCII

```python
In [39]: test = b'привет'
  File "<ipython-input-39-e8b153ea3e66>", line 1
    test = b'привет'
          ^
SyntaxError: bytes can only contain ASCII literal characters.
```

#HSLIDE
### encode или decode

#VSLIDE

#### unicode .encode() &#8594; bytes
#### bytes .decode() &#8594; unicode

```python
In [19]: hi_unicode = 'привет'

In [19]: hi_bytes = hi_unicode.encode('utf-8')

In [19]: hi_bytes
Out[19]: b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'

In [19]: len(hi_bytes)
Out[19]: 12

In [20]: hi_bytes.decode('utf-8')
Out[20]: 'привет'
```

#VSLIDE
### encode или decode

```python
In [13]: import subprocess

In [14]: result = subprocess.run('ls', stdout=subprocess.PIPE)

In [15]: result.stdout
Out[15]: b'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode или decode

```python
In [16]: output_unicode = result.stdout.decode('utf-8')

In [17]: output_unicode
Out[17]: 'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode или decode

```python
In [20]: result = subprocess.run('ls', stdout=subprocess.PIPE, encoding='utf-8')

In [21]: result.stdout
Out[21]: 'about.md\nacknowledgments.md\nbook\nbook.json\ncourse_presentations\ncourse_presentations.zip\ncover.jpg\nexamples\nexamples.tar.gz\nexamples.zip\nexercises\nexercises.tar.gz\nexercises.zip\nfaq.md\nhowto.md\nimages\nLICENSE.md\nREADME.md\nresources\nschedule.md\nSUMMARY.md\ntestimonials.md\nToDo.md\n'
```

#VSLIDE
### encode или decode


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

#HSLIDE
### Ошибки


#VSLIDE
### Ошибки

```python
In [210]: hi_unicode = 'привет'

In [211]: hi_unicode.encode('ascii')
------------------------------------------------------------
UnicodeEncodeError         Traceback (most recent call last)
<ipython-input-211-ec69c9fd2dae> in <module>()
----> 1 hi_unicode.encode('ascii')

UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)
```

#VSLIDE
### Ошибки

```python
In [215]: de_hi_unicode = 'grüezi'

In [216]: de_hi_unicode.encode('ascii')
---------------------------------------------------------------------------
UnicodeEncodeError                        Traceback (most recent call last)
<ipython-input-216-31c172a5bbb1> in <module>()
----> 1 de_hi_unicode.encode('ascii')

UnicodeEncodeError: 'ascii' codec can't encode character '\xfc' in position 2: ordinal not in range(128)`:w

```


#VSLIDE
### Ошибки

```python
In [217]: hi_unicode = 'привет'

In [218]: hi_bytes = hi_unicode.encode('utf-8')

In [219]: hi_bytes.decode('ascii')
------------------------------------------------------------
UnicodeDecodeError         Traceback (most recent call last)
<ipython-input-219-aa0ada5e44e9> in <module>()
----> 1 hi_bytes.decode('ascii')

UnicodeDecodeError: 'ascii' codec can't decode byte 0xd0 in position 0: ordinal not in range(128)

```

#VSLIDE
### Ошибки

```python
In [223]: utf_16 = de_hi_unicode.encode('utf-16')

In [224]: de_hi_unicode = 'grüezi'

In [225]: utf_16 = de_hi_unicode.encode('utf-16')

In [226]: utf_16.decode('utf-8')
------------------------------------------------------------
UnicodeDecodeError         Traceback (most recent call last)
<ipython-input-226-4b4c731e69e4> in <module>()
----> 1 utf_16.decode('utf-8')

UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

```

#VSLIDE
### Ошибки


```python
In [20]: hi_unicode = 'привет'

In [20]: hi_bytes = hi_unicode.encode('utf-8')

In [20]: hi_bytes
Out[20]: b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'

In [20]: hi_bytes.decode('utf-16')
Out[20]: '뿐胑룐닐뗐苑'

```

#HSLIDE
### Обработка ошибок

#VSLIDE
### Обработка ошибок



#HSLIDE
### Unicode sandwic

#VSLIDE
### Unicode sandwich

![unicode-sandwich](http://engineering.cerner.com/assets/2014-08-02-the-plain-text-is-a-lie/unicode-sandwich.png)

#VSLIDE
### Unicode sandwich

![unicode-sandwich](https://nedbatchelder.com/text/unipain_pix/034.png)

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

&#128564;
&#128561;

При этом модуль может автоматически конвертировать байты.

