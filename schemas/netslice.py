# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:02:39
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:05:28
from pydantic import BaseModel
from typing import List, Optional
import schemas.enums as enums

class N6Protection(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    # priority: Optional[int] = None
    # ServerIP: Optional[str] = None
    # MaskLen: Optional[int] = None
    # startport: Optional[int] = None
    # endport: Optional[int] = None
    # ULGBR: Optional[int] = None
    # DLGBR: Optional[int] = None
    # ULMBR: Optional[int] = None
    # DLMBR: Optional[int] = None
    # Protocol: Optional[str] = None
    # PassBlock: Optional[str] = None
    
class NetworkSliceBase(BaseModel):
    coverage_area: list
    plmnid: Optional[int] = None
    operational_state: Optional[enums.OperationalState] = None
    administrative_state: Optional[enums.AdministrativeState] = None
    sst: int
    sd: str
    prioritylabel: Optional[int] = None
    dllatency: Optional[int] = None
    ullatency: Optional[int] = None
    maxnumberofues: Optional[int] = None
    dlguathptperue: Optional[float] = None
    ulguathptperue: Optional[float] = None
    dlmaxthptperue: Optional[float] = None
    ulmaxthptperue: Optional[float] = None
    dlguathptperslice: Optional[float] = None
    ulguathptperslice: Optional[float] = None
    dlmaxthptperslice: Optional[float] = None
    ulmaxthptperslice: Optional[float] = None
    dlmaxpktsize: Optional[int] = None
    ulmaxpktsize: Optional[int] = None
    maxnumberofpdusessions: Optional[int] = None
    nroperatingbands: Optional[str] = None
    slicesimultaneoususe: Optional[enums.sliceuse] = None
    delaytolerance: Optional[enums.DelayTolerance] = None
    energyefficiency: Optional[enums.energyKPI] = None
    termdensity: Optional[int] = None
    activityfactor: Optional[float] = None
    resourcesharinglevel: Optional[enums.sharing] = None
    uemobilitylevel: Optional[enums.uEmobilityLevel] = None
    uespeed: Optional[int] = None
    reliability: Optional[float] = None
    dldeterministiccomm: Optional[enums.DeterministicCommAvailability] = None
    dldeterminperiodicity: Optional[int] = None
    uldeterministiccomm: Optional[enums.DeterministicCommAvailability] = None
    uldeterminperiodicity: Optional[int] = None
    survivaltime: Optional[float] = None
    positioningtype: Optional[enums.positioning] = None
    positioningfrequency: Optional[enums.positioningfreq] = None
    positioningaccuracy: Optional[float] = None
    synchronicitysupport: Optional[enums.synchonicity] = None
    synchronicityaccuracy: Optional[float] = None
    nssaasupport: Optional[enums.nssaa] = None
    n6protection: Optional[List[N6Protection]] = []     # changed from nn6 protection
    #not in 3GPP
    dnn: str
    name: Optional[str] = None

class NetworkSliceCreate(NetworkSliceBase):
    operational_state: enums.OperationalState
    administrative_state: enums.AdministrativeState
    id: str

class NetworkSliceEdit(NetworkSliceBase):
    id: Optional[str] = None
    name: Optional[str] = None
    sst: Optional[int] = None
    sd: Optional[str] = None
    dnn: Optional[str] = None
    coverage_area: Optional[list] = None

class ProductOrder(BaseModel):
   id: Optional[str] = None
   name: Optional[str] = None
   DNN: Optional[str] = None                                # changed from dnn
   administrative_state: Optional[str] = None
   operational_state: Optional[str] = None
   sst: Optional[str] = None                                # changed to str to match response
   sd: Optional[str] = None
   dllatency: Optional[str] = None                          # changed to str to match response
   ullatency: Optional[str] = None                          # changed to str to match response
   dlguathptperue: Optional[str] = None                     # changed to str to match response
   ulguathptperue: Optional[str] = None                     # changed to str to match response
   dlmaxthptperue: Optional[str] = None                     # changed to str to match response
   ulmaxthptperue: Optional[str] = None                     # changed to str to match response
   delaytolerance: Optional[str] = None
   reliability: Optional[str] = None                        # changed to str to match response
   dldeterministiccomm: Optional[str] = None
   uldeterministiccomm: Optional[str] = None
   coverage_area: Optional[dict] = None                     # changed to dict to match response format
   n6protections: Optional[List[N6Protection]] = []         # changed from n6protection
   kpis: Optional[List[str]] = []                           # changed from kpi

#    prioritylabel: Optional[int] = None
#    uemobilitylevel: Optional[str] = None
#    ulmaxpktsize: Optional[int] = None
#    dldeterminperiodicity: Optional[int] = None
#    uldeterminperiodicity: Optional[int] = None
#    dlguathptperslice: Optional[int] = None
#    ulguathptperslice: Optional[int] = None
#    dlmaxthptperslice: Optional[int] = None
#    ulmaxthptperslice: Optional[int] = None
#    termdensity: Optional[int] = None
#    maxnumberofpdusessions: Optional[int] = None
#    maxnumberofues: Optional[int] = None
