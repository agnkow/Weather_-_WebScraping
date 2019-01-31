# Weather 

* ### OGIMET (web scraping)

Function **get_city_id** returns all cities (weather stations) and their id for the given countries.
```python
get_city_id(p_state, p_state_name, file, p_date = '2018-11-11')
```

Function **get_weather** returns the weather for the given city id and for the given period of time.
```python
get_weather(date_start, date_end, city_id, file)
```


* ### Yahoo Weather New API

The code comes from [dhenxie09/yahoo-weather](https://github.com/dhenxie09/yahoo-weather), but it has been ported to Python 3.
[Sample Usage.](https://github.com/dhenxie09/yahoo-weather)

