import os
import json
import requests
from abc import ABC

class OpenWeatherMapBase(ABC):
	main_data = None

	def requests_get(self):
		url = self.link + self.name + self.token
		page = requests.get(url)
		self.main_data = page.json()
		if not os.path.exists('docs'):
			os.mkdir("docs")
		with open('docs/data.json', 'w') as file:
			json.dump(self.main_data, file, indent=4, ensure_ascii=False)

	def __init__(self, link, name, token):
		self.link = link
		self.name = '+'.join((name.strip()).split())
		self.token = token
		self.requests_get()

	def coordinates(self):
		coord_lon = self.main_data['coord']['lon']
		coord_lat = self.main_data['coord']['lat']
		coordinate = [coord_lon, coord_lat]

		return coordinate

	def cloud(self):
		cloud_all = self.main_data['clouds']['all']
		clouds = [cloud_all]

		return clouds

	def sys(self):
		sys_type = self.main_data['sys']['type']
		sys_id = self.main_data['sys']['id']
		sys_country = self.main_data['sys']['country']
		sys_sunrise = self.main_data['sys']['sunrise']
		sys_sunset = self.main_data['sys']['sunset']
		sys = [sys_type, sys_id, sys_country, sys_sunrise, sys_sunset]

		return sys

	def temperatures(self):
		temp = self.main_data['main']['temp']
		feels_like = self.main_data['main']['feels_like']
		temp_min = self.main_data['main']['temp_min']
		temp_max = self.main_data['main']['temp_max']
		pressure = self.main_data['main']['pressure']
		humidity = self.main_data['main']['humidity']
		temperature = [
			temp, feels_like, temp_min,
			temp_max, pressure, humidity
		]

		return temperature

	def weathers(self):
		weather_id = self.main_data['weather'][0]['id']
		weather_main = self.main_data['weather'][0]['main']
		weather_description = self.main_data['weather'][0]['description']
		weather_icon = self.main_data['weather'][0]['icon']
		weather = [
			weather_id, weather_main, weather_description,
			weather_icon
		]

		return weather

	def winds(self):
		wind_speed = self.main_data['wind']['speed']
		wind_deg = self.main_data['wind']['deg']
		wind = [wind_speed, wind_deg]

		return wind

	def city_parameter(self):
		city_name = self.main_data['name']
		city_id = self.main_data['id']
		city_timezone = self.main_data['timezone']
		city_cod = self.main_data['cod']
		city_visibility = self.main_data["visibility"]
		parameter = [
			city_name, city_id, city_timezone, city_cod, city_visibility,
		]

		return parameter
