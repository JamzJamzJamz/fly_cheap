import requests
import json

def pull_data(origin, departure, date, api_key='oIkAPQAiwHwJc7cUHCblNxkwwm0wqAZM'):
    flights = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey={0}&origin={1}&destination={2}&departure_date={3}'.format(api_key, origin, departure, date))
    json_data = json.loads(flights.text)
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
            flights_list = d[i]['itineraries'][0]['outbound']['flights']
            flight_path = []
            for j, value in enumerate(flights_list):
                    origin = d[i]['itineraries'][0]['outbound']['flights'][j]['origin']['airport']
                    destination = d[i]['itineraries'][0]['outbound']['flights'][j]['destination']['airport']
                    flight_path.append((origin, destination))
            routes.append((flight_num, fare + tax, flight_path))
    return sorted(routes, key=lambda x:x[1])

def main():
    origin = input('Input Initial Location. ')
    departure = input('Input Destination. ')
    date = input('Inpute Departure Date. ')
    result = pull_data(origin, departure, date)
    if result == 'No matching results.':
        print(result)
    else:
        for x in result:
            flight_number, cost, flight_path = x
            if len(flight_path) == 1:
                flight_path = 'Direct Flight'
            else:
                flight_path = ' -> '.join([x[0] for x in flight_path] + [flight_path[-1][1]])
            print('Flight {0:8} {2:40} ${1:.2f}'.format(flight_number, cost, flight_path))

if __name__ == '__main__':
    main()
