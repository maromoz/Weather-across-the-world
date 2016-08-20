#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unirest
import urllib
import urllib2
import urlparse
import json
import sys
import optparse
from optparse import OptionParser
import sys
from progressbar import ProgressBar

def country_temprature_callback(option, opt_str, value, parser):
	is_average = parser.values.average
	country_temprature(is_average)
	sys.exit()


#######################################################################################################
def country_temprature(is_average):
	country = sys.argv[3]
	#Checking for the user's input type(should be a country name)
	if not country.isalpha():
		print "You typed wrong please run the program try again"
		sys.exit()
	#Checking the user internet connection
	response = None
	attempt = 0
	while not response and attempt < 3:
		attempt += 1
	        try:
	         	response = unirest.get("https://restcountries-v1.p.mashape.com/name/"+country,
	 	        headers={"X-Mashape-Key": "26D2fnt4QPmshTRjJ8zhI6oDR03dp11be9KjsnRxxFLkVPpVbG",
	                   "Accept": "application/json"}
	                    		    )
		except: 
	        	print "failed %d times, trying again" % attempt
	if not response:
	        print "the program fail, please check your internt and access the program again"
		sys.exit()
	try:
		country_initials = response.body[0]["alpha2Code"]
	except KeyError: 
		print "You typed wrong please run the program try again"
		sys.exit()
	#converting the country name to the country initials for further actions
	attempt = 0
	data = None
	while not data and attempt <3:
		attempt +=1
		try:
			data = urllib.urlopen('http://openweathermap.org/help/city_list.txt')
		except:
			 print "failed %d times, trying again" % attempt
	
	cities_list = list()
	i=1
	if is_average == False:
		print "The cities inside the country you have choosen"
	for line in data:
	#Appending each line that the country initials are equal to the user input
		if country_initials == line[-3]+line[-2]:
			elements = line.split()
	     		city =  " ".join(elements[1:-3])
	       		cities_list.append(city)
			if is_average == False:
	       			print i,city
			#Printing each city of the country with a number for the user to choose from
	      		i+=1
	if not data:
		print "the program fail, please check your internt and access the program again"
		sys.exit()
	if not is_average == True:	
		user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
		#Checking if the user's input is an interger and that the same interger is next to a city above and not equal to 0
		while True:
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
	       		 		print "the number you typed is unsuitable, please try again"
					user_choice = raw_input()
	               			continue
			else:
				print "you need to type a number, please try again"
				user_choice = raw_input()
				continue

	#Taking the city that the user choose and checking all the weather attributes in the "open weather" API
	attempt = 0
	response = None
	while not response and attempt < 3:
		attempt +=1
		try:
			if is_average == True:
				temp_average = 0
				temp_min_average = 0
				temp_max_average = 0
				pressure_average = 0
				humidity_average = 0
				average_counter = 0
				pbar = ProgressBar()
				for city in pbar(cities_list):
					city = city.strip().replace(" ", "-")
					url = 'http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid=9aa4492b034cef3250be6f72629b73e9'
					values = {}
					data = urllib.urlencode(values)
					data = data.encode('utf-8')
					req = urllib2.Request(url, data)
					response = urllib2.urlopen(req)
					data = json.loads(response.read())	
					temp = data['main']['temp']
					temp = float(temp-273)
					temp_average += temp
					pressure = data['main']['pressure']
					pressure_average += pressure
					humidity = data['main']['humidity']
					humidity_average += humidity	
					temp_min = data['main']['temp_min']
					temp_min = float(temp_min-273)
					temp_min_average += temp_min
					temp_max = data['main']['temp_max']
					temp_max = float(temp_max-273)
					temp_max_average += temp_max
					average_counter += 1
					if average_counter == 5:
						break

				temp_average = temp_average / average_counter
				pressure_average = pressure_average / average_counter
				humidity_average = humidity_average / average_counter
				temp_min_average = temp_min_average / average_counter
				temp_max_average = temp_max_average / average_counter
				print "The average temprature in " + country + " is " +str(round(temp_average,1))+ "°C" 
				print "The average pressure in " + country + " is " + str(round(pressure_average,1))
				print "The average humidity in " + country + " is " + str(round(humidity_average,1))
				print "The average minimum temprature in " + country + " is " +str(round(temp_min_average,1))+ "°C" 
				print "The average maximum temprature in " + country + " is " +str(round(temp_max_average,1))+ "°C" 


			else:
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

		except:		
			print "failed %d times, trying again" % attempt
	if not response:
		print "the program fail, please check your internt and access the program again"
		sys.exit()

	
################################################################################################################################

parser = OptionParser(usage = "Weather forecast software",
                description = "Welcome to Weather across the world, please choose and option:\n to select a country please type -c or --country and then your counrty name")

parser.add_option("-a", "--average",
                 action = "store_true", default = False,dest = "average",
		 help = "This option will print the average temprature information of the choosen country")


parser.add_option("-c", "--country",
                 action = "callback", callback = country_temprature_callback ,dest = "country",
		 help = "This option will print all the cities inside the choosen country")


parser.parse_args()

options, args = parser.parse_args()

