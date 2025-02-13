from pydantic import BaseModel, Field, field_validator, model_validator


# ********************************************************************************
#     Схемы для работы с товарами
class SLocaleModel(BaseModel):
    locale: str = Field(min_length=2, max_length=2, description="Язык полей ответа (ru — русский, "
                                                                "en — английский, zh — китайский)")

    @field_validator("locale")
    def validate_height(cls, value: str) -> str:
        if value == 'ru' or value == 'en' or value == 'zh':
            return value
        raise ValueError('Языки: ru, en, zh')


class SObjectPost(SLocaleModel):
    name: str = Field(min_length=2, max_length=50, description="Поиск по названию предмета, "
                                                               "поиск работает по подстроке, "
                                                               "искать можно на любом из поддерживаемых языков.")
    limit: int = Field(lt=1000, description="Количество предметов, максимум 1 000")
    offset: int = Field(description="Номер позиции, с которой необходимо получить ответ")
    parentID: int = Field(description="ID родительской категории предмета")


class SCharacteristicsPost(SLocaleModel):
    subjectID: int = Field(description="ID предмета (path Parameters)")


class STnvedPost(SLocaleModel):
    subjectID: int = Field(description="ID предмета")
    search: int = Field(description="Поиск по ТНВЭД-коду. Работает только в паре с subjectID")

    @model_validator(mode="after")
    def check_id(self):
        if self.subjectID:
            return self
        raise ValueError("Необходим ID")
