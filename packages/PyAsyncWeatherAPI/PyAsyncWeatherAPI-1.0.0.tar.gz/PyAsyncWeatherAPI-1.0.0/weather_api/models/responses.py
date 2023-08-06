from typing import Optional, List

from pydantic import BaseModel

from .models import Location, Current, Astronomy, SportEvent, Forecast


class CurrentResponse(BaseModel):
    location: Optional[Location] = None
    current: Optional[Current] = None


class AstronomyResponse(BaseModel):
    location: Optional[Location] = None
    astronomy: Optional[Astronomy] = None


class TimeZoneResponse(BaseModel):
    location: Optional[List[Location]] = None


class SportsResponse(BaseModel):
    football: Optional[List[SportEvent]] = None
    cricket: Optional[List[SportEvent]] = None
    golf: Optional[List[SportEvent]] = None


class HistoryResponse(BaseModel):
    location: Optional[Location] = None
    forecast: Optional[Forecast] = None


class ForecastResponse(BaseModel):
    location: Optional[Location] = None
    current: Optional[Current] = None
    forecast: Optional[Forecast] = None

