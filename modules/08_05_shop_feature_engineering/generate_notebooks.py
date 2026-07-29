#!/usr/bin/env python3
"""Generate the 18 notebooks for module 08_05.

This file is the source of truth. Student notebooks contain unfinished code
and executable contracts; solutions repeat the same sections one by one.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CSV_NAMES = ("orders_slim.csv", "customers_slim.csv", "payments_slim.csv")
DIRS = (
    "01_feature_types_apply", "02_practice_apply_orders", "03_rfm_groupby",
    "04_practice_aggregates", "05_logging_raise", "06_practice_pipeline",
)
LOAD = """from pathlib import Path
import pandas as pd
import numpy as np

def find_csv(name):
    for path in (Path(name), Path("../../data") / name):
        if path.exists():
            return path.resolve()
    raise FileNotFoundError(f"{name} не найден рядом с ноутбуком или в ../../data")

orders = pd.read_csv(find_csv("orders_slim.csv"), parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
customers = pd.read_csv(find_csv("customers_slim.csv"))
payments = pd.read_csv(find_csv("payments_slim.csv"))
assert len(orders) and len(customers) and len(payments)
assert orders["order_id"].is_unique and customers["customer_id"].is_unique
print(f"orders={len(orders)}, customers={len(customers)}, payments={len(payments)}")
"""
INTRO = """
Работаем как команда CRM маркетплейса: из трёх связанных таблиц нужно получить
объяснимые признаки, а не просто добиться вывода без ошибки. Перед каждой
операцией сформулируйте единицу наблюдения, ключ соединения и ожидаемое число
строк. После операции прочитайте assert как исполняемый контракт.

Сначала сделайте минимальный рабочий вариант, затем проверьте его на данных и
только после этого интерпретируйте результат. Не вводите метку churn: в этом
модуле мы строим и проверяем признаки, но не обучаем модель оттока.
"""
SOL_BANNER = "**Для преподавателя.** Секционный эталон урока и ДЗ; до сдачи ученикам не показывать."

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code(text):
    return {"cell_type": "code", "metadata": {}, "source": text.splitlines(keepends=True), "outputs": [], "execution_count": None}

def notebook(cells):
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"}}, "cells": cells}

def explain(i, heading, task, concept):
    return (f"## {i}. {heading}\n\n{task}\n\n"
            f"**Зачем:** {concept} Зафиксируйте ожидаемую форму результата до запуска. "
            "Если assert падает, сравните единицу наблюдения до и после операции; "
            "не удаляйте проверку и не подгоняйте константу под случайный вывод.")

def build(title, concept, lesson_sections, hw_sections):
    lesson = [md(f"# {title}\n\n{INTRO}\n\n**Центральная идея:** {concept}"), code(LOAD)]
    for i, (heading, task, stub, _) in enumerate(lesson_sections, 1):
        lesson += [md(explain(i, heading, task, concept)), code(stub)]
    homework = [md(f"# ДЗ: {title}\n\n{INTRO}\n\nPart A обязателен. Challenge выполняется после зелёных assert Part A."), code(LOAD)]
    for i, (heading, task, stub, _) in enumerate(hw_sections, 1):
        prefix = "### Part A — обязательно\n\n" if i == 1 else ("### Challenge\n\n" if i == 4 else "")
        homework += [md(prefix + explain(i, heading, task, concept)), code(stub)]
    solutions = [md(f"# Решения: {title}\n\n{SOL_BANNER}\n\n{INTRO}"), code(LOAD)]
    for i, (heading, _, _, answer) in enumerate(lesson_sections, 1):
        solutions += [md(f"## Урок. {i}. {heading}"), code(answer)]
    for i, (heading, _, _, answer) in enumerate(hw_sections, 1):
        solutions += [md(f"## ДЗ. {i}. {heading}"), code(answer)]
    return notebook(lesson), notebook(homework), notebook(solutions)

def rfm_code(frame="merged", result="rfm"):
    return f"""ref_date = {frame}["order_purchase_timestamp"].max()
{result} = ({frame}.groupby("customer_id").agg(
    last_purchase=("order_purchase_timestamp", "max"),
    Frequency=("order_id", "nunique"), Monetary=("payment_value", "sum")
).reset_index())
{result}["Recency"] = (ref_date - {result}["last_purchase"]).dt.days
{result} = {result}[["customer_id", "Recency", "Frequency", "Monetary"]]
"""

SPECS = []

SPECS.append((
"Типы признаков и apply на заказах",
"Тип признака определяет допустимое преобразование; ключ и форма таблицы определяют корректность join.",
[
("Три таблицы — три единицы наблюдения","Посчитайте строки и назовите единицу наблюдения каждой таблицы.",
"""sizes = {}  # TODO: orders/customers/payments -> len
assert sizes == {"orders": 3500, "customers": 778, "payments": 3500}
UNITS_NOTE = ""  # TODO: не менее 140 символов
assert len(UNITS_NOTE) >= 140
""","""sizes = {"orders": len(orders), "customers": len(customers), "payments": len(payments)}
UNITS_NOTE = "Строка orders — заказ, customers — запись клиента, payments — оплата заказа. Перед join проверяем ключ и ожидаем сохранение 3500 заказов."
assert sizes == {"orders": 3500, "customers": 778, "payments": 3500}
"""),
("Числовые и категориальные столбцы","Соберите словарь типов вручную для четырёх бизнес-полей.",
"""feature_types = {"payment_value": None, "payment_type": None, "customer_state": None, "order_status": None}  # TODO
assert feature_types["payment_value"] == "numeric"
assert set(feature_types.values()) == {"numeric", "categorical"}
""","""feature_types = {"payment_value": "numeric", "payment_type": "categorical", "customer_state": "categorical", "order_status": "categorical"}
assert feature_types["payment_value"] == "numeric"
"""),
("Безопасный join заказов и оплат","Соедините по order_id слева и докажите сохранение строк.",
"""orders_pay = None  # TODO
assert isinstance(orders_pay, pd.DataFrame) and len(orders_pay) == len(orders)
assert {"payment_type", "payment_value"} <= set(orders_pay)
assert orders_pay["order_id"].is_unique
""","""orders_pay = orders.merge(payments, on="order_id", how="left", validate="one_to_one")
assert len(orders_pay) == len(orders) and orders_pay["order_id"].is_unique
"""),
("Функция категории оплаты","Напишите именованную функцию amount_band и проверьте границы 100 и 300.",
"""def amount_band(value):
    # TODO: small <=100, mid <=300, иначе big
    ...
assert [amount_band(x) for x in (50, 100, 101, 300, 301)] == ["small","small","mid","mid","big"]
""","""def amount_band(value):
    if value <= 100: return "small"
    if value <= 300: return "mid"
    return "big"
assert amount_band(300) == "mid"
"""),
("Apply к одному столбцу","Примените amount_band и проверьте покрытие всех строк.",
"""orders_pay["payment_band"] = None  # TODO
band_counts = None  # TODO
assert set(orders_pay["payment_band"]) == {"small", "mid", "big"}
assert int(band_counts.sum()) == len(orders_pay)
""","""orders_pay["payment_band"] = orders_pay["payment_value"].apply(amount_band)
band_counts = orders_pay["payment_band"].value_counts()
assert int(band_counts.sum()) == len(orders_pay)
"""),
("Apply по строке","Рассчитайте days_to_deliver из двух дат с обработкой недоставленных заказов.",
"""orders_pay["days_to_deliver"] = None  # TODO: apply(axis=1)
assert orders_pay["days_to_deliver"].notna().sum() > 3000
assert orders_pay["days_to_deliver"].dropna().ge(0).all()
""","""orders_pay["days_to_deliver"] = orders_pay.apply(lambda r: (r["order_delivered_customer_date"] - r["order_purchase_timestamp"]).days if pd.notna(r["order_delivered_customer_date"]) else np.nan, axis=1)
assert orders_pay["days_to_deliver"].dropna().ge(0).all()
"""),
("Apply или векторизация","Повторите расчёт векторно и сравните совпадение.",
"""vector_days = None  # TODO
same_days = None  # TODO
assert same_days is True
VECTOR_NOTE = ""  # TODO: минимум 160 символов
assert len(VECTOR_NOTE) >= 160
""","""vector_days = (orders_pay["order_delivered_customer_date"] - orders_pay["order_purchase_timestamp"]).dt.days
same_days = bool(vector_days.equals(orders_pay["days_to_deliver"]))
VECTOR_NOTE = "Apply удобен для сложного правила из нескольких полей строки, но разность datetime уже векторизована. Векторная запись короче, обычно быстрее и лучше показывает смысл операции."
assert same_days and len(VECTOR_NOTE) >= 160
"""),
("Карточка признака","Опишите источник, тип, правило, пропуски и риск для days_to_deliver.",
"""FEATURE_CARD = ""  # TODO: минимум 240 символов
assert len(FEATURE_CARD) >= 240
assert all(word in FEATURE_CARD.lower() for word in ["источник", "пропуск", "риск"])
""","""FEATURE_CARD = "Источник: две даты orders. Тип: числовой, дни. Правило: delivery minus purchase; для недоставленного заказа пропуск сохраняется. Риск: признак появляется после покупки и может быть недоступен в момент раннего решения; отрицательные значения означают ошибку данных. Перед моделью проверяем момент доступности."
assert len(FEATURE_CARD) >= 240
""")
],[
("Диапазон дат","Найдите min/max и продолжительность наблюдения.", """min_date=max_date=None  # TODO
span_days=None  # TODO
assert str(min_date.date())=="2017-01-01" and str(max_date.date())=="2018-08-31"
assert span_days > 500
""","""min_date=orders["order_purchase_timestamp"].min(); max_date=orders["order_purchase_timestamp"].max()
span_days=(max_date-min_date).days
assert span_days > 500
"""),
("Доли типов оплаты","Получите нормированные доли и лидера.", """pay_share=None; top_payment=None  # TODO
assert np.isclose(pay_share.sum(),1)
assert top_payment=="credit_card"
""","""pay_share=payments["payment_type"].value_counts(normalize=True); top_payment=pay_share.idxmax()
assert top_payment=="credit_card"
"""),
("Признак is_card","Создайте бинарный признак через apply.", """payments["is_card"]=None  # TODO
assert set(payments["is_card"])=={0,1}
assert payments["is_card"].mean()>0.6
""","""payments["is_card"]=payments["payment_type"].apply(lambda x: int(x=="credit_card"))
assert set(payments["is_card"])=={0,1}
"""),
("Challenge: универсальный биннер","Верните функцию-замыкание для двух порогов.", """def make_binner(low, high):
    # TODO
    ...
binner=make_binner(100,300)
assert [binner(x) for x in (100,101,300,301)]==["small","mid","mid","big"]
""","""def make_binner(low, high):
    return lambda x: "small" if x<=low else ("mid" if x<=high else "big")
binner=make_binner(100,300)
assert binner(301)=="big"
"""),
("Challenge: инженерная записка","Сравните apply и векторизацию, укажите тест границ.", """APPLY_NOTE=""  # TODO
assert len(APPLY_NOTE)>=220
assert all(w in APPLY_NOTE.lower() for w in ["apply","вектор","границ"])
""","""APPLY_NOTE="Apply оставляем для составного построчного правила, когда ветвление использует несколько полей. Векторную операцию выбираем для арифметики столбцов: она проще и быстрее. Для биннинга отдельно тестируем значения на границах 100 и 300, а также пропуски, чтобы контракт категорий не менялся незаметно."
assert len(APPLY_NOTE)>=220
""")
]))

SPECS.append((
"Практика: признаки строки заказа",
"Признак должен быть вычислим в заявленный момент, сохранять форму данных и иметь проверяемый диапазон.",
[
("Календарные признаки","Создайте month и weekday векторно.", """work=orders.copy()
work["order_month"]=None; work["weekday"]=None  # TODO
assert work["order_month"].between(1,12).all()
assert work["weekday"].between(0,6).all()
""","""work=orders.copy()
work["order_month"]=work["order_purchase_timestamp"].dt.month
work["weekday"]=work["order_purchase_timestamp"].dt.weekday
assert work["weekday"].between(0,6).all()
"""),
("Выходной день через lambda","Сделайте is_weekend из weekday.", """work["is_weekend"]=None  # TODO
assert set(work["is_weekend"])=={0,1}
assert (work["is_weekend"] == work["weekday"].isin([5,6]).astype(int)).all()
""","""work["is_weekend"]=work["weekday"].apply(lambda d: int(d>=5))
assert set(work["is_weekend"])=={0,1}
"""),
("Join с оплатой","Добавьте тип и сумму, используя validate.", """joined=None  # TODO
assert len(joined)==len(work) and joined["order_id"].is_unique
assert joined["payment_value"].notna().all()
""","""joined=work.merge(payments,on="order_id",how="left",validate="one_to_one")
assert len(joined)==len(work)
"""),
("Срок доставки","Создайте days_to_deliver векторно.", """joined["days_to_deliver"]=None  # TODO
assert joined["days_to_deliver"].dropna().ge(0).all()
assert joined["days_to_deliver"].notna().sum()>3000
""","""joined["days_to_deliver"]=(joined["order_delivered_customer_date"]-joined["order_purchase_timestamp"]).dt.days
assert joined["days_to_deliver"].dropna().ge(0).all()
"""),
("Порог выброса","Найдите p99 и выделите строки не ниже него; учитывайте совпадения на границе.", """p99=None; outlier_mask=None  # TODO
assert p99>0 and outlier_mask.dtype==bool
assert 1 <= int(outlier_mask.sum()) < len(joined)
""","""p99=float(joined["days_to_deliver"].quantile(.99)); outlier_mask=joined["days_to_deliver"]>=p99
assert 1<=int(outlier_mask.sum())
"""),
("Категория срока","Напишите функцию: missing, fast <=7, normal <=14, slow.", """def delivery_band(days):
    # TODO
    ...
joined["delivery_band"]=joined["days_to_deliver"].apply(delivery_band)
assert {"fast","normal","slow"} <= set(joined["delivery_band"]) <= {"missing","fast","normal","slow"}
""","""def delivery_band(days):
    if pd.isna(days): return "missing"
    if days<=7: return "fast"
    if days<=14: return "normal"
    return "slow"
joined["delivery_band"]=joined["days_to_deliver"].apply(delivery_band)
assert {"fast","normal","slow"} <= set(joined["delivery_band"]) <= {"missing","fast","normal","slow"}
"""),
("Проверка формы и ключа","Соберите quality_checks из четырёх булевых проверок.", """quality_checks={"rows":None,"unique_key":None,"payment_complete":None,"dates_nonnegative":None}  # TODO
assert set(quality_checks.values())=={True}
""","""quality_checks={"rows":len(joined)==len(orders),"unique_key":joined["order_id"].is_unique,"payment_complete":joined["payment_value"].notna().all(),"dates_nonnegative":joined["days_to_deliver"].dropna().ge(0).all()}
assert set(quality_checks.values())=={True}
"""),
("Риск утечки времени","Объясните, когда delivery-признак недоступен.", """LEAKAGE_NOTE=""  # TODO
assert len(LEAKAGE_NOTE)>=240
assert all(w in LEAKAGE_NOTE.lower() for w in ["момент","достав","модель"])
""","""LEAKAGE_NOTE="Момент расчёта определяет допустимость признака. Дата доставки и итоговый срок известны только после доставки, поэтому модель, принимающая решение при оформлении заказа, не должна видеть days_to_deliver. Для позднего описательного отчёта признак допустим; документация обязана назвать момент доступности."
assert len(LEAKAGE_NOTE)>=240
""")
],[
("Средний чек по месяцам","Постройте Series из 12+ месяцев.", """joined=orders.merge(payments,on="order_id"); joined["month"]=joined["order_purchase_timestamp"].dt.to_period("M").astype(str)
month_mean=None  # TODO
assert len(month_mean)>=12 and month_mean.notna().all()
""","""joined=orders.merge(payments,on="order_id"); joined["month"]=joined["order_purchase_timestamp"].dt.to_period("M").astype(str)
month_mean=joined.groupby("month")["payment_value"].mean()
assert len(month_mean)>=12
"""),
("Доля card по weekday","Сгруппируйте бинарный признак.", """joined["weekday"]=joined["order_purchase_timestamp"].dt.weekday
joined["is_card"]=(joined["payment_type"]=="credit_card").astype(int)
weekday_card=None  # TODO
assert len(weekday_card)==7 and weekday_card.between(0,1).all()
""","""joined["weekday"]=joined["order_purchase_timestamp"].dt.weekday
joined["is_card"]=(joined["payment_type"]=="credit_card").astype(int)
weekday_card=joined.groupby("weekday")["is_card"].mean()
assert len(weekday_card)==7
"""),
("Лог преобразований","Запишите не менее пяти конкретных шагов.", """log_steps=[]  # TODO
assert len(log_steps)>=5 and all(isinstance(x,str) and len(x)>=12 for x in log_steps)
""","""log_steps=["loaded three source tables","parsed purchase and delivery dates","created calendar features","joined payments one-to-one","checked output shape and key"]
assert len(log_steps)>=5
"""),
("Challenge: функция признаков","Верните копию с четырьмя новыми столбцами.", """def add_order_features(frame):
    # TODO
    ...
featured=add_order_features(orders)
assert len(featured)==len(orders)
assert {"order_month","weekday","is_weekend","days_to_deliver"}<=set(featured)
assert "order_month" not in orders
""","""def add_order_features(frame):
    x=frame.copy(); x["order_month"]=x["order_purchase_timestamp"].dt.month; x["weekday"]=x["order_purchase_timestamp"].dt.weekday
    x["is_weekend"]=x["weekday"].ge(5).astype(int); x["days_to_deliver"]=(x["order_delivered_customer_date"]-x["order_purchase_timestamp"]).dt.days
    return x
featured=add_order_features(orders)
assert "order_month" not in orders
"""),
("Challenge: решение по выбросам","Обоснуйте сохранение или обработку p99.", """OUTLIER_NOTE=""  # TODO
assert len(OUTLIER_NOTE)>=240
assert all(w in OUTLIER_NOTE.lower() for w in ["p99","удал","бизнес"])
""","""OUTLIER_NOTE="Порог p99 выделяет редкие сроки, но автоматически удалять их нельзя: это могут быть реальные бизнес-кейсы с высокой ценой для клиента. Сначала проверяем качество дат и статус заказа, затем сохраняем флаг выброса. Удаление допустимо только при доказанной технической ошибке и с записью в лог."
assert len(OUTLIER_NOTE)>=240
""")
]))

SPECS.append((
"RFM через groupby",
"RFM переводит строки заказов в одну строку клиента по заранее зафиксированным агрегатам.",
[
("Проверка ключей","Проверьте уникальность ключей и покрытие оплат.", """key_checks={"orders":None,"customers":None,"payments":None}  # TODO
assert set(key_checks.values())=={True}
""","""key_checks={"orders":orders["order_id"].is_unique,"customers":customers["customer_id"].is_unique,"payments":payments["order_id"].is_unique}
assert set(key_checks.values())=={True}
"""),
("Таблица заказ+оплата","Сделайте one-to-one join.", """merged=None  # TODO
assert len(merged)==3500 and merged["payment_value"].notna().all()
""","""merged=orders.merge(payments,on="order_id",validate="one_to_one")
assert len(merged)==3500
"""),
("Опорная дата","Используйте максимум даты всей таблицы.", """ref_date=None  # TODO
assert ref_date==orders["order_purchase_timestamp"].max()
REF_NOTE=""  # TODO, >=160
assert len(REF_NOTE)>=160
""","""ref_date=orders["order_purchase_timestamp"].max()
REF_NOTE="Одна общая опорная дата делает Recency сопоставимым между клиентами. Если взять максимум внутри каждого клиента, Recency станет нулём для всех и потеряет смысл давности."
assert len(REF_NOTE)>=160
"""),
("Frequency","Посчитайте число уникальных order_id на клиента.", """frequency=None  # TODO: Series
assert len(frequency)==778 and int(frequency.sum())==3500
assert frequency.ge(1).all()
""","""frequency=merged.groupby("customer_id")["order_id"].nunique()
assert int(frequency.sum())==3500
"""),
("Monetary","Посчитайте сумму payment_value.", """monetary=None  # TODO
assert len(monetary)==778 and np.isclose(monetary.sum(),payments["payment_value"].sum())
assert monetary.gt(0).all()
""","""monetary=merged.groupby("customer_id")["payment_value"].sum()
assert np.isclose(monetary.sum(),payments["payment_value"].sum())
"""),
("Recency","Посчитайте дни от последней покупки до ref_date.", """last_purchase=None; recency=None  # TODO
assert len(recency)==778 and recency.ge(0).all()
assert recency.min()==0
""","""last_purchase=merged.groupby("customer_id")["order_purchase_timestamp"].max()
recency=(ref_date-last_purchase).dt.days
assert recency.min()==0
"""),
("Сборка RFM","Объедините три Series в DataFrame.", """rfm=None  # TODO
assert list(rfm.columns)==["customer_id","Recency","Frequency","Monetary"]
assert len(rfm)==778 and rfm["customer_id"].is_unique
""","""rfm=pd.concat([recency.rename("Recency"),frequency.rename("Frequency"),monetary.rename("Monetary")],axis=1).reset_index()
assert len(rfm)==778
"""),
("Профиль и интерпретация","Получите describe и объясните высокий M при низком F.", """stats=None; top5=None  # TODO
assert stats.shape==(8,3) and len(top5)==5 and top5["Monetary"].is_monotonic_decreasing
RFM_NOTE=""  # TODO >=220
assert len(RFM_NOTE)>=220
""","""stats=rfm[["Recency","Frequency","Monetary"]].describe(); top5=rfm.nlargest(5,"Monetary")
RFM_NOTE="Высокий Monetary при низком Frequency означает редкие крупные покупки, а не высокую лояльность автоматически. Recency показывает, насколько давно была последняя покупка. CRM должна читать три измерения вместе и проверить устойчивость сегмента, прежде чем выбирать коммуникацию."
assert len(RFM_NOTE)>=220
""")
],[
("Чистая функция build_rfm","Верните таблицу без изменения входа.", """def build_rfm(orders_df,payments_df):
    # TODO
    ...
rfm=build_rfm(orders,payments)
assert len(rfm)==778 and list(rfm.columns)==["customer_id","Recency","Frequency","Monetary"]
""","""def build_rfm(orders_df,payments_df):
    merged=orders_df.merge(payments_df,on="order_id",validate="one_to_one")
    ref_date=merged["order_purchase_timestamp"].max()
    out=merged.groupby("customer_id").agg(last=("order_purchase_timestamp","max"),Frequency=("order_id","nunique"),Monetary=("payment_value","sum")).reset_index()
    out["Recency"]=(ref_date-out["last"]).dt.days
    return out[["customer_id","Recency","Frequency","Monetary"]]
rfm=build_rfm(orders,payments)
"""),
("Frequency bands","Разбейте 1–2, 3–5, 6+ и найдите доли.", """rfm["freq_band"]=None; freq_share=None  # TODO
assert np.isclose(freq_share.sum(),1) and int(freq_share.size)==3
""","""rfm["freq_band"]=pd.cut(rfm["Frequency"],[0,2,5,np.inf],labels=["1-2","3-5","6+"])
freq_share=rfm["freq_band"].value_counts(normalize=True,sort=False)
assert np.isclose(freq_share.sum(),1)
"""),
("Давние клиенты","Получите десять максимальных Recency.", """oldest=None  # TODO
assert len(oldest)==10 and oldest["Recency"].is_monotonic_decreasing
""","""oldest=rfm.nlargest(10,"Recency")
assert oldest["Recency"].is_monotonic_decreasing
"""),
("Challenge: сверка инвариантов","Верните словарь проверок суммы и количества.", """checks={}  # TODO
assert set(checks)=={"customers","orders","money","nonnegative_recency"}
assert set(checks.values())=={True}
""","""checks={"customers":len(rfm)==customers["customer_id"].nunique(),"orders":int(rfm["Frequency"].sum())==len(orders),"money":np.isclose(rfm["Monetary"].sum(),payments["payment_value"].sum()),"nonnegative_recency":rfm["Recency"].ge(0).all()}
assert set(checks.values())=={True}
"""),
("Challenge: CRM-рекомендация","Сформулируйте действие и ограничение RFM.", """CRM_NOTE=""  # TODO
assert len(CRM_NOTE)>=260
assert all(w in CRM_NOTE.lower() for w in ["recency","frequency","monetary","огранич"])
""","""CRM_NOTE="Recency помогает выделить давно не покупавших, Frequency — регулярных, Monetary — клиентов с высокой суммой покупок. CRM может начать с персональной проверки редких дорогих клиентов и отдельной коммуникации частым. Ограничение: RFM описывает историю, не доказывает будущую покупку и не является меткой churn."
assert len(CRM_NOTE)>=260
""")
]))

SPECS.append((
"Практика: RFM плюс производные признаки",
"Производный признак полезен только при ясном правиле, корректной агрегации и документированном масштабе.",
[
("Базовый RFM","Соберите канонический RFM через одну цепочку.", """merged=orders.merge(payments,on="order_id",validate="one_to_one")
rfm=None  # TODO
assert len(rfm)==778 and {"Recency","Frequency","Monetary"}<=set(rfm)
""","""merged=orders.merge(payments,on="order_id",validate="one_to_one")
""" + rfm_code() + """assert len(rfm)==778
"""),
("Бинарная оплата","Создайте is_card перед агрегацией.", """merged["is_card"]=None  # TODO
assert set(merged["is_card"])=={0,1}
""","""merged["is_card"]=(merged["payment_type"]=="credit_card").astype(int)
assert set(merged["is_card"])=={0,1}
"""),
("Доля card","Агрегируйте среднее is_card на клиента и присоедините.", """card_share=None; rfm_plus=None  # TODO
assert len(rfm_plus)==len(rfm) and rfm_plus["share_card"].between(0,1).all()
""","""card_share=merged.groupby("customer_id")["is_card"].mean().rename("share_card")
rfm_plus=rfm.merge(card_share,on="customer_id",validate="one_to_one")
assert rfm_plus["share_card"].between(0,1).all()
"""),
("Средний срок доставки","Создайте и агрегируйте days_to_deliver.", """merged["days_to_deliver"]=None; delivery_mean=None  # TODO
rfm_plus=rfm_plus.merge(delivery_mean.rename("avg_days_to_deliver"),on="customer_id",how="left")
assert rfm_plus["avg_days_to_deliver"].notna().sum()>700
""","""merged["days_to_deliver"]=(merged["order_delivered_customer_date"]-merged["order_purchase_timestamp"]).dt.days
delivery_mean=merged.groupby("customer_id")["days_to_deliver"].mean()
rfm_plus=rfm_plus.merge(delivery_mean.rename("avg_days_to_deliver"),on="customer_id",how="left")
assert rfm_plus["avg_days_to_deliver"].notna().sum()>700
"""),
("Штат клиента","Присоедините категорию customer_state после агрегации.", """rfm_plus=None  # TODO: merge customers
assert len(rfm_plus)==778 and rfm_plus["customer_state"].notna().all()
""","""rfm_plus=rfm_plus.merge(customers[["customer_id","customer_state"]],on="customer_id",validate="one_to_one")
assert len(rfm_plus)==778
"""),
("Корреляция F и M","Рассчитайте Pearson и напишите осторожную интерпретацию.", """corr_fm=None; CORR_NOTE=""  # TODO
assert -1<=corr_fm<=1 and len(CORR_NOTE)>=190
assert "причин" in CORR_NOTE.lower()
""","""corr_fm=float(rfm_plus["Frequency"].corr(rfm_plus["Monetary"]))
CORR_NOTE="Положительная корреляция означает, что в этих данных клиенты с большим числом заказов обычно имеют большую суммарную оплату. Это не причинная связь: Monetary по определению накапливается с заказами, а размер чека и период наблюдения создают дополнительную вариацию."
assert -1<=corr_fm<=1
"""),
("Масштабированный score","Нормируйте F и M средними; меньший Recency должен повышать score.", """scored=rfm_plus.copy()
scored["score"]=None  # TODO
assert np.isfinite(scored["score"]).all()
assert scored.nlargest(1,"score").index.size==1
""","""scored=rfm_plus.copy()
scored["score"]=scored["Frequency"]/scored["Frequency"].mean()+scored["Monetary"]/scored["Monetary"].mean()-scored["Recency"]/scored["Recency"].mean()
assert np.isfinite(scored["score"]).all()
"""),
("Контракт RFM+","Проверьте границы, уникальность и отсутствие churn.", """checks={"unique":None,"frequency":None,"money":None,"share":None,"no_churn":None}  # TODO
assert set(checks.values())=={True}
""","""checks={"unique":rfm_plus["customer_id"].is_unique,"frequency":rfm_plus["Frequency"].ge(1).all(),"money":rfm_plus["Monetary"].gt(0).all(),"share":rfm_plus["share_card"].between(0,1).all(),"no_churn":"churn" not in rfm_plus}
assert set(checks.values())=={True}
""")
],[
("Median Monetary по штату","Сгруппируйте клиентскую таблицу.", """state_median=None  # TODO
assert len(state_median)==customers["customer_state"].nunique()
assert state_median.gt(0).all()
""","""state_median=rfm_plus.groupby("customer_state")["Monetary"].median()
assert state_median.gt(0).all()
"""),
("Квантили признаков","Получите 25/50/75 процентили RFM.", """quantiles=None  # TODO
assert quantiles.shape==(3,3) and list(quantiles.index)==[.25,.5,.75]
""","""quantiles=rfm_plus[["Recency","Frequency","Monetary"]].quantile([.25,.5,.75])
assert quantiles.shape==(3,3)
"""),
("Top-10 score","Отсортируйте и сохраните десять строк.", """top10=None  # TODO
assert len(top10)==10 and top10["score"].is_monotonic_decreasing
""","""top10=scored.nlargest(10,"score")
assert top10["score"].is_monotonic_decreasing
"""),
("Challenge: функция add_extras","Добавьте share_card и avg_days_to_deliver к RFM.", """def add_extras(rfm_df,merged_df):
    # TODO
    ...
extra=add_extras(rfm,merged)
assert len(extra)==len(rfm) and {"share_card","avg_days_to_deliver"}<=set(extra)
""","""def add_extras(rfm_df,merged_df):
    x=merged_df.copy(); x["is_card"]=(x["payment_type"]=="credit_card").astype(int)
    x["days_to_deliver"]=(x["order_delivered_customer_date"]-x["order_purchase_timestamp"]).dt.days
    agg=x.groupby("customer_id").agg(share_card=("is_card","mean"),avg_days_to_deliver=("days_to_deliver","mean"))
    return rfm_df.merge(agg,on="customer_id",how="left",validate="one_to_one")
extra=add_extras(rfm,merged)
"""),
("Challenge: паспорт score","Опишите формулу, масштаб, назначение и ограничения.", """SCORE_NOTE=""  # TODO
assert len(SCORE_NOTE)>=280
assert all(w in SCORE_NOTE.lower() for w in ["масштаб","recency","frequency","monetary","огранич"])
""","""SCORE_NOTE="Score складывает Frequency и Monetary после деления на их средние и вычитает нормированный Recency: недавняя активность повышает результат. Масштабирование не даёт денежным единицам автоматически доминировать. Назначение — ранжирование для исследования, не прогноз. Ограничение: веса выбраны экспертно и требуют проверки бизнес-эффекта."
assert len(SCORE_NOTE)>=280
""")
]))

SPECS.append((
"Логирование и raise: контракт preprocessing",
"Валидация останавливает неверные данные до признаков, а лог объясняет порядок успешно выполненных шагов.",
[
("Схема обязательных столбцов","Напишите require_columns с информативным KeyError.", """def require_columns(frame,required):
    # TODO
    ...
assert require_columns(orders,{"order_id","customer_id"}) is True
try: require_columns(orders,{"missing_column"})
except KeyError as e: missing_message=str(e)
assert "missing_column" in missing_message
""","""def require_columns(frame,required):
    missing=sorted(set(required)-set(frame.columns))
    if missing: raise KeyError(f"missing columns: {missing}")
    return True
assert require_columns(orders,{"order_id"}) is True
"""),
("Уникальный ключ заказов","Напишите проверку дублей order_id.", """def require_unique(frame,column):
    # TODO
    ...
assert require_unique(orders,"order_id") is True
bad=orders.head(2).copy(); bad.loc[bad.index[1],"order_id"]=bad.iloc[0]["order_id"]
try: require_unique(bad,"order_id")
except ValueError as e: duplicate_message=str(e)
assert "order_id" in duplicate_message
""","""def require_unique(frame,column):
    if frame[column].duplicated().any(): raise ValueError(f"duplicate {column}")
    return True
assert require_unique(orders,"order_id") is True
"""),
("Неотрицательные оплаты","Остановите NaN и отрицательные значения.", """def validate_payment_values(frame):
    # TODO
    ...
assert validate_payment_values(payments) is True
bad=payments.head(2).copy(); bad.loc[bad.index[0],"payment_value"]=-1
try: validate_payment_values(bad)
except ValueError as e: payment_message=str(e)
assert "payment_value" in payment_message
""","""def validate_payment_values(frame):
    if frame["payment_value"].isna().any(): raise ValueError("payment_value has missing values")
    if frame["payment_value"].lt(0).any(): raise ValueError("payment_value must be non-negative")
    return True
assert validate_payment_values(payments) is True
"""),
("Обязательная дата покупки","Остановите NaT до расчёта Recency.", """def validate_purchase_dates(frame):
    # TODO
    ...
assert validate_purchase_dates(orders) is True
bad=orders.head(2).copy(); bad.loc[bad.index[0],"order_purchase_timestamp"]=pd.NaT
try: validate_purchase_dates(bad)
except ValueError as e: date_message=str(e)
assert "timestamp" in date_message
""","""def validate_purchase_dates(frame):
    if frame["order_purchase_timestamp"].isna().any(): raise ValueError("order_purchase_timestamp has missing values")
    return True
assert validate_purchase_dates(orders) is True
"""),
("Единый валидатор","Соберите validate_inputs для трёх таблиц.", """def validate_inputs(orders_df,customers_df,payments_df):
    # TODO
    ...
assert validate_inputs(orders,customers,payments) is True
""","""def validate_inputs(orders_df,customers_df,payments_df):
    require_columns(orders_df,{"order_id","customer_id","order_purchase_timestamp"})
    require_columns(customers_df,{"customer_id","customer_unique_id","customer_state"})
    require_columns(payments_df,{"order_id","payment_type","payment_value"})
    require_unique(orders_df,"order_id"); require_unique(customers_df,"customer_id"); require_unique(payments_df,"order_id")
    validate_purchase_dates(orders_df); validate_payment_values(payments_df); return True
assert validate_inputs(orders,customers,payments) is True
"""),
("Лог успешного пути","Запишите шаг только после успешной проверки.", """log=[]  # TODO
validate_inputs(orders,customers,payments)
# TODO: append
merged=None  # TODO; затем append
assert len(log)==2 and log[0].startswith("validated") and log[1].startswith("merged")
""","""log=[]
validate_inputs(orders,customers,payments); log.append("validated input contracts")
merged=orders.merge(payments,on="order_id",validate="one_to_one"); log.append("merged orders and payments")
assert len(log)==2
"""),
("Проверка плохого пути","Докажите, что после raise шаг merge не логируется.", """bad=payments.head(3).copy(); bad.loc[bad.index[0],"payment_value"]=-5
bad_log=[]; caught=""
try:
    # TODO: validate, append, merge
    ...
except ValueError as e: caught=str(e)
assert caught and bad_log==[]
""","""bad=payments.head(3).copy(); bad.loc[bad.index[0],"payment_value"]=-5
bad_log=[]; caught=""
try:
    validate_inputs(orders,customers,bad); bad_log.append("validated")
except ValueError as e: caught=str(e)
assert caught and bad_log==[]
"""),
("Инженерная записка","Объясните отличие assert, raise и лога.", """CONTRACT_NOTE=""  # TODO
assert len(CONTRACT_NOTE)>=280
assert all(w in CONTRACT_NOTE.lower() for w in ["assert","raise","лог"])
""","""CONTRACT_NOTE="Assert в учебном ноутбуке проверяет ожидаемый результат задачи и быстро показывает нарушение. Raise внутри pipeline является частью публичного контракта: останавливает обработку плохого входа с понятным сообщением. Лог не заменяет проверку; он фиксирует только завершённые шаги и помогает найти границу сбоя."
assert len(CONTRACT_NOTE)>=280
""")
],[
("Валидатор payments","Проверьте схему, пропуски, отрицательные значения и ключ.", """def validate_payments(frame):
    # TODO
    ...
assert validate_payments(payments) is True
""","""def validate_payments(frame):
    require_columns(frame,{"order_id","payment_type","payment_value"}); require_unique(frame,"order_id"); validate_payment_values(frame); return True
assert validate_payments(payments) is True
"""),
("Три негативных теста","Проверьте missing column, duplicate key, negative value.", """messages=[]  # TODO: три try/except
assert len(messages)==3 and all(messages)
""","""messages=[]
cases=[payments.drop(columns="payment_type"),pd.concat([payments.head(1),payments.head(1)]),payments.head(2).assign(payment_value=[-1,2])]
for case in cases:
    try: validate_payments(case)
    except (KeyError,ValueError) as e: messages.append(str(e))
assert len(messages)==3
"""),
("Структурированный лог","Храните dict step/rows/columns.", """audit=[]  # TODO: load, validate, merge
assert [x["step"] for x in audit]==["load","validate","merge"]
assert all({"step","rows","columns"}<=set(x) for x in audit)
""","""audit=[{"step":"load","rows":len(orders),"columns":len(orders.columns)}]
validate_inputs(orders,customers,payments); audit.append({"step":"validate","rows":len(orders),"columns":len(orders.columns)})
x=orders.merge(payments,on="order_id"); audit.append({"step":"merge","rows":len(x),"columns":len(x.columns)})
assert len(audit)==3
"""),
("Challenge: контракт как функция","Верните validated copies и лог, не меняя вход.", """def prepare_inputs(o,c,p):
    # TODO
    ...
(o2,c2,p2),audit=prepare_inputs(orders,customers,payments)
assert len(audit)>=2 and o2 is not orders and p2 is not payments
""","""def prepare_inputs(o,c,p):
    copies=(o.copy(),c.copy(),p.copy()); validate_inputs(*copies)
    return copies,["copied input frames","validated input contracts"]
(o2,c2,p2),audit=prepare_inputs(orders,customers,payments)
"""),
("Challenge: политика ошибок","Опишите fail-fast и содержание сообщения.", """ERROR_NOTE=""  # TODO
assert len(ERROR_NOTE)>=260
assert all(w in ERROR_NOTE.lower() for w in ["fail","строк","столб"])
""","""ERROR_NOTE="Политика fail-fast останавливает pipeline до join и агрегации, чтобы дефект не распространился в признаки. Сообщение должно назвать нарушенный столбец, правило и по возможности число или пример строк. Оно не должно молча исправлять вход: решение об удалении, заполнении или возврате источнику принимает владелец данных."
assert len(ERROR_NOTE)>=260
""")
]))

PIPELINE_DEF = """def preprocess_customers(orders_df, customers_df, payments_df):
    log=[]
    o,c,p=orders_df.copy(),customers_df.copy(),payments_df.copy()
    required_o={"order_id","customer_id","order_purchase_timestamp","order_delivered_customer_date"}
    required_c={"customer_id","customer_state"}
    required_p={"order_id","payment_type","payment_value"}
    for frame,required,name in ((o,required_o,"orders"),(c,required_c,"customers"),(p,required_p,"payments")):
        missing=required-set(frame.columns)
        if missing: raise KeyError(f"{name} missing columns: {sorted(missing)}")
    if o["order_id"].duplicated().any() or p["order_id"].duplicated().any(): raise ValueError("duplicate order_id")
    if o["order_purchase_timestamp"].isna().any(): raise ValueError("missing order_purchase_timestamp")
    if p["payment_value"].isna().any() or p["payment_value"].lt(0).any(): raise ValueError("invalid payment_value")
    log.append("validated input contracts")
    x=o.merge(p,on="order_id",validate="one_to_one").merge(c[["customer_id","customer_state"]],on="customer_id",validate="many_to_one")
    log.append("merged orders, payments, customers")
    x["days_to_deliver"]=(x["order_delivered_customer_date"]-x["order_purchase_timestamp"]).dt.days
    x["is_card"]=(x["payment_type"]=="credit_card").astype(int)
    ref=x["order_purchase_timestamp"].max()
    features=x.groupby("customer_id").agg(last_purchase=("order_purchase_timestamp","max"),Frequency=("order_id","nunique"),Monetary=("payment_value","sum"),share_card=("is_card","mean"),avg_days_to_deliver=("days_to_deliver","mean"),customer_state=("customer_state","first")).reset_index()
    features["Recency"]=(ref-features["last_purchase"]).dt.days
    features=features[["customer_id","Recency","Frequency","Monetary","share_card","avg_days_to_deliver","customer_state"]]
    log.append("built customer RFM plus features")
    return features,log
"""
SPECS.append((
"Практика: воспроизводимый preprocessing pipeline",
"Итоговый pipeline объединяет копирование, контракт, join, признаки, агрегацию и аудит в одной повторяемой функции.",
[
("Контракт функции","Запишите сигнатуру и docstring, пока тело может быть заглушкой.", """def preprocess_customers(orders_df,customers_df,payments_df):
    '''Return customer features and ordered audit log.'''
    # TODO
    ...
assert preprocess_customers.__doc__
""","""def preprocess_customers(orders_df,customers_df,payments_df):
    '''Return customer features and ordered audit log.'''
    return None,[]
assert preprocess_customers.__doc__
"""),
("Копии и валидация","Реализуйте начало функции: копии, schema/key/value checks, первый лог.", PIPELINE_DEF.replace("    log.append(\"merged orders, payments, customers\")","    log.append(\"merged orders, payments, customers\")") + """
features,log=preprocess_customers(orders,customers,payments)
assert log[0]=="validated input contracts"
assert "Recency" not in orders
""",PIPELINE_DEF+"""
features,log=preprocess_customers(orders,customers,payments)
assert log[0]=="validated input contracts"
"""),
("Форма результата","Проверьте одну строку клиента и семь ожидаемых полей.", """required={"customer_id","Recency","Frequency","Monetary","share_card","avg_days_to_deliver","customer_state"}
assert required==set(features.columns)
assert len(features)==778 and features["customer_id"].is_unique
""","""required={"customer_id","Recency","Frequency","Monetary","share_card","avg_days_to_deliver","customer_state"}
assert required==set(features.columns) and len(features)==778
"""),
("Инварианты RFM","Сверьте сумму заказов, денег и границы.", """checks={"orders":None,"money":None,"recency":None,"share_card":None}  # TODO
assert set(checks.values())=={True}
""","""checks={"orders":int(features["Frequency"].sum())==len(orders),"money":np.isclose(features["Monetary"].sum(),payments["payment_value"].sum()),"recency":features["Recency"].ge(0).all(),"share_card":features["share_card"].between(0,1).all()}
assert set(checks.values())=={True}
"""),
("Негативный тест","Подайте отрицательную оплату и проверьте raise.", """bad=payments.copy(); bad.loc[bad.index[0],"payment_value"]=-10
caught=""
try: preprocess_customers(orders,customers,bad)
except ValueError as e: caught=str(e)
assert "payment_value" in caught
""","""bad=payments.copy(); bad.loc[bad.index[0],"payment_value"]=-10
caught=""
try: preprocess_customers(orders,customers,bad)
except ValueError as e: caught=str(e)
assert "payment_value" in caught
"""),
("Повторяемость","Запустите дважды и сравните DataFrame и лог.", """features2,log2=preprocess_customers(orders,customers,payments)
same=None  # TODO
assert same is True and log2==log
""","""features2,log2=preprocess_customers(orders,customers,payments)
same=bool(features.equals(features2))
assert same and log2==log
"""),
("Preview артефакта","Сохраните первые 25 строк и прочитайте обратно.", """preview_path=Path("features_preview.csv")
# TODO
loaded_preview=None  # TODO
assert preview_path.exists() and len(loaded_preview)==25
assert list(loaded_preview.columns)==list(features.columns)
""","""preview_path=Path("features_preview.csv")
features.head(25).to_csv(preview_path,index=False)
loaded_preview=pd.read_csv(preview_path)
assert len(loaded_preview)==25
"""),
("Acceptance и отчёт","Закройте пять критериев и напишите итог без обещания модели.", """acceptance={"contract":None,"rfm":None,"extras":None,"audit":None,"preview":None}  # TODO
REPORT=""  # TODO
assert set(acceptance.values())=={True}
assert len(REPORT)>=320 and "churn" not in REPORT.lower()
""","""acceptance={"contract":log[0].startswith("validated"),"rfm":{"Recency","Frequency","Monetary"}<=set(features),"extras":{"share_card","avg_days_to_deliver"}<=set(features),"audit":len(log)>=3,"preview":preview_path.exists()}
REPORT=f"Pipeline обработал {len(orders)} заказов и получил {len(features)} клиентских строк. Контракт проверяет схему, ключи, даты и оплаты до join. Выход содержит RFM, долю card, средний срок доставки и штат. Лог фиксирует порядок шагов, preview сохраняет проверяемый срез. Результат описывает историю покупок и готов для следующего этапа, но сам не является прогнозом или доказательством поведения."
assert set(acceptance.values())=={True} and len(REPORT)>=320
""")
],[
("Повторная реализация","Соберите функцию самостоятельно и проверьте контракт.", """# TODO: перенесите чистую реализацию preprocess_customers
features,log=preprocess_customers(orders,customers,payments)
assert len(features)==778 and len(log)>=3
""",PIPELINE_DEF+"""
features,log=preprocess_customers(orders,customers,payments)
assert len(features)==778
"""),
("Стабильность при перестановке строк","Перемешайте вход и сравните результат после сортировки.", """shuffled=orders.sample(frac=1,random_state=55).reset_index(drop=True)
f2,_=preprocess_customers(shuffled,customers,payments)
stable=None  # TODO
assert stable is True
""","""shuffled=orders.sample(frac=1,random_state=55).reset_index(drop=True)
f2,_=preprocess_customers(shuffled,customers,payments)
cols=["customer_id","Recency","Frequency","Monetary","share_card","avg_days_to_deliver","customer_state"]
left=features.sort_values("customer_id")[cols].reset_index(drop=True)
right=f2.sort_values("customer_id")[cols].reset_index(drop=True)
stable=bool(left[["customer_id","customer_state"]].equals(right[["customer_id","customer_state"]]) and np.allclose(left[["Recency","Frequency","Monetary","share_card","avg_days_to_deliver"]],right[["Recency","Frequency","Monetary","share_card","avg_days_to_deliver"]],equal_nan=True))
assert stable
"""),
("Quality gate","Соберите шесть булевых проверок сдачи.", """gate={}  # TODO
assert len(gate)==6 and set(gate.values())=={True}
""","""gate={"rows":len(features)==778,"unique":features["customer_id"].is_unique,"orders":int(features["Frequency"].sum())==3500,"money":np.isclose(features["Monetary"].sum(),payments["payment_value"].sum()),"log":len(log)>=3,"no_churn":"churn" not in features}
assert len(gate)==6 and set(gate.values())=={True}
"""),
("Challenge: параметр ref_date","Добавьте необязательную дату и запрет даты раньше максимальной покупки.", """def preprocess_at_date(o,c,p,ref_date=None):
    # TODO: используйте базовый pipeline, пересчитайте Recency
    ...
future=orders["order_purchase_timestamp"].max()+pd.Timedelta(days=7)
f_future,_=preprocess_at_date(orders,customers,payments,future)
assert (f_future["Recency"]==features["Recency"]+7).all()
""","""def preprocess_at_date(o,c,p,ref_date=None):
    out,log=preprocess_customers(o,c,p); base=o["order_purchase_timestamp"].max()
    ref_date=base if ref_date is None else pd.Timestamp(ref_date)
    if ref_date<base: raise ValueError("ref_date before latest purchase")
    out["Recency"]=out["Recency"]+(ref_date-base).days
    return out,log+[f"used ref_date {ref_date.date()}"]
future=orders["order_purchase_timestamp"].max()+pd.Timedelta(days=7)
f_future,_=preprocess_at_date(orders,customers,payments,future)
assert (f_future["Recency"]==features["Recency"]+7).all()
"""),
("Challenge: handoff note","Опишите вход, выход, гарантии и следующий шаг.", """HANDOFF_NOTE=""  # TODO
assert len(HANDOFF_NOTE)>=340
assert all(w in HANDOFF_NOTE.lower() for w in ["вход","выход","гарант","следующ"])
""","""HANDOFF_NOTE="Вход pipeline — три slim-таблицы заказов, клиентов и оплат с зафиксированными ключами и datetime. Выход — одна строка customer_id с RFM и двумя производными признаками, плюс последовательный лог. Гарантии: схема и ключи проверены, оплаты неотрицательны, суммы и число заказов сохраняются, входы не меняются. Следующий шаг — разделить данные по времени, выбрать задачу и оценить признаки без утечки; обучение модели не входит в этот модуль."
assert len(HANDOFF_NOTE)>=340
""")
]))

DESIGN = (
    {
        "pair": 30, "role": "введение", "first": "«Признак начинается не с формулы, а с единицы наблюдения, типа и момента доступности»",
        "minimum": "зелёные assert §§1–7; карточка признака §8; устно: когда apply уступает векторной операции",
        "next": "признаки строки заказа", "outcomes": [
            "Различить числовые и категориальные признаки на полях Olist.",
            "Выполнить проверяемый one-to-one join заказов и оплат.",
            "Применить именованную функцию и lambda через apply.",
            "Сравнить построчное и векторное вычисление одного признака."],
        "errors": [
            ("Считает строку всех таблиц «клиентом»", "Перед join назвать единицу наблюдения каждой таблицы."),
            ("Соединяет без проверки формы", "До запуска записать ожидаемые 3500 строк и validate='one_to_one'."),
            ("Использует apply для простой разности дат", "Сначала добиться равенства, затем показать векторную запись."),
            ("Теряет недоставленные заказы", "Пропуск — осмысленное состояние, а не повод удалить строку.")],
    },
    {
        "pair": 31, "role": "отработка", "first": "«Сегодня каждый новый столбец проходит три вопроса: когда известен, какой диапазон, сохранилась ли строка заказа»",
        "minimum": "зелёные assert §§1–7; leakage note §8; функция add_order_features в Challenge ДЗ",
        "next": "RFM и groupby", "outcomes": [
            "Создать календарные и бинарные признаки строки заказа.",
            "Проверить форму и уникальность ключа после join.",
            "Выделить редкие сроки по p99 без автоматического удаления.",
            "Объяснить временную утечку для даты доставки."],
        "errors": [
            ("weekday ожидает 1–7", "В pandas Monday=0, Sunday=6; закрепить assert диапазона."),
            ("После join появляются суффиксы или дубли", "Выбирать ключ и validate до объединения."),
            ("Называет p99 ошибкой", "Порог выделяет редкость, но не доказывает дефект."),
            ("Использует срок доставки при оформлении", "На временной линии отметить момент появления поля.")],
    },
    {
        "pair": 32, "role": "введение", "first": "«Одна строка клиента получается не удалением дублей, а тремя осмысленными агрегатами»",
        "minimum": "зелёные assert §§1–7; интерпретация §8; суммы Frequency и Monetary сходятся с источником",
        "next": "производные признаки RFM+", "outcomes": [
            "Зафиксировать общую опорную дату Recency.",
            "Вычислить Frequency как nunique заказов.",
            "Вычислить Monetary как сумму оплат.",
            "Собрать и проверить таблицу клиент×RFM."],
        "errors": [
            ("Recency равен нулю у всех", "Не брать максимум отдельно внутри клиента как опорную дату."),
            ("Frequency считает строки после опасного join", "Считать nunique order_id и сверить сумму."),
            ("Monetary превращает пропуски в незаметные нули", "До groupby проверить покрытие оплат."),
            ("Высокий M называет лояльностью", "Читать R, F и M вместе; это описание истории.")],
    },
    {
        "pair": 33, "role": "отработка", "first": "«RFM — база; новый признак принимаем только вместе с правилом агрегации и паспортом»",
        "minimum": "зелёные assert §§1–8; RFM+ сохраняет 778 клиентов; в таблице нет churn",
        "next": "контракт и логирование", "outcomes": [
            "Агрегировать долю card и средний срок доставки на клиента.",
            "Добавить категориальный штат без размножения строк.",
            "Осторожно интерпретировать корреляцию Frequency и Monetary.",
            "Проверить границы и документировать экспертный score."],
        "errors": [
            ("Суммирует is_card вместо среднего", "Доля бинарного признака — mean."),
            ("Добавляет штат до проверки many-to-one", "Клиентская таблица должна сохранить 778 строк."),
            ("Складывает R/F/M в исходных единицах", "Сначала сделать масштабы сопоставимыми."),
            ("Называет корреляцию причиной", "Корреляция описывает совместное изменение.")],
    },
    {
        "pair": 34, "role": "введение", "first": "«Хороший pipeline не угадывает, что делать с плохими данными: он останавливается и объясняет правило»",
        "minimum": "валидаторы §§1–5; два негативных теста; лог плохого пути остаётся пустым",
        "next": "интеграция preprocessing", "outcomes": [
            "Проверить схему, уникальность, даты и оплаты.",
            "Поднять информативные KeyError и ValueError.",
            "Написать позитивные и негативные тесты контракта.",
            "Отделить assert учебной проверки, raise контракта и аудит-лог."],
        "errors": [
            ("Валидатор молча удаляет строку", "Контракт сообщает дефект; политика исправления задаётся отдельно."),
            ("Логирует шаг до его завершения", "Append только после успешной операции."),
            ("Ловит Exception без анализа", "Проверять ожидаемый тип и содержание сообщения."),
            ("Проверяет значения после агрегации", "Fail-fast до join и признаков.")],
    },
    {
        "pair": 35, "role": "интеграция и сдача", "first": "«Сдаём не таблицу из удачного запуска, а функцию с контрактом, инвариантами и повторяемым результатом»",
        "minimum": "функция возвращает 778×7 и лог; негативный тест; повторяемость; acceptance полностью True",
        "next": "следующие модули: временное разбиение и модель", "outcomes": [
            "Собрать raw→client RFM+ в чистой функции.",
            "Сохранить входы неизменными и проверить инварианты.",
            "Проверить повторяемость и устойчивость к перестановке строк.",
            "Передать preview, quality gate и инженерную записку."],
        "errors": [
            ("Функция меняет исходные DataFrame", "Копировать входы в начале и тестировать отсутствие новых столбцов."),
            ("Результат зависит от порядка строк", "Сравнить после сортировки по customer_id."),
            ("Acceptance заполняется вручную", "Каждый флаг вычисляется из результата или лога."),
            ("Называет features прогнозом", "Это transform; задача и модель появятся позже.")],
    },
)

def render_design(folder, spec, design):
    title, concept, lesson_sections, hw_sections = spec
    stages = []
    minutes = [8, 10, 10, 10, 10, 10, 12, 10]
    for i, (heading, task, _, _) in enumerate(lesson_sections, 1):
        stages.append(
            f"| {i} | {heading} | {minutes[i-1]} | {task} | Задаёт вопрос о форме, ключе или диапазоне; "
            f"не диктует строку кода | `## {i}. {heading}` | assert раздела зелёный; ученик объясняет проверку |"
        )
    outcomes = "\n".join(f"{i}. {text}" for i, text in enumerate(design["outcomes"], 1))
    errors = "\n".join(f"| {symptom} | {response} |" for symptom, response in design["errors"])
    headings = ", ".join(f"§{i} {x[0]}" for i, x in enumerate(lesson_sections, 1))
    return f"""# Lesson Design: {title}

## A. Сценарий пары

| Поле | Значение |
|---|---|
| Модуль | Интернет-магазин / маркетплейс: Feature Engineering и lambda (`08_05`) |
| Название урока | {title} |
| Пара КТП | **{design["pair"]}** |
| Длительность | 2 академических часа (**80 минут**) |
| Роль | {design["role"]} |
| Пререквизиты | Python и pandas из модулей 1–3; три slim CSV рядом с ноутбуком; схема в [data/README](../../data/README.md) |
| **Открыть** | [lesson.ipynb](lesson.ipynb) — копия на ученика; первая code-ячейка загружает три CSV |
| **Первая фраза** | {design["first"]} |
| **Минимум сдачи** | {design["minimum"]} |
| **Домашнее задание** | [homework.ipynb](homework.ipynb) — Part A обязательно; Challenge после основной части (~1 ч) |
| **Дальше** | {design["next"]} |
| **Canvas** | не опубликовано |

### A. Чего хотим от пары

Главное — {concept.lower()} Ученик не копирует готовую цепочку: на каждом этапе сначала
называет единицу наблюдения и ожидаемый инвариант, затем пишет код и использует assert
как доказательство. Бизнес-контекст — CRM Olist; метку churn не создаём и модель не обучаем.

Материал ноутбука: {headings}. CSV лежат рядом, поэтому урок работает офлайн.

---

## B. Ход пары

| # | Этап | ~мин | Ученик | Учитель | Материал | Критерий закрытия |
|---|---|---|---|---|---|---|
{chr(10).join(stages)}

Обязательные этапы для минимума сдачи: **1–7**. §8 закрывает интерпретацию и переход к ДЗ.
Если этап занял больше времени, сокращать письменный объём заметки, но не убирать проверку данных.

---

## C. Если сбились

### Типичные ошибки

| Симптом / мысль ученика | Что сказать или показать |
|---|---|
{errors}

### Дифференциация (кратко)

| | |
|---|---|
| Слабее базы | §§1–5 с парным проговариванием формы; §§6–7 по шаблону; в ДЗ первые два задания Part A |
| Сильнее базы | §§1–8 без подсказок; Challenge обоих типов: функция и инженерное обоснование |

---

## D. Проектирование

### Зачем урок

{concept} Без этой пары следующий шаг превращается в цепочку pandas-команд без контракта:
непонятно, что означает строка, почему сохранилось число объектов и доступен ли признак в момент решения.

### Центральная идея

| Поле | Значение |
|---|---|
| Центральная идея | {concept} |
| Что поддерживает, но не отвлекает | Реальная схема Olist и CRM-интерпретация; predict и churn остаются вне scope |
| Данные урока | `orders_slim.csv`, `customers_slim.csv`, `payments_slim.csv`; правила RFM — [data/README](../../data/README.md) |

### Результаты обучения

{outcomes}

### Профессиональный контекст

Это работа до обучения модели: аналитик превращает источники в воспроизводимую таблицу признаков,
фиксирует ключи, момент доступности, границы и аудит. Такой handoff можно проверять независимо от автора.

### Решения учащегося

| # | Какой выбор делает учащийся | На что влияет |
|---|---|---|
| 1 | Формулирует единицу наблюдения и ожидаемую форму | Корректность join/groupby и отсутствие размножения строк |
| 2 | Выбирает правило преобразования или агрегации | Интерпретируемость и воспроизводимость признака |
| 3 | Решает, какая проверка доказывает результат | Возможность заметить дефект до следующего этапа |

### Материалы (зачем каждый)

- [x] [lesson.ipynb](lesson.ipynb) — §§1–8, stubs и исполняемые assert
- [x] [homework.ipynb](homework.ipynb) — Part A + Challenge
- [x] [solutions.ipynb](solutions.ipynb) — секционные эталоны урока и ДЗ, только преподавателю
- [x] три slim CSV — автономный запуск без Kaggle
- [ ] Canvas — не опубликовано
- [ ] презентация — не нужна: ход и фиксации встроены в ноутбук

### Домашнее задание

| Поле | Значение |
|---|---|
| Назначается | **да** |
| Файл | [homework.ipynb](homework.ipynb) |
| Формулировка | Три задания Part A закрепляют вычисление и gate; Challenge переносит идею в функцию и письменное решение |
| Ориентир времени | **~1 ч** |
| Почему не на уроке | Самостоятельная функция и обоснование требуют повторного запуска без пошаговых подсказок |
| Какую способность развивает | Перенос контракта признака в новый, но структурно похожий сценарий |

---

## E. Карточка урока (§13)

| Поле | Значение |
|---|---|
| Часы | 2 |
| Стратегии обучения / виды деятельности | Guided coding → самостоятельная секция; прогноз формы до запуска; чтение assert как контракта |
| Формирующее оценивание | Зелёные assert §§1–7; объяснение одного инварианта и одного ограничения |
| Дифференциация (общая) | База: §§1–5 и шаблон §§6–7; усиление: §8 и Challenge |
| По содержанию | {concept} |
| По процессу | Индивидуальный код, короткие сверки после §§2, 5 и 7, взаимная проверка формулировки §8 |
| По продукту | Заполненный `lesson.ipynb`; сданный `homework.ipynb` Part A; Challenge по готовности |
| Canvas | не опубликовано |
"""

def main():
    missing=[DATA/name for name in CSV_NAMES if not (DATA/name).exists()]
    if missing: raise SystemExit(f"Missing CSV files: {missing}")
    for folder,spec in zip(DIRS,SPECS):
        base=ROOT/"lessons"/folder; base.mkdir(parents=True,exist_ok=True)
        lesson,homework,solutions=build(*spec)
        for name,obj in (("lesson.ipynb",lesson),("homework.ipynb",homework),("solutions.ipynb",solutions)):
            (base/name).write_text(json.dumps(obj,ensure_ascii=False,indent=1),encoding="utf-8")
            print(f"wrote {folder}/{name}: {len(obj['cells'])} cells")
        for csv_name in CSV_NAMES:
            shutil.copy2(DATA/csv_name,base/csv_name)
            print(f"copied {csv_name} -> {folder}")
        design_text = render_design(folder, spec, DESIGN[DIRS.index(folder)])
        (base/"LESSON.md").write_text(design_text, encoding="utf-8")
        print(f"wrote {folder}/LESSON.md: {len(design_text)} chars")
    print("done: 18 notebooks, 6 lesson designs, and 18 CSV copies")

if __name__=="__main__":
    main()
