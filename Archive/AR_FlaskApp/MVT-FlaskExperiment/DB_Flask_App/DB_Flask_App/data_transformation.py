
def existing_station_numbers(engine):
    """A function to check which station numbers are already in the database"""
    station_list=[]
    
    try:
        Select_SQL="""
        SELECT
            number
        FROM
            01_station
        """

        result=engine.execute(Select_SQL)

        rows = result.fetchall()

        for station_number in rows:
            print(station_number)
            station_list+=[station_number[0]]
            
        result.close()
            
    except:
        print('Test')
        station_list=[]
        
        
    return station_list
