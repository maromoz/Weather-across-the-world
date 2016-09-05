#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unirest
import urllib
import urllib2
import urlparse
import json
import sys
import MySQLdb
import pymysql.cursors
from time import sleep
from timeit import timeit
from progress.bar import Bar



#######################################################################################################################################

def update_attributes(city,country_initials):
	print "working on", city
	attempt = 0
	response = None
	while not response and attempt < 3:
	        attempt +=1
	        try:
	        	url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=9aa4492b034cef3250be6f72629b73e9'
	                values = {}
	                data = urllib.urlencode(values)
	                data = data.encode('utf-8')
	                req = urllib2.Request(url, data)
	                response = urllib2.urlopen(req)
	                data = json.loads(response.read())
	                temp =  data['main']['temp']
	                temp = float(round(temp-273,1))
	                pressure = data['main']['pressure']
			pressure = float(round(pressure,1))
	                humidity = data['main']['humidity']
			humidity = float(round(humidity,1))
	                temp_min = data['main']['temp_min']
	                temp_min = float(round(temp_min-273,1))
	                temp_max = data['main']['temp_max']
	                temp_max = float(round(temp_max-273,1))
		
		except:
			break
	if not response:
	        print "the program fail, please check your internt and access the program again"
	        sys.exit()

	response = None
	attempt = 0
	while not response and attempt < 3:
		attempt += 1
	        try:
	        	response = unirest.get("https://restcountries-v1.p.mashape.com/alpha/"+country_initials,
			headers={
			"X-Mashape-Key": "26D2fnt4QPmshTRjJ8zhI6oDR03dp11be9KjsnRxxFLkVPpVbG",
			"Accept": "application/json"
			}
			)
	        except:
	        	print "failed %d times, trying again" % attempt
	if not response:
		print "the program fail, please check your internet and access the program again"
		sys.exit()
	
	country_name = response.body["name"]
	
	connection = pymysql.connect(host='localhost',
					user='root',
					password='1q2w3e4r',
					db='weather',
					cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:
		try:
			cursor.execute("select now()")
			last_updated = cursor.fetchone()[0]
			cursor.execute("SELECT count(*) FROM weather.countries where name = %s" , country_name)
	        	count_country = cursor.fetchone()[0]
	                if count_country == 0:
				cursor.execute("insert into countries (name, initials,last_updated) values (%s, %s, %s)" , (country_name, country_initials,last_updated))

			cursor.execute("insert into cities (name, temprature, humidity, pressure, temprature_min, temprature_max, country_initials,last_updated) values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update last_updated = values(last_updated);" , (city, temp, humidity, pressure, temp_min, temp_max, country_initials, last_updated))
				
	
	        except UnicodeEncodeError:
	                pass
	connection.commit()


def main():
	attempt = 0
	data = None
	while not data and attempt <3:
	        attempt +=1
	        try:
	                request = urllib2.Request('http://openweathermap.org/help/city_list.txt')
			response = urllib2.urlopen(request)
			data = response.readlines()
	        except:
	                print "failed %d times, trying again" % attempt
	if not data:
	        print "the program fail, please check your internt and access the program again"
	        sys.exit()
	country_initials = str()
	firstline = True
	count = 0
	length = list()
	length = len(data)
	bar = Bar('Processing', max = length)
	for line in data:
		#Appending each line that the country initials are equal to the user input
	        if firstline:
			firstline = False
			continue
		count += 1
		if count > 20:
			break
		country_initials = line[-3]+line[-2]
	        elements = line.split()
	        city =  " ".join(elements[1:-3])
		city = city.strip().replace(" ", "-")
		connection = pymysql.connect(host='localhost',
						user='root',
						password='1q2w3e4r',
						db='weather',
						cursorclass=pymysql.cursors.SSCursor)
		with connection.cursor() as cursor:
			try:
				cursor.execute("select count(*) from weather.cities where name = %s" , city) 
				city_exists = cursor.fetchone()[0]
				if city_exists == 1:
					cursor.execute("select TIMESTAMPDIFF(minute,(select last_updated from weather.cities where name = %s), now())" , city)
					time_dif = cursor.fetchone()[0]	
					if time_dif > 60:
						update_attributes(city,country_initials)
						bar.next()
					else:
						bar.next()
						continue
					
				else:
					update_attributes(city,country_initials)
					bar.next()
		        except UnicodeEncodeError:
		                pass
		connection.commit()
	bar.finish()	

##################################################################################################################################
if __name__ == "__main__":
	main()
