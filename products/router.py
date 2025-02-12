import json

from fastapi import APIRouter

from general.router import def_requests_get
from products.schemas import SLocaleModel, SObjectGet, SCharacteristicsGet, STnvedGet

router_products = APIRouter(prefix='/products', tags=['Работа с товарами'])


# работа с товарами
# https://dev.wildberries.ru/openapi/work-with-products#tag/Kategorii-predmety-i-harakteristiki


# Метод предоставляет названия и ID всех родительских категорий для создания карточек товаров:
# например, Электроника, Бытовая химия, Рукоделие.
@router_products.post("/parent")
async def def_parent(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/object/parent/all'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет список названий родительских категорий предметов и их предметов с ID.
# Например, у категории Игрушки будут предметы Калейдоскопы, Куклы, Мячики.
# работает не корректно
@router_products.post("/object")
async def def_object(params_object: SObjectGet):
    """
    {
      "name": "Калейдоскопы",
      "limit": 10,
      "locale": "ru",
      "offset": 30,
      "parentID": 7
    }
    """
    url_api = 'https://content-api.wildberries.ru/content/v2/object/all'
    params = params_object.json()
    return def_requests_get(url_api, params)


# Метод предоставляет параметры характеристик предмета: названия, типы данных, единицы измерения и так далее.
# В запросе необходимо указать ID предмета.
@router_products.post("/charcs")
async def def_charcs(params_characteristics: SCharacteristicsGet):
    """
    {
      "locale": "ru",
      "subjectId": 105
    }
    """
    url_api = f'https://content-api.wildberries.ru/content/v2/object/charcs/{params_characteristics.subjectID}'
    params = {'locale': params_characteristics.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет возможные значения характеристики предмета Цвет
@router_products.post("/colors")
async def def_colors(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/directory/colors'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет возможные значения характеристики предмета Пол.
@router_products.post("/kinds")
async def def_kinds(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/directory/kinds'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет возможные значения характеристики предмета Страна производства.
@router_products.post("/countries")
async def def_countries(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/directory/countries'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет возможные значения характеристики предмета Сезон.
@router_products.post("/seasons")
async def def_seasons(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/directory/seasons'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет возможные значения характеристики предмета Ставка НДС.
@router_products.post("/vat")
async def def_vat(params_locale: SLocaleModel):
    url_api = 'https://content-api.wildberries.ru/content/v2/directory/vat'
    params = {"locale": params_locale.locale}
    return def_requests_get(url_api, params)


# Метод предоставляет список ТНВЭД-кодов по ID предмета и фрагменту ТНВЭД-кода.
@router_products.post("/tnved")
async def def_tnved(params_tnved: STnvedGet):
    """
    {
      "subjectID": 105,
      "search": 9021101000,
      "locale": "ru"
    }
    """
    params_json = params_tnved.json()
    params = json.loads(params_json)
    if not params['search']:
        del params['search']
    url_api = f'https://content-api.wildberries.ru/content/v2/directory/tnved'
    return def_requests_get(url_api, params)

