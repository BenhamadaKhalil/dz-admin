"""
dz-admin shared types
Shared Pydantic models used across wilaya, daira, and commune schemas.
"""
from typing import Optional
from pydantic import BaseModel, field_validator


class Coordinates(BaseModel):
    """Geographic coordinates (WGS84)."""
    lat: float
    lng: float

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, v: float) -> float:
        if not (19.0 <= v <= 37.5):
            raise ValueError(
                f"Latitude {v} is outside Algeria's bounding box (19–37.5°N). "
                "Check coordinates."
            )
        return v

    @field_validator("lng")
    @classmethod
    def validate_lng(cls, v: float) -> float:
        if not (-9.0 <= v <= 12.0):
            raise ValueError(
                f"Longitude {v} is outside Algeria's bounding box (-9–12°E). "
                "Check coordinates."
            )
        return v


class LocalizedName(BaseModel):
    """Multilingual name supporting Arabic, French, and English."""
    ar: str
    fr: str
    en: str

    @field_validator("ar")
    @classmethod
    def validate_arabic(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Arabic name must not be empty.")
        return v

    @field_validator("fr", "en")
    @classmethod
    def validate_latin(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty.")
        return v
