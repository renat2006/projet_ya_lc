# Техническое задание:

- меню ввода темы презентации
    * Заголовок
    * поле для ввода
    * кнопка "Далее"

![hippo](tz/1.gif)

- Меню выбора шаблона
    * Заголовок
    * Слайдер для выбора шаблона презентации
    * кнопка "Далее"

![hippo](tz/ScreenRecorderProject7.gif)

- Алгоритм генерирования презентаций, посредством библиотек:
    * python-pptx
    * wikipedia

- предпросмотр готового результата
    * Заголовок
    * слайдер для просмотра презентации

![hippo](tz/4.gif)

- возможность изменения некоторых параметров(не реализовано)
- возможность загружать в общий доступ свои шаблоны(не реализовано)

## Файлы

* [main.py](https://github.com/renat2006/projet_ya_lc/blob/master/main.py) <br>  
  ___Это основной файл, в котором находится логика программы, также основные формы и алгоритмы___
* [variables.py](https://github.com/renat2006/projet_ya_lc/blob/master/variables.py) <br>  
  ___Здесь хранятся основные переменные, для удобного доступа из других файлов___
* [generator.py](https://github.com/renat2006/projet_ya_lc/blob/master/generator.py) <br>  
  ___Здесь происходит основной процесс генерации презентаций___
* [text_parser.py](https://github.com/renat2006/projet_ya_lc/blob/master/text_parser.py)  <br>  
  ___Здесь происходит парсинг поисковой выдачи___
* [dialog.py](https://github.com/renat2006/projet_ya_lc/blob/master/dialog.py) <br>  
  ___Здесь находится макет диалогового окна___

## Классы

`File_viewer` - Класс для работы с файлами и конвертации **pptx** в **png** <br>  
`Main_window` - Окно ввода темы<br>  
`Window2` - Окно выбора шаблона <br>  
`Window3` - Окно предпросмотра презентации <br>  
`Generator` - Класс генерирования презентаций и записи информации в txt<br>  
`CustomDialog`  - Класс c моделью диалогового окна<br>

## Библиотеки

___Все используемые библиотеки находятся в
файле [requirements.txt](https://github.com/renat2006/projet_ya_lc/blob/master/requirements/requirements.txt)___

* [PyQt5](https://pypi.org/project/PyQt5/)
  Используется для вывода графического интерфейса
* [wikipedia](https://pypi.org/project/wikipedia/)
  Википедия - это библиотека Python, которая упрощает доступ и анализ данных из Википедии
* [python-pptx](https://pypi.org/project/python-pptx/)
  python-pptx - это библиотека Python для создания и обновления файлов PowerPoint (.pptx).

