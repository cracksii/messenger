from typing import List, Dict

from server import log, LogLevel

from .message import Message
from .client import Client
from .senders import ClientHandlerId


class Party:
    """
    Server side representation of a party with n members.
    """

    def __init__(self,
                 party_id: int = 0,
                 name: str = "",
                 owner: int = 0,
                 description: str = "",
                 members: List[Client] = None,
                 messages: List[Message] = None,
                 member_count: int = 0,
                 image: str = "",
                 settings: Dict[str, str] = None,
                 admins: List[Client] = None):
        self.party_id = party_id
        self.name = name
        self.members = [] if not members else members  # A list storing the members uids
        self.messages = [] if not messages else messages
        self.member_count = member_count
        self.owner = owner  # The uid of the owner
        self.image = image
        self.description = description
        self.settings = {} if not settings else settings
        self.admins = [] if not admins else admins  # The uids of admins (users who can change settings in the party)

    @staticmethod
    def from_sql_query(query):
        return Party(*query[:-2])

    @staticmethod
    def get(destination: str):
        from .application import App
        party = App.db.utility.get_party(destination)
        log(party.__dict__, LogLevel.EXT_DEBUG)
        return party

    def send(self, message: Message):
        log(f"Members: {self.members}", LogLevel.EXT_DEBUG)
        for member in self.members:
            if member.client_id != message.author.client_id:
                member.network_client.send(message.to_json(), ClientHandlerId.MESSAGE_SEND)


r"""
  ⋀
 / \
/   \
  |
  |

"""