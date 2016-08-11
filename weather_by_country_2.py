#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unirest
import urllib
import urllib2
import urlparse
import json
import sys


print "Welcome to the broadcast weather app"
print "What country would you like to check the weather?"
country = raw_input("Please enter your country name:")
while country.isdigit() == False  and country.isalpha() == False or country.isalpha() or country.isdigit():
#Checking for the user's input type(should be a country name)
        if country.isdigit() == False  and country.isalpha() == False:
                print "you typed wrong please try again:"
                country = raw_input()
                continue
        if country.isdigit():
                print "Oops, you typed a number,please try again"
                country = raw_input()
                continue
        if country.isalpha():
                try:
                        #Checking the user internet connection
                        attempt = 0
                        while attempt <3:
                                try:
                                        response = unirest.get("https://restcountries-v1.p.mashape.com/name/"+country,
                                        headers={"X-Mashape-Key": "26D2fnt4QPmshTRjJ8zhI6oDR03dp11be9KjsnRxxFLkVPpVbG",
                                          "Accept": "application/json"}
                                        )
                                        break
                                except: 
                                        print "your internet connection is not working, please check your internet connection"
                                        attempt += 1
                                        if attempt == 3:
                                                print "the program fail, please check your internt and access the program again"
						sys.exit()
                        country_initials = response.body[0]["alpha2Code"]
                        break
                except KeyError:
                        print "the country you typed does not exists, please type again"
                        country = raw_input()
                        continue
#converting the country name to the country initials for further actions
data = urllib.urlopen('http://openweathermap.org/help/city_list.txt')
cities_list = list()
i=1
print "The cities inside the country you have choosen"
for line in data:
#Appending each line that the country initials are equal to the user input
        if country_initials == line[-3]+line[-2]:
                elements = line.split()
                city =  " ".join(elements[1:-3])
                cities_list.append(city)
                print i,city
		#Printing each city of the country with a number for the user to choose from
                i+=1
user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
while user_choice.isdigit() == False and user_choice.isalpha() == False or user_choice.isalpha() or int(user_choice):
#Checking if the user's input is an interger and that the same interger is next to a city above
        if user_choice.isdigit() == False and user_choice.isalpha() == False:
                print "you typed wrong please try again:"
                user_choice = raw_input()
                continue
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




#Taking the city that the user choose and checking all the weather attributes in the "open weather" API
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









