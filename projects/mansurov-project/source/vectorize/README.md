# Векторизация текста

## Задания

1. Формирование словаря токенов и матрицы "термин-документ"

- модуль `matrix.py` содержит классы словаря и матрицы

- модуль `get_data.py`
  - `collect_words()`, `filter_words_collection()`, `sort_words_collection()` создают словарь токенов, отсортированный по алфавиту и отфильтрованный, в файле `terms.tsv`
  - `create_term_document()` создает матрицу "термин-документ" и сохраняет в файл `tdm.tsv`

2. tfidf векторизация

- модуль `vectorize.py` класс `VectorizationTFIDF`
  - метод get_text_vector преобразовывает произвольный текст в вектор значений tf-idf

3. w2v векторизация

- модуль `vectorize.py` класс `VectorizationNeuro`
  - метод get_text_vector преобразовывает произвольный текст в вектор значений

4. Тестирование модели w2v

- модуль `cosine_test.py`
- результат находится в файле `cosine_test.txt`

5. PCA для tfidf векторизации

- модуль `vectorize.py` класс VectorizationTFIDF метод save_pca_scores - для 4000 предложений из тренировочного сета находятся вектора по которым считается PCA. Объект PCA сохраняется в `pca.pkl`

6. Сравнение векторизации w2v и pca(tfidf)

- модуль `model_compare.py`
- результат находится в файле `compare_test.txt`

7. Векторизация текста с взвешенным средним по предложению

- модуль `vectorize.py` метод `vectorize_text()`

8. Векторизация тестовой выборки

- модуль `vectorize.py` метод `vectorize_test()`
- векторизовано 1560 текстов
