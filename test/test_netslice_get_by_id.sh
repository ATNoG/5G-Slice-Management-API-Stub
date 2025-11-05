#!/bin/bash
# @Author: Test Suite
# @Date:   2025-11-05
# Test script for GET /productOrder/{id}/get endpoint
# Tests all response codes: 200 (success), 404, 400, 401

BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "Testing GET /productOrder/{id}/get - Get Network Slice By ID"
echo "=================================================="
echo ""

# Setup
echo -e "${YELLOW}Setting up test data...${NC}"
curl -s --request POST "http://${BASE_URL}/clear/all" --header "${AUTH_HEADER}" > /dev/null

curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_slice", 
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT", "PDA"], 
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
echo ""

# Test 1: HTTP 200 - Success
echo -e "${GREEN}Test 1: HTTP 200 - Get slice by ID${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/test_slice/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 2: HTTP 200 - Success with fields filter
echo -e "${GREEN}Test 2: HTTP 200 - Get slice with fields filter (id, name, sst, sd)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/test_slice/get?fields=id,name,sst,sd" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 3: HTTP 404 - Slice not found
echo -e "${YELLOW}Test 3: HTTP 404 - Slice not found${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/nonexistent_slice/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 4: HTTP 400 - (id = -1)
echo -e "${RED}Test 4: HTTP 400 - (id = -1)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/-1/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 5: HTTP 401 - Invalid credentials
echo -e "${RED}Test 5: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/test_slice/get" \
--header "${INVALID_AUTH_HEADER}" | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
