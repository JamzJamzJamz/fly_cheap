from flask import Flask, request, render_template
import json_api

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_data():
    departure = request.form['text']
    arrival = request.form['text']
    date = request.form['text']
    
    return render_template('index.html',departure, arrival, date)
@app.route('/')
def show_data():
    flights = json_api.find_flights(departure,arrival,date)
    print(flights)

if __name__ == '__main__':
    app.run(debug=True)