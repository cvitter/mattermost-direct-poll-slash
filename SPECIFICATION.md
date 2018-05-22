# Specification/Use Case

The following is an overview of the planned functionality of this integration:

* [Getting Help with the Slash Command](#getting-help-with-the-slash-command)
* [Creating and Publishing a Poll](#creating-and-publishing-a-poll)
* [Responding to a Poll](#responding-to-a-poll)
* [Viewing a List of All Polls](#viewing-a-list-of-all-polls)
* [Viewing the Results of a Poll](#viewing-the-results-of-a-poll)
* [Closing a Poll](#closing-a-poll)

# Getting Help with the Slash Command

Markdown formatted help for the slash command is available by executing the ``/direct-poll`` command without arguments.

# Creating and Publishing a Poll

1. A user creates a poll using the ``direct-poll`` slash command:

   ```
   /direct-poll create|Have you completed your monthly HR training yet?|Yes/No/Maybe
   ```
   or
   ```
   /direct-poll create|Have you completed your monthly HR training yet?|Yes/No/Maybe|Channel Name
   ```
   The slash commands takes four arguments separated by the pipe character (``|``): The command to execute (``create``), the question, possible answers (separated by the forward slash character (``/``), and optionally the name of the channel to poll users from if you don't wish to poll the entire team.

2. The system creates a database record in the ``poll`` table with the following fields: ``poll_id, created, team_id, channel_id, token, user_id, user_name, question, answers, channel_to_poll_id, published, closed``.

3. The system returns an ephemeral with interactive message buttons asking the user to confirm that they wish to run the poll that they created:

   ```
   You want to publish a poll for all uses in [Team/Channel] that asks:
   
   [Question]
   
   and has the following possible answers:
   
   [Answer], [Answer], ...
   
   If that is correct please push the Yes button. If you need to change 
   the poll or do not wish to publish it please click the No button 
   and start again.
   ```
   
4. If the user selects ``No`` the system deletes the record in the ``poll`` table created in ``Step 2`` above and returns an ephemeral message alerting the user that the poll has been canceled.

   ```
   Alert: The poll has been canceled.
   ```

5. If the user selects ``Yes`` the system:

   a. Creates a record for each answer in the poll in the ``poll_result`` table with the following fields: ``poll_result_id, poll_id, answer, votes, timestamp`` (where the ``votes`` field is set to ``0`` intitially);
   
   b. Retrieves a list of each active user in the Team or Channel who will receive the poll using the Mattermost API (https://api.mattermost.com/#tag/users%2Fpaths%2F~1users%2Fget);
   
   c. Creates a record for each user who will participate in the poll in the ``poll_answer`` table with the following fields: ``poll_answer_id, poll_id, user_id, answer, timestamp`` (where the ``answer`` field is set to ``null`` intitially);
   
   d. Sends a message with a message attachment and interactive message buttons via incoming webhook (https://docs.mattermost.com/developer/webhooks-incoming.html) to each user in the ``poll_answer`` table for the poll:
   
   ```
   Please answer the following poll question:
   
   [Question]

   [Answer], [Answer], ...
   ```
   
   e. Returns an ephemeral message alerting the user that the poll has been published.

   ```
   Alert: The poll has been published. You can view the results for the poll using the 
   /direct-poll-results [pollid] slash command
   ```

# Responding to a Poll

Polls will appear to users as direct messages:

   ```
   Please answer the following poll question:
   
   [Question]

   [Answer], [Answer], ...
   ```

Where the ``[Answer]`` fields are interactive message buttons. When a user clicks on one of the buttons it sends a JSON payload to the URL specified in the attachment (see: https://docs.mattermost.com/developer/interactive-message-buttons.html#button-options). When the system receives the response it will:

1. Check the ``poll`` table to verify that they poll is still open.

2. If the poll is closed the system will return an ephemeral message telling the user that the poll is closed:

   ```
   Alert: The poll is closed and no longer accepting answers.
   ```

3. If the poll is open the system will:

   a. Check the ``poll_answer`` table to retrieve the current answer if the user has previously responded to the poll;
   
   b. If a previous answer exists the system will update the ``poll_result`` table to decrement one from the old answer;
   
   c. Update the ``poll_answer`` table for the user with the answer that they selected;
   
   d. Update the ``poll_result`` table for the answer selected incrementing the number by one;
   
   e. Return the following ephemeral message to the user:

   ```
   Alert: Your answer has been recorded.
   ```

# Viewing a List of All Polls

Users can view a list of all polls by executing the slash command with the ``list`` command: ``/direct-poll list``.

**Note**: In intial release of this project all users will be able to execute this command.

# Viewing the Results of a Poll

Users can view the results of a poll by executing the slash command with the ``view`` command and poll ID separated by the pipe character (``|``): ``/direct-poll view|[pollid]``.

**Note**: In intial release of this project all users will be able to execute this command.

# Closing a Poll

Closing a poll stops the process of updating the ``poll_answer`` table when users vote via interactive message buttons. A user who attempts to vote in a poll after it has closed with receive a message notifying them that the poll has closed and that their vote did not count.

The user who created a poll and close the poll by executing the slash command with the ``close`` command and poll ID separated by the pipe character (``|``): ``/direct-poll close|[pollid]``.

**Note**: In intial release of this project only the user who created the poll will be able to close the poll.







