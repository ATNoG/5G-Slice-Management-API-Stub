from fastapi import APIRouter, Header, status, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from auth.auth import authenticate
from aux.constants import STANDARD_SLICES, NETWORK_SLICES, MAX_SLICES
from aux.constants import RESERVED_IDS, RESERVED_DNNS, RESERVED_SST_SD, RESERVED_RULE_NAMES
import logging

# start the router
router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)

@router.get(
    "/{id}/get",
    tags=["OrderIPs"],
    summary="Get Network Slice IP Pool",
    description="Get the IP address pool for a specific Network Slice",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": "10.16.9.37-10.16.9.54"
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
        },
    }
)
async def get_slice_ip_pool(
    id: str,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    if id.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 404 - NetworkSlice does not exist
    if id not in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    # Mock IP pool generation based on slice ID
    # In a real implementation, this would retrieve the actual IP pool
    ip_pool = f"10.16.9.37-10.16.9.54"
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"description": "Success", "data": ip_pool}
    )