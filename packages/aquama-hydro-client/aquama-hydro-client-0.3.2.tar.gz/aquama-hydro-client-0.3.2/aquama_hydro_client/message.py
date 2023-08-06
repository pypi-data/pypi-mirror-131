"""Message returned by Aquama-Hydro"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021

from typing import Dict
from enum import Enum
from dataclasses import dataclass


MESSAGE_KEYS = (
    'text',
    'messageID',
    'messageType',
)


class MessageType(Enum):
    """The type of a received message"""
    SUCCESS = 0
    NOTSUCCESS = 1
    ERROR = 2
    WARNING = 3


class MessageID(Enum):
    UNDEFINED = 0
    WALLET_NOT_ENOUGH_MONEY = 1
    WALLET_CREDIT_LIMIT = 2
    WALLET_ONLINE_VALUE = 3
    WALLET_NOT_VALID = 4
    CONSUMPTION_UPLOADED = 5
    CONSUMPTION_NOTUPLOADED = 6
    WRONGVERSION = 7
    COULDNOTCONNECTTODB = 8
    WRONGPSWLOGIN = 9
    EMAIL_EXISTS = 10
    FIRST_NAME_LENGHT = 11
    LAST_NAME_LENGHT = 12
    PASSWORD_LENGHT = 13
    PRESTACUSTOMER_DESERIALIZE = 14
    NOT_VALID_EMAIL = 15
    SMARTAPPINFO_DESERIALIZE = 16
    MACHINEINFO_NOTUPDATED = 17
    MACHINE_NOTCREATED = 18
    MOBILESTACKINFO_NOTSAVED = 19
    MOBILESTACKINFO_NOTVALIDATED = 20
    VALIDATION = 21
    NO_ACCESS_RIGHTS = 22
    WALLET_NOT_DECRYPT = 23
    BLOCKUUID_USED = 24


@dataclass
class Message():
    """A message received by the API"""
    text: str
    message_id: MessageID = None
    message_type: MessageType = MessageType.SUCCESS

    @staticmethod
    def is_json_message(data: Dict) -> bool:
        """Test is a given json object is an AquamaHydro message"""
        return all(
            key in data.keys()
            for key in MESSAGE_KEYS
        )

    
    @classmethod
    def from_aquama_hydro_json(cls, data: Dict) -> 'Message':
        """Construct a message from a JSON object given by Aquama-Hydro"""
        return Message(
            text = data.get('text') or '',
            message_id = MessageID(data.get('messageID')
                                   or MessageID.UNDEFINED.value),
            message_type = MessageType(data.get('messageType')
                                       or MessageType.SUCCESS.value),
        )
