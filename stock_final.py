# Jeremy Bridges
# 4/14/20
# CS 340
# final project

import json
import datetime
from pip._vendor.distlib.compat import raw_input
from pymongo import MongoClient
from bottle import abort


# connect to database and collection
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']


# function to add documents to collection
def insert_document(document):
    if collection.count(document) == 0:
        try:
            result = collection.insert(document)
            print("Document added")
            return result
        except:
            abort(400, "Validation Error")
    else:
        print("Document already exists, try Update")
        return


# function to read documents found in range
def find_document_by50(min, max):
    try:
        item_count = collection.count_documents({"50-Day Simple Moving Average": {"$lt": float(max), "$gt": float(min)}})
        if item_count != 0:
            print('Item count is: ', item_count)
        else:
            print("Could not find document")
    except:
        print("Documents not found")
    return


# function to read documents found by industry
def find_document_industry(industry):
    try:
        cursor = collection.find({"Industry": industry}, {"_id": 0, "Ticker": 1})
        item_count = collection.count_documents({"Industry": industry})
        print("items found ", item_count)
        if item_count != 0:
            for item in cursor:
                print(item)
        else:
            print("Could not find document")
    except:
        print("READ DOC ERROR")
    return


# function to update volume field using ticker symbol to find documents
def update_document(document):
    try:
        cursor = collection.find(document)
        item_count = collection.count(document)
        if item_count != 0:
            key_field = "Volume"
            int_key_value = 0;
            while int_key_value <= 0:
                int_key_value = int(raw_input("Enter " + key_field + " value: "))
            key_value = str(int_key_value)
            result = collection.update_one(document, {"$set": {key_field: key_value}})
            print(key_field + " data updated with " + key_value)
        else:
            print("Could not find document")
    except:
        print("UPDATE DOC ERROR")
    return


# function to delete document by ticker symbol
def delete_document(document):
    try:
        x = collection.delete_many(document)
        if x.deleted_count == 0:
            print("No documents found")
        else:
            print(x.deleted_count, "Document deleted")
    except:
        print("DELETE DOC ERROR")


def main():
    # simple menu
    menu = {}
    menu['1'] = "Add Document"
    menu['2'] = "Read Document"
    menu['3'] = "Update Document"
    menu['4'] = "Delete Document"
    menu['5'] = "Aggregate"
    menu['6'] = "Exit"
    while True:
        options = menu.keys()
#        options.sorted()
        print(" ")
        for entry in options:
            print(entry, menu[entry])
        selection = raw_input("Please Select:")
        # Option 1 to add document from file or inline curl POST
        if selection == '1':
            menuexit = '0'
            while menuexit == '0':
                print('ADD')
                addOption = raw_input("1 for file import, 2 for manual entry, 0 to exit. ")
                if addOption == '1':
                    with open('sample.json', 'r') as f:
                        myDocument = json.load(f)
                        print(myDocument)
                        menuexit = '1'
                elif addOption == '2':
                    print("Please enter business information")
                    myDocument = raw_input('Enter data in JSON format: ')
                    print(myDocument)
                    menuexit = raw_input("if this is correct, enter 1. or enter 0 to re-enter.")
                else:
                    menuexit = '0'
                    break
            if menuexit == '1':
                insert_document(myDocument)
            else:
                print("Exiting to Main Menu")
        # Option 2 to find a document by moving average range or by industry
        elif selection == '2':
            print("READ")
            readmenu = '0'
            readmenu = raw_input("1 to search by 50 day moving average range\n2 to search by industry\n")
            if readmenu == '1':
                min = raw_input("Enter minimum value for moving average: ")
                max = raw_input("Enter maximum value for moving average: ")
                find_document_by50(min, max)
            elif readmenu == '2':
                industry = raw_input("Enter Industry: ")
                find_document_industry(industry)
        # Option 3 to update document volume field queried by ticker symbol
        elif selection == '3':
            print("UPDATE")
            myInput = raw_input("Search by Ticker symbol: ")
            myDocument = {"Ticker": myInput}
            update_document(myDocument)
        # Option 4 to delete a document queried by its ticker symbol
        elif selection == '4':
            print("DELETE")
            myInput = raw_input("Search by Ticker symbol: ")
            myDocument = {"Ticker": myInput}
            delete_document(myDocument)
        # Option 5 returns an aggregate pipeline of query by sector, projecting outstanding shares
        # grouped by industry
        elif selection == '5':
            print("Aggregate")
            myInput = raw_input("Enter Sector: ")
            pipeline = [
                {"$match": {"Sector": myInput}},
                {"$group": {"_id": "$Industry", "Total_Shares_Outstanding": {"$sum": "$Shares Outstanding"}}},
                {"$project": {"_id": 1, "Total_Shares_Outstanding": 1}},
                {"$sort": {"_id": 1, "Total_Shares_Outstanding": 1}}
            ]
            cursor = collection.aggregate(pipeline)
            val = list(collection.aggregate(pipeline))
            for item in val:
                print(item)

        elif selection == '6':
            break
        else:
            print("Unknown Option Selected!")


# main function call        
main()
