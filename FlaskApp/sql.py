##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-24
##DLM:      2021-03-24
##MC:       COMP30830
##SD:       SQL Statements
##LD:       This section should hold all of the CODEBASE for SQL commands. SQL Commands should not exist in other app areas.
##
##------------------APP---------------##


####
#---01. Station Queries
####

####All Stations
SQL_select_station="""
    SELECT
         stat.{}                              AS                      number
        ,stat.{}                              AS                      address
        ,stat.{}                              AS                      banking
        ,stat.{}                              AS                      bike_status
        ,stat.{}                              AS                      bike_stands
        ,stat.{}                              AS                      contract_name
        ,stat.{}                              AS                      name
        ,stat.{}                              AS                      position_lat
        ,stat.{}                              AS                      position_long
        ,FROM_UNIXTIME(stat.{})               AS                      created_date
    FROM
        {} stat
    """.format('number'
            ,'address'
            ,'banking'
            ,'bike_stands'
            ,'bonus'
            ,'contract_name'
            ,'name'
            ,'position_lat'
            ,'position_long'
            ,'created_date'
            ,'01_station')



###Stations Given Station Number
SQL_select_station_where_number="""
    SELECT
         stat.{}                              AS                      number
        ,stat.{}                              AS                      address
        ,stat.{}                              AS                      banking
        ,stat.{}                              AS                      bike_status
        ,stat.{}                              AS                      bike_stands
        ,stat.{}                              AS                      contract_name
        ,stat.{}                              AS                      name
        ,stat.{}                              AS                      position_lat
        ,stat.{}                              AS                      position_long
        ,FROM_UNIXTIME(stat.{})               AS                      created_date
    FROM
        {} stat
    WHERE
        stat.{}
    """.format('number'
                ,'address'
                ,'banking'
                ,'bike_stands'
                ,'bonus'
                ,'contract_name'
                ,'name'
                ,'position_lat'
                ,'position_long'
                ,'created_date'
                ,'01_station'
                ,'number') + """={}"""


####
#---02. Availability Queries
####

SQL_select_availability="""
    SELECT
         avail.{}                               AS              number
        ,avail.{}                               AS              available_bikes
        ,avail.{}                               AS              available_bike_stands
        ,FROM_UNIXTIME({})                      AS              last_update
        ,FROM_UNIXTIME({})                      AS              created_date
    FROM
        {} avail
    """.format(
            'number'
            ,'available_bikes'
            ,'available_bike_stands'
            ,'last_update'
            ,'created_date'
            ,'01_availability'
            )


SQL_select_availability_where_number="""
    SELECT
         avail.{}                            AS              number
        ,avail.{}                            AS              available_bikes
        ,avail.{}                            AS              available_bike_stands
        ,FROM_UNIXTIME(avail.{})             AS              last_update
        ,FROM_UNIXTIME(avail.{})             AS              created_date
    FROM
        avail.{} avail
    WHERE
        avail.{}
    """.format(
            'number'
            ,'available_bikes'
            ,'available_bike_stands'
            ,'last_update'
            ,'created_date'
            ,'01_availability'
            ,'number'
            ) + "={}"

#Get the Last Update Availability Info for each station
SQL_select_availability_last_update="""
    SELECT
         all_avail.{}                            AS              number
        ,all_avail.{}                            AS              available_bikes
        ,all_avail.{}                            AS              available_bike_stands
        ,FROM_UNIXTIME(all_avail.{})             AS              last_update
        ,FROM_UNIXTIME(all_avail.{})             AS              created_date
    FROM
        (    
            SELECT
                 {}                  AS              number
                ,MAX({})             AS              created_date
            FROM
                {}
            GROUP BY
                {}
        ) max_avail
        
    INNER JOIN
        {} all_avail
    ON
        all_avail.{}=max_avail.number
    AND
        all_avail.{}=max_avail.created_date

    """.format('number'
                ,'available_bikes'
                ,'available_bike_stands'
                ,'last_update'
                ,'created_date'

                ,'number'
                ,'created_date'
                ,'01_availability'
                ,'number'

                ,'01_availability'
                ,'number'
                ,'created_date'
            )

