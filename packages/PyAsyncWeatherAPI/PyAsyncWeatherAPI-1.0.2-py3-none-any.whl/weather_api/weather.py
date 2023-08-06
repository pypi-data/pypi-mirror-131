import datetime
from typing import Optional, Union

import aiohttp

from .errors.handler import ErrorHandler
from .models import CurrentResponse, Language, AstronomyResponse, TimeZoneResponse, SportsResponse, HistoryResponse, \
    ForecastResponse

API_URL = "https://api.weatherapi.com/v1/"


class WeatherAPI:
    def __init__(self, key: str):
        self._key = key

        self._error_handler = ErrorHandler()

    async def current(
            self, city: str, lang: Union[Language, str] = Language.RU
    ) -> Optional[CurrentResponse]:
        response = await self.request(
            "GET", "current.json",
            params={
                "key": self._key,
                "q": city,
                "lang": lang,
                "aqi": "no"
            }
        )
        return CurrentResponse(**response)

    async def forecast(
            self, city: str, days: int, lang: Union[Language, str] = Language.RU
    ) -> Optional[ForecastResponse]:
        response = await self.request(
            "GET", "forecast.json",
            params={
                "key": self._key,
                "q": city,
                "days": days,
                "lang": lang,
                "aqi": "no",
                "alerts": "no"
            }
        )
        return ForecastResponse(**response)

    async def day(
            self, city, date: datetime.date, lang: Union[Language, str] = Language.RU
    ) -> Optional[HistoryResponse]:
        response = await self.request(
            "GET", "history.json",
            params={
                "key": self._key,
                "q": city,
                "dt": str(date),
                "lang": lang
            }
        )
        return HistoryResponse(**response)

    async def astronomy(
            self, city, date: datetime.date, lang: Union[Language, str] = Language.RU
    ) -> Optional[AstronomyResponse]:
        response = await self.request(
            "GET", "astronomy.json",
            params={
                "key": self._key,
                "q": city,
                "dt": str(date),
                "lang": lang
            }
        )
        return AstronomyResponse(**response)

    async def timezone(
            self, city, lang: Union[Language, str] = Language.RU
    ) -> Optional[TimeZoneResponse]:
        response = await self.request(
            "GET", "timezone.json",
            params={
                "key": self._key,
                "q": city,
                "lang": lang
            }
        )
        return TimeZoneResponse(**response)

    async def sports(
            self, city, lang: Union[Language, str] = Language.RU
    ) -> Optional[SportsResponse]:
        response = await self.request(
            "GET", "sports.json",
            params={
                "key": self._key,
                "q": city,
                "lang": lang
            }
        )
        return SportsResponse(**response)

    async def request(
        self, method: str, path: str, params: dict = None
    ) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, API_URL + path, params=params
            ) as response:
                print(await response.json())
                return self._error_handler.check(await response.text())
