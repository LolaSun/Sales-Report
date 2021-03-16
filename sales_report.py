"""Скрипт по файлу с продажами считает:
1. Сумму продаж за июнь.
2. Сумму продаж по дням, неделям, по дням недели.
3. Топ 10 самых покупаемых товаров, по сумме и количеству.
4. Топ 10 самых покупаемых категорий, по сумме и количеству.
5. Среднее количество товров и средняя сумма на одного человека
"""

import json
import pandas as pd
import numpy as np

path = "sales.json"
with open(path, 'r') as f:
    data = json.loads(f.read())

df_sales = pd.DataFrame(data)

df_sales["event_date"] = pd.to_datetime(df_sales["event_date"])

# сумма продаж за июнь:
june_sales = np.round(df_sales[(df_sales['event_date'] >= "2017-06-01") & (df_sales['event_date'] <= "2017-06-30")]['product_price'].sum(), 2)
print("Cумма продаж за июнь: {}".format(june_sales))

# сумма продаж за день:
for_day = df_sales.groupby("event_date")['product_price'].sum()
print("\nСумма продаж за день:\n{}".format(for_day))

# сумма продаж за неделю:
for_week = df_sales.set_index("event_date").resample('W')['product_price'].sum()
print("\nСумма продаж по неделям:\n{}".format(for_week))

df_sales['Weekday'] = df_sales["event_date"].dt.day_name()
# сумма продаж по дням недели:
for_day_of_week = df_sales.groupby('Weekday')['product_price'].sum()
print("\nСумма продаж по дням недели:\n{}".format(for_day_of_week))

# топ 10 самых покупаемых товаров по сумме:
top10bying_product_by_summ = df_sales.groupby("product_id")['product_price'].sum().to_frame().sort_values("product_price", ascending=False).head(10)
print("\nТоп 10 самых покупаемых товаров по сумме:\n{}".format(top10bying_product_by_summ))

# топ 10 самых покупаемых товаров по количеству:
top10bying_product_by_count = df_sales.groupby("product_id")['product_price'].count().to_frame().sort_values("product_price", ascending=False).head(10)
print("\nТоп 10 самых покупаемых товаров по количеству:\n{}".format(top10bying_product_by_count))

# топ 10 самых покупаемых категорий по сумме:
top10bying_category_by_summ = df_sales.groupby("product_category")['product_price'].sum().to_frame().sort_values("product_price", ascending=False).head(10)
print("\nТоп 10 самых покупаемых категорий по сумме:\n{}".format(top10bying_category_by_summ))

# топ 10 самых покупаемых категорий по количеству:
top10bying_category_by_count = df_sales.groupby("product_category")['product_price'].count().to_frame().sort_values('product_price', ascending=False).head(10)
print("\nТоп 10 самых покупаемых категорий по количеству:\n{}".format(top10bying_category_by_count))

# cреднее количество товров на одного человека:
for_user_middle_count = np.round(df_sales.groupby("user")["product_id"].count().mean(), 2)
print("\nСреднее количество товров на одного человека: {}".format(for_user_middle_count))

# средняя сумма продаж на одного человека:
for_user_middle_summ = np.round(df_sales.groupby("user")['product_price'].sum().mean(), 2)
print("\nСредняя сумма продаж на одного человека: {}".format(for_user_middle_summ))
