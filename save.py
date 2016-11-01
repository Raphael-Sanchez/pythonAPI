from __future__ import print_function
import httplib2
import os

from flask import Flask
from flask import request
from flask import jsonify

import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


app = Flask(__name__)

# scope = ['https://spreadsheets.google.com/feeds']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-95911cabb342.json', scope)
# sh = gspread.authorize(credentials)
# sheet1 = sh.open_by_key('1KqbZTNpaf2mgGwLzdSDaMuszjEm-PAT5ypijm7-zoAg')

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
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


# 
# ---------- ADD, UPDATE, DELETE ----------- 
# 

users = {}

def checkIsNotEmptyAndString(contactName, enterpriseName, state):
    if not isinstance(contactName, str) or not isinstance(enterpriseName, str) or not isinstance(state, str) or not contactName or not enterpriseName or not state:
        response = False
    else:
        response = True
    
    return response



@app.route("/addUser", methods=['POST'])
def addUser():
    if request.method == 'POST':

        content = request.json

        if checkIsNotEmptyAndString(content['contactName'], content['enterpriseName'], content['state']):
            user = {}
            user = {'contactName':content['contactName'], 'enterpriseName':content['enterpriseName'], 'state':content['state']}
            
            if len(users) == 0:
                users[0] = user
            elif len(users)-1 == 0:
                key = len(users) -1 + 1
                users[1] = user
            else:
                key = len(users) -1 + 1
                users[key] = user

            response = {
              "status": 'success',
              "data": {
                    "user": user
              }
            }

            status = 200

        else:
            
            response = {
                "status" : "error",
                "message" : "Value of user are empty or not a string"
            }

            status = 400

    return json.dumps(response), status



@app.route("/updateUser/<string:user_name>", methods=['PUT'])
def updateUser(user_name):
    if request.method == 'PUT':

        content = request.json
        
        if checkIsNotEmptyAndString(content['contactName'], content['enterpriseName'], content['state']):
            
            userFound = False

            for key in users:
                for index in users[key]:
                    if users[key]['contactName'] == user_name:
                        
                        userFound = True

                        userForUpdate = users[key]

                        userForUpdate['contactName'] = content['contactName']
                        userForUpdate['enterpriseName'] = content['enterpriseName']
                        userForUpdate['state'] = content['state']

                        response = {
                          "status": 'success',
                          "data": {
                                "userUpdated": userForUpdate
                          }
                        }

                        status = 200

                    if userFound == False:
                
                        response = {
                            "status" : "error",
                            "message" : "Username not found in database"
                        }       

                        status = 404

        else:
            
            response = {
                "status" : "error",
                "message" : "Value of user are empty or not a string"
            }

            status = 400


    return json.dumps(response), status




@app.route("/deleteUser/<string:user_name>", methods=['DELETE'])
def deleteUser(user_name):
    if request.method == 'DELETE':

        for key in users:
            for index in users[key]:

                if users[key]['contactName'] == user_name:
                    break
                    del users[key]



            # for index in users[key]:
            #     if users[key]['contactName'] == user_name:
                    

            #     else:
        
            #         response = {
            #             "status" : "error",
            #             "message" : "Bad username, not found"
            #         }

            #         status = 400

        # userDeleted = users[user_id]
        # userDeletedStr = str(userDeleted)

        # del users[user_id]
        
        # response = 'User ID -> ' + str(user_id) + ' deleted : ' + userDeletedStr

        # print("Tableau d'users : ", users)
        response = {
                      "status": 'success',
                      "data": {

                        "users": users

                      }
                }

        status = 200

    return json.dumps(response), status




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

@app.route("/export", methods=['GET'])
def export():
    if request.method == 'GET':

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        value_input_option = 'RAW'
        spreadsheetId = '1KqbZTNpaf2mgGwLzdSDaMuszjEm-PAT5ypijm7-zoAg'
        rangeName = 'A:C'

        values = [
        [
            
        ],
        # Additional rows ...
        ]

        i = 0

        for index in users:
            if i > 0:
                newUser = [users[index]['contactName'], users[index]['enterpriseName'], users[index]['state']]
                values.append(newUser)
            else:
                values[0].append(users[index]['contactName'])
                values[0].append(users[index]['enterpriseName'])
                values[0].append(users[index]['state'])
                i = +1

       
        body = {
          'values': values
        }

        # WRITE VALUES IN SHEET
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range=rangeName,
            valueInputOption=value_input_option, body=body).execute()
        
 
        response = 'Status 200' + json.dumps(values)

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
    # main()
    app.run(debug=True)
