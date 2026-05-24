from pydantic import BaseModel

class Wilaya(BaseModel):
    id: int
    code: str

    name_ar: str
    name_fr: str
    name_en: str