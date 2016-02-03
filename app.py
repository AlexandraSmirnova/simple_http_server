__author__ = 'AlexSmirnova'

from flask import Flask, request, abort
import json
from datetime import datetime
app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5000

data = {}


# curl -X GET http://0.0.0.0:5000/dictionary/testkey
@app.route('/dictionary/<key>', methods=['GET'])
def get_value(key = None):		
	if data.get(key) == None:			
		abort(404)
	return json.dumps({"result" : data[key], "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})


#curl -X PUT -H "Content-Type: application/json" -d '{"value": "newvalue"}' http://localhost:5000/dictionary/testkey
@app.route('/dictionary/<key>', methods=['PUT'])
def change_value(key = None):			
	if data.get(key) == None:			
		abort(404)
	content = request.json
	required_data = ["value"]        
	check_data(content, required_data)		
	data[key] = content["value"]	
	return json.dumps({"result" : 200, "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})


#curl -X POST -H "Content-Type: application/json" -d '{"key": "testkey", "value": "somevalue"}' http://localhost:5000/dictionary
@app.route('/dictionary', methods=['POST'])
def add_value():
	content = request.json
	required_data = ["key", "value"]        
	check_data(content, required_data)
	if data.get(content["key"]) != None:
		abort(409)
	data[content["key"]] = content["value"]
	return json.dumps({"result" : 200, "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})


# curl -X DELETE http://0.0.0.0:5000/dictionary/testkey
@app.route('/dictionary/<key>', methods=['DELETE'])
def delete_value(key = None):
	if data.get(key) != None:
		data.pop(key)
	return json.dumps({"result" : 200, "time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")})


# for checking json data
def check_data(data, required):
	for el in required:
		if el not in data:
			abort(400)         
	return

if __name__ == "__main__":  
	app.run(host = HOST, port = PORT)