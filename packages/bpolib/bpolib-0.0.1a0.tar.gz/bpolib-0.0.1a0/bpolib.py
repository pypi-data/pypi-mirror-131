"""Module for BPOs."""

import bs4
import requests
import itertools
from dateutil.parser import parse as _parsedate

ISSUE_URL = "https://bugs.python.org/issue"
__version__ = "0.0.1.a"


def _create_list(text):
    r = text.split(", ")
    return r if r != [""] else []


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

    Don't instantiate this object yourself - it is
    hardcoded to wrap text found in the BPO.
    """

    # I plan to eventually add extra details found
    # in the URL for the message such as the SpamBayes Score
    # and message id, etc
    def __init__(self, details: str, content: str):
        self.content = content.strip()
        details = details.split("\n")[2:-1]
        msg = details[0]
        author = details[1]
        date = details[2]
        self.author = author[author.find("(") + 1 : author.find(")")]
        self.number = int("".join(filter(str.isdigit, msg)))
        self.created_at = _parsedate(date[5:])
        self.url = f"https://bugs.python.org/msg{self.number}"

    def __str__(self):
        return self.content


class BPO:
    """An object to represent a BPO (bugs.python.org)."""

    def __init__(self, bpo_number: int):
        url = ISSUE_URL + str(bpo_number)
        request = requests.get(url)
        if request.status_code != 200:
            raise RuntimeError("BPO not found")
        soup = bs4.BeautifulSoup(request.text, "html.parser")
        content_body = soup.find(id="content-body")
        info_text = content_body.p.text
        lc = info_text.rfind(", last changed")
        td_all = content_body.find_all("td")
        m = list(map(lambda x: getattr(x, "text"), soup.find(class_="messages").find_all("tr")))[1:]
        self.url = url
        self.title = content_body.input.get("value")
        self.bpo_number = int(soup.find(id="breadcrumb").text.strip()[5:])
        self.messages = list(itertools.starmap(BPOMessage, list(zip(m[0::2], m[1::2]))))
        self.message_count = len(self.messages)
        self.type = td_all[1].text or None
        self.stage = td_all[2].text or None
        self.components = _create_list(td_all[3].text.strip())
        self.versions = _create_list(td_all[4].text.strip())
        self.status = td_all[5].text  # this will always have a value
        self.resolution = td_all[6].text or None
        self.dependencies = _create_list(td_all[7].text.strip())
        self.superseder = td_all[8].text.strip() or None
        self.assigned_to = td_all[9].text.strip() or None
        self.nosy_list = _create_list(td_all[10].text.strip())
        self.priority = td_all[11].text
        self.keywords = _create_list(td_all[12].text.strip())
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

    def __int__(self):
        return self.bpo_number

    def __repr__(self):
        return f"<BPO {self.bpo_number}, url='{self.url}'>"

    def __str__(self):
        return f"bpo-{self.bpo_number}"
