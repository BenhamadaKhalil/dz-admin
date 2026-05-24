from pydantic import BaseModel, Field

class Wilaya(BaseModel):
    id: int
    code: str = Field(min_length=2, max_length=2)

    name_ar: str
    name_fr: str
    name_en: str