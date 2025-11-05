# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2025-06-21 09:56:19
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 09:58:56
import os

# Constants for the mock slice manager API
AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "password")

# Mock Structures
NETWORK_SLICES = {}     # Network Slices
SLICE_UES = {}          # UEs associated with slices
MAX_SLICES = 10         # Maximum number of slices allowed

# Constants for Network Slices
STANDARD_SLICES = ["slice1", "slice2"]
RESERVED_IDS = ["admin", "system", "root", "default"]
RESERVED_DNNS = ["operator", "internal"]
RESERVED_SST_SD = [("1", "010101"), ("1", "020202")]
RESERVED_RULE_NAMES = ["system_rule", "admin_rule"]

