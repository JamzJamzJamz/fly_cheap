from flask import Flask, request, render_template
import fly_cheap

app = Flask(__name__)

@app.route('/')
def form():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def form_update():
	if request.method == 'POST':
		departure = request.form['dept']
		destination = request.form['dest']
		date = request.form['day']
		flights = fly_cheap.find_flights(departure, destination, date)
		if flights != 'Invalid Starting Location.' and flights != 'Invalid Destination.' and flights != 'No matching results.':
			flights = '\n'.join(flights)
		return render_template('index.html', flights = flights)

if __name__ == '__main__':
    app.run(debug=True)