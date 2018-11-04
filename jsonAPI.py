import requests
import json

def pull_data():
	flights = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey=oIkAPQAiwHwJc7cUHCblNxkwwm0wqAZM&origin=HOU&destination=AUS&departure_date=2018-11-10')

	json_data = json.loads(flights.text)

	#print(json_data)
	d = json_data['results']
	for i, result in enumerate(d):
		fare = float(d[i]['fare']['price_per_adult']['total_fare'])
		tax = float(d[i]['fare']['price_per_adult']['tax'])
		flight_num = d[i]['itineraries'][0]['outbound']['flights'][0]['flight_number']
		print('Total Price: {0:.2f} Flight Number: {1}'.format(fare+tax, flight_num))
	return json_data

pull_data()
