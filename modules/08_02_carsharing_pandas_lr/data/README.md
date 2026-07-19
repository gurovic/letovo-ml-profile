# Данные модуля 2 (Airbnb listings)

| Файл | Назначение |
|---|---|
| `listings.csv` | Учебный срез объявлений Airbnb (Porto, ~300 строк) |
| `generate_listings.py` | Пересборка CSV: Inside Airbnb → фильтр → sample (seed 42); при сбое сети — synthetic |

## Источник

- **Inside Airbnb**, город Porto (Norte, Portugal), снимок `2024-12-14`
- Файл-источник: `data/listings.csv.gz` (detailed), URL в `generate_listings.py`
- Локальный кэш сырого gz: `data/_cache/` (не канон модуля; можно удалить и скачать заново)
- Лицензия данных Inside Airbnb: **CC0 1.0** (публичный домен / отказ от прав) — см. [insideairbnb.com](https://insideairbnb.com/data-policies/)

Учебный CSV — **сэмпл и упрощённая схема** для 8 класса (pandas + LinearRegression), не полный дамп города.

## Столбцы

| Столбец | Роль | Примечание |
|---|---|---|
| `listing_id` | id | `L0001` … |
| `accommodates` | feature (main) | int; бывш. роль `distance_km` |
| `price` | **target** | float, nightly; бывш. роль `duration_min` |
| `number_of_reviews` | feature | int; бывш. роль `hour` |
| `neighbourhood` | categorical | short English: center, riverside, old_town, beach, suburb, east, university; бывш. `zone` |
| `room_type` | categorical | `entire` / `private` / `shared`; бывш. `vehicle_type` |
| `bedrooms` | feature (optional) | int; для пар с несколькими признаками (уроки 17–18 / multi-feature) |

Фильтры при сборке: цена в \[20, 350\], `accommodates` 1–12, только выбранные районы (маппинг в скрипте), sample **300** строк, `seed=42`.

## Пересборка

```bash
# из кэша (без сети), если gz уже в data/_cache/
python modules/08_02_carsharing_pandas_lr/data/generate_listings.py --from-cache

# скачать gz заново (нужен интернет) и пересобрать
python modules/08_02_carsharing_pandas_lr/data/generate_listings.py

# только synthetic (если сеть недоступна)
python modules/08_02_carsharing_pandas_lr/data/generate_listings.py --synthetic
```

После пересборки скопируйте `listings.csv` в папки уроков и `artifact/starter/` (или повторите шаг распространения из задания на замену датасета).
