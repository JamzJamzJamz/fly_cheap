import requests
import json

def pull_data(origin, departure, date, api_key='oIkAPQAiwHwJc7cUHCblNxkwwm0wqAZM'):
        flights = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey={0}&origin={1}&destination={2}&departure_date={3}'.format(api_key, origin, departure, date))
        json_data = json.loads(flights.text)
	#print(json_data)
        if 'results' in json_data:
                d = json_data['results']
        else:
                return 'No matching results.'
        routes = []
        for i, result in enumerate(d):
                fare = float(d[i]['fare']['price_per_adult']['total_fare'])
                tax = float(d[i]['fare']['price_per_adult']['tax'])
                flight_num = d[i]['itineraries'][0]['outbound']['flights'][0]['flight_number']
                airline = d[i]['itineraries'][0]['outbound']['flights'][0]['marketing_airline']
                num_of_flights = d[i]['itineraries'][0]['outbound']['flights']
                flight_path = []
                for j, value in enumerate(num_of_flights):
                	origin = d[i]['itineraries'][0]['outbound']['flights'][j]['origin']['airport']
                	destination = d[i]['itineraries'][0]['outbound']['flights'][j]['destination']['airport']
                	flight_path.append((origin, destination))
                #print(flight_path)
                print("Flight {0}: ${1: .2f} Number of Flights: {2} Flight Path: {3}".format(flight_num, fare+tax, len(num_of_flights), flight_path))
                routes.append((flight_num, fare + tax))
        return sorted(routes, key=lambda x:x[1])

pull_data('IAH', 'LDE', '2018-11-20')
