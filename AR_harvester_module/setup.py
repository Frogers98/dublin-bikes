from setuptools import setup

setup(name="station_info",
      version="0.3",
      description="Extract info for DB Bikes API and Post to MySQL",
      url="",
      author="Adam Ryan",
      author_email="aryan@brownthomas.ie",
      license="GPL3",
      packages=['station_info'],
      entry_points={
        'console_scripts':['station_info=station_info.main:main']
        }
      )
