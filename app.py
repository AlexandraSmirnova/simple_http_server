__author__ = 'AlexSmirnova'

from flask import Flask, request, abort
import json
from datetime import datetime
app = Flask(__name__)

data = {
	'hello': 'Hello World!',
	'name': 'My name is Flask Server',
}

@app.route('/dictionary/<key>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/dictionary', methods=['POST'])
def dictionary(key = None):
	if request.method == 'POST':
		content = request.json
		required_data = ["key", "value"]        
		check_data(content, required_data)
		if data.get(content["key"]) != None:
			abort(409)
		data[content["key"]] = content["value"]
	elif request.method == 'GET':
		if data.get(key) == None:			
			abort(404)
		return json.dumps({"result" : data[key], "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})
	elif request.method == 'PUT':
		if data.get(key) == None:			
			abort(404)
		content = request.json
		required_data = ["value"]        
		check_data(content, required_data)		
		data[key] = content["value"]
	elif request.method == 'DELETE':
		if data.get(key) != None:
			data.pop(key)
	return json.dumps({"result" : 200, "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})


def check_data(data, required):
	for el in required:
		if el not in data:
			abort(400)         
	return

if __name__ == "__main__":  
	app.run()