####
#---03. Weather Queries
####

SQL_select_weather="""
    SELECT
         weath.{}                             AS                        number
        ,weath.{}                             AS                        position_long
        ,weath.{}                             AS                        position_lat
        ,weath.{}                             AS                        weather_id
        ,weath.{}                             AS                        main
        ,weath.{}                             AS                        description
        ,weath.{}                             AS                        icon
        ,weath.{}                             AS                        icon_url
        ,weath.{}                             AS                        base
        ,weath.{}                             AS                        temp
        ,weath.{}                             AS                        feels_like
        ,weath.{}                             AS                        temp_min
        ,weath.{}                             AS                        temp_max
        ,weath.{}                             AS                        pressure
        ,weath.{}                             AS                        humidity
        ,weath.{}                             AS                        visibility
        ,weath.{}                             AS                        wind_speed
        ,weath.{}                             AS                        wind_degree
        ,weath.{}                             AS                        clouds_all
        ,weath.{}                             AS                        datetime
        ,weath.{}                             AS                        sys_id
        ,weath.{}                             AS                        sys_country
        ,weath.{}                             AS                        sys_sunrise
        ,weath.{}                             AS                        sys_sunset
        ,weath.{}                             AS                        sys_type
        ,weath.{}                             AS                        timezone
        ,weath.{}                             AS                        id
        ,weath.{}                             AS                        weather_name
        ,weath.{}                             AS                        cod
        ,FROM_UNIXTIME(weath.{})              AS                        created_date
    FROM
        {} weath
    """.format('number'
                ,'position_long'
                ,'position_lat'
                ,'weather_id'
                ,'main'
                ,'description'
                ,'icon'
                ,'icon_url'
                ,'base'
                ,'temp'
                ,'feels_like'
                ,'temp_min'
                ,'temp_max'
                ,'pressure'
                ,'humidity'
                ,'visibility'
                ,'wind_speed'
                ,'wind_degree'
                ,'clouds_all'
                ,'datetime'
                ,'sys_id'
                ,'sys_country'
                ,'sys_sunrise'
                ,'sys_sunset'
                ,'sys_type'
                ,'timezone'
                ,'id'
                ,'name'
                ,'cod'
                ,'created_date'
                ,'01_weather')


SQL_select_weather_where_number="""
    SELECT
         weath.{}                             AS                        number
        ,weath.{}                             AS                        position_long
        ,weath.{}                             AS                        position_lat
        ,weath.{}                             AS                        weather_id
        ,weath.{}                             AS                        main
        ,weath.{}                             AS                        description
        ,weath.{}                             AS                        icon
        ,weath.{}                             AS                        icon_url
        ,weath.{}                             AS                        base
        ,weath.{}                             AS                        temp
        ,weath.{}                             AS                        feels_like
        ,weath.{}                             AS                        temp_min
        ,weath.{}                             AS                        temp_max
        ,weath.{}                             AS                        pressure
        ,weath.{}                             AS                        humidity
        ,weath.{}                             AS                        visibility
        ,weath.{}                             AS                        wind_speed
        ,weath.{}                             AS                        wind_degree
        ,weath.{}                             AS                        clouds_all
        ,weath.{}                             AS                        datetime
        ,weath.{}                             AS                        sys_id
        ,weath.{}                             AS                        sys_country
        ,weath.{}                             AS                        sys_sunrise
        ,weath.{}                             AS                        sys_sunset
        ,weath.{}                             AS                        sys_type
        ,weath.{}                             AS                        timezone
        ,weath.{}                             AS                        id
        ,weath.{}                             AS                        weather_name
        ,weath.{}                             AS                        cod
        ,FROM_UNIXTIME(weath.{})              AS                        created_date
    FROM
        {} weath
    WHERE
        weath.{}
    """.format('number'
                ,'position_long'
                ,'position_lat'
                ,'weather_id'
                ,'main'
                ,'description'
                ,'icon'
                ,'icon_url'
                ,'base'
                ,'temp'
                ,'feels_like'
                ,'temp_min'
                ,'temp_max'
                ,'pressure'
                ,'humidity'
                ,'visibility'
                ,'wind_speed'
                ,'wind_degree'
                ,'clouds_all'
                ,'datetime'
                ,'sys_id'
                ,'sys_country'
                ,'sys_sunrise'
                ,'sys_sunset'
                ,'sys_type'
                ,'timezone'
                ,'id'
                ,'name'
                ,'cod'
                ,'created_date'
                ,'01_weather'
                ,'number')+"={}"



