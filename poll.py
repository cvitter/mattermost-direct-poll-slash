from flask import Flask
from flask import request
import json
import requests
from database_functions import create_poll_record
from database_functions import create_poll_result_record
from database_functions import cancel_poll_record


def read_config():
    """
    Read the config.json file and populate global variables
    """
    global token, db_url, db_name, db_username, db_password
    global error_color, alert_color, success_color

    d = json.load(open('config.json'))
    token = d["security"]["token"]
    db_url = d["database"]["url"]
    db_name = d["database"]["database"]
    db_username = d["database"]["user"]
    db_password = d["database"]["password"]
    error_color = d["colors"]["error"]
    alert_color = d["colors"]["alert"]
    success_color = d["colors"]["success"]


def get_help():
    return open('help.txt').read()


def create_reponse_object(response_type_val, text_content, attachement_content,
                          status_number):
    """
    """
    if len(attachement_content) > 0:
        data = {
            "response_type": response_type_val,
            "text": text_content,
            "attachments": [attachement_content]
        }
    else:
        data = {
            "response_type": response_type_val,
            "text": text_content
        }

    response_obj = app.response_class(
        response=json.dumps(data),
        status=status_number,
        mimetype='application/json'
    )
    return response_obj


def create_poll(team_id, channel_id, token, user_id, user_name,
                question, answers, channel_to_poll_id, channel_name):
    """
    """
    out_color = success_color
    answer_arr = answers.split("/")
    answer_str = "[" + answers.replace("/", "] [") + "]"

    poll_id = create_poll_record(db_url, db_username, db_password, db_name,
                                 team_id, channel_id, token, user_id,
                                 user_name, question, answers,
                                 channel_to_poll_id)

    if poll_id > 0:
        for answer in answer_arr:
            poll_result_id = create_poll_result_record(db_url, db_username,
                                                       db_password, db_name,
                                                       poll_id, answer)

        # Add channel name into message
        channel_to_print = ""
        if len(channel_to_poll_id) > 0:
            channel_to_print = "in " + channel_name + " "

        message = "You want to publish a poll for all users " + \
            channel_to_print + "that asks:\n" + \
            "* " + question + "\n" + \
            "\n" + \
            "And has the following possible answers:\n" + \
            "* " + answer_str + "\n" \
            "\n" + \
            "To publish the poll please enter: ``/direct-poll publish|" + \
            str(poll_id) + "``\n" + \
            "To cancel the poll please enter: ``/direct-poll cancel|" + \
            str(poll_id) + "``\n"
    else:
        out_color = error_eolor
        message = "**Error**: Your poll could not be created."

    reponse_dict = {
        "color": out_color,
        "text": message
    }
    return reponse_dict


def cancel_poll(poll_id):
    rows_deleted = cancel_poll_record(db_url, db_username, db_password,
                                      db_name, poll_id)

    if rows_deleted > 0:
        reponse_dict = {
            "color": success_color,
            "text": "Poll " + poll_id + " has been canceled."
        }
    else:
        reponse_dict = {
            "color": error_color,
            "text": "Poll " + poll_id + " could not be canceled."
        }
    return reponse_dict


def handle_actions(form_data):
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

            attachment_dict = create_poll(team_id, channel_id, token_sent,
                                          user_id, user_name, params[1],
                                          params[2], channel_to_poll,
                                          channel_name)
        else:
            attachment_dict = create_poll(team_id, channel_id, token_sent,
                                          user_id, user_name, params[1],
                                          params[2], "", "")

    elif params[0] == "publish":
        attachment_dict = {"color": error_color, "text": "**Error**: The " +
                           params[0] + " command has not yet been implemented."}
    elif params[0] == "cancel":
        attachment_dict = cancel_poll(params[1])
    elif params[0] == "view":
        attachment_dict = {"color": error_color, "text": "**Error**: The " +
                           params[0] + " command has not yet been implemented."}
    elif params[0] == "close":
        attachment_dict = {"color": error_color, "text": "**Error**: The " +
                           params[0] + " command has not yet been implemented."}
    else:
        attachment_dict = {"color": error_color, "text": "**Error**: The " +
                           params[0] + " command does not exist."}

    return create_reponse_object(response_type, text_value, attachment_dict, 200)


def get_polls():
    return create_reponse_object("ephemeral", "Polls go here...", "", 200)

"""
------------------------------------------------------------------------------------------
Flask application below
"""

read_config()

app = Flask(__name__)


@app.route("/direct-poll", methods=['POST'])
def slash_command():

    if len(request.form) < 1:
        # No data passed in via request.form
        return create_reponse_object("ephemeral", "Bad Request", "", 400)

    if token != request.form["token"]:
        # The token in config.json must match the token sent
        return create_reponse_object("ephemeral", "Access Denied", "", 403)

    if len(request.form["text"]) > 0:
        # User passed arguments in, parse the arguments and take action
        if request.form["text"].find("|") != -1:
            # Multiple arguments separated by | passed in, send action handler
            return handle_actions(request.form)
        else:
            if request.form["text"] == "list":
                return get_polls()

    """
    If we reach this stage simply return the help response to the user
    """
    return create_reponse_object("ephemeral", get_help(), "", 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)
