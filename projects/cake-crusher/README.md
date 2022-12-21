# Cake crusher
____
## Настройка Окружения
____
Для настройки окружения и установки зависимостей требуется выполнить следующую команду из корневой директории проекта (должна быть установлена anaconda):

```
conda env create -f assets/environment.yml
conda activate cake-crusher
set PYTHONPATH=./source
```
# Запуск проекта
____
## 1. Токенизатор текстовых файлов (+ стемматизация, лемматизация)
Данный модуль позволяет токенизировать текстовый датасет, состоящий из файлов. Для токенов также проводится стемматизация и лемматизация. Результат представляется в виде tsv файлов в следующей директории: 
`assets/annotated-corpus`.

С целью токенизации датасета требуется выполнить следующую команду из корневой директории проекта:
`python source/tokenization/__main__.py full/path/to/dataset/`

Система отображает сообщения о текущей обрабатываемой категории.
```
20news-bydate-test >>>
        alt.atheism
        comp.graphics
        comp.os.ms-windows.misc
```

### Запуск тестов токенизации
Для системы разработан набор модульных тестов, позволяющих оценить корректность генерируемых результатов. Для запуска тестов используется следующая команда, которую необходимо выполнять из корневой директории проекта:
`python source/tokenization/tests/test_tokenizer.py`

Система отображает стандартный отчет о результатах выполнения тестов:
```
.......
----------------------------------------------------------------------
Ran 9 tests in 0.005s

OK
```
____
## 2. Исправитель опечаток
Модуль использует алгоритм Левенштейна для поиска редакционного расстояния. 
Учитывается расстояние между буквами при использовании раскладки `QWERTY`.
### 2.1 Создание словаря
Чтобы создать словарь, необходимо запустить программу `dict-creator.py`.
Словарь создается на основе tsv файлов, сгенерированных модулем токенизации.
Можно сократить словарь, запустив скрипт `dict-cleaner.py`.
Результат работы:
`The dictionary has: 150015 tokens`
### 2.2 Запуск корректора
Найти и сохранить невыравненные файлы, запустив `typos-fixer/unaligned_finder.py`.
Запустить программу `typos-fixer/__main__.py`. Скорректированные токены записываются в директорию 
`assets/annotated-corpus/corrected_test` в виде tsv файлов.
### 2.3 Тестирование модуля исправления опечаток
`python source/typos_fixer/tests/typos-fixer-test.py`
### 2.4 Оценка модуля исправления опечаток
Необходимо запустить скрипт `evaluator.py`. Программа выдает отчет об исправлении опечаток:
```
Corrected files count is 296
Test tokens count is 56983
Corrupted tokens count is 9957
Corrupted tokens in corrupted set: 17.473632486882053
Corrected tokens count is 5044
Corrupted tokens in corrected set: 9.401049435796642
Difference is 8.072583051085411
```
____
## 3. N-grams
Модуль находит меру ассоциативной связности для n-грам, используя оценку t-score. По умолчанию для n = 3.

Для запуска требуется выполнить следующую команду из корневой директории проекта:
`python source/n_grams/__main__.py`

Результат представлен в виде столбчатой диаграммы для 30 триграмм, получивших наибольшую оценку.
____
## 4. Text vectorization
Модуль `vectorization` предоставляет 2 метода для векторизации текста: 
* **векторизация через среднее tf-idf отдельных предложений текста**
* **text2sentence2word2vec**

_Далее важен порядок запуска_.
### 4.1 Создание словаря
Чтобы создать словарь, необходимо запустить `vectorization/dictionary.py`.
Словарь создается на основе tsv файлов, сгенерированных модулем токенизации.

Результат работы:
`The dictionary has: 32140 tokens`
### 4.2 Создание матрицы termin-document
Чтобы создать матрицу термин-документ, необходимо запустить `vectorization/dictionary.py`.
### 4.3 Обучение моделей
Для обучения моделей необходимо запустить скрипты 
`vectorization/custom_model_tf_idf.py` и `vectorization/w2vec.py`
### 4.4 Запуск метода векторизации через среднее tf-idf отдельных предложений текста
Метод `custom_vectorize` доступен из файла `vectorization/custom_model_tf_idf.py`. Принимает на вход произвольный текст.
### 4.5 Запуск метода векторизации text2sentence2word2vec
Метод `w2vec_vectorize` доступен из файла `vectorization/w2vec.py`. Принимает на вход произвольный текст.
### 4.6 Демонстрация работы модели word2vec
Для демонстрации работы модели word2vec необходимо запустить скрипт `vectorization/w2vec_demo.py`.

Результат работы:
```
{
'word': 'research', 
'similar': {'scientific': 0.86, 'analysis': 0.78}, 
'same_field': {'study': 0.76, 'theory': 0.61}, 
'different': {'fish': 0.22, 'color': 0.09}
}
```
### 4.7 Сравнение моделей
Для сравнения моделей необходимо запустить скрипт `vectorization/comparison.py`.

Результат работы:
```
Test 1. time: 10.35 sec %% Custom cosine similarity is 0.71
Test 1. time: 0.84 sec %% Word2vec cosine similarity is 0.85
```
### 4.8 Векторизация в формат tsv
Для преобразования документов датасета 
в векторное представление с использованием text2sentence2word2vec применяется скрипт `vectorization/test_vectorizer.py`
____
## 5. Text classification
Классификация текстов на основе ранее полученных векторных представлений.
Для прохождения всего процесса машинного обучения (получение данных, обработка данных, обучение моделей, оценка на тестовых данных) необходимо запустить `classification/clf_exps.py`.
В выводе представлены гиперпараметры, `confusion matrix` и метрики для используемых моделей:
```
Training MLPClassifier(max_iter=500)...
MLPClassifier(max_iter=500) training time: 73.69797086715698

Reference   0     1    2     3    4    5    6
Actual                                       
0          79    13    0    40   41   60   86
1           3  1685   28    78  156    2    3
2           0   141  156    67   26    0    0
3           4   128   26  1184  159    6   83
4          12   345    9   189  896   12  116
5          31    18    0    26   25  236   62
6          42    30    2   116  171   68  872

Custom | Library Accuracy: 0.68 | 0.68
Custom | Library Precision: 0.67 | 0.67
Custom | Library Recall: 0.68 | 0.68
Custom | Library F1: 0.67 | 0.67
```
____
## 5. Topic modelling
Кластеризация текстов по темам на основе ранее полученных векторных представлений.
Необходимо запустить `topic_modelling/lda.py`.
В выводе представлены: обучаемая модель, топ документов для каждой темы, топ слов для каждой темы, метрика perplexity.
```
Model: LatentDirichletAllocation(n_components=10)

                                    top1                             top2                              top3
Topic0     talk.politics.mideast/77370.tsv  talk.politics.mideast/77275.tsv   talk.politics.mideast/77389.tsv
Topic1              misc.forsale/76812.tsv        sci.electronics/54333.tsv                 sci.med/59564.tsv
Topic2            comp.windows.x/68198.tsv          comp.graphics/38851.tsv           comp.graphics/39007.tsv
...
          Word 0    Word 1        Word 2   Word 3     Word 4
Topic 0  turkish  armenian        people      gun  armenians
Topic 1    lines   subject  organization  posting       host       
Topic 2      use      file     available    data    window
...
4687.86
```