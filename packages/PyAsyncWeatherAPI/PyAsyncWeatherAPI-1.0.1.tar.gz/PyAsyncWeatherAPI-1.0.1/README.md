# Asynchronous api wrapper for www.weatherapi.com!

## Usage

### Quick Start

Install from PyPi:
```
pip install PyAsyncWeatherAPI==1.0.0
```

### Example

```python
import asyncio

from weather_api import WeatherAPI


async def main():
    w_api = WeatherAPI("api-key")
    weather = await w_api.current(city="Yoshkar-Ola")
    print(weather.current.temp_c)

asyncio.run(main())
```

- Library docs
- API [docs](https://www.weatherapi.com/docs/)