SQL_select_weather_last_update="""
    SELECT
         weath.{}                             AS                        number
        ,weath.{}                             AS                        position_long
        ,weath.{}                             AS                        position_lat
        ,weath.{}                             AS                        weather_id
        ,weath.{}                             AS                        main
        ,weath.{}                             AS                        description
        ,weath.{}                             AS                        icon
        ,weath.{}                             AS                        icon_url
        ,weath.{}                             AS                        base
        ,weath.{}                             AS                        temp
        ,weath.{}                             AS                        feels_like
        ,weath.{}                             AS                        temp_min
        ,weath.{}                             AS                        temp_max
        ,weath.{}                             AS                        pressure
        ,weath.{}                             AS                        humidity
        ,weath.{}                             AS                        visibility
        ,weath.{}                             AS                        wind_speed
        ,weath.{}                             AS                        wind_degree
        ,weath.{}                             AS                        clouds_all
        ,weath.{}                             AS                        datetime
        ,weath.{}                             AS                        sys_id
        ,weath.{}                             AS                        sys_country
        ,weath.{}                             AS                        sys_sunrise
        ,weath.{}                             AS                        sys_sunset
        ,weath.{}                             AS                        sys_type
        ,weath.{}                             AS                        timezone
        ,weath.{}                             AS                        id
        ,weath.{}                             AS                        weather_name
        ,weath.{}                             AS                        cod
        ,FROM_UNIXTIME(weath.{})              AS                        created_date
    FROM
        (SELECT
            {}                                AS                        number
            ,MAX({})                          AS                        created_date
        FROM
            {}
        GROUP BY
            {}
        ) max_weath

    INNER JOIN
        {} weath
    ON
        max_weath.created_date=weath.{}
        AND
        max_weath.number=weath.{}
    """.format('number'
                ,'position_long'
                ,'position_lat'
                ,'weather_id'
                ,'main'
                ,'description'
                ,'icon'
                ,'icon_url'
                ,'base'
                ,'temp'
                ,'feels_like'
                ,'temp_min'
                ,'temp_max'
                ,'pressure'
                ,'humidity'
                ,'visibility'
                ,'wind_speed'
                ,'wind_degree'
                ,'clouds_all'
                ,'datetime'
                ,'sys_id'
                ,'sys_country'
                ,'sys_sunrise'
                ,'sys_sunset'
                ,'sys_type'
                ,'timezone'
                ,'id'
                ,'name'
                ,'cod'
                ,'created_date'

                ,'number'
                ,'created_date'
                ,'01_weather'
                ,'number'

                ,'01_weather'
                ,'created_date'
                ,'number'
                )



####
#---04. Joining Queries
####


SQL_select_avail_weather="""
    SELECT
        available.number                              AS          number
        ,available.available_bikes                    AS          available_bikes
        ,available.available_bike_stands              AS          available_bike_stands
        ,available.last_update                        AS          last_update
        ,available.created_date                       AS          created_date
        ,weather.position_long                        AS          weather_position_long
        ,weather.position_lat                         AS          weather_position_lat
        ,weather.weather_id
        ,weather.main
        ,weather.description
        ,weather.icon
        ,weather.icon_url
        ,weather.base
        ,weather.temp
        ,weather.feels_like
        ,weather.temp_min
        ,weather.temp_max
        ,weather.pressure
        ,weather.humidity
        ,weather.visibility
        ,weather.wind_speed
        ,weather.wind_degree
        ,weather.clouds_all
        ,weather.datetime
        ,weather.sys_id
        ,weather.sys_country
        ,weather.sys_sunrise
        ,weather.sys_sunset
        ,weather.sys_type
        ,weather.timezone
        ,weather.id
        ,weather.name                                   AS              weather_name
        ,weather.cod
    FROM
        ({}) available

    INNER JOIN
        ({}) weather
    ON
        available.number=weather.number
        AND
        available.created_date=weather.created_date
    """.format(SQL_select_availability
           ,SQL_select_weather)




