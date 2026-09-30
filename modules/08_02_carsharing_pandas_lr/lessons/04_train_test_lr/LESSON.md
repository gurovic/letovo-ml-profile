Основная линия: выделить признак и цель, отложить часть строк через `train_test_split` и обучить `LinearRegression`: `fit` на train, `predict` на test.

Побочно: почему нельзя учить и проверять на одних и тех же строках и зачем фиксировать `random_state`.

| Линия | На паре |
|---|---|
| Анализ данных | Столбец `accommodates` как таблица `X` из одного столбца, столбец `price` как `y` |
| ML | `train_test_split`, `LinearRegression`, `fit`, `predict`, `coef_` и `intercept_` |
