from email.mime.text import MIMEText
from model.message import Message
import base64
import os

JOB_OFFER_REPLY_BODY = os.environ['JOB_REPLY_BODY']
REMARKS = os.environ['JOB_OFFER_REPLY_REMARKS']
SALUTATION = os.environ.get("SALUTATION", "Dear $name,")
SIGNATURE = os.environ.get("SIGNATURE", "Sincerely,\n\n$name")


def create_salutation(name: str) -> str:
    """Creates the salutation part of an e-mail."""
    return SALUTATION.replace("$name", name)


def create_signature(name: str) -> str:
    """Creates the signature part of an e-mail."""
    return SIGNATURE.replace("$name", name)


def create_job_reply_body(receiver_name: str, sender_name: str, body: str = JOB_OFFER_REPLY_BODY, ps: str = REMARKS):
    return f"""{create_salutation(sender_name)}

{body}

{create_signature(receiver_name)}

{ps}
"""


def create_reply_message(body: str, reply_to: Message) -> dict:
    reply = MIMEText(body)
    reply['To'] = reply_to.from_address
    reply['From'] = reply_to.to_address
    reply['In-Reply-To'] = reply_to.message_id
    reply['References'] = reply_to.message_id
    reply['Subject'] = f'RE: {reply_to.subject}'

    return {
        'message': {
            'raw': base64.urlsafe_b64encode(reply.as_string().encode()).decode(),
            'threadId': reply_to.thread_id,
        }
    }
