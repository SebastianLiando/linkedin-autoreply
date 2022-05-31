from wit import Wit
from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core import SCOPES, CONF_THRESHOLD, WIT_ACCESS_TOKEN, INMAIL_ADDR, first_where
from model.thread import Thread
from core.reply import create_reply_message, create_job_reply_body


def authenticate(token='token.json', client_secret='credentials.json') -> Credentials:
    creds: Credentials = None

    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                client_secret, SCOPES)
            creds = flow.run_local_server()

        with open(token, 'w') as token:
            token.write(creds.to_json())

    return creds


def is_job_offer(wit: Wit, message: str, conf_thresh: float = CONF_THRESHOLD) -> bool:
    intent = wit.message(message)
    job_offer_intent = first_where(
        intent['intents'], lambda i: i['name'] == 'job_offer')

    # Not detected
    if job_offer_intent == None:
        print('Job offer not detected')
        return False

    # Detected, but low-confidence
    confidence = job_offer_intent['confidence']
    if confidence < conf_thresh:
        print('Job offer of low-confidence detected')
        return False

    return True


def main():
    creds = authenticate()
    wit = Wit(WIT_ACCESS_TOKEN)

    try:
        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Get the user's email address
        user_profile = service.users().getProfile(userId='me').execute()
        user_email = user_profile['emailAddress']

        # Get all emails from LinkedIn in-mail service from the last 24 hours
        yesterday = (datetime.now() - timedelta(hours=24)).date()
        yesterday = yesterday.strftime("%m/%d/%Y")
        print('Emails from ' + yesterday)

        query = f"from:{INMAIL_ADDR} after:{yesterday}"

        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        # Quit if there are none
        if not messages:
            print('No unread messages found.')
            return

        # Get the thread ids - we want to examine by thread
        thread_ids = set(message['threadId'] for message in messages)

        for thread_id in thread_ids:
            thread = service.users().threads().get(userId='me', id=thread_id).execute()
            thread = Thread.from_json(thread)

            # Get Subject
            first_msg = thread.messages[0]
            first_msg_subject = first_msg.subject
            print(f'Subject: {first_msg_subject}')

            # Ignore if message has been replied
            if thread.is_replied(user_email):
                print('This thread has been replied. Ignoring...')
                return

            # Don't reply if it's not a job offer
            job_offer = is_job_offer(wit, first_msg_subject)
            if not job_offer:
                print('Not replying.')
                return

            print('Job offer detected. Sending a reply.')
            body = create_job_reply_body(
                first_msg.receiver_first_name, first_msg.sender_first_name)
            reply = create_reply_message(body, first_msg)

            service.users().messages().send(
                userId='me', body=reply['message']).execute()

    except HttpError as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    main()
