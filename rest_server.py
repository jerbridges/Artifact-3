#!/usr/bin/python
# Jeremy Bridges
# CS 340
# 4/10/2020

import json
from bson import json_util
import bottle
from bottle import route, run, get, request, abort
import datetime
from pymongo import MongoClient

# connect to database and collection
connection = MongoClient('localhost', 27017)
db = connection['city']
collection = db['inspections']

id = 0
# setup URI paths for REST service
@route('/greeting', method='GET')
def get_greeting():
    global id
    id = id + 1
    try:
      request.query.name
      name=request.query.name
      if name:
        string ="{ \"id\": "+str(id)+", \"content\": \"Hello, \""+request.query.name+"\"}\n"
      else:
        string="{ \"id\": "+str(id)+", \"content\": \"Hello, World!\"}\n"
    except NameError:
      abort(404, 'No Parameter for id %s' % id)

    if not string:
      abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

# set up URI paths for REST service
@route('/currentTime', method='GET')
def get_currentTime():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.datetime.now().strftime("%H:%M:%S")
    string= "{ \"date\": "+dateString+", \"time\": "+timeString+"}\n"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

# setup URI paths for REST service
@route('/hello', method='GET')
def get_hello():
    request.query.name
    name=request.query.name
    if name:
      string="{ \"hello\": \""+request.query.name+"\"}\n"
    else:
      string="{ \"hello\": \"world\"}\n"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

# setup URI paths for REST service
@route('/strings', method='POST')
def add_string():
  string = "{ \"first\": \""+request.json.get("string1")+"\" , \"second\": \""+request.json.get("string2")+"\" }\n"
  return json.loads(json.dumps(string, indent=4, default=json_util.default))

# setup URI paths for REST service
@route('/create', method='POST')
def add_document():
  data = request.body.read()
  if not data:
    abort(400, 'No Data Received')
  entity = json.loads(data)
  try:
    collection.insert(entity)
  except:
    abort(400, str(ve))
  return json.loads(json.dumps(entity, indent=4, default=json_util.default))

# setup URI paths for REST service
@route('/read', method='GET')
def get_document():
  business_name = request.query.business_name
  cursor = collection.find_one({'business_name' : request.query.business_name})
  if not cursor:
    abort(404, 'No doc found')
  return json.loads(json.dumps(cursor, indent=4, default=json_util.default))
 
# setup URI paths for REST service
@route('/update', method=['GET'])
def update_document():
  id = request.query.id
  result = request.query.result
  cursor = collection.update_one({'id' : request.query.id}, {"$set" : {'result' : result}})
  if not cursor:
    abort(404, 'No doc found')
  return "{0} is now {1}\n".format(id,result)

# setup URI paths for REST service
@route('/delete', method=['GET'])
def delete_document():
  id = request.query.id
  cursor = collection.remove({'id' : id})
  if not cursor:
    abort(404, 'No document found')
  return "{0} in now removed\n".format(id)

if __name__ == '__main__':
  #app.run(debug=True)
  run(reloader=True, host='localhost', port=8080)
  
  
