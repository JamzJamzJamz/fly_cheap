#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests

def create_url(start, end, date, children=0, adults=1, seniors=0):
    start = '%20'.join(start.split(' '))
    end = '%20'.join(end.split(' '))
    url = 'https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0}(NYC-All%20Airports),to:{1},departure:{2}TANYT&passengers=children:{3},adults:{4},seniors:{5},infantinlap:Y&mode=search'.format(start, end, date, children, adults, seniors)
    return url

def parse_page(start, end, date, children=0, adults=1, seniors=0):
        page = requests.get(create_url(start, end, date, children, adults, seniors))
        soup = bs(page.content, 'html.parser')
        departure_times = soup.find_all('span', {'data-test-id': 'departure-time'})
        arrival_times = soup.find_all('span', {'data-test-id': 'arrival-time'})
        duration = soup.find_all('span', {'data-test-id': 'duration'})
        num_stops = soup.find_all('span', {'data-test-num-stops': '0'})
        seats_left = soup.find_all('span', {'class': 'primary-sub-content', 'data-test-id': 'seats-left'})
        price = soup.find_all('span', {'data-test-id': 'listing-price-dollars'})
        print(departure_times, arrival_times, duration, num_stops, seats_left, price)
        return zip(departure_times, arrival_times, duration, num_stops, seats_left, price)
            

parse_page('new york city, ny', 'miami, florida', '12/01/2018')
