import requests
import json
import csv

def time_format(time):
    hours, minutes = [int(x) for x in time.split(':')]
    days = hours // 24
    if days:
        if days == 1:
            day_string = '1 day'
        else:
            day_string = '{0} days'.format(days)
    else:
        day_string = ''
    if hours:
        if hours == 1:
            hour_string = '1 hour'
        else:
            hour_string = ' {0} hours'.format(hours)
    else:
        hour_string = ''
    if minutes:
        if minutes == 1:
            minute_string = '1 minute'
        else:
            minute_string = ' {0} minutes'.format(minutes)
    else:
        minute_string = ''
    duration = day_string + hour_string + minute_string
    if duration[0] == ' ':
        duration = duration[1:]
    if days == 0 and hours == 0:
        return minute_string[1:]
    else:
        return duration

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
            duration = d[i]['itineraries'][0]['outbound']['duration']
            routes.append((flight_num, fare + tax, flight_path, duration))
    return sorted(routes, key=lambda x:x[1])

def find_flights(origin, departure, date, iata_codes=None):
##    origin = input('Input Initial Location. ')
##    departure = input('Input Destination. ')
##    date = input('Inpute Departure Date. ')
    if iata_codes is None:
        iata_codes = set()
        with open('iata.sql', 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                iata_codes.add(line[1].replace("'", ''))
    if origin not in iata_codes:
        return 'Invalid Starting Location.'
    if departure not in iata_codes:
        return 'Invalid Destination.'
    result = pull_data(origin, departure, date)
    if result == 'No matching results.':
        return result
    else:
        flights = ['Flight {0:8} {2:35} {3:30} {1}'.format('Number', ' Cost', '   Itinerary', '   Duration'), '-' * 100]
        for x in result:
            flight_number, cost, flight_path, duration = x
            duration = time_format(duration)
            if len(flight_path) == 1:
                flight_path = 'Direct Flight'
            else:
                flight_path = ' -> '.join([x[0] for x in flight_path] + [flight_path[-1][1]])
            flights.append('Flight {0:8} {2:35} {3:30} ${1:.2f}'.format(flight_number, cost, flight_path, duration))
        return flights

def main(origin, departure, date):
    for flight in find_flights(origin, departure, date):
        print(flight)

if __name__ == '__main__':
    main('IST', 'BOS', '2018-12-01')
