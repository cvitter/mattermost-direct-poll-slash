from flask import Flask
from flask import request
import json
import requests

__doc__ = """\
jenkins.py

"""

def readConfig():
    """
    Read the config.json file and populate global variables
    """
    # Create global configuration variables
    global dbUrl, dbUsername, dbPassword
    # Load the file contents as JSON
    d = json.load( open('config.json') )
    # Set globals
    dbUrl = d["database"]["url"]
    dbUsername = d["database"]["user"]
    dbPassword = d["database"]["password"]
    

def getHelp():
    """
    Retrieve help from the help.txt file and return
    """
    responseValue = open('help.txt').read()
    return responseValue
    


"""
------------------------------------------------------------------------------------------
Flask application below
"""

readConfig()

app = Flask(__name__)
 
@app.route( "/direct-poll", methods = [ 'POST' ] )
def slashCommand():
    """
    Get the text/body of the slash command sent by the user
    """
    paramstring = ""
    if len(request.form) > 0:
        paramstring = request.form["text"]
    
    response_type = "ephemeral"
    
    output = ""
    if len(paramstring) > 0:
        
       if paramstring.find("|") != -1:
           output = ""
       else:
            if paramstring == "list":
                output = ""
            else:
                output = getHelp()

        
    else:
        output = getHelp()
    
    """
    Create data json object to return to Mattermost with
        response_type = in_channel (everyone sees) or ephemeral (only sender sees)
        text = the message to send
    """
    data = {
        "response_type": response_type,
        "text": output,
    }
    
    """
    Create the response object to send to Mattermost with the
    data object written as json, 200 status, and proper mimetype
    """
    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    return response
 
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5005, debug = False)
