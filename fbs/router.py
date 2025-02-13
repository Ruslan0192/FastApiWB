import json
from datetime import datetime

from fastapi import APIRouter

from fbs.schemas import *
from general.router import def_requests_get, def_requests_post, def_requests_patch

router_fbs = APIRouter(prefix='/fbs', tags=['Заказы FBS'])


# Заказы FBS
# https://dev.wildberries.ru/openapi/orders-fbs


# Метод предоставляет список всех новых сборочных заданий, которые есть у продавца на момент запроса.
@router_fbs.get("/new")
async def def_new():
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders/new'
    return def_requests_get(url_api)


# Метод предоставляет информацию о сборочных заданиях без их актуального статуса.
# Можно получить данные за заданный период, максимум 30 календарных дней.
@router_fbs.post("/orders")
async def def_orders(param_post: SOrdersPost):
    """
    {
      "limit": 10,
      "next": 0,
      "dateFrom": "2025-01-12",
      "dateTo": "2025-02-11"
    }
    """
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders'

    params_json = param_post.json()
    params = json.loads(params_json)
    params['dateFrom'] = def_convert_timestamp(param_post.dateFrom)
    params['dateTo'] = def_convert_timestamp(param_post.dateTo)
    return def_requests_get(url_api, params)


# преобразование даты в формат Unix timestamp
def def_convert_timestamp(date_in: date) -> int:
    dt = datetime.fromisoformat(str(date_in))
    timestamp_unix = dt.timestamp()
    return int(timestamp_unix)


# Метод предоставляет статусы сборочных заданий по их ID.
# supplierStatus — статус сборочного задания. Триггер его изменения — сам продавец.
@router_fbs.post("/status")
async def def_status(param_post: SStatusPost):
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders/status'
    data = {'orders': param_post.orders}
    return def_requests_post(url_api, data=data)


# Метод предоставляет все сборочные задания, требующие повторной отгрузки.
# Повторная отгрузка требуется, если поставка была отсканирована в пункте приёмки,
# но при этом в ней всё ещё есть неотсканированные товары.
# Спустя определённое время необходимо доставить эти товары заново.
# Данные сборочные задания можно перевести в другую активную поставку.
@router_fbs.get("/reshipment")
async def def_reshipment():
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/supplies/orders/reshipment'
    return def_requests_get(url_api)


# Метод отменяет сборочное задание и переводит в статус cancel — отменено продавцом.
@router_fbs.post("/cancel")
async def def_cancel(param_post: SCancelPost):
    url_api = f'https://marketplace-api.wildberries.ru/api/v3/orders/{param_post.orderId}/cancel'
    return def_requests_patch(url_api)


# Метод предоставляет список стикеров для сборочных заданий.
# Можно получить стикер в форматах:
# SVG
# ZPLV (вертикальный)
# ZPLH (горизонтальный)
# PNG
# Ограничения:
# За один запрос можно получить максимум 100 стикеров.
# Можно получить стикеры только для сборочных заданий, находящихся на сборке — статус confirm.
# Доступны размеры:
# 580x400 px при параметрах "width": 58, "height": 40
# 400x300 px при параметрах "width": 40, "height": 30
@router_fbs.post("/stickers")
async def def_stickers(param_post: SStickersPost):
    """
    {
      "type": "PNG",
      "width": 58,
      "height": 40,
      "orders": [1,2]
    }
    """
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders/stickers'

    params_json = param_post.json()
    params = json.loads(params_json)
    data = {'orders': params.pop('orders')}
    return def_requests_post(url_api, data=data, params=params)


# Метод предоставляет список ссылок на стикеры сборочных заданий,
# которые требуются при кроссбордере.
# Ограничения:
# За один запрос можно получить максимум 100 стикеров.
# Можно получить стикеры только для сборочных заданий,
# находящихся в доставке — статус complete.
@router_fbs.post("/external-stickers")
async def def_external_stickers(param_post: SOrdersModel):
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/files/orders/external-stickers'
    data = {'orders': param_post.orders}
    return def_requests_post(url_api, data=data)


# Метод предоставляет историю статусов для сборочных заданий кроссбордера.
@router_fbs.post("/history")
async def def_history(param_post: SOrdersModel):
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders/status/history'
    data = {'orders': param_post.orders}
    return def_requests_post(url_api, data=data)


# Метод позволяет получать информацию о покупателе по ID сборочного задания.
# Только для кроссбордера из Турции.
@router_fbs.post("/client")
async def def_client(param_post: SOrdersModel):
    url_api = 'https://marketplace-api.wildberries.ru/api/v3/orders/client'
    data = {'orders': param_post.orders}
    return def_requests_post(url_api, data=data)


# ********************************************************************
# Метаданные
# С помощью этих методов вы можете получать, удалять и редактировать метаданные сборочных заданий:
# Код маркировки
# УИН
# IMEI
# GTIN
