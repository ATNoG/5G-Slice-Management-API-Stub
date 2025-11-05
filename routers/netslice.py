# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 16:08:06
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-05 16:43:19

from fastapi import APIRouter, Header, Response, status, Depends, Query
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional, List
from schemas import netslice as netslice_schemas 
from auth.auth import authenticate
from aux.utils import filter_and_stringify_model, convert_to_product_order
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


@router.post(
    "/post",
    tags=["productOrder"],
    summary="Create a new Network Slice Product Order",
    description="Create a new Network Slice Product Order",
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Created",
                        "data": {
                            "description":"Success",
                            "data":{
                                "id":"5GASPHigh",
                                "name":"5gasp",
                                "DNN":"5gasp.eu",
                                "administrative_state":"AdministrativeState.UNLOCKED",
                                "operational_state":"OperationalState.ENABLED",
                                "sst":"1",
                                "sd":"222222",
                                "dllatency":"20",
                                "ullatency":"20",
                                "dlguathptperue":"20000.0",
                                "ulguathptperue":"20000.0",
                                "dlmaxthptperue":"50000.0",
                                "ulmaxthptperue":"50000.0",
                                "delaytolerance":"DelayTolerance.NOT_SUPPORTED",
                                "reliability":"99.9",
                                "dldeterministiccomm":"DeterministicCommAvailability.NOT_SUPPORTED",
                                "uldeterministiccomm":"DeterministicCommAvailability.NOT_SUPPORTED",
                                "coverage_area":{
                                    "IT":"Coverage Area Description"
                                },
                                "n6protections":[{"type": "PCC Rule", "name": "rule_any"}],
                                "kpis":[]
                            }
                        }
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
        476: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"The maximum number of slices created was reached.",
                        "data": "Slice number reached the limit."
                    }
                }
            }
        },
        475: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"c1, c2",
                        "data": {
                            # Return body payload back
                            # dnn, n6protection and not KPIs
                            "coverage_area": [
                                "IT"
                            ],
                            "operational_state": "OperationalState.ENABLED",
                            "administrative_state": "AdministrativeState.UNLOCKED",
                            "sst": "1",
                            "sd": "222222",
                            "prioritylabel": "100",
                            "dllatency": "20",
                            "ullatency": "20",
                            "dlguathptperue": "20000.0",
                            "ulguathptperue": "20000.0",
                            "dlmaxthptperue": "50000.0",
                            "ulmaxthptperue": "50000.0",
                            "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                            "reliability": "99.9",
                            "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "n6protection": [{ "type": "PCC Rule", "name": "rule_any"}],
                            "dnn": "test.eu",
                            "name": "fail_475_0",
                            "id": "test_slice_0"
                        }
                    }
                }
            }
        },
        475: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"c1, c2 commands failed during Product order creation",
                        "data": {
                            # TODO not sure about the data in this one
                            "id": "test_slice_1",
                            "name": "fail_475_1",
                            "DNN": "test.eu",
                            "administrative_state": "AdministrativeState.UNLOCKED",
                            "operational_state": "OperationalState.ENABLED",
                            "sst": "1",
                            "sd": "222222",
                            "dllatency": "20",
                            "ullatency": "20",
                            "dlguathptperue": "20000.0",
                            "ulguathptperue": "20000.0",
                            "dlmaxthptperue": "50000.0",
                            "ulmaxthptperue": "50000.0",
                            "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                            "reliability": "99.9",
                            "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "coverage_area": { "IT": "Coverage Area Description" },
                            "n6protections": [{ "type": "PCC Rule", "name": "rule_any" }],
                            "kpis": []
                        }
                    }
                }
            }
        },
        405: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Operation not allowed",
                        "errors": "NetworkSlice ID already exists."
                    }
                }
            }
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "description":"Bad request",
                        "errors": "Exception string"
                    }
                }
            }
        },
    }
)
async def create_product_order(
    product_order: netslice_schemas.NetworkSliceCreate,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # Convert product_order to a dictionary, including empty lists and dicts but excluding None
    # Cast non-list and non-dict values to strings
    filtered_product_order = filter_and_stringify_model(product_order)
    slice_id = filtered_product_order["id"]
    dnn = filtered_product_order["dnn"]
    sst = filtered_product_order["sst"]
    sd = filtered_product_order["sd"]
    name = filtered_product_order.get("name", slice_id)

    # HTTP 476 - Maximum number of slices reached
    if len(NETWORK_SLICES) >= MAX_SLICES:
        return JSONResponse(
            status_code=476,
            content={
                "description": "The maximum number of slices created was reached.",
                "data": "Slice number reached the limit."
            }
        )
    
    # HTTP 405 - Operation not allowed examples
    # Check if ID is reserved
    if slice_id in RESERVED_IDS:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "Slice ID reserved."
            }
        )
    
    # Check if NetworkSlice ID already exists
    if slice_id in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "NetworkSlice ID already exists."
            }
        )
    
    # Check if DNN is reserved
    if dnn in RESERVED_DNNS:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "This DNN cannot be used outside of standard slice."
            }
        )
    
    # Check if SST/SD combination is reserved
    if (sst, sd) in RESERVED_SST_SD:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "This sst and sd combination cannot be used outside of standard slice."
            }
        )
    
    # Check for reserved rule names in n6protection
    n6protection = filtered_product_order.get("n6protection", [])
    for rule in n6protection:
        if isinstance(rule, dict) and rule.get("name") in RESERVED_RULE_NAMES:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={
                    "description": "Operation not allowed",
                    "errors": f"Rule name {rule.get('name')} is reserved."
                }
            )
    
    # HTTP 400 - Bad request (if name == fail_400_0)
    if name and name.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception string"}
        )

    # Convert to ProductOrder response format
    product_order_response = convert_to_product_order(filtered_product_order)

    # HTTP 475 - Simulated command failure (triggered by special name "fail_475_0")
    if name and name.lower() == "fail_475_0":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2",
                "data": filtered_product_order
            }
        )
    
    # HTTP 475 - Simulated command failure (triggered by special name "fail_475_1")
    if name and name.lower() == "fail_475_1":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed during Product order creation",
                "data": product_order_response
            }
        )
    
    # Store in mock database (using response format)
    NETWORK_SLICES[slice_id] = product_order_response
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content={"description": "Success", "data": product_order_response}
    )