SQL_select_station_avail="""
    SELECT
        station.number                                AS                      number
        ,station.address                              AS                      address
        ,station.banking                              AS                      banking
        ,station.bike_status                          AS                      bike_status
        ,station.bike_stands                          AS                      bike_stands
        ,station.contract_name                        AS                      contract_name
        ,station.name                                 AS                      name
        ,station.position_lat                         AS                      position_lat
        ,station.position_long                        AS                      position_long
        ,available.available_bikes                    AS                      available_bikes
        ,available.available_bike_stands              AS                      available_bike_stands
        ,available.last_update                        AS                      last_update
        ,available.created_date                       AS                      created_date
    FROM
        ({}) station

    INNER JOIN
        ({}) available
    ON
        station.number=available.number
    """.format(SQL_select_station
           ,SQL_select_availability)


SQL_select_station_avail_conditionals="""
    SELECT
        station.number                                AS                      number
        ,station.address                              AS                      address
        ,station.banking                              AS                      banking
        ,station.bike_status                          AS                      bike_status
        ,station.bike_stands                          AS                      bike_stands
        ,station.contract_name                        AS                      contract_name
        ,station.name                                 AS                      name
        ,station.position_lat                         AS                      position_lat
        ,station.position_long                        AS                      position_long
        ,available.available_bikes                    AS                      available_bikes
        ,available.available_bike_stands              AS                      available_bike_stands
        ,available.last_update                        AS                      last_update
        ,available.created_date                       AS                      created_date
    FROM
        ({}) station

    INNER JOIN
        ({}) available
    ON
        station.number=available.number
    """

SQL_select_station_avail_latest_update="""
    SELECT
        station.number                                AS                      number
        ,station.address                              AS                      address
        ,station.banking                              AS                      banking
        ,station.bike_status                          AS                      bike_status
        ,station.bike_stands                          AS                      bike_stands
        ,station.contract_name                        AS                      contract_name
        ,station.name                                 AS                      name
        ,station.position_lat                         AS                      position_lat
        ,station.position_long                        AS                      position_long
        ,available.available_bikes                    AS                      available_bikes
        ,available.available_bike_stands              AS                      available_bike_stands
        ,available.last_update                        AS                      last_update
        ,available.created_date                       AS                      created_date
    FROM
        ({}) station

    INNER JOIN
        ({}) available
    ON
        station.number=available.number
    """.format(SQL_select_station,SQL_select_availability_last_update)


SQL_select_station_avail_weather="""
    SELECT
        station.number                                AS                      number
        ,station.address                              AS                      address
        ,station.banking                              AS                      banking
        ,station.bike_status                          AS                      bike_status
        ,station.bike_stands                          AS                      bike_stands
        ,station.contract_name                        AS                      contract_name
        ,station.name                                 AS                      name
        ,station.position_lat                         AS                      position_lat
        ,station.position_long                        AS                      position_long
        ,available.available_bikes                    AS                      available_bikes
        ,available.available_bike_stands              AS                      available_bike_stands
        ,available.last_update                        AS                      last_update
        ,available.created_date                       AS                      created_date
        ,weather.position_long                        AS                      weather_position_long
        ,weather.position_lat                         AS                      weather_position_lat
        ,weather.weather_id
        ,weather.main
        ,weather.description
        ,weather.icon
        ,weather.icon_url
        ,weather.base
        ,weather.temp
        ,weather.feels_like
        ,weather.temp_min
        ,weather.temp_max
        ,weather.pressure
        ,weather.humidity
        ,weather.visibility
        ,weather.wind_speed
        ,weather.wind_degree
        ,weather.clouds_all
        ,weather.datetime
        ,weather.sys_id
        ,weather.sys_country
        ,weather.sys_sunrise
        ,weather.sys_sunset
        ,weather.sys_type
        ,weather.timezone
        ,weather.id
        ,weather.weather_name
        ,weather.cod
    FROM
        ({}) station

    INNER JOIN
        ({}) available
    ON
        station.number=available.number

    INNER JOIN
        ({}) weather
    ON
        available.number=weather.number
        AND
        available.created_date=weather.created_date
    """.format(SQL_select_station
           ,SQL_select_availability
           ,SQL_select_weather)




