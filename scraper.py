#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests
import urllib.request

def price(string):
    return string[string.find('$') + 1:]

def create_url(start, end, date, children=0, adults=1, seniors=0):
    start = '%20'.join(start.split(' '))
    end = '%20'.join(end.split(' '))
    url = 'https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0}(NYC-All%20Airports),to:{1},departure:{2}TANYT&passengers=children:{3},adults:{4},seniors:{5},infantinlap:Y&mode=search'.format(start, end, date, children, adults, seniors)
    return url

def parse_page(start, end, date, children=0, adults=1, seniors=0):
    url = create_url(start, end, date, children, adults, seniors)
    page = urllib.request.urlopen(url)
    soup = bs(page.read(), 'html.parser')
    departure_times = [html.text.replace('\n', '').replace(' ','') for html in soup.find_all('span', {'data-test-id': 'departure-time'})]
    arrival_times = [html.text for html in soup.find_all('span', {'data-test-id': 'arrival-time'})]
    durations = [html.text.replace('\n', '').replace(' ','')  for html in soup.find_all('span', {'data-test-id': 'duration'})]
    num_stops = [html.text.replace('\n', '').replace(' ','')  for html in soup.find_all('span', {'data-test-num-stops': '0'})]
    #seats_left = soup.find_all('span', {'class': 'primary-sub-content', 'data-test-id': 'seats-left'})
    prices = [price(html.text) for html in soup.find_all('h3', {'class': 'visuallyhidden', 'data-test-id': 'result-header'})]
    #print(departure_times, arrival_times, durations, num_stops, prices)
    return zip(departure_times, arrival_times, durations, num_stops, prices)
            

for x in parse_page('new york city, ny', 'miami, florida', '12/01/2018'):
    print(x)
