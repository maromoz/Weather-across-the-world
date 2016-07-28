#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import urlparse
import json

print "Welcome to the broadcast weather app"
print "What country would you like to check the weather?"
country = raw_input("Please enter your country initials:")
country = country.upper()
data = urllib.urlopen('http://openweathermap.org/help/city_list.txt')
cities_list = list()
i=1
print "The cities inside the country you have choosen"
for line in data:
	if country == line[-3]+line[-2]:
		elements = line.split()
		cities =  " ".join(elements[1:-3]) 
		new_line = i,cities
		print new_line
		i+=1
		cities_list += new_line
user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
for i in cities_list:
	if str(user_choice) == str(i):
		s = int(user_choice) + 1
		s = 2*s - 3
		city = cities_list[s]
		print "The city you have chosen is " + str(city)

url = 'http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid=9aa4492b034cef3250be6f72629b73e9'
values = {}
data = urllib.urlencode(values)
data = data.encode('utf-8')
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
data = json.loads(response.read())
temp =  data['main']['temp']
temp = float(temp/10)
print "The current temperature in "+ city+ " is " + str(round(temp,1)) + "°C"
pressure = data['main']['pressure']
print "The current pressure in "+ city+ " is " + str(pressure)
humidity = data['main']['humidity']
print "The current humidity in "+ city+ " is " + str(humidity)
temp_min = data['main']['temp_min']
temp_min = float(temp_min/10)
print "The minimum temperature in "+ city+ " is " + str(round(temp_min,1)) + "°C"
temp_max = data['main']['temp_max']
temp_max = float(temp_max/10)
print "The maximum temperature in " +city+ " is " + str(round(temp_max,1)) + "°C"
