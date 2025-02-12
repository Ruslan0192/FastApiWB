from pydantic import BaseModel, Field


# ********************************************************************************
#     Схемы для работы с товарами
class SLocaleModel(BaseModel):
    locale: str = Field(min_length=2, max_length=2, description="Язык полей ответа (ru — русский, "
                                                                "en — английский, zh — китайский)")


class SObjectGet(SLocaleModel):
    name: str = Field(min_length=2, max_length=50, description="Поиск по названию предмета, "
                                                               "поиск работает по подстроке, "
                                                               "искать можно на любом из поддерживаемых языков.")
    limit: int = Field(description="Количество предметов, максимум 1 000")
    offset: int = Field(description="Номер позиции, с которой необходимо получить ответ")
    parentID: int = Field(description="ID родительской категории предмета")


class SCharacteristicsGet(SLocaleModel):
    subjectID: int = Field(description="ID предмета (path Parameters)")


class STnvedGet(SLocaleModel):
    subjectID: int = Field(description="ID предмета")
    search: int = Field(description="Поиск по ТНВЭД-коду. Работает только в паре с subjectID")
