from setuptools import setup

setup(name="forecast_info",
      version="0.3",
      description="Extract info for Forecast and Post to MySQL",
      url="",
      author="Adam Ryan",
      author_email="aryan@brownthomas.ie",
      license="GPL3",
      packages=['forecast_info'],
      entry_points={
        'console_scripts':['forecast_info=forecast_info.main:main']
        }
      )