@router.get(
    "/get",
    tags=["productOrder"],
    summary="Get Network Slices",
    description="Get all Network Slice Product Orders (CSMF Get Products)",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": [
                            {
                                "id": "test_slice_1",
                                "name": "test1",
                                "DNN": "test1.eu",
                                "administrative_state": "AdministrativeState.UNLOCKED",
                                "operational_state": "OperationalState.ENABLED",
                                "sst": "1",
                                "sd": "222221",
                                "dllatency": "20",
                                "ullatency": "20",
                                "dlguathptperue": "20000.0",
                                "ulguathptperue": "20000.0",
                                "dlmaxthptperue": "50000.0",
                                "ulmaxthptperue": "50000.0",
                                "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                                "reliability": "99.9",
                                "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                                "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                                "coverage_area": { "IT": "Coverage Area Description" },
                                "n6protections": [{ "type": "PCC Rule", "name": "rule_any" }],
                                "kpis": []
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
        },
    }
)
async def get_product_orders(
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to return"),
    offset: Optional[int] = Query(None, description="Number of items to skip"),
    limit: Optional[int] = Query(None, description="Maximum number of items to return"),
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    if not NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    if (limit is not None and limit < 0) or (offset is not None and offset < 0):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception string"}
        )
    
    # Get all slices and apply pagination
    all_slices = list(NETWORK_SLICES.values())
    total_count = len(all_slices)
    start = offset if offset is not None else 0
    end = start + limit if limit is not None else total_count
    slices = all_slices[start:end]
    
    # Filter fields if requested
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        slices = [
            {k: v for k, v in slice_data.items() if k in field_list}
            for slice_data in slices
        ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"description": "Success", "data": slices},
        headers={"X-Result-Count": str(len(slices)), "X-Total-Count": str(total_count)}
    )


