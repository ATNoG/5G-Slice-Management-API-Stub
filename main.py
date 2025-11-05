# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-11 16:29:17
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:11:19
# Fully Generated with AI

from fastapi import FastAPI
from routers import (
    clear as clear_router,
    ue as ue_router,
    netslice as netslice_router,
    orderips as orderips_router
)
import logging


# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

fast_api_tags_metadata = [
    {
        "name": "UE",
        "description": "Operations related with UEs.",
    },
    {
        "name": "productOrder",
        "description": "Operations related with Network Slices.",
    },
    {
        "name": "OrderIPs",
        "description": "Operations related with IPs allocation for Network Slices.",
    },
    {
        "name": "clear",
        "description": "Clear operations (not present in production Slice Manager).",
    },
]

fast_api_description = "ITAv's 5G Slice Management API Mock"


app = FastAPI(
    title="Slice Management API Mock",
    description=fast_api_description,
    version="0.0.1",
    contact={
        "name": "Rafael Direito",
        "email": "rdireito@av.it.pt",
    },
    openapi_tags=fast_api_tags_metadata
)

app.include_router(ue_router.router, prefix="/UE", tags=["UE"])
app.include_router(netslice_router.router, prefix="/productOrder", tags=["productOrder"])
app.include_router(orderips_router.router, prefix="/OrderIPs", tags=["OrderIPs"])
app.include_router(clear_router.router, prefix="/clear", tags=["clear"])