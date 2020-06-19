#!/usr/bin/python
# Jeremy Bridges
# CS 340
# 4/14/2020
# CS 499
# updated 6/2/2020

import json
from bson import json_util
import bottle
from bottle import request, route
import datetime
from pymongo import MongoClient

# connect to database and collection
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']


# setup URI paths for create stock REST service
# uses json from POST to create a new document in stocks collection
@bottle.route('/stocks/api/v1.0/createStock/', method='POST')
def add_document():
    data = request.forms.get('data')
    stock = request.forms.get("ticker")
    if not data:
        bottle.abort(400, 'No Data Received')
    entity = json.loads(data)
    ticker = {"Ticker": stock}
    entity.update(ticker)
    print(entity)
    try:
        collection.insert_one(entity)
    except:
        bottle.abort(400, 'Unable to add document')
    return json.loads(json.dumps(entity, indent=4, default=json_util.default))


# setup URI paths for get stock REST service
# queries one document by ticker symbol and returns json document
@bottle.route('/stocks/api/v1.0/getStock/', method='GET')
def get_document():
    stock = bottle.request.query.ticker
    cursor = collection.find_one({'Ticker': stock})
    if not cursor:
        bottle.abort(404, 'No stock found')
    return json.loads(json.dumps(cursor, indent=4, default=json_util.default))


# setup URI paths for updating document REST service
# queries document by ticker symbol and updates parameters from curl PUT command
@bottle.route('/stocks/api/v1.0/updateStock/', method=['POST'])
def update_document():
    ticker = request.forms.get('ticker')
    field = request.forms.get('field')
#    value = request.forms.get('value')
    if not field:
        bottle.abort(400, 'No Data Received')
    entity = json.loads(field)
    cursor = collection.update_one({'Ticker': ticker}, {"$set": entity})
    if not cursor:
        bottle.abort(404, 'No document found')
    return "{0} is has been updated with {1}\n".format(ticker, entity)


# setup URI paths for delete REST service
# deletes document queried by ticker symbol
@bottle.route('/stocks/api/v1.0/deleteStock/', method=['POST'])
def delete_document():
    ticker = request.forms.get('ticker')
    cursor = collection.remove({'Ticker': ticker})
    if not cursor:
        bottle.abort(404, 'No document found')
    return "{0} is now removed\n".format(ticker)


if __name__ == '__main__':
    # app.run(debug=True)
    bottle.run(reloader=True, host='localhost', port=8080)
