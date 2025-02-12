from datetime import date

from pydantic import BaseModel, Field


# ********************************************************************************
#     Схема для общих методов
class SNewsDateGet(BaseModel):
    from_date: date | None = Field(description="От какой даты новость")
    fromID: int | None = Field(description="ID новости, от которой необходимо выдать новости")

