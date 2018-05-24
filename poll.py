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
    global token, dbUrl, dbUsername, dbPassword
    global errorColor, alertColor, questionColor
    
    d = json.load( open('config.json') )
    
    token = d["security"]["token"]
    dbUrl = d["database"]["url"]
    dbUsername = d["database"]["user"]
    dbPassword = d["database"]["password"]
    errorColor = d["colors"]["error"]
    alertColor = d["colors"]["alert"]
    questionColor = d["colors"]["question"]
    


def getHelp():
    """
    Retrieve help from the help.txt file and return
    """
    return open('help.txt').read()
    

def createReponseObject( response_type_val, text_content, attachement_content, status_number ):
    """
    """
    if len( attachement_content ) > 0:
        data = {
            "response_type": response_type_val,
            "text": text_content,
            "attachments" : [ attachement_content ]
        }
    else:
        data = {
            "response_type": response_type_val,
            "text": text_content
        }

    responseObj = app.response_class(
        response = json.dumps( data ),
        status = status_number,
        mimetype = 'application/json'
    )
    return responseObj



def getChannelId(channel_display_name):
    """
    TODO: Implement this...
    """
    return channel_id


def createPoll(question, answers, channel):
    """
    """
    answer_arr = answers.split("/")
    answer_str = "[" + answers.replace("/","] [") + "]"
        
    message = "You want to publish a poll for all users in [Team/Channel] that asks:\n" + \
              "* " + question + "\n" + \
              "\n" + \
              "And has the following possible answers:\n" + \
              "* " + answer_str + "\n" \
              "\n" + \
              "To publish the poll please enter: ``/direct-poll publish|[poll-id]``\n" + \
              "To cancel the poll please enter: ``/direct-poll cancel|[poll-id]``\n"
              
    
    reponse_dict = { 
        "color": questionColor, 
        "text": message #json.dumps( message )
    }
    
    return reponse_dict


def handleActions( form_data ):
    """
    """
    response_type = "ephemeral"
    text_value = ""
    
    paramstring = form_data["text"]
    token_sent = form_data["token"]
    channel_id = form_data["channel_id"]
    channel_name = form_data["channel_name"]
    team_id = form_data["team_id"]
    user_id = form_data["user_id"]
    user_name = form_data["user_name"]
    
    params = paramstring.split("|") 
    
    if params[0] == "create":
        attachment_dict = createPoll( params[1], params[2], "" )
    elif params[0] == "publish":
        attachment_dict = { "color": errorColor, "text": "Error: The " + params[0] + " command has not yet been implemented." }
    elif params[0] == "cancel":
        attachment_dict = { "color": errorColor, "text": "Error: The " + params[0] + " command has not yet been implemented." }
    elif params[0] == "view":
        attachment_dict = { "color": errorColor, "text": "Error: The " + params[0] + " command has not yet been implemented." }
    elif params[0] == "close":
        attachment_dict = { "color": errorColor, "text": "Error: The " + params[0] + " command has not yet been implemented." }
    else:
        attachment_dict = { "color": errorColor, "text": "Error: The " + params[0] + " command does not exist." }
    
    return createReponseObject( response_type, text_value, attachment_dict, 200 )


def getPolls():
    return createReponseObject( "ephemeral", "Polls go here...", "", 200 )

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
        return createReponseObject("ephemeral", "Bad Request", "", 400)
    
    if token <> request.form["token"]:
        #The token in config.json must match the token sent
        return createReponseObject("ephemeral", "Access Denied", "", 403)
    
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
    return createReponseObject( "ephemeral", getHelp(), "", 200 )
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5005, debug = False)
