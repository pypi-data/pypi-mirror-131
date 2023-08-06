from setuptools import find_packages, setup

setup(
    name="PyAsyncWeatherAPI",
    version="1.0.1",
    author="@ichetiva",
    license="gpl-3.0",
    url="https://github.com/ichetiva/weather-api",
    description="Asynchronous api wrapper for www.weatherapi.com!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=["weather", "weather-api", "api-weather", "async-weather", "async-weather-api"],
    include_package_data=True,
    exclude=["examples"]
)
