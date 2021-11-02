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
                 members: List[int] = None,
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
    def from_sql_query(query, members):
        return Party(*query[:-2], members=members)

    @staticmethod
    def get(destination: str):
        from . import App
        party = App.db.utility.get_party(destination)
        if party:
            return party
        return None

    def send(self, message: Message):
        from . import App
        App.db.utility.add_message(message, self.party_id)
        for member in self.members:
            if member != message.author.client_id:
                for c in App.clients:
                    if c.client_id == member:
                        log(message.prepare(), LogLevel.EXT_DEBUG)
                        log(f"Sending message to {c.client_id}", LogLevel.DEBUG, c.network_client)
                        c.network_client.send(message.prepare(), ClientHandlerId.MESSAGE_SEND)
                        break

    def __repr__(self):
        return f"Party: ({self.party_id}, {[_ for _ in self.members]}, {self.owner})"

    def get_messages_since(self, last_id: int) -> List[Message]:
        from . import App, TableType
        result = App.db.query(f"select * from {self.party_id}{TableType.MESSAGE_SUFFIX} where id > {last_id}")
        messages = []
        for msg in result:
            msg = Message({})
            msg.content = result[1]
            msg.author = result[2]
            msg.timestamp = result[3]
            messages.append(msg)
        print(messages)
        return messages

r"""
  ⋀
 / \
/   \
  |
  |

"""
