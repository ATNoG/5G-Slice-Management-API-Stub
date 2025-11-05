# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 10:49:45
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-05 16:43:08

from fastapi import APIRouter, Header, Response, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from routers.response import ResponseWrapper
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
    response_model=ResponseWrapper[ue_schemas.UEResponse],
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Created",
                        "data": {
                            "id": 20,
                            "IMSI": 999080100001125,
                            "slice": "test",
                            "operational_state": "ENABLED",
                            "AMDATA": True,
                            "SNSSAI": "1-222222",
                            "DNN": "test",
                            "DEFAULT": "TRUE",
                            "UEcanSendSNSSAI": "FALSE",
                            "IMSIGroupNAME": "test999080100001125",
                            "numIMSIs": 1
                        }
                    }
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
                        "description": "c1, c2 commands failed when creating UEs",
                        "data": {
                            "id": 20,
                            "IMSI": 999080100001125,
                            "slice": "test",
                            "operational_state": "ENABLED",
                            "AMDATA": True,
                            "SNSSAI": "1-222222",
                            "DNN": "test",
                            "DEFAULT": "TRUE",
                            "UEcanSendSNSSAI": "FALSE",
                            "IMSIGroupNAME": "test999080100001125",
                            "numIMSIs": 1
                        }
                    }
                }
            }
        },
        405: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Not Allowed",
                        "errors": "UE association already exists."
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
def create_ue(
    ue: ue_schemas.UEBase,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    filtered_ue = {key: value for key, value in ue.dict().items() if value is not None}

    # HTTP 400 - Bad request (triggered by IMSI == -1)
    if filtered_ue["IMSI"] == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 405 - Slice does not exist
    slice_name = filtered_ue["slice"]
    if slice_name not in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={"description": "Not Allowed", "errors": "Slice does not exist."}
        )
    
    # HTTP 405 - Check if IMSI already exists
    for slice_ues in SLICE_UES.values():
        for existing_ue in slice_ues:
            if existing_ue["IMSI"] == filtered_ue["IMSI"]:
                return JSONResponse(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    content={"description": "Not Allowed", "errors": "UE association already exists."}
                )
    
    # Generate UE ID
    ue_id = 1
    for slice_ues in SLICE_UES.values():
        ue_id = max(ue_id, max([ue["id"] for ue in slice_ues], default=0) + 1)
    
    filtered_ue["id"] = ue_id
    filtered_ue["operational_state"] = "ENABLED"
    
    # Get SNSSAI from slice
    if slice_name in NETWORK_SLICES:
        slice_data = NETWORK_SLICES[slice_name]
        sst = slice_data.get("sst", "1")
        sd = slice_data.get("sd", "222222")
        filtered_ue["SNSSAI"] = f"{sst}-{sd}"
        filtered_ue["DNN"] = slice_data.get("DNN", slice_name)
    else:
        filtered_ue["SNSSAI"] = "1-222222"
        filtered_ue["DNN"] = slice_name
    
    filtered_ue["IMSIGroupNAME"] = slice_name + str(filtered_ue["IMSI"])
    
    # HTTP 475 - Simulated command failure (triggered by special slice name "delete")
    if slice_name.lower() == "delete":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed when creating UEs",
                "data": filtered_ue
            }
        )
    
    # Store UE in mock database
    if slice_name not in SLICE_UES:
        SLICE_UES[slice_name] = []
    SLICE_UES[slice_name].append(filtered_ue)
    
    return {"description": "Created", "data": filtered_ue}


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
        headers={"description": "Deleted"}
    )


