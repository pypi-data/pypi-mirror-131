"""Module for BPOs."""

import bs4
import requests
from dateutil.parser import parse as _parsedate

BPO_BASE = "https://bugs.python.org/"
__version__ = "0.0.2a0"


def _create_list(text):
    r = text.split(", ")
    return r if r != [""] else []


def _create_request(inst, endpoint) -> requests.Response:
    request = requests.get(BPO_BASE + endpoint)
    if request.status_code != 200:
        raise RuntimeError(f"{inst} not found")
    return request


class BPOTimeEvent:
    """An object to represent a time event."""

    __slots__ = ("date", "author")

    def __init__(self, date: str, author: str):
        self.date = date
        self.author = author

    def __repr__(self):
        return f"<class 'BPOTimeEvent(date={self.date}, author='{self.author}')'>"


class BPOMessage:
    """An object to represent a message in an issue.

    You shouldn't need to instantiate this object yourself,
    but if you do - pass the message number to it.
    """

    def __init__(self, message_number: int):
        endpoint = f"msg{message_number}"
        soup = bs4.BeautifulSoup(_create_request("message", endpoint).text, "html.parser")
        td_all = tuple(map(lambda x: x.td, soup.find(class_="form").find_all("tr")))
        self.url = BPO_BASE + endpoint
        self.message_number = message_number
        self.author = td_all[0].text
        self.recipients = _create_list(td_all[1].text)
        self.date = _parsedate(td_all[2].text.replace(".", " "))
        self.spambayes_score = float(td_all[3].text)
        self.marked_as_misclassified = True if td_all[4].text == "Yes" else False
        self.message_id = td_all[5].text
        self.in_reply_to = td_all[6].text or None
        self.content = soup.find(class_="messages").pre.text

    def __repr__(self):
        return f"<msg#{self.message_number}, url='{self.url}'>"

    def __str__(self):
        return self.content

    def __int__(self):
        return self.message_number


class BPO:
    """An object to represent a BPO (bugs.python.org)."""

    def __init__(self, bpo_number: int):
        url = f"issue{bpo_number}"
        soup = bs4.BeautifulSoup(_create_request("BPO", url).text, "html.parser")
        content_body = soup.find(id="content-body")
        info_text = content_body.p.text
        lc = info_text.rfind(", last changed")
        td_all = tuple(map(lambda x: x.text, content_body.find_all("td")))
        self.url = BPO_BASE + url
        self.title = content_body.input.get("value")
        self.bpo_number = int(soup.find(id="breadcrumb").text.strip()[5:])
        self.messages = tuple(
            map(
                BPOMessage,
                map(
                    lambda x: int(x.a.text[3:]), soup.find(class_="messages").find_all("tr")[1::2]
                ),
            )
        )
        self.message_count = len(self.messages)
        self.type = td_all[1] or None
        self.stage = td_all[2] or None
        self.components = _create_list(td_all[3].strip())
        self.versions = _create_list(td_all[4].strip())
        self.status = td_all[5]  # this will always have a value
        self.resolution = td_all[6] or None
        self.dependencies = _create_list(td_all[7].strip())
        self.superseder = td_all[8].strip() or None
        self.assigned_to = td_all[9].strip() or None
        self.nosy_list = _create_list(td_all[10].strip())
        self.priority = td_all[11]
        self.keywords = _create_list(td_all[12].strip())
        self.last_edited_at = BPOTimeEvent(
            _parsedate(dt := info_text[lc + 14 : lc + 14 + 16]),
            info_text[info_text.rfind(dt) + len(dt) + 5 :][
                slice(None, -1) if self.status != "closed" else slice(None, -27)
            ],
        )
        self.created_at = BPOTimeEvent(
            _parsedate(info_text[11:27]),
            info_text[31 : info_text.index(", last changed")],
        )
        self.author = self.created_at.author
        self.last_edited_at = self.last_edited_at.author

    def __int__(self):
        return self.bpo_number

    def __repr__(self):
        return f"<BPO {self.bpo_number}, url='{self.url}'>"

    def __str__(self):
        return f"bpo-{self.bpo_number}"
