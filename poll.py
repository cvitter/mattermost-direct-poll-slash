from flask import Flask
from flask import request
import json
import requests

__doc__ = """\
poll.py

"""

def readConfig():
    """
    Read the config.json file and populate global variables
    """
    # Create global configuration variables
    global token, dbUrl, dbUsername, dbPassword
    # Load the file contents as JSON
    d = json.load( open('config.json') )
    # Set globals
    token = d["security"]["token"]
    dbUrl = d["database"]["url"]
    dbUsername = d["database"]["user"]
    dbPassword = d["database"]["password"]
    

def getHelp():
    """
    Retrieve help from the help.txt file and return
    """
    responseValue = open('help.txt').read()
    return responseValue
    

def createReponseObject( response_type_val, content, status_number ):
    """
    Method that takes:
        - response_type_val: ephemeral, in_channel 
        - content: The text to respond with - can be formatted with markdown
        - HTTP response code: 200 normally, 403 access denied, etc.
    And outputs the response object to send back to Mattermost
    """
    data = {
        "response_type": response_type_val,
        "text": content,
    }

    responseObj = app.response_class(
        response = json.dumps( data ),
        status = status_number,
        mimetype = 'application/json'
    )
    return responseObj


def handleActions( form_data ):
    response_type = "ephemeral"
    
    paramstring = form_data["text"]
    token_sent = form_data["token"]
    channel_id = form_data["channel_id"]
    channel_name = form_data["channel_name"]
    team_id = form_data["team_id"]
    user_id = form_data["user_id"]
    user_name = form_data["user_name"]

    return createReponseObject( response_type, "Handle actions called " + user_name, 200 )


def getPolls():
    response_type = "ephemeral"

    return createReponseObject( response_type, "Polls go here...", 200 )

"""
------------------------------------------------------------------------------------------
Flask application below
"""

readConfig()

app = Flask(__name__)
 
@app.route( "/direct-poll", methods = [ 'POST' ] )
def slashCommand():
    
    if len( request.form ) < 1:
        # No data passed in via request.form
        return createReponseObject("ephemeral", "Bad Request", 400)
    
    if token <> request.form["token"]:
        #The token in config.json must match the token sent
        return createReponseObject("ephemeral", "Access Denied", 403)
    
    if len( request.form["text"] ) > 0:
        # User passed arguments in, parse the arguments and take action
        if request.form["text"].find( "|" ) != -1:
           # Multiple arguments separated by | passed in, send action handler
           return handleActions( request.form )
        else:
            if request.form["text"] == "list":
                return getPolls()

    """
    If we reach this stage simply return the help response to the user
    """
    return createReponseObject( "ephemeral", getHelp(), 200 )
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5005, debug = False)
