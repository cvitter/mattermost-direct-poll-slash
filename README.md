# Mattermost - Direct Poll Slash Command

**TODO**: Build a Mattermost (https://www.mattermost.com) integration that uses a Slash Command (https://docs.mattermost.com/developer/slash-commands.html), the Mattermost API (https://api.mattermost.com/), Message Attachments (https://docs.mattermost.com/developer/message-attachments.html), and Interactive Message Buttons (https://docs.mattermost.com/developer/interactive-message-buttons.html) to poll users in a Team or Channel via direct message.

# Specification/Use Case

The following is an overview of the planned functionality of this integration.

1. A user creates a poll using the ``direct-poll`` slash command:

   ```
   /direct-poll Have you completed your monthly HR training yet?|Yes/No/Maybe
   ```
   or
   ```
   /direct-poll Have you completed your monthly HR training yet?|Yes/No/Maybe|Channel Name
   ```
   The slash commands takes three arguments separated by the pipe character (``|``): The question, possible answers (separated by the forward slash character (``/``), and optionally the name of the channel to poll users from if you don't wish to poll the entire team.

2. The system creates a database record in the ``poll`` table with the following fields: ``question_id, timestamp, team_id, channel_id, token, user_id, user_name, questions, answers, channel_to_poll_id, published, closed``

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

5. 




# License
The content in this repository is Open Source material released under the MIT License. Please see the [LICENSE](LICENSE) file for full license details.

# Disclaimer

The code in this repository is not sponsored or supported by Mattermost, Inc.

# Authors
* Author: [Craig Vitter](https://github.com/cvitter)

# Contributors 
Please submit Issues and/or Pull Requests.
