#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unirest
import urllib
import urllib2
import urlparse
import json

print "Welcome to the broadcast weather app"
print "What country would you like to check the weather?"
country = raw_input("Please enter your country name:")
while country.isalpha() or country.isdigit():
	if country.isdigit():
		print "Oops, you typed a number,please try again"
		country = raw_input()
		continue
	if country.isalpha():
		try:
			response = unirest.get("https://restcountries-v1.p.mashape.com/name/"+country,
			headers={"X-Mashape-Key": "26D2fnt4QPmshTRjJ8zhI6oDR03dp11be9KjsnRxxFLkVPpVbG",
  			  "Accept": "application/json"},params = {"body":"alpha2Code"}
			)	
			country_initials = response.body[0]["alpha2Code"]
			break
		except KeyError:
			print "the country you typed does not exists, please type again"
			country = raw_input()	
			continue
country_initials = response.body[0]["alpha2Code"]
data = urllib.urlopen('http://openweathermap.org/help/city_list.txt')
cities_list = list()
i=1
print "The cities inside the country you have choosen"
for line in data:
	if country_initials == line[-3]+line[-2]:
		elements = line.split()
		city =  " ".join(elements[1:-3]) 
		cities_list.append(city)
		print i,city
		i+=1
user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
while user_choice.isalpha() or int(user_choice) <= 0 or int(user_choice):
	if user_choice.isalpha():
		print "Oops,you did'nt typed a integer, please try again"
		user_choice = raw_input()
		continue
	if int(user_choice) <=0:
		print "Please type a number bigger than 0"
		user_choice = raw_input()
		continue
	if int(user_choice):
		try:
			user_choice = int(user_choice) - 1
			city = cities_list[user_choice]
			city = city.strip().replace(" ", "-")
			break	
		except IndexError:
			print "the number you typed is unsuitable, please type again:"
			user_choice = raw_input()
			continue





url = 'http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid=9aa4492b034cef3250be6f72629b73e9'
values = {}
data = urllib.urlencode(values)
data = data.encode('utf-8')
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
data = json.loads(response.read())
temp =  data['main']['temp']
temp = float(temp-273)
print "The current temperature in "+ city+ " is " + str(round(temp,1)) + "°C"
pressure = data['main']['pressure']
print "The current pressure in "+ city+ " is " + str(pressure)
humidity = data['main']['humidity']
print "The current humidity in "+ city+ " is " + str(humidity)
temp_min = data['main']['temp_min']
temp_min = float(temp_min-273)
print "The minimum temperature in "+ city+ " is " + str(round(temp_min,1)) + "°C"
temp_max = data['main']['temp_max']
temp_max = float(temp_max-273)
print "The maximum temperature in " +city+ " is " + str(round(temp_max,1)) + "°C"
