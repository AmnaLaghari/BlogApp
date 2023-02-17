# Slack Integration

Blog App has been integrated with slack. Whenever a comment is reported we get a message in channel with the content of comment and two buttons, **Keep** and **Delete**. Clicking on these buttons we can either keep/delete the comment. 

## Setup
We will be following these steps for integrating slack with our app.

**1. Create Slack Application**: First login or signup (if you don't already have an account) to your slack account. Then go it [https://api.slack.com/](https://api.slack.com/) and create an app. Select a workplace and confirm it. 

**2. Insall to workspace:** Then go to [https://api.slack.com/apps](https://api.slack.com/apps) and *install to workspace*. 

**3. Generate OAuth Token:** To connect the application with any programming language, in this case, Python, we will need the OAuth Token. Slack automatically generates these tokens when you install the app on your team, as we did in the previous step. So we will only need to copy it later; just check that the token is there for now. Go to **OAuth & Permissions** on you left to check.    

**4. Creating channel and integration:** Now you can either create a new channel or use and existing one. Now click on the channel, go to the Integrations tab, and Add an App.

**5. Integration with django App:** 

For this purpose we will use a python package called [**slack_sdk**](https://slack.dev/python-slack-sdk/). Lets install it.  
```bash
pip install slack_sdk
```
To send a message, we need the **chat_postMessage** function. We also need the Token that we got in the first step and the channel's name that we created in the second step.
 ```bash
client = WebClient(token=<your token here>)

client.chat_postMessage(channel=<your channel here>, text=<message>)
```
You can add attachments to ad button to your message and make message interactive. For more details [https://api.slack.com/legacy/interactive-messages](https://api.slack.com/legacy/interactive-messages)