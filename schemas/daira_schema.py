"""
dz-admin daira schema
Pydantic model for Algerian daïras (sub-provincial districts).

Algeria has approximately 553 daïras. Each daïra belongs to one wilaya.
The authoritative dataset lives in datasets/raw/dairas.json.
"""
import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from schemas.common import LocalizedName


class Daira(BaseModel):
    """
    Represents an Algerian daïra (administrative district).

    A daïra is a sub-division of a wilaya, grouping several communes.
    The daïra code is the wilaya code concatenated with a 2-digit sequence.
    Example: daïra "0101" = first daïra of wilaya "01" (Adrar).
    """
    id: int = Field(..., ge=1, description="Unique daïra ID (sequential)")
    code: str = Field(..., min_length=4, max_length=4, description="4-digit code: WWDD")
    wilaya_id: int = Field(..., ge=1, le=69, description="Parent wilaya ID")
    wilaya_code: str = Field(..., min_length=2, max_length=2, description="Parent wilaya code")
    name: LocalizedName
    slug: str = Field(..., description="URL-safe ASCII slug")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Daïra code '{v}' must be 4 numeric digits (WWDD).")
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

    def wilaya_code_int(self) -> int:
        """Return the numeric wilaya code."""
        return int(self.wilaya_code)

    def sequence_number(self) -> int:
        """Return the daïra's sequence number within its wilaya."""
        return int(self.code[2:])
