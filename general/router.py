import requests
from fastapi import APIRouter

from config import settings
from general.schemas import SNewsDateGet

router_general = APIRouter(prefix='/main', tags=['Общие методы'])


def def_requests_get(api_url: str, params: any = None):
    response = requests.get(api_url, params=params, headers={'Authorization': settings.TOKEN_WB})

    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 400:
        data = 'Неправильный запрос'
    elif response.status_code == 401:
        data = 'Пользователь не авторизован'
    elif response.status_code == 403:
        data = 'Доступ запрещен'
    elif response.status_code == 429:
        data = 'Слишком много запросов'
    else:
        data = 'Неизвестная ошибка'
    return {"message": data}


# ************************************************************************************************************
# Общие методы
# https://dev.wildberries.ru/openapi/api-information#tag/Proverka-podklyucheniya-k-WB-API/paths/~1ping/get

# проверка подключения
@router_general.get("/ping")
async def def_ping():
    return def_requests_get('https://common-api.wildberries.ru/ping')


# новости
@router_general.post("/news")
async def def_news(news_date: SNewsDateGet):
    url_api = 'https://common-api.wildberries.ru/api/communications/v1/news'

    params = {}
    if news_date.fromID:
        params.update({"fromID": news_date.fromID})
    if news_date.from_date:
        date = news_date.from_date.strftime("%Y-%m-%d")
        params.update({"from": date})

    return def_requests_get(url_api, params)


# информация о продавце
@router_general.get("/seller")
async def def_seller():
    return def_requests_get('https://common-api.wildberries.ru/api/v1/seller-info')
