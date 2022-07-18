
import requests
from pprint import pprint

city = input('Выберите город: ')

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=239d9dde71f85ea3175e9c09f3b3abd3&units=metric'.format(city)

res = requests.get(url)

data = res.json()

temp = data["main"]["temp"]
wind_speed = data['wind']['speed']
description = data['weather'][0]['description']

print('Температура : {} Цельсий'.format(temp))
print('Скорось ветра : {} м/с'.format(wind_speed))
print('Описание : {}'.format(description))


