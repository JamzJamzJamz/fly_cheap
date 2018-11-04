from flask import Flask, request, render_template
import fly_cheap

app = Flask(__name__)

@app.route('/')
def form():
	#flights = '\n'.join(fly_cheap.find_flights('HOU','AUS','2018-12-01'))
	return render_template('index.html')

@app.route('/', methods=['POST'])
def form_update():
	if request.method == 'POST':
		departure = request.form['dept']
		destination = request.form['dest']
		date = request.form['day']

		flights = '\n'.join(fly_cheap.find_flights(departure, destination, date))
		return render_template('index.html', flights = flights)
'''
@app.route('/', methods=['POST'])
def handle_data():
	if request.method == 'POST':
    	departure = request.form["dept"]
    	arrival = request.form["dest"]
    	date = request.form["day"]
    	print('{0} {1} {2}'.format(departure, arrival, date))
    return departure
'''

'''
@app.route('/')
def show_data():
    flights = json_api.find_flights(departure,arrival,date)
    print(flights)
'''

if __name__ == '__main__':
    app.run(debug=True)