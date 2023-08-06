import datetime
from typing import Optional, List

from pydantic import BaseModel


class Condition(BaseModel):
    text: Optional[str] = None
    icon: Optional[str] = None
    code: Optional[int] = None


class Location(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz_id: Optional[str] = None
    localtime_epoch: Optional[int] = None
    localtime: Optional[datetime.datetime] = None


class Current(BaseModel):
    last_updated_epoch: Optional[int] = None
    last_updated: Optional[datetime.datetime] = None
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None
    is_day: Optional[bool] = None
    condition: Optional[Condition] = None
    wind_mph: Optional[float] = None
    wind_kph: Optional[float] = None
    wind_degree: Optional[int] = None
    wind_dir: Optional[str] = None
    pressure_mb: Optional[float] = None
    pressure_in: Optional[float] = None
    precip_mm: Optional[float] = None
    precip_in: Optional[float] = None
    humidity: Optional[int] = None
    cloud: Optional[int] = None
    uv: Optional[float] = None
    gust_mph: Optional[float] = None
    gust_kph: Optional[float] = None


class Astro(BaseModel):
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    moonrise: Optional[str] = None
    moonset: Optional[str] = None
    moon_phase: Optional[str] = None
    moon_illumination: Optional[str] = None


class Astronomy(BaseModel):
    astro: Optional[Astro] = None


class SportEvent(BaseModel):
    stadium: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    tournament: Optional[str] = None
    start: Optional[datetime.datetime] = None
    match: Optional[str] = None


class Day(BaseModel):
    maxtemp_c: Optional[float] = None
    maxtemp_f: Optional[float] = None
    mintemp_c: Optional[float] = None
    mintemp_f: Optional[float] = None
    avgtemp_c: Optional[float] = None
    avgtemp_f: Optional[float] = None
    maxwind_mph: Optional[float] = None
    maxwind_kph: Optional[float] = None
    totalprecip_mm: Optional[float] = None
    totalprecip_in: Optional[float] = None
    avgvis_km: Optional[float] = None
    avgvis_miles: Optional[float] = None
    avghumidity: Optional[float] = None
    condition: Optional[Condition] = None
    uv: Optional[float] = None


class Hour(BaseModel):
    time_epoch: Optional[int] = None
    time: Optional[datetime.datetime] = None
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None
    is_day: Optional[bool] = None
    condition: Optional[Condition] = None
    wind_mph: Optional[float] = None
    wind_kph: Optional[float] = None
    wind_degree: Optional[int] = None
    wind_dir: Optional[str] = None
    pressure_mb: Optional[float] = None
    pressure_in: Optional[float] = None
    precip_mm: Optional[float] = None
    precip_in: Optional[float] = None
    humidity: Optional[int] = None
    cloud: Optional[int] = None
    feelslike_c: Optional[float] = None
    feelslike_f: Optional[float] = None
    windchill_c: Optional[float] = None
    windchill_f: Optional[float] = None
    heatindex_c: Optional[float] = None
    heatindex_f: Optional[float] = None
    dewpoint_c: Optional[float] = None
    dewpoint_f: Optional[float] = None
    will_it_rain: Optional[bool] = None
    chance_of_rain: Optional[int] = None
    will_it_snow: Optional[bool] = None
    chance_of_snow: Optional[int] = None
    vis_km: Optional[float] = None
    vis_miles: Optional[float] = None
    gust_mph: Optional[float] = None
    gust_kph: Optional[float] = None


class ForecastDay(BaseModel):
    date: Optional[datetime.date] = None
    date_epoch: Optional[int] = None
    day: Optional[Day] = None
    astro: Optional[Astro] = None
    hour: Optional[List[Hour]] = None


class Forecast(BaseModel):
    forecastday: Optional[List[ForecastDay]] = None
