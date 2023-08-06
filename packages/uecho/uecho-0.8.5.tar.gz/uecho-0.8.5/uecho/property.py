# Copyright (C) 2021 Satoshi Konno. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from typing import List, Optional, Any
from .protocol.property import Property as ProtocolProperty
from .protocol.message import Message


class Property(ProtocolProperty):
    """Property represents a property of ECHONET Lite, and it includes the specification attributes and the dynamic data.
    """

    CODE_MIN = 0x80
    CODE_MAX = 0xFF

    GET = 0
    SET = 1
    ANNO = 2

    PROHIBITED = 0
    REQUIRED = 1
    OPTIONAL = 2

    attrs: List[int]
    name: str
    size: int
    anno_status: bool
    object: Optional[Any]

    def __init__(self):
        super().__init__()
        self.attrs = [Property.PROHIBITED, Property.PROHIBITED, Property.PROHIBITED, Property.PROHIBITED]
        self.object = None

    def set_attribute(self, typ: int, attr: int):
        self.attrs[typ] = attr

    def get_attribute(self, typ: int) -> int:
        return self.attrs[typ]

    def __is_attribute_enabled(self, val) -> bool:
        if (val & Property.REQUIRED):
            return True
        if (val & Property.OPTIONAL):
            return True
        return False

    def __is_attribute_required(self, val) -> bool:
        if (val & Property.REQUIRED):
            return True
        return False

    def is_read_enabled(self) -> bool:
        return self.__is_attribute_enabled(self.attrs[Property.GET])

    def is_write_enabled(self) -> bool:
        return self.__is_attribute_enabled(self.attrs[Property.SET])

    def is_announce_enabled(self) -> bool:
        return self.__is_attribute_enabled(self.attrs[Property.ANNO])

    def is_read_required(self) -> bool:
        return self.__is_attribute_required(self.attrs[Property.GET])

    def is_write_required(self) -> bool:
        return self.__is_attribute_required(self.attrs[Property.SET])

    def is_announce_required(self) -> bool:
        return self.__is_attribute_required(self.attrs[Property.ANNO])

    def send_message(self, esv: int, data: bytes = bytearray()) -> bool:
        """Sends a unicast message to the property asynchronously.


        Args:
            esv (int): A service type of ECHONET Lite.
            data (bytes, optional): : A property data. Defaults to bytearray().

        Returns:
            bool: True if successful, otherwise False.
        """
        return self.object.send_message(esv, [(self.code, data)])

    def post_message(self, esv: int, data: bytes = bytearray()) -> Optional[Message]:
        """Posts a unicast message to the property and return the response message synchronously.

        Args:
            esv (int): A service type of ECHONET Lite.
            data (bytes, optional): A property data. Defaults to bytearray().

        Returns:
            Optional[Message]: The response message if successful receiving the response message, otherwise None.
        """
        return self.object.post_message(esv, [(self.code, data)])

    def copy(self):
        return copy.deepcopy(self)