@router.get(
    "/{id}/get",
    tags=["productOrder"],
    summary="Get Network Slice By ID",
    description="Get a specific Network Slice Product Order by ID (CSMF Get Product by ID)",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Success",
                        "data": {
                            "id": "test_slice",
                            "name": "test",
                            "DNN": "test.eu",
                            "administrative_state": "AdministrativeState.UNLOCKED",
                            "operational_state": "OperationalState.ENABLED",
                            "sst": "1",
                            "sd": "222222",
                            "dllatency": "20",
                            "ullatency": "20",
                            "dlguathptperue": "20000.0",
                            "ulguathptperue": "20000.0",
                            "dlmaxthptperue": "50000.0",
                            "ulmaxthptperue": "50000.0",
                            "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                            "reliability": "99.9",
                            "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "coverage_area": {"IT": "Coverage Area Description", "PDA": "Coverage Area Description"},
                            "n6protections": [{ "type": "PCC Rule", "name": "rule_any" }],
                            "kpis": []
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
        },
    }
)
async def get_product_order_by_id(
    id: str,
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to return"),
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    if id == "-1":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception string"}
        )

    if id not in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"description": "Not Found"}
        )
    
    slice_data = NETWORK_SLICES[id]
    
    # Filter fields if requested
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        slice_data = {k: v for k, v in slice_data.items() if k in field_list}
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"description": "Success", "data": slice_data}
    )


