# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:49:45
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:08:41

from fastapi import APIRouter, Header, Response, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from schemas import ue as ue_schemas 
from auth.auth import authenticate
from aux.constants import SLICE_UES, NETWORK_SLICES
import logging

# start the router
router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)

@router.post(
    "/post",
    tags=["UE"],
    summary="Create a new UE and associate it with a slice",
    description="Create a new UE and associate it with a slice.",
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Created",
                        "data": {
                            "IMSI":1,
                            "numIMSIs":2,
                            "slice":"second_slice",
                            "IPV4":"",
                            "IPV6":"",
                            "AMDATA":True,
                            "DEFAULT":"TRUE",
                            "UEcanSendSNSSAI":"TRUE",
                            "AMBRUP":2000000,
                            "AMBRDW":2000000,
                            "id":1,
                            "operational_state":"ENABLED",
                            "SNSSAI":"1-222222",
                            "IMSIGroupNAME":"second_slice1"
                        }
                    }
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Error",
                        "reason": "unknown"
                    }
                }
            }
        },
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail":"Invalid authentication credentials"
                    }
                }
            }
        },
        
    }
)
def create_ue(
    ue: ue_schemas.UEBase,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    filtered_ue = {key: value for key, value in ue.dict().items()}

    # If IMSI == -1 -> return error
    if filtered_ue["IMSI"] == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Error", "reason": "uknown"}
        )
        
    filtered_ue["id"] = 1
    filtered_ue["operational_state"] = "ENABLED"
    filtered_ue["SNSSAI"] = "1-222222"
    filtered_ue["DNN"] = filtered_ue["slice"]
    filtered_ue["IMSIGroupNAME"] = filtered_ue["slice"] + \
        str(filtered_ue["IMSI"])
    
    # Store UE in mock database
    slice_name = filtered_ue["slice"]
    if slice_name not in SLICE_UES:
        SLICE_UES[slice_name] = []
    SLICE_UES[slice_name].append(filtered_ue)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"description": "Created", "data": filtered_ue})


@router.delete(
    "/{slice}/delete_slice",
    tags=["UE"],
    summary="Delete all Network Slice UEs",
    description="Delete all UEs associated with a specific network slice",
    status_code=204,
    responses={
        204: {
            "description": "Deleted",
            "headers": {
                "description": {
                    "description": "Deleted",
                    "schema": {"type": "string"}
                }
            }
        },
        401: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid authentication credentials"
                    }
                }
            }
        },
        475: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "c1, c2 commands failed when deleting UEs"
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Not Found"
                    }
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Bad request",
                        "errors": "Exception String"
                    }
                }
            }
        }
    }
)
async def delete_ues_by_slice(
    slice: str,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 475 - Simulated command failure (triggered by special slice name "fail_475_0")
    if slice.lower() == "fail_475_0":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed when deleting UEs"
            }
        )
    
    # HTTP 400 - Simulated bad request (triggered by special slice name "fail_400_0")
    if slice.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 404 - Slice does not exist
    if slice not in NETWORK_SLICES and slice not in SLICE_UES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    # Delete all UEs for this slice from mock database
    if slice in SLICE_UES:
        del SLICE_UES[slice]
    
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None,
        headers={"description": "Deleted"}
    )


