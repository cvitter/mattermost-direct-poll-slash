from flask import Flask
from flask import request
import json
import requests

from database_functions import createPollRecord, createPollResultRecord, cancelPollRecord

__doc__ = """\
poll.py

"""


def readConfig():
    """
    Read the config.json file and populate global variables
    """
    global token, dbUrl, dbName, dbUsername, dbPassword
    global errorColor, alertColor, successColor
    
    d = json.load( open('config.json') )
    token = d["security"]["token"]
    dbUrl = d["database"]["url"]
    dbName = d["database"]["database"]
    dbUsername = d["database"]["user"]
    dbPassword = d["database"]["password"]
    errorColor = d["colors"]["error"]
    alertColor = d["colors"]["alert"]
    successColor = d["colors"]["success"]
    


def getHelp():
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


def createPoll( team_id, channel_id, token, user_id, user_name, 
                question, answers, channel_to_poll_id ):
    """
    """
    outColor = successColor
    answer_arr = answers.split("/")
    answer_str = "[" + answers.replace("/","] [") + "]"
    
    poll_id = createPollRecord( dbUrl, dbUsername, dbPassword, dbName, 
                            team_id, channel_id, token, user_id, user_name, question, answers, channel_to_poll_id )
    
    if poll_id > 0:
        for answer in answer_arr:
            poll_result_id = createPollResultRecord( dbUrl, dbUsername, dbPassword, dbName, poll_id, answer )
    
        message = "You want to publish a poll for all users in [Team/Channel] that asks:\n" + \
              "* " + question + "\n" + \
              "\n" + \
              "And has the following possible answers:\n" + \
              "* " + answer_str + "\n" \
              "\n" + \
              "To publish the poll please enter: ``/direct-poll publish|" + str( poll_id ) + "``\n" + \
              "To cancel the poll please enter: ``/direct-poll cancel|" + str( poll_id ) + "``\n"
    else:
        outColor = errorColor
        message = "**Error**: Your poll could not be created." 
    
    reponse_dict = { 
        "color": outColor, 
        "text": message
    }
    return reponse_dict


def cancelPoll( poll_id ):
    rows_deleted = cancelPollRecord( dbUrl, dbUsername, dbPassword, dbName, poll_id )
    
    if rows_deleted > 0:
        reponse_dict = { 
            "color": successColor, 
            "text": "Poll " + poll_id + " has been canceled."
        }
    else:
        reponse_dict = { 
            "color": errorColor, 
            "text": "Poll " + poll_id + " could not canceled."
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
        if len(params) == 4:
            """
            Check whether this is channel specific or not
            """
            poll_channel = ""
            if params[3].lower() == "yes":
                channel_to_poll = channel_id
                
            attachment_dict = createPoll( team_id, channel_id, token_sent, user_id, user_name,
                                          params[1], params[2], channel_to_poll )
        else:
            attachment_dict = createPoll( team_id, channel_id, token_sent, user_id, user_name,
                                          params[1], params[2], "" )
            
    elif params[0] == "publish":
        attachment_dict = { "color": errorColor, "text": "**Error**: The " + params[0] + " command has not yet been implemented." }
    elif params[0] == "cancel":
        attachment_dict = cancelPoll( params[1] )
    elif params[0] == "view":
        attachment_dict = { "color": errorColor, "text": "**Error**: The " + params[0] + " command has not yet been implemented." }
    elif params[0] == "close":
        attachment_dict = { "color": errorColor, "text": "**Error**: The " + params[0] + " command has not yet been implemented." }
    else:
        attachment_dict = { "color": errorColor, "text": "**Error**: The " + params[0] + " command does not exist." }
    
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
