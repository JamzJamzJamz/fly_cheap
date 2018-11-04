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
                routes.append((flight_num, fare + tax))
        return sorted(routes, key=lambda x:x[1])

#pull_data('HOU', 'AUS', '2018-11-10')

def main():
        origin = input('Input starting location. ')
        departure = input('Input destination. ')
        date = input('Inpute desired travel date. ')
        for flight_num, total_cost in pull_data(origin, departure, date):
                print('Flight {0}: ${1}'.format(flight_num, total_cost))

if __name__ == '__main__':
        main()
