"""
dz-admin schemas package
Exports all Pydantic models for Algeria administrative divisions.

Usage:
    from schemas import Wilaya, Daira, Commune, Coordinates, LocalizedName
"""
from common import Coordinates, LocalizedName
from wilaya_schema import Wilaya, Region, DataStatus
from daira_schema import Daira
from commune_schema import Commune

__all__ = [
    "Coordinates",
    "LocalizedName",
    "Wilaya",
    "Region",
    "DataStatus",
    "Daira",
    "Commune",
]