@router.get(
    "/{slice}/get_slice",
    tags=["UE"],
    summary="Get UEs by Slice",
    description="Get all UEs associated with a specific network slice",
    status_code=200,
    response_model=ResponseWrapper[list[ue_schemas.UEResponse]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": [
                            {
                                "id": 20,
                                "IMSI": 999080100001125,
                                "slice": "test",
                                "operational_state": "ENABLED",
                                "AMDATA": True,
                                "SNSSAI": "1-222222",
                                "DNN": "test",
                                "DEFAULT": "TRUE",
                                "UEcanSendSNSSAI": "FALSE",
                                "IMSIGroupNAME": "test999080100001125",
                                "numIMSIs": 1
                            }
                        ]
                    }
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
async def get_ues_by_slice(
    slice: str,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 400 - Simulated bad request (triggered by special slice name "fail_400_0")
    if slice.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 404 - Slice does not exist or has no UEs
    if slice not in SLICE_UES or len(SLICE_UES[slice]) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    return {"description": "Success", "data": SLICE_UES[slice]}


@router.get(
    "/{imsi}/get_IMSI",
    tags=["UE"],
    summary="Get UE by IMSI",
    description="Get UE information by IMSI number",
    status_code=200,
    response_model=ResponseWrapper[list[ue_schemas.UEResponse]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": [
                            {
                                "id": 20,
                                "IMSI": 999080100001125,
                                "slice": "test",
                                "operational_state": "ENABLED",
                                "AMDATA": True,
                                "SNSSAI": "1-222222",
                                "DNN": "test",
                                "DEFAULT": "TRUE",
                                "UEcanSendSNSSAI": "FALSE",
                                "IMSIGroupNAME": "test999080100001125",
                                "numIMSIs": 1
                            }
                        ]
                    }
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
async def get_ue_by_imsi(
    imsi: int,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 400 - Simulated bad request (triggered by IMSI == -1)
    if imsi == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # Search for UE with this IMSI across all slices
    found_ues = []
    for slice_ues in SLICE_UES.values():
        for ue in slice_ues:
            if ue["IMSI"] == imsi:
                found_ues.append(ue)
    
    # HTTP 404 - IMSI not found
    if len(found_ues) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    return {"description": "Success", "data": found_ues}


@router.get(
    "/{id}/get",
    tags=["UE"],
    summary="Get UE by ID",
    description="Get UE information by ID",
    status_code=200,
    response_model=ResponseWrapper[ue_schemas.UEResponse],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": {
                            "id": 20,
                            "IMSI": 999080100001125,
                            "slice": "test",
                            "operational_state": "ENABLED",
                            "AMDATA": True,
                            "SNSSAI": "1-222222",
                            "DNN": "test",
                            "DEFAULT": "TRUE",
                            "UEcanSendSNSSAI": "FALSE",
                            "IMSIGroupNAME": "test999080100001125",
                            "numIMSIs": 1
                        }
                    }
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
async def get_ue_by_id(
    id: int,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 400 - Simulated bad request (triggered by ID == -1)
    if id == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # Search for UE with this ID across all slices
    for slice_ues in SLICE_UES.values():
        for ue in slice_ues:
            if ue["id"] == id:
                return {"description": "Success", "data": ue}

    # HTTP 404 - ID not found
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"description": "Not Found"}
    )


@router.get(
    "/get",
    tags=["UE"],
    summary="Get All UEs",
    description="Get all UEs across all network slices",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": [
                            {
                                "id": 5,
                                "IMSI": 999080100001122,
                                "slice": "huawei.com",
                                "operational_state": "DISABLED",
                                "AMDATA": False,
                                "SNSSAI": "1-010101",
                                "DNN": "huawei.com",
                                "DEFAULT": "TRUE",
                                "UEcanSendSNSSAI": "FALSE",
                                "IMSIGroupNAME": "huawei.com999080100001122",
                                "numIMSIs": 1
                            }
                        ]
                    }
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
async def get_all_ues(
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # Collect all UEs from all slices
    all_ues = []
    for slice_ues in SLICE_UES.values():
        for ue in slice_ues:
            all_ues.append(ue_schemas.UEResponse.model_validate(ue).model_dump())
    
    # HTTP 404 - No UEs found
    if len(all_ues) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    # Simulate Bad Request when there are exactly 3 UEs
    if len(all_ues) == 10:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )

    # Return with custom headers for count
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"description": "Success", "data": all_ues},
        headers={
            "X-Result-Count": str(len(all_ues)),
            "X-Total-Count": str(len(all_ues))
        }
    )


@router.delete(
    "/{imsi}/delete_IMSI",
    tags=["UE"],
    summary="Delete UE by IMSI",
    description="Delete a UE by its IMSI number",
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
async def delete_ue_by_imsi(
    imsi: int,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 400 - Simulated bad request (triggered by IMSI == -1)
    if imsi == -1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 475 - Simulated command failure (triggered by special IMSI == 999999999999999)
    if imsi == 999999999999999:
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed when deleting UEs"
            },
            headers={"description": "Deleted"}
        )
    
    # Search for and delete UE with this IMSI
    found = False
    for slice_name, slice_ues in SLICE_UES.items():
        for i, ue in enumerate(slice_ues):
            if ue["IMSI"] == imsi:
                slice_ues.pop(i)
                found = True
                break
        if found:
            break
    
    # HTTP 404 - IMSI not found
    if not found:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"description": "Deleted"}
    )


