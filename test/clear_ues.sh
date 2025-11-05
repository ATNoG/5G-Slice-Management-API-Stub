#!/bin/bash
# @Author: Miguel Figueiredo
# @Date:   2025-11-05
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-05

# Clear all UEs
# Credentials: admin:password

curl -s --location --request POST '127.0.0.1:8000/clear/ue' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' | jq .
