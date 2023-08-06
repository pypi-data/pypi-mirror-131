"""Access rights and authentication

This module provide all needed to define access rights and
authentication to the Aquama-Hydro service.
"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021

from enum import Enum
from dataclasses import dataclass
from typing import Dict


class Origin(Enum):
    """Indicate from where you do the call to the API"""
    MobileApp = 0
    HydroDevice = 1
    RemoteApp = 2
    Shop = 3
    Erp = 4
    Api = 5
    Operator = 6
    Hotspot = 7


class User(Enum):
    """Indicate the user who do the call to the API"""
    Client = 0
    Buisness = 1
    Employee = 2
    Technical = 3
    Admin = 4
    SuperAdmin = 5
    Guest = 6


@dataclass
class Auth:
    """Athentication used for API call"""
    api_key: str
    origin: Origin
    user: User
    user_key: str
    info: str = ''

    def to_aquama_hydro_json(self) -> Dict:
        """Serialize this object to json in a format accepted by
        Aquama-Hydro"""
        return {
            'Key': self.api_key,
            'AccessFrom': self.origin.value,
            'AccessUser': self.user.value,
            'AccessInfo': self.info,
            'KeyUser': self.user_key,
        }
