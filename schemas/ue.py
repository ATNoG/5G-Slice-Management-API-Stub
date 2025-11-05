# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:02:51
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-05 16:42:24
from pydantic import BaseModel
from typing import Optional
import schemas.enums as enums

class UE(BaseModel):
    IMSI: int
    numIMSIs: int 
    slice: str 
    IPV4: str
    IPV6: str
    AMDATA: bool
    DEFAULT: str
    UEcanSendSNSSAI: str
    AMBRUP: Optional[int] = None
    AMBRDW: Optional[int] = None


class UEBase(BaseModel):
    operational_state: Optional[enums.OperationalState]=enums.OperationalState.DISABLED
    IMSI: int
    numIMSIs: Optional[int]=1
    slice: str
    IPV4: Optional[str]=None
    IPV6: Optional[str]=None
    AMDATA: Optional[bool]=True
    DEFAULT: Optional[enums.CustomBoolean]=enums.CustomBoolean.TRUE
    UEcanSendSNSSAI: Optional[enums.CustomBoolean]=enums.CustomBoolean.FALSE
    AMBRUP: Optional[int]=None
    AMBRDW: Optional[int]=None

    IPV4count: Optional[int]=None
    UPUnit: Optional[enums.CNThptUnit]=enums.CNThptUnit.Kbps
    DWUnit: Optional[enums.CNThptUnit]=enums.CNThptUnit.Kbps
    SNSSAI: Optional[str]=None
    DNN: Optional[str]=None
    IMSIGroupNAME: Optional[str]=None
    
class UEremover(BaseModel):
    Mode: Optional[enums.UEMode]=enums.UEMode.Implicit
    Type: Optional[enums.UEType]=enums.UEType.ReRegister_Required
    Cause: Optional[enums.UECause]=enums.UECause.ServerNotAllowed
    Customized_Cause: Optional[int]=3

class UEschema(UEBase):
    MultimediaPriorityService: Optional[enums.CustomBoolean]=None
    MissionCriticalService: Optional[enums.CustomBoolean]=None
    HighLatencyComm: Optional[enums.CNHighLatencyCommBuffer]=None
    HighLatenCommBuffer: Optional[int]=None
    MICO: Optional[enums.CustomBoolean]=None
    DNNQOSTPLID: Optional[int]=None

class UEResponse(BaseModel):
    id: int
    IMSI: int
    slice: str
    operational_state: Optional[enums.OperationalState]=enums.OperationalState.DISABLED
    AMDATA: Optional[bool]=True
    SNSSAI: Optional[str]=None
    DNN: Optional[str]=None
    DEFAULT: Optional[enums.CustomBoolean]=enums.CustomBoolean.TRUE
    UEcanSendSNSSAI: Optional[enums.CustomBoolean]=enums.CustomBoolean.FALSE
    IMSIGroupNAME: Optional[str]=None
    numIMSIs: Optional[int]=1


class CNSlice(UEschema):
    class Config:
        orm_mode = True
        