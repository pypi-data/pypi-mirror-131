"""Aquama Machine

This python module provide anything related to Aquama hydro machines
"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021

from typing import List, Dict, Iterator
from dataclasses import dataclass
import json


@dataclass
class AquamaMachine:
    """One Aquama hydro machine"""
    serial_number: int
    name: str
    bluetooth_name: str
    rfid_reader_enabled: bool

    @classmethod
    def deserialize_from_aquama_hydro(cls, machine: Dict) -> 'AquamaMachine':
        """Desirize dictionary get from Aquama hydro API"""
        return cls(
            serial_number=machine.get('SerialNumber'),
            name=machine.get('HdName'),
            bluetooth_name=machine.get('HdName'),
            rfid_reader_enabled=machine.get('Rfid', False),
        )
    
    @classmethod
    def deserialize_list_from_aquama_hydro(cls, machines: List[Dict]
                                           ) -> Iterator['AquamaMachine']:
        """Desirize list of dictionary get from Aquama hydro API"""
        return map(
            lambda machine: cls.deserialize_from_aquama_hydro(
                json.loads(
                    machine
                )
            ),
            machines,
        )
