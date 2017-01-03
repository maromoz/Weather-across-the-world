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
import MySQLdb
import pymysql.cursors

parser = OptionParser(usage="Weather forecast software",
                      description="Welcome to Weather across the world, please choose and option:\n to select a country please type -c or --country and then your counrty name, if you wish to know the average weather information in your country type -a or --average after the -c of before the -c")

parser.add_option("-a", "--average",
                  action="store_true", default=False, dest="average",
                  help="This option will print the average temprature information of the choosen country")

parser.add_option("-c", "--country",
                  action="store", type="string", dest="country",
                  help="This option will print all the cities inside the choosen country")

parser.parse_args()

options, args = parser.parse_args()


#######################################################################################################
def city_temprature(country):
    # Checking for the user's input type(should be a country name)
    if not country.isalpha():
        print "You typed wrong please run the program try again"
        sys.exit()
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='weather',
                                 cursorclass=pymysql.cursors.SSCursor)
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "select cities.name from cities inner join countries on cities.country_initials = countries.initials where countries.name = %s",
                country)
            cities_list = cursor.fetchall()
            cities_list = list(cities_list)

        except UnicodeEncodeError:
            pass
    connection.commit()
    i = 1
    for city in cities_list:
        if is_average == False:
            print i, city[0]
            # Printing each city of the country with a number for the user to choose from
        i += 1

    # Checking the user internet connection
    user_choice = raw_input("Please type the nubmer of city you would like to check the weather: ")
    # Checking if the user's input is an interger and that the same interger is next to a city above and not equal to 0
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
                city = city[0]
                break
            except IndexError:
                print "the number you typed is unsuitable, please try again"
                user_choice = raw_input()
                continue
        else:
            print "you need to type a number, please try again"
            user_choice = raw_input()
            continue

    # Taking the city that the user choose and checking all the weather attributes in the DB
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='weather',
                                 cursorclass=pymysql.cursors.SSCursor)
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "select temprature, pressure, humidity,  temprature_min, temprature_max from cities where name = %s",
                city)

            weather = cursor.fetchone()
            temp = weather[0]
            pressure = weather[1]
            humidity = weather[2]
            temp_min = weather[3]
            temp_max = weather[4]

            print "The current temprature in " + city + " is " + str(round(temp, 1)) + "°C"
            print "The current pressure in " + city + " is " + str(round(pressure, 1))
            print "The current humidity in " + city + " is " + str(round(humidity, 1))
            print "The current minimum temprature in " + city + " is " + str(round(temp_min, 1)) + "°C"
            print "The current maximum temprature in " + city + " is " + str(round(temp_max, 1)) + "°C"

        except UnicodeEncodeError:
            pass
    connection.commit()


def country_average_temprature(country):
    # Checking for the user's input type(should be a country name)
    if not country.isalpha():
        print "You typed wrong please run the program try again"
        sys.exit()

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='weather',
                                 cursorclass=pymysql.cursors.SSCursor)
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "select avg(temprature), avg(pressure),avg(humidity),avg(temprature_min),avg(temprature_min) from countries inner join cities on countries.initials = cities.country_initials where countries.name = %s",
                country)
            average_weather = cursor.fetchone()
            temp_average = average_weather[0]
            pressure_average = average_weather[1]
            humidity_average = average_weather[2]
            temp_min_average = average_weather[3]
            temp_max_average = average_weather[4]

            print "The average temprature in " + country + " is " + str(round(temp_average, 1)) + "°C"
            print "The average pressure in " + country + " is " + str(round(pressure_average, 1))
            print "The average humidity in " + country + " is " + str(round(humidity_average, 1))
            print "The average minimum temprature in " + country + " is " + str(round(temp_min_average, 1)) + "°C"
            print "The average maximum temprature in " + country + " is " + str(round(temp_max_average, 1)) + "°C"

        except UnicodeEncodeError:
            pass
    connection.commit()


################################################################################################################################


is_average = parser.values.average
country = options.country
if is_average:
    country_average_temprature(country)
else:
    city_temprature(country)
sys.exit()
