from __future__ import print_function
import httplib2
import os

from flask import Flask
from flask import request

import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# from oauth2client.service_account import ServiceAccountCredentials
# import gspread

app = Flask(__name__)

# scope = ['https://spreadsheets.google.com/feeds']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-95911cabb342.json', scope)
# sh = gspread.authorize(credentials)
# sheet1 = sh.open_by_key('1KqbZTNpaf2mgGwLzdSDaMuszjEm-PAT5ypijm7-zoAg')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1KqbZTNpaf2mgGwLzdSDaMuszjEm-PAT5ypijm7-zoAg'
    rangeName = 'A1:A2'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)




# 
# ---------- ADD, UPDATE, DELETE ----------- 
# 

users = {}

@app.route("/addUser", methods=['POST'])
def addUser():
    if request.method == 'POST':
        answer = 'POST'

        user = {}
        content = request.json
        user = {'contactName':content['contactName'], 'enterpriseName':content['enterpriseName'], 'state':content['state']}
        
        if len(users) == 0:
            users[0] = user
        elif len(users)-1 == 0:
            key = len(users) -1 + 1
            users[1] = user
        else:
            key = len(users) -1 + 1
            users[key] = user

        response = json.dumps(user)

    return response, 200

@app.route("/updateUser/<int:user_id>", methods=['PUT'])
def updateUser(user_id):
    if request.method == 'PUT':

        userForUpdate = users[user_id]
        content = request.json
        
        userForUpdate['contactName'] = content['contactName']
        userForUpdate['enterpriseName'] = content['enterpriseName']
        userForUpdate['state'] = content['state']
        
        response = json.dumps(users[user_id])

    return response, 200

@app.route("/deleteUser/<int:user_id>", methods=['DELETE'])
def deleteUser(user_id):
    if request.method == 'DELETE':

        userDeleted = users[user_id]
        userDeletedStr = str(userDeleted)

        del users[user_id]
        
        response = 'User ID -> ' + str(user_id) + ' deleted : ' + userDeletedStr

        print("Tableau d'users : ", users)

    return response, 200

# 
# ---------- GETTER ----------- 
# 

@app.route("/getUserByName/<string:user_name>", methods=['GET'])
def getUserByName(user_name):
    if request.method == 'GET':
        getUsersByName = {}
        key = 0

        for key in users:
            for index in users[key]:
                if users[key]['contactName'] == user_name:
                    getUsersByName[key] = {'contactName': users[key]['contactName'], 'enterpriseName': users[key]['enterpriseName'], 'state': users[key]['state']}
                    key = +1
        
        response = 'User get by name ' + str(user_name) + ' : ' + json.dumps(getUsersByName)

    return response, 200

@app.route("/getUserByEnterpriseName/<string:enterprise_name>", methods=['GET'])
def getUserByEnterpriseName(enterprise_name):
    if request.method == 'GET':
        getUsersByEnterpriseName = {}
        key = 0

        for key in users:
            for index in users[key]:
                if users[key]['enterpriseName'] == enterprise_name:
                    getUsersByEnterpriseName[key] = {'contactName': users[key]['contactName'], 'enterpriseName': users[key]['enterpriseName'], 'state': users[key]['state']}
                    key = +1
        
        response = 'Users get by enterprise name ' + str(enterprise_name) + ' : ' + json.dumps(getUsersByEnterpriseName)

    return response, 200

@app.route("/getUserByState/<string:state>", methods=['GET'])
def getUserByState(state):
    if request.method == 'GET':
        getUserByState = {}
        key = 0

        for key in users:
            for index in users[key]:
                if users[key]['state'] == state:
                    getUserByState[key] = {'contactName': users[key]['contactName'], 'enterpriseName': users[key]['enterpriseName'], 'state': users[key]['state']}
                    key = +1
        
        response = 'Users get by state ' + str(state) + ' : ' + json.dumps(getUserByState)

    return response, 200

@app.route("/getUserByParameter/<string:parameter>", methods=['GET'])
def getUserByParameter(parameter):
    if request.method == 'GET':
        getUserByParameter = {}
        key = 0

        for key in users:
            for index in users[key]:
                if users[key]['contactName'] == parameter or users[key]['enterpriseName'] == parameter or users[key]['state'] == parameter:
                    getUserByParameter[key] = {'contactName': users[key]['contactName'], 'enterpriseName': users[key]['enterpriseName'], 'state': users[key]['state']}
                    key = +1
        
        response = 'Users get by parameter ' + str(parameter) + ' : ' + json.dumps(getUserByParameter)

    return response, 200
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
# def addUser():
#
#     print(request.data)
#     print(request.json)
#     print(request.args)
#
#     return "yes"
#     # return flask.jsonify("request ok")

if __name__ == '__main__':
    main()
    app.run(debug=True)