@router.patch(
    "/{id}/patch",
    tags=["productOrder"],
    summary="Patch Network Slice",
    description="Update an existing Network Slice Product Order (CSMF Patch Product)",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Updated",
                        "data": {
                            "id": "test_update",
                            "name": "test_updated",
                            "DNN": "test.eu",
                            "administrative_state": "AdministrativeState.UNLOCKED",
                            "operational_state": "OperationalState.ENABLED",
                            "sst": "1",
                            "sd": "222222",
                            "dllatency": "25",
                            "ullatency": "25",
                            "dlguathptperue": "30000.0",
                            "ulguathptperue": "30000.0",
                            "dlmaxthptperue": "60000.0",
                            "ulmaxthptperue": "60000.0",
                            "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                            "reliability": "99.5",
                            "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "coverage_area": { "IT": "Coverage Area Description", "PDA": "Coverage Area Description"},
                            "n6protections": [{ "type": "PCC Rule", "name": "rule_any" }],
                            "kpis": []
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
                        "description": "c1, c2 commands failed during ProductOrder update",
                        "data": {
                            # returns data request payload back with id (name = fail_475_0)
                            "coverage_area": ["IT"],
                            "operational_state": "OperationalState.ENABLED",
                            "administrative_state": "AdministrativeState.UNLOCKED",
                            "sst": "1",
                            "sd": "222222",
                            "prioritylabel": "100",
                            "dllatency": "20",
                            "ullatency": "20",
                            "dlguathptperue": "20000.0",
                            "ulguathptperue": "20000.0",
                            "dlmaxthptperue": "50000.0",
                            "ulmaxthptperue": "50000.0",
                            "delaytolerance": "DelayTolerance.NOT_SUPPORTED",
                            "reliability": "99.9",
                            "dldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "uldeterministiccomm": "DeterministicCommAvailability.NOT_SUPPORTED",
                            "n6protection": [{ "type": "PCC Rule", "name": "rule_any"}],
                            "dnn": "test.eu",
                            "name": "fail_475_0",
                            "id": "test_update"
                        }
                    }
                }
            }
        },
        475: {
            "content": {
                "application/json": {
                    "example": {
                        # returns only message (name = fail_475_1)
                        "description": "c1, c2 commands failed during ProductOrder update",
                    }
                }
            }
        },
        405: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Operation not allowed",
                        "errors": "This sst and sd combination cannot be used outside of standard slice."
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Not Found",
                        "errors": "NetworkSlice ID does not exists in ProductOrders"
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
async def patch_product_order(
    id: str,
    product_order: netslice_schemas.NetworkSliceCreate,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 405 - Standard slice cannot be updated
    if id in STANDARD_SLICES:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "Standard slice cannot be updated."
            }
        )
    
    # HTTP 404 - NetworkSlice does not exist
    if id not in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "description": "Not Found",
                "errors": "NetworkSlice ID does not exists in ProductOrders"
            }
        )
    
    # Convert product_order to dictionary
    filtered_product_order = filter_and_stringify_model(product_order)
    dnn = filtered_product_order.get("dnn")
    sst = filtered_product_order.get("sst")
    sd = filtered_product_order.get("sd")
    name = filtered_product_order.get("name", id)
    
    # HTTP 405 - Check if DNN is reserved
    if dnn in RESERVED_DNNS:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "This DNN cannot be used outside of standard slice."
            }
        )
    
    # HTTP 405 - Check if SST/SD combination is reserved
    if (sst, sd) in RESERVED_SST_SD:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "This sst and sd combination cannot be used outside of standard slice."
            }
        )

    # HTTP 475 - Simulated command failure (triggered by special name "fail_475_0")
    if name and name.lower() == "fail_475_0":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2",
                "data": filtered_product_order | {"id": id}
            }
        )
    
    # HTTP 475 - Simulated command failure (triggered by special name "fail_475_1")
    if name and name.lower() == "fail_475_1":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed during ProductOrder update"
            }
        )
    
    if name and name.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception string"}
        )
    
    # Check for reserved rule names in n6protection
    n6protection = filtered_product_order.get("n6protection", [])
    for rule in n6protection:
        if isinstance(rule, dict) and rule.get("name") in RESERVED_RULE_NAMES:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={
                    "description": "Operation not allowed",
                    "errors": f"Rule name {rule.get('name')} is reserved."
                }
            )
    
    # Convert to ProductOrder response format
    response_data = convert_to_product_order(filtered_product_order)
    
    # Update the slice in mock database
    NETWORK_SLICES[id] = response_data
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"description": "Updated", "data": response_data}
    )

@router.delete(
    "/{id}/delete",
    tags=["productOrder"],
    summary="Delete Network Slice",
    description="Delete a Network Slice Product Order",
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
                        "description": "c1, c2 commands failed during Product order deletion"
                    }
                }
            }
        },
        405: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Operation not allowed",
                        "errors": "Standard slice cannot be deleted."
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "description": "Not Found",
                        "errors": "NetworkSlice does not exists"
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
async def delete_product_order(
    id: str,
    authorization: Optional[str] = Header(None),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    # HTTP 475 - Simulated command failure (triggered by special id "delete")
    if id.lower() == "fail_475_0":
        return JSONResponse(
            status_code=475,
            content={
                "description": "c1, c2 commands failed during Product order deletion"
            }
        )
    
    # HTTP 400 - Bad request (if id == fail_400_0)
    if id.lower() == "fail_400_0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"description": "Bad request", "errors": "Exception String"}
        )
    
    # HTTP 405 - Standard slice cannot be deleted
    if id in STANDARD_SLICES:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={
                "description": "Operation not allowed",
                "errors": "Standard slice cannot be deleted."
            }
        )
    
    # HTTP 404 - NetworkSlice does not exist
    if id not in NETWORK_SLICES:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "description": "Not Found",
                "errors": "NetworkSlice does not exists"
            }
        )

    # Delete the slice from mock database
    del NETWORK_SLICES[id]
    
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"description": "Deleted"}
    )

