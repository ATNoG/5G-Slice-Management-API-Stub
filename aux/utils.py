# -*- coding: utf-8 -*-
# @Author: Miguel Figueiredo
# @Date:   2025-11-02 13:05:42
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-02 13:05:42


from pydantic import BaseModel
from typing import Dict, Any, Union
from schemas.netslice import NetworkSliceCreate, ProductOrder
import logging

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)


def filter_and_stringify_model(data: BaseModel) -> Dict[str, Any]:
    """
    Filter and transform a pydantic body by:
    - Converting it to a dictionary
    - Including empty lists and dicts
    - Excluding keys with None values
    - Converting non-list and non-dict values to strings
    
    Args:
        data: Pydantic model to filter and transform

    Returns:
        Filtered dictionary with non-collection values converted to strings
    """
    return {
        key: str(value) if not isinstance(value, (list, dict)) else value
        for key, value in data.model_dump().items()
        if value is not None or isinstance(value, (list, dict))
    }


def convert_to_product_order(payload: Union[NetworkSliceCreate, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert a NetworkSliceCreate payload or filtered dictionary to ProductOrder response format.
    
    This function transforms the input slice data into the response format by:
    - Converting 'dnn' field to 'DNN'
    - Transforming coverage_area list to dictionary with descriptions
    - Converting 'n6protection' to 'n6protections'
    - Cleaning n6protection rules (removing None values)
    - Adding empty 'kpis' list
    - Converting enum values to strings
    
    Args:
        payload: NetworkSliceCreate model or filtered dictionary from filter_and_stringify_model
        
    Returns:
        Dictionary matching ProductOrder schema for API responses
    """
    # Convert to dict if it's a Pydantic model
    if isinstance(payload, BaseModel):
        data = filter_and_stringify_model(payload)
    else:
        data = payload.copy()
    
    # Transform coverage_area from list to dict with descriptions
    coverage_area = data.get("coverage_area", [])
    if isinstance(coverage_area, list):
        data["coverage_area"] = {
            area: "Coverage Area Description" for area in coverage_area
        }
    
    # Clean n6protection rules - remove None values from each rule
    n6protection = data.get("n6protection", [])
    if n6protection:
        data["n6protection"] = [
            {k: v for k, v in rule.items() if v is not None} 
            for rule in n6protection
        ]
    
    # Convert 'dnn' to 'DNN' for response
    if "dnn" in data:
        data["DNN"] = data.pop("dnn")
    
    # Set 'n6protections' (plural) from 'n6protection'
    data["n6protections"] = data.get("n6protection", [])
    
    # Add empty kpis list if not present
    if "kpis" not in data:
        data["kpis"] = []
    
    # Create ProductOrder model to validate structure
    try:
        product_order = ProductOrder(**data)
        # Return as dict, excluding None values
        return {k: v for k, v in product_order.model_dump().items() if v is not None}
    except Exception:
        logging.info("Validation to ProductOrder failed.", exc_info=True)
        return data
