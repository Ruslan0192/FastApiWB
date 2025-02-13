# from typing import Optional
from datetime import date


from pydantic import BaseModel, Field, field_validator, model_validator


class SOrdersModel(BaseModel):
    orders: list[int] = Field(description="Список ID сборочных заданий")

    @field_validator("orders")
    def validate_orders(cls, value: list):
        if 0 < len(value) < 101:
            return value
        raise ValueError('Количество заданий от 1 до 100')


# ********************************************************************************
#     Схемы для работы с заказами по FBS

class SOrdersPost(BaseModel):
    limit: int = Field(gt=0, lt=1000,
                       description="Параметр пагинации. "
                                   "Устанавливает предельное количество возвращаемых данных [ 1 .. 1000 ]")
    next: int = Field(description="Параметр пагинации. "
                                  "Устанавливает значение, с которого надо получить следующий пакет данных. "
                                  "Для получения полного списка данных должен быть равен 0 в первом запросе. "
                                  "Для следующих запросов необходимо брать значения из одноимённого поля в ответе.")
    dateFrom: date = Field(description="Дата начала периода в формате Unix timestamp. "
                                       "По умолчанию — дата за 30 дней до запроса")
    dateTo: date = Field(description="Дата конца периода в формате Unix timestamp")


class SStatusPost(BaseModel):
    orders: list[int] = Field(description="Список ID сборочных заданий")

    @field_validator("orders")
    def validate_orders(cls, value: list):
        if 0 < len(value) < 1001:
            return value
        raise ValueError('Количество заданий от 1 до 1000')


class SCancelPost(BaseModel):
    orderId: int = Field(description="ID сборочного задания")


class SStickersPost(SOrdersModel):
    type: str = Field(min_length=2, max_length=3, description="Тип стикера")
    width: int = Field(description="Ширина стикера")
    height: int = Field(description="Высота стикера")

    @field_validator("type")
    def validate_width(cls, value: str):
        if value == 'SVG' or value == 'ZPLV' or value == 'ZPLH' or value == 'PNG':
            return value
        raise ValueError('Форматы: SVG, ZPLV (вертикальный), ZPLH (горизонтальный), PNG')

    @model_validator(mode="after")
    def check_size(self):
        if self.width == 58 and self.height == 40:
            return self
        elif self.width == 40 and self.height == 30:
            return self
        raise ValueError("Размеры стикера должны быть 58х40 или 40х30")


