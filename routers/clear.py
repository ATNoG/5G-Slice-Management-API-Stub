# -*- coding: utf-8 -*-
# @Author: Miguel Figueiredo
# @Date:   2025-11-02 13:46:28
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-02 13:46:28

from fastapi import APIRouter, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from auth.auth import authenticate
from aux.constants import NETWORK_SLICES, SLICE_UES
import logging

# start the router
router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)


@router.post(
    "/all",
    tags=["clear"],
    summary="Clear All Data",
    description="Clear all network slices and UEs data",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": {
                            "message": "All data has been cleared.",
                            "slices_cleared": 2,
                            "ues_cleared": 2
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
    }
)
async def clear_all(
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    slices_cleared = len(NETWORK_SLICES)
    ues_cleared = sum(len(ues) for ues in SLICE_UES.values())
    SLICE_UES.clear()
    NETWORK_SLICES.clear()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "description": "Success.",
            "data": {
                "slices_cleared": slices_cleared,
                "ues_cleared": ues_cleared
            }
        }
    )

@router.post(
    "/ue",
    tags=["clear"],
    summary="Clear Network Slice UEs Data",
    description="Clear all UEs associated with network slices",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": {
                            "message": "All UEs have been cleared.",
                            "ues_cleared": 2
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
    }
)
async def clear_ue(
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    ues_count = sum(len(ues) for ues in SLICE_UES.values())
    SLICE_UES.clear()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "description": "Success",
            "data": {
                "message": "All UEs have been cleared.",
                "ues_cleared": ues_count
            }
        }
    )


@router.post(
    "/slice",
    tags=["clear"],
    summary="Clear Network Slices Data",
    description="Clear all network slices data",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": {
                            "message": "All network slices have been cleared.",
                            "slices_cleared": 2
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
    }
)
async def clear_slice(
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    slices_count = len(NETWORK_SLICES)
    NETWORK_SLICES.clear()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "description": "Success",
            "data": {
                "message": "All network slices have been cleared.",
                "slices_cleared": slices_count
            }
        }
    )


    
