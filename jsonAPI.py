import requests
import json

def pull_data():
  #using my api key
  #need to format the url
  #need to also navigate the dictionary created
	flights = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey=oIkAPQAiwHwJc7cUHCblNxkwwm0wqAZM&origin=BOS&destination=LON&departure_date=2018-12-25')

	json_data = json.loads(flights.text)

	print(json_data)

	return json_data

pull_data()	
