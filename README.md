# LinkedIn AutoReply

[![Tests](https://github.com/SebastianLiando/linkedin-autoreply/actions/workflows/tests.yml/badge.svg)](https://github.com/SebastianLiando/linkedin-autoreply/actions/workflows/tests.yml)

This script automatically replies to LinkedIn InMail messages according to the detected intention of the message. The purpose of this script is to send a timely reply while allowing the user to read the message at a later time.

## How it Works

### [Gmail API](https://developers.google.com/gmail/api)

Gmail API retrieves InMail messages from the user's inbox received from one day before the time the script is executed. The script replies to those emails that has not been replied, which is **assumed** that the user has not made a reply. The assumption is not true if the user sent a reply directly from LinkedIn, which is not reflected in the user's mailbox.

> LinkedIn official API does not have the feature to read and send messages at the time of development.

### [Wit.ai](https://wit.ai/)

To know the appropriate reply, the subject of the email is checked. The script needs to know what the intention of the sender is. Wit.ai provides this intent recognition capability for free. Based on the recognized intent, the script sends the corresponding reply.

> Currently, only job offer messages can be detected.

## Getting Started

### Setup Gmail API

1. Login to [google cloud console](https://console.cloud.google.com/) and create a new project
2. With the project selected, enable Gmail API
3. Go to "Credentials" tab, create an OAuth Client ID credential, set the application type to `desktop`
4. Go to "OAuth Consent Screen" tab and scroll to "Test users" section. Add your LinkedIn connected email as a test user
5. Download the JSON credential file, name it `credentials.json` and put it in the root project folder
6. Run `main.py` and open the link in the browser to authorize Gmail API

If the above steps are successful, you should have `token.json` file in the root project folder

### Setup Wit.ai

1. [Login to Wit.ai](https://wit.ai/) using your Facebook account
2. Create a new application
3. Using some sample email subjects about job offers, train the `job_offer` intent.

### Setup Environment Variables

Add the following environment variables to the host operating system.

| Name                    | Desc                                                                                                           |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| WIT_ACCESS_TOKEN        | The client access token of your Wit.ai application                                                             |
| JOB_OFFER_REPLY_BODY    | The reply email body to reply job offer emails.                                                                |
| JOB_OFFER_REPLY_REMARKS | Additional remarks when replying job offer emails. This is added at the bottom of the email.                   |
| SALUTATION              | The greeting part of the email. Use "$name" as a placeholder of the sender name. For example: "Dear $name,"    |
| SIGNATURE               | The signature part of the email. Use "$name" as a placeholder of your name. For example: "Sincerely,\n\n$name" |
