"""
dz-admin commune schema
Pydantic model for Algerian communes (municipalities).

Algeria has 1,541 communes. Each commune belongs to one daïra and one wilaya.
The authoritative dataset lives in datasets/raw/communes.json.
"""
import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from schemas.common import Coordinates, LocalizedName


class Commune(BaseModel):
    """
    Represents an Algerian commune (municipality).

    A commune is the lowest official administrative subdivision.
    The commune code is 6 digits: WWDDCC where:
      WW = wilaya code, DD = daïra sequence, CC = commune sequence.
    Example: "010101" = first commune of first daïra of wilaya 01.
    """
    id: int = Field(..., ge=1, description="Unique commune ID (sequential)")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit code: WWDDCC")
    daira_id: int = Field(..., ge=1, description="Parent daïra ID")
    daira_code: str = Field(..., min_length=4, max_length=4, description="Parent daïra code")
    wilaya_id: int = Field(..., ge=1, le=69, description="Parent wilaya ID")
    wilaya_code: str = Field(..., min_length=2, max_length=2, description="Parent wilaya code")
    name: LocalizedName
    slug: str = Field(..., description="URL-safe ASCII slug")
    postal_code: str = Field(..., min_length=5, max_length=5, description="5-digit postal code")
    coordinates: Optional[Coordinates] = Field(
        None, description="Centroid coordinates (may be null)"
    )

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Commune code '{v}' must be 6 numeric digits (WWDDCC).")
        return v

    @field_validator("daira_code")
    @classmethod
    def validate_daira_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Daïra code '{v}' must be 4 numeric digits.")
        return v

    @field_validator("wilaya_code")
    @classmethod
    def validate_wilaya_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Wilaya code '{v}' must be 2 numeric digits.")
        return v

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", v):
            raise ValueError(
                f"Slug '{v}' must be lowercase alphanumeric with hyphens only."
            )
        return v

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Postal code '{v}' must contain digits only.")
        return v

    def wilaya_code_int(self) -> int:
        return int(self.wilaya_code)

    def daira_code_int(self) -> int:
        return int(self.daira_code)
