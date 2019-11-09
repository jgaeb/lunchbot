import os

from slack import WebClient

from .goog import get_current_dictator
from .dd import (
        DoorDashOrder, LoginError, NavigationError, NotLoggedInError,
        GroupOrderFailedError
)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1pJ8NdaQ8SMGVoDWx6SGKMhonkFY7s6wyYjgi-w6DEsE/edit?usp=sharing"
ICON_URL = "https://raw.githubusercontent.com/jg43b/lunchbot/master/LunchBot.jpg"

class LunchBot(WebClient):
    def __init__(self):
        super().__init__(token=os.environ.get("SLACK_TOKEN"))
        self.channel = "WD8PPA17Z"
        self.dictator = get_current_dictator()
        self.order = DoorDashOrder()
        if not self.dictator:
            self.send_order_message = self._no_lunch
            return
        try:
            self.order.login(
                    username = os.environ.get("DOORDASH_USERNAME"),
                    password = os.environ.get("DOORDASH_PASSWORD")
            )
        except LoginError:
            self.send_order_message = self._login_failed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.order:
            self.order.close()

    def _login_failed(self):
        self.chat_postMessage(
                channel=self.channel,
                text=(
                    "<!channel>: Sorry! I encountered an error logging into"
                    " DoorDash this week :sadfile: Can a human take over?"
                    f" (This week's dictator is {self.dictator.name}.)"
                ),
                icon_url=ICON_URL
        )
    
    def _no_lunch(self):
        self.chat_postMessage(
                channel=self.channel,
                text=(
                    "<!channel>: I didn't find a dictator, so I'm assuming"
                    " there's no lunch this week. See you next week!"
                ),
                icon_url = ICON_URL
        )

    def _get_order_urls(self, day):
        text = [f"*{day.title()}*"]
        notes = {False: "", True: " for a vegan-friendly option"}
        urls = [
            getattr(self.dictator, f"{day}{suffix}")
            for suffix in ["", "_vegan"]
        ]
        for url, vegan in zip(urls, [False, True]):
            try:
                if url:
                    rest_url = url
                else:
                    rest_url = self.dictator.get_random_rest(vegan=vegan) 
                order_url, rest_name = self.order.group_order(rest_url)
                message = (
                        f"Click <{order_url} | here> to place your order for lunch"
                        f" on {day.title()} from {rest_name}{notes[vegan]}."
                )
                if not url:
                    message += (
                            f" ({self.dictator.name} doesn't appear to have picked"
                            f" anything, so I chose at random.)"
                    )
            except (NavigationError, GroupOrderFailedError):
                message = (
                        f"I tried to start a group order{notes[vegan]}, but I wasn't"
                        f" able to. Maybe there was a problem with the link?"
                        f" (It's ` {rest_url} `.)"
                )
            text.append(message)
        block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n    • ".join(text)
                }
        }
        return block

    def send_order_message(self):
        try:
            blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"*This Week's Dictator:* :crown:"
                                f" {self.dictator.name} :crown:\n"
                                f"_Long may they reign!_"
                            )
                        }
                    },
                    {
                        "type": "divider"
                    },
                    self._get_order_urls("monday"),
                    {
                        "type": "divider"
                    },
                    self._get_order_urls("thursday"),
                    {
                        "type": "divider",
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"(<!channel>: Don't forget to add your"
                                f" prefrences to the"
                                f" <{SPREADSHEET_URL} | spreadsheet>!)"
                            )
                        }
                    }
            ]
            self.chat_postMessage(
                    channel=self.channel,
                    blocks=blocks,
                    icon_url=ICON_URL
            )
        except Exception as e:
            self.chat_postMessage(
                    channel=self.channel,
                    text=(
                        "<!channel>: Sorry! I encountered a mysterious error"
                        " placing an order this week :sadfile: Can a human"
                        " take over while Hans makes an ill-fated attempt to"
                        " fix me? (This week's dictator is"
                        f" {self.dictator.name}.)"
                    )
            )
            raise e
