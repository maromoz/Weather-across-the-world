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
while True:
	#Checking for the user's input type(should be a country name)
        if country.isalpha():
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
		try:
                        country_initials = response.body[0]["alpha2Code"]
                        break
                except KeyError:
                        print "the country you typed does not exists, please type again"
                        country = raw_input()
                        continue
	else:
		print "You typed wrong please try again:"
		country = raw_input()
		continue
#converting the country name to the country initials for further actions
attempt_2 = 0
while True:
	try:
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
	except IOError:
		print "your internet connection is not working, please check your internet connection"
		attempt_2 += 1
		if attempt_2 == 3:
			print "the program fail, please check your internt and access the program again"
			sys.exit()
		continue

user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
while True:
#Checking if the user's input is an interger and that the same interger is next to a city above and not equal to 0
	if user_choice.isdigit():
		user_choice = int(user_choice)
		if user_choice == 0:
			print "you typed 0, please try again:"
			user_choice = raw_input()	
			continue
                try:
                        user_choice = int(user_choice) - 1
			city = cities_list[user_choice]
                        city = city.strip().replace(" ", "-")
                        break
                except IndexError:
                        print "the number you typed is unsuitable, please type again:"
                        user_choice = raw_input()
                        continue
	else:
		print "You typed wrong please try again:"
		user_choice = raw_input()
		continue




#Taking the city that the user choose and checking all the weather attributes in the "open weather" API
attempt_3 = 0
while  True:
	try:
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
		break
	except:		
		print "your internet connection is not working, please check your internet connection"
		attempt_3 += 1
		if attempt_3 == 3:
			print "the program fail, please check your internt and access the program again"
			sys.exit()
		continue



