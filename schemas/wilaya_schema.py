"""
dz-admin wilaya schema
Pydantic model for Algerian wilayas (provinces).

This module contains only the model definition.
The authoritative dataset lives in datasets/raw/wilayas.json.
"""
import re
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

from common import Coordinates, LocalizedName


class Region(str, Enum):
    """Geographical macro-regions of Algeria."""
    NORTH_CENTER = "North-Center"
    NORTH_EAST = "North-East"
    NORTH_WEST = "North-West"
    HIGHLANDS_CENTER = "Highlands-Center"
    HIGHLANDS_EAST = "Highlands-East"
    HIGHLANDS_WEST = "Highlands-West"
    SAHARA_NORTH = "Sahara-North"
    SAHARA_SOUTH = "Sahara-South"
    SAHARA_EAST = "Sahara-East"
    SAHARA_WEST = "Sahara-West"


class DataStatus(str, Enum):
    """Completeness indicator for a wilaya record."""
    COMPLETE = "complete"
    PARTIAL = "partial"
    STUB = "stub"


class Wilaya(BaseModel):
    """
    Represents an Algerian wilaya (province).

    Algeria has 69 wilayas as of Loi 26-06.
    Wilayas 59–69 were created by splitting existing wilayas.
    """
    id: int = Field(..., ge=1, le=69, description="Wilaya numeric ID (1–69)")
    code: str = Field(..., min_length=2, max_length=2, description="Zero-padded 2-digit code")
    iso_code: str = Field(..., description="ISO 3166-2 code (e.g. DZ-16)")
    name: LocalizedName
    slug: str = Field(..., description="URL-safe ASCII slug")
    region: Region
    capital: bool = Field(False, description="True only for Algiers (national capital)")
    capital_city: str = Field(..., description="Name of the wilaya seat/capital")
    postal_code: str = Field(..., min_length=5, max_length=5, description="5-digit postal code")
    coordinates: Coordinates
    area_km2: Optional[int] = Field(None, description="Area in km² (may be null for new wilayas)")
    population: Optional[int] = Field(None, description="Population (updated periodically)")
    data_status: DataStatus = DataStatus.COMPLETE
    notes: Optional[str] = Field(None, description="Administrative notes (e.g. split history)")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"Wilaya code '{v}' must be numeric digits only.")
        return v

    @field_validator("iso_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if not re.match(r"^DZ-\d{2}$", v):
            raise ValueError(
                f"ISO code '{v}' must match pattern DZ-XX (e.g. DZ-16)."
            )
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

    def code_int(self) -> int:
        """Return the numeric wilaya ID derived from the code string."""
        return int(self.code)

    def iso_number(self) -> int:
        """Return the numeric portion of the ISO code."""
        return int(self.iso_code.split("-")[1])