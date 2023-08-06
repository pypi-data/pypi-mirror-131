#!/usr/bin/env python
# Copyright (c) 2019 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.TargetAddrNewCfgTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError

class SNMPv3TargetAddrNewCfgParameters(RadwareParametersStruct):
    index: int
    name: str
    TransIp: Optional[str]
    port: Optional[int]
    taglist: Optional[str]
    paramsName: Optional[str]
    EnaTrap: Optional[str]
    DisTrap: Optional[str]
    TransIpv6: Optional[str]
    IpVer: Optional[str]
    TrapBmap: Optional[str]

    def __init__(self, Name: int = None):
        self.index = None
        self.name = Name
        self.TransIp = None
        self.port = None
        self.taglist = None
        self.paramsName = None
        self.EnaTrap = None
        self.DisTrap = None
        self.TransIpv6 = None
        self.IpVer = None
        self.TrapBmap = None

bean_map = {
    TargetAddrNewCfgTable: dict(
        struct=SNMPv3TargetAddrNewCfgParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Name='name',
            TransIp='TransIp',
            TransPort='port',
            TagList='taglist',
            ParamsName='paramsName',
            EnaTrap='EnaTrap',
            DisTrap='DisTrap',
            TransIpv6='TransIpv6',
            IpVer='IpVer',
            TrapBmap='TrapBmap'
        )
    )
}


class SNMPv3TargetAddrNewCfgConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3TargetAddrNewCfgParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3TargetAddrNewCfgConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3TargetAddrNewCfgParameters) -> SNMPv3TargetAddrNewCfgParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.TrapBmap = BeanUtils.decode_bmp(parameters.TrapBmap)
            trapList = list()
            for v in parameters.TrapBmap:
                if EnumTargetAddrDisTrap.enum(v) is not None:
                    trapList.append(EnumTargetAddrDisTrap.enum(v).name)
            parameters.TrapBmap = str(trapList).strip('[]')
            return parameters

    def _update(self, parameters: SNMPv3TargetAddrNewCfgParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(TargetAddrNewCfgTable, parameters)

