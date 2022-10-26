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