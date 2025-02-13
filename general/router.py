import requests
from fastapi import APIRouter

from config import settings
from general.schemas import *

router_general = APIRouter(prefix='/general', tags=['Общие методы'])


#  GET запрос на WB
def def_requests_get(api_url: str, params: any = None):
    response = requests.get(api_url, params=params, headers={'Authorization': settings.TOKEN_WB})
    return def_status_code(response)


#  Post запрос на WB
def def_requests_post(api_url: str,  data: any,  params: any = None):
    response = requests.post(api_url, params=params, json=data, headers={'Authorization': settings.TOKEN_WB})
    return def_status_code(response)


#  Patch запрос на WB
def def_requests_patch(api_url: str):
    response = requests.patch(api_url, headers={'Authorization': settings.TOKEN_WB})
    return def_status_code(response)


#  обработка статуса ответа от WB
def def_status_code(response: requests.Response):
    data = response.json()

    if response.status_code == 200:
        return {'message': data}
    elif response.status_code == 204:
        return {'message': 'Отменено'}

    elif response.status_code == 400:
        error = 'Неправильный запрос '
    elif response.status_code == 401:
        error = 'Пользователь не авторизован '
    elif response.status_code == 403:
        error = 'Доступ запрещен '
    elif response.status_code == 404:
        error = 'Не найдено '
    elif response.status_code == 409:
        error = 'Ошибка обновление статуса '
    elif response.status_code == 429:
        error = 'Слишком много запросов '
    else:
        error = 'Неизвестная ошибка '
    error += str(response.status_code)
    return {'код ошибки': error, 'message': data}


# ************************************************************************************************************
# Общие методы
# https://dev.wildberries.ru/openapi/api-information#tag/Proverka-podklyucheniya-k-WB-API/paths/~1ping/get

# проверка подключения
@router_general.get("/ping")
async def def_ping():
    return def_requests_get('https://common-api.wildberries.ru/ping')


# новости
@router_general.post("/news")
async def def_news(param_post: SNewsDatePost):
    url_api = 'https://common-api.wildberries.ru/api/communications/v1/news'

    params = {}
    if param_post.fromID:
        params.update({"fromID": param_post.fromID})
    if param_post.from_date:
        date = param_post.from_date.strftime("%Y-%m-%d")
        params.update({"from": date})

    return def_requests_get(url_api, params)


# информация о продавце
@router_general.get("/seller")
async def def_seller():
    return def_requests_get('https://common-api.wildberries.ru/api/v1/seller-info')
