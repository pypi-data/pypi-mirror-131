def my_weather(zipcode): 
    import os
    from dotenv import load_dotenv
    load_dotenv('MY_ENV_VAR.env')
    weather_key = os.getenv('MY_ENV_VAR')
    
    import requests
    params = {'appid': weather_key, 'q': zipcode}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = params)
    
    import json
    import pandas as pd
    weather_json = r.json()
    df = pd.DataFrame(weather_json['main'], index = [1])
    return df

def weather_sector(zipcode, column): 
    import os
    from dotenv import load_dotenv
    load_dotenv('MY_ENV_VAR.env')
    weather_key = os.getenv('MY_ENV_VAR')
    
    import requests
    params = {'appid': weather_key, 'q': zipcode}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = params)
    
    import json
    import pandas as pd
    weather_json = r.json()
    df = pd.DataFrame(weather_json['main'], index = [1])
    info = df.iloc[0][column]
    return info