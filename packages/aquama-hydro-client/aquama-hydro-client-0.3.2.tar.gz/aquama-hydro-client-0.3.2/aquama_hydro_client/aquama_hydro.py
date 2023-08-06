"""Aquama-hydro service

This python module provide the class AquamaHydro you can use to
communicate with the Aquama-hydro service API
"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021

from typing import List
from dataclasses import dataclass
from enum import Enum
import requests
import json

from aquama_hydro_client.access import (
    Auth,
)
from aquama_hydro_client.exceptions import (
    ApiHttpNot200,
    ApiResponseEmpty,
    ApiResponseNotMessage,
    ApiError,
)
from aquama_hydro_client.message import (
    Message,
    MessageType,
)

from aquama_hydro_client.aquama_machine import (
    AquamaMachine,
)


# Consts
API_SCHEME_DEFAULT = 'https'
API_ADDRESS_DEFAULT = 'localhost'
API_PORT_DEFAULT = 10080
API_ENDPOINT_DEFAULT = '/api/va_Function'
API_VERSION_DEFAULT = '4.0.0.0'


class DataType(Enum):
    none = 0
    protobuf = 1
    json = 2


@dataclass
class AquamaHydro:
    """A class used to interact with an Aquama-Hydro service"""
    auth: Auth
    api_scheme: str = API_SCHEME_DEFAULT
    api_address: str = API_ADDRESS_DEFAULT
    api_port: int = API_PORT_DEFAULT
    api_endpoint: str = API_ENDPOINT_DEFAULT
    api_version: str = API_VERSION_DEFAULT


    @property
    def api_url(self) -> str:
        """The URL of the API
        
        Build dynamically with self.api_scheme, self.api_address,
        self.api_port and self.api_endpoint.
        """
        return '{scheme}://{address}:{port}{endpoint}'.format(
            scheme=self.api_scheme,
            address=self.api_address,
            port=self.api_port,
            endpoint=self.api_endpoint,
        )
    
    def _api_call(self, function_name: str,
                  function_args: str) -> Message:
        """Call the API with the given function_name and function_args.

        This is a private method, don't call it directly.

        function_name are used as functionNameRaw and function_args as
        functionParametersRaw on the Aquama-hydro API. Make sure to
        use values accepted by the API.

        Arguments:
        - function_name (str): The function name to call on the API, passed
          as functionNameRaw to the API
        - function_args (str): The function arguments for the API, passed
          as functionParametersRaw to the API
        
        Return:
        A message object, the message returned by Aquama-Hydro
        """
        payload = {
            'versionRaw': self.api_version,
            'accessRaw': json.dumps(self.auth.to_aquama_hydro_json()),
            'functionNameRaw': function_name,
            'functionParametersRaw': function_args,
        }
        response = requests.post(self.api_url, data=payload)

        # Check if HTTP status code of the API response is 200,
        # raise exception if not
        if response.status_code != 200:
            raise ApiHttpNot200(
                "HTTP request return status code {}".format(
                    response.status_code,
                )
            )
        # Raise exception if response is embty
        if not response.json():
            raise ApiResponseEmpty(
                'The received response from the API is empty'
            )
        # Raise exception if Json is not for an Aquama-Hydro Message
        if not Message.is_json_message(response.json()):
            raise ApiResponseNotMessage(
                'Json get from API not a Message.\nResponse:\n{}'.format(
                    response.json(),
                )
            )
        # Build a Message object from the Json received from
        # Aquama-Hydro
        response_message = Message.from_aquama_hydro_json(
            response.json()
        )
        # Raise exception if the message is an error message
        if response_message.message_type is MessageType.ERROR:
            raise ApiError(response_message.text)
        
        return response_message

    def ping(self) -> bool:
        """Ping the service Aquama-Hydro.

        Return true if the service respond, false if not"""
        response = requests.get(
            '{scheme}://{address}:{port}/api/test'.format(
                scheme=self.api_scheme,
                address=self.api_address,
                port=self.api_port,
            )
        )
        return True if response.status_code == 200 else False

    def get_aquama_machines(self, serial_numbers: List[int]
                           ) -> List[AquamaMachine]:
        """Get informations about aquama machines designated by their ID

        Note: Search results are filtered to only return machines with
        serial number.

        Parameters:
        - serial_numbers: List of serial numbers of machines
        
        Return:
        - List of machines and their informations

        """
        call_params = {
            'SerialNumber': serial_numbers,
            'MaxEntry': 0,
            'DataType': DataType.json.value,
            'MissingAccount': False,
            'MissingAccountGroupId': False,
        }
        response_message = self._api_call(
            function_name='VA_GET_HD_INFO',
            function_args=json.dumps(call_params),
        )
        aquama_machines = AquamaMachine.deserialize_list_from_aquama_hydro(
            json.loads(
                response_message.text
            )
        )
        return (
            machine for machine in aquama_machines
            if machine.serial_number != 0
        )

    def get_all_aquama_machines(self) -> List[AquamaMachine]:
        """Get informations about all aquama machines designated by their ID

        Note: Search results are filtered to only return machines with
        serial number.
        
        Return:
        - List of machines and their informations

        """
        return self.get_aquama_machines([])
    
    def is_aquama_machine_exist(self, serial_number: int) -> bool:
        """Tell if a given Aquama machine exist

        Parameters:
        - serial_number: Serial number of the machin to search

        Return:
        - If machine found"""
        machines = list(self.get_aquama_machines([serial_number]))
        if len(machines) == 0:
            return False
        return any(
            map(
                lambda machine: machine.serial_number == serial_number,
                machines,
            )
        )

    def get_aquama_machine_solution_type(self, serial_number: int) -> int:
        """Get the type of solution of a given aquama machine indicated by its
        serial number.

        Parameters:
        - serial_number: Serial number of the machine whose solution
        type you want to know

        Return: 
        - The solution type, expressed as un integer (see Aquama-hydro
        to know which solution correspond to which number)"""
        # Call the API
        response_message = self._api_call(
            function_name='VC_GET_CL_USE',
            function_args=f'{serial_number}',
        )
        # Convert and return the response
        return int(response_message.text)
