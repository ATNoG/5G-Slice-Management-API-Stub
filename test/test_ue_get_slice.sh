#!/bin/bash
# @Author: Miguel Figueiredo (Test Suite generated with AI)
# @Date:   2025-11-05
# Test script for GET /UE/{slice}/get_slice endpoint
# Tests all response codes: 200 (success), 401, 404, 400

BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "Testing GET /UE/{slice}/get_slice - Get UEs by Slice"
echo "=================================================="
echo ""

# Setup
echo -e "${YELLOW}Setting up test data...${NC}"
curl -s --request POST "http://${BASE_URL}/clear/all" --header "${AUTH_HEADER}" > /dev/null

# Create test slice
curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test", 
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222222", 
    "dnn": "test.eu", 
    "prioritylabel": 100,
    "reliability": 99.9, 
    "dllatency": 20, 
    "ullatency": 20,
    "delaytolerance": "NOT_SUPPORTED", 
    "dldeterministiccomm": "NOT_SUPPORTED", 
    "uldeterministiccomm": "NOT_SUPPORTED",
    "ulguathptperue": 20000,
    "ulmaxthptperue": 50000,
    "dlguathptperue": 20000,
    "dlmaxthptperue": 50000,
    "n6protection":[{"type":"PCC Rule","name":"rule_any"}] 
}' > /dev/null

# Create UEs on test slice
curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "IMSI": 999080100001125,
    "numIMSIs": 1,
    "slice": "test",
    "IPV4": "",
    "IPV6": "",
    "AMDATA": true,
    "DEFAULT": "TRUE",
    "UEcanSendSNSSAI": "FALSE",
    "AMBRUP": 4000000,
    "AMBRDW": 4000000
}' > /dev/null

curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "IMSI": 999080100001126,
    "numIMSIs": 1,
    "slice": "test",
    "IPV4": "",
    "IPV6": "",
    "AMDATA": true,
    "DEFAULT": "TRUE",
    "UEcanSendSNSSAI": "FALSE",
    "AMBRUP": 4000000,
    "AMBRDW": 4000000
}' > /dev/null
echo ""

# Test 1: HTTP 200 - Success
echo -e "${GREEN}Test 1: HTTP 200 - Successful retrieval of UEs by slice${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/test/get_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 2: HTTP 401 - Invalid credentials
echo -e "${RED}Test 2: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/test/get_slice" \
--header "${INVALID_AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 3: HTTP 404 - Slice not found
echo -e "${YELLOW}Test 3: HTTP 404 - Slice does not exist${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/nonexistent/get_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 4: HTTP 400 - Bad request
echo -e "${RED}Test 4: HTTP 400 - Bad request${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/fail_400_0/get_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
