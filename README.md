# Weather 

* ### OGIMET (web scraping)

Function **get_city_id** returns all cities (weather stations) and their ids for the given countries.
```python
get_city_id(p_state, p_state_name, file)
```

Function **get_weather** returns the weather for the given city id and for the given period of time.
```python
get_weather(date_start, date_end, city_id, file)
```

Examples: 
```python
get_city_id(p_state='Pola', p_state_name='Poland', file='output/city_code_pl.csv')

get_weather(date_start = '2018-11-11', date_end = '2018-11-12',
            city_id = '12566', file = 'output/weather_test.csv')
```



* ### Yahoo Weather New API

The code comes from [dhenxie09/yahoo-weather](https://github.com/dhenxie09/yahoo-weather), but it has been ported to Python 3.
[Sample Usage.](https://github.com/dhenxie09/yahoo-weather)

