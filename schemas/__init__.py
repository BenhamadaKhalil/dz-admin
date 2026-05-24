"""
dz-admin schemas package
Exports all Pydantic models for Algeria administrative divisions.

Usage:
    from schemas import Wilaya, Daira, Commune, Coordinates, LocalizedName
"""
from schemas.common import Coordinates, LocalizedName
from schemas.wilaya_schema import Wilaya, Region, DataStatus
from schemas.daira_schema import Daira
from schemas.commune_schema import Commune

__all__ = [
    "Coordinates",
    "LocalizedName",
    "Wilaya",
    "Region",
    "DataStatus",
    "Daira",
    "Commune",
]
