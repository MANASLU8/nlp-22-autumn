# Tokenizer

## Tests

Тесты для токенизации в [projects/mansurov-project/source/tests/test_tokenizer.py]()

# Spellfix

## Tests

Тесты для исправления ошибок в [projects/mansurov-project/source/tests/test_spellcheck.py]()

## Modules

### create_dict.py

Создает словарь по токенизированным данным из файлов
`projects/mansurov-project/assets/annotated-corpus/train/*`

### hirshberg.py

Реализует алгоритм Хиршберга. 
Содержит 
- функцию нахождения расстояния между словами;
- функцию находжения операций для преобразования одного слова в другое
- класс с рассояниями между символами на клавиатуре (вычисление рассояний для клавиатуры  QWERTY или получение рассояний из файла)

### spellcheck.py

Проводит поиск слова в словаре двоичным поиском. Если слово не найдено - находит ближайшее к нему, используя расстояние Левенштайна

### fix_corrupted

Содержит функцию для исправления опечаток в тексте.

Исправляет опечатки во всех текстах датасета, результирующие значения записывает в файл `projects/mansurov-project/assets/test-corrupted-fixed.csv`

Вычисляет среднее значение и записывает его в `projects/mansurov-project/assets/test-corrupted-fixed.csv`

### other

В файле spellcheck.py импорт модуля hirschberg должен быть
`from hirschberg import lev_hirschberg, len_lev_hirschberg`
для запуска файлов и
`from .hirschberg import lev_hirschberg, len_lev_hirschberg`
для запуска тестов.

# Trigrams

## Modules

### get_ngrams.py

Содержит следующие функции:
- выбор только словоформ/лексем
- очистка коллекции слов от знаков препинания и стоп слов 
- подсчет триграмм
- посчет слов

Результаты каждой функции сохраняются в файлы

В начале файла стоит параметр `data_type_number` позволяющий задать работу с словоформами или лексемами

### calculate_measure.py

Содержит функции для расчета MI и T-score для коллекции слов с помощью реализованного алгоритма или библиотеки `nltk`

В начале файла стоит параметр `data_type_number` позволяющий задать работу с словоформами или лексемами

## Results

Триграммы с наибольшим показателем находятся в файлах.

|тип|значение|файл|
|-|-|-|
|словоформы|MI|words-MI-compare.tsv|
|словоформы|T-score|words-T-compare.tsv|
|лексемы|MI|lexemes-MI-compare.tsv|
|лексемы|T-score|lexemes-T-compare.tsv|
