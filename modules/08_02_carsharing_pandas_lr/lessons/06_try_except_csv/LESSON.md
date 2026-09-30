Основная линия: загрузить CSV так, чтобы отсутствие файла давало понятную ошибку, и убрать строки без цены или числа гостей до любой модели.

Побочно: проверка, что после очистки таблица не пустая и в ней есть столбцы `accommodates` и `price`.

| Линия | На паре |
|---|---|
| Python | `try` и `except FileNotFoundError`; функции `load_listings`, `clean_listings`, `assert_usable` |
| Анализ данных | `read_csv` и `dropna` по столбцам `accommodates` и `price` |
