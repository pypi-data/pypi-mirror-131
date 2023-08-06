from OpenWeatherMapBase.open_weather_map_base import OpenWeatherMapBase

link = 'http://api.openweathermap.org/data/2.5/weather?q='
name = 'Amsterdam'
token = '&appid=8605670c5573e75489dab32b3a5b7b18&units=metric'

ob = OpenWeatherMapBase(link, name, token)

print(ob.coordinates())
print(ob.winds())
print(ob.weathers())
print(ob.city_parameter())
print(ob.sys())
print(ob.cloud())
print(ob.temperatures())
