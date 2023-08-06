import os

from slack_sdk.webhook import WebhookClient
from supaconify.message import builder


def slack(url=None, template=None):
    if url is None:
        try:
            url = os.environ["SUPACONIFY_SLACK_WEBHOOK_URL"]
        except Exception:
            print(
                "Cannot get webhook url.",
                "Set SUPACONIFY_SLACK_WEBHOOK_URL as a environment variable",
            )
            exit(code=1)
    message = builder(template=template)
    WebhookClient(url).send(text=message)
