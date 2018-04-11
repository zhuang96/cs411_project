import json
import requests
import urllib
from flask import *

app = Flask(__name__)
exportStops=""
# displays web form
@app.route('/', methods=['GET'])
def index():
	return render_template('route.html')

# when request for stop list is sent
@app.route('/stops', methods=['POST','GET'])
def sendStops():
	# exportStops=["Dudley Station", "Washington St opp Ruggles St", "Washington St @ Melnea Cass Blvd", "Melnea Cass Blvd @ Harrison Ave", "Albany St opp Randall St", "Massachusetts Ave @ Albany St", "Massachusetts Ave @ Harrison Ave", "Massachusetts Ave @ Washington St", "Massachusetts Ave @ Tremont St", "Massachusetts Ave @ Columbus Ave", "Massachusetts Ave.", "Massachusetts Ave @ St Botolph St", "Massachusetts Ave @ Clearway St", "Hynes Convention Center", "Massachusetts Ave @ Beacon St", "Massachusetts Ave @ Memorial Dr", "77 Massachusetts Ave", "Massachusetts Ave @ Albany St", "Massachusetts Ave @ Sidney St", "Massachusetts Ave @ Prospect St", "Massachusetts Ave @ Bigelow St", "Massachusetts Ave @ Hancock St", "Massachusetts Ave @ Dana St", "Massachusetts Ave @ Trowbridge St", "Massachusetts Ave @ Bow St", "Massachusetts Ave @ Holyoke St", "Massachusetts Ave @ Johnston Gate", "Quincy St @ Broadway opp Fogg Museum", "Quincy St @ Harvard St", "Mt Auburn St @ DeWolfe St", "Mt Auburn St @ Putnam Ave", "Massachusetts Ave @ Bay St", "Massachusetts Ave @ Hancock St", "Massachusetts Ave @ Pleasant St", "Massachusetts Ave @ Pearl St", "Massachusetts Ave @ Sidney St", "Massachusetts Ave @ Albany St", "84 Massachusetts Ave", "Massachusetts Ave @ Marlborough St", "Massachusetts Ave opp Christian Science Ctr", "Massachusetts Ave @ Huntington Ave", "Massachusetts Ave @ Columbus Ave", "Massachusetts Ave @ Tremont St", "Massachusetts Ave @ Washington St", "Massachusetts Ave @ Harrison Ave", "Massachusetts Ave @ Albany St", "Albany St @ Randall St", "Melnea Cass Blvd @ Harrison Ave", "Washington St @ Williams St", "Washington St @ Ruggles St"]
	if request.method == 'POST':
		# load and get Route & Direction
		jsonFront = request.get_json()
		# jsonFront = render_template('route.html',fc=json)
		json.dumps(jsonFront)
		route = jsonFront["route"]
		direction = jsonFront["direction"]
		# route = "Red"#jsonFront["route"]
		# direction = "Southbound"#jsonFront["direction"]

		# load and get all stops for route
		stopsURL = "https://api-v3.mbta.com/stops?filter%5Broute%5D="+str(route)
		stopsDATA = urllib.urlopen(stopsURL)
		stopsJSON = json.loads(stopsDATA.read())

		# filter out stops for route in direction
		stopsList = getStops(stopsJSON)
		returnStops = getOrder(stopsList, direction)
		# create and export JSON of stops for route in direction
		global exportStops
		exportStops = json.dumps(returnStops)
		return Response(json.dumps(exportStops), mimetype='application/json')
		# return render_template('route.html',exportStops=exportStops)
		# sendback= request.args.get('name', "stop", type=str)
		# return jsonify(result=exportStops)
	print("ELSE")
	print(exportStops)
	return Response(json.dumps(exportStops), mimetype='application/json')
	# return render_template('route.html',user=user)
# when request for stop prediction is sent
@app.route('/prediction', methods=['POST'])
# @app.route('/', methods=['POST','GET'])
def sendPredictions():

	# load and get Stop, Route, & Direction
	jsonFront = request.get_json()
	stop = jsonFront["stop"]
	route = jsonFront["route"]
	direction = jsonFront["direction"]

	# WIP
	predictionURL = "https://api-v3.mbta.com/predictions?filter[route]={}".format(stop)
	predictionDATA = urllib.urlopen(predictionURL)
	predictionJSON= json.loads(predictionDATA.read())

	# WIP
	prediction = predictionJSON["stop"]

	# WIP
	exportPrediction = json.dumps(prediction)
	return exportPrediction

# create list of stop names
def getStops(stopsJSON):
	stopsList = []
	for i in range(len(stopsJSON["data"])):
		data = stopsJSON["data"][i]["attributes"]["name"]
		stopsList.append(data)
	return stopsList

# determine order of 'stopsList'
def getOrder(stopsList, direction):
	zero = ["Outbound","Southbound","Westbound","South Station"]
	one = ["Inbound","Northbound","Eastbound","TF Green Airport"]
	if direction in zero:
		return stopsList
	if direction in one:
		return stopsList[::-1]

if __name__ == '__main__':
    app.run(debug=True)