SQL_select_avail_weather_conditional="""
    SELECT
        available.number                              AS          number
        ,available.available_bikes                    AS          available_bikes
        ,available.available_bike_stands              AS          available_bike_stands
        ,available.last_update                        AS          last_update
        ,available.created_date                       AS          created_date
        ,weather.position_long                        AS          weather_position_long
        ,weather.position_lat                         AS          weather_position_lat
        ,weather.weather_id
        ,weather.main
        ,weather.description
        ,weather.icon
        ,weather.icon_url
        ,weather.base
        ,weather.temp
        ,weather.feels_like
        ,weather.temp_min
        ,weather.temp_max
        ,weather.pressure
        ,weather.humidity
        ,weather.visibility
        ,weather.wind_speed
        ,weather.wind_degree
        ,weather.clouds_all
        ,weather.datetime
        ,weather.sys_id
        ,weather.sys_country
        ,weather.sys_sunrise
        ,weather.sys_sunset
        ,weather.sys_type
        ,weather.timezone
        ,weather.id
        ,weather.weather_name
        ,weather.cod
    FROM
        ({}) available

    INNER JOIN
        ({}) weather
    ON
        available.number=weather.number
        AND
        available.created_date=weather.created_date
    """

SQL_select_station_avail_weather_conditionals="""
    SELECT
        station.number                                AS                      number
        ,station.address                              AS                      address
        ,station.banking                              AS                      banking
        ,station.bike_status                          AS                      bike_status
        ,station.bike_stands                          AS                      bike_stands
        ,station.contract_name                        AS                      contract_name
        ,station.name                                 AS                      name
        ,station.position_lat                         AS                      position_lat
        ,station.position_long                        AS                      position_long
        ,available.available_bikes                    AS                      available_bikes
        ,available.available_bike_stands              AS                      available_bike_stands
        ,available.last_update                        AS                      last_update
        ,available.created_date                       AS                      created_date
        ,weather.position_long                        AS                      weather_position_long
        ,weather.position_lat                         AS                      weather_position_lat
        ,weather.weather_id
        ,weather.main
        ,weather.description
        ,weather.icon
        ,weather.icon_url
        ,weather.base
        ,weather.temp
        ,weather.feels_like
        ,weather.temp_min
        ,weather.temp_max
        ,weather.pressure
        ,weather.humidity
        ,weather.visibility
        ,weather.wind_speed
        ,weather.wind_degree
        ,weather.clouds_all
        ,weather.datetime
        ,weather.sys_id
        ,weather.sys_country
        ,weather.sys_sunrise
        ,weather.sys_sunset
        ,weather.sys_type
        ,weather.timezone
        ,weather.id
        ,weather.weather_name
        ,weather.cod
    FROM
        ({}) station

    INNER JOIN
        ({}) available
    ON
        station.number=available.number

    INNER JOIN
        ({}) weather
    ON
        available.number=weather.number
        AND
        available.created_date=weather.created_date
    """



SQL_select_limit_availability= """SELECT 
                                        * 
                                FROM 
                                    {}
                                ORDER BY 
                                    created_date 
                                DESC
                                    LIMIT 109;""".format(
                                            '01_availability'
                                    )