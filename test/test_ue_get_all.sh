#!/bin/bash
# @Author: Test Suite
# @Date:   2025-11-05
# Test script for GET /UE/get endpoint
# Tests all response codes: 200 (success), 401, 404, 400

BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "Testing GET /UE/get - Get All UEs"
echo "=================================================="
echo ""

# Setup
echo -e "${YELLOW}Setting up test data...${NC}"
curl -s --request POST "http://${BASE_URL}/clear/all" --header "${AUTH_HEADER}" > /dev/null

# Create test slices
curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test1", 
    "name": "test1",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222222", 
    "dnn": "test1.eu", 
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

curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test2", 
    "name": "test2",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222223", 
    "dnn": "test2.eu", 
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

# Create UEs on different slices
curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "IMSI": 999080100001125,
    "numIMSIs": 1,
    "slice": "test1",
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
    "slice": "test2",
    "IPV4": "",
    "IPV6": "",
    "AMDATA": true,
    "DEFAULT": "TRUE",
    "UEcanSendSNSSAI": "FALSE",
    "AMBRUP": 4000000,
    "AMBRDW": 4000000
}' > /dev/null


# Test 1: HTTP 200 - Success
echo -e "${GREEN}Test 1: HTTP 200 - Successful retrieval of all UEs${NC}"
echo "-------------------------------------------"
echo "Response with headers:"
curl -i -s --request GET "http://${BASE_URL}/UE/get" \
--header "${AUTH_HEADER}" | grep -E "HTTP|X-Result-Count|X-Total-Count"
echo ""
echo "Response body:"
curl -s --request GET "http://${BASE_URL}/UE/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 2: HTTP 401 - Invalid credentials
echo -e "${RED}Test 2: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/get" \
--header "${INVALID_AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 3: HTTP 404 - No UEs found
echo -e "${YELLOW}Test 3: HTTP 404 - No UEs found (after clearing)${NC}"
echo "-------------------------------------------"
curl -s --request POST "http://${BASE_URL}/clear/ue" --header "${AUTH_HEADER}" > /dev/null
curl -s --request GET "http://${BASE_URL}/UE/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Create test slice and exactly 10 UEs
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

for i in {1..10}; do
    curl -s --request POST "http://${BASE_URL}/UE/post" \
    --header 'Content-Type: application/json' \
    --header "${AUTH_HEADER}" \
    --data "{
        \"IMSI\": $((999080100001100 + i)),
        \"numIMSIs\": 1,
        \"slice\": \"test\",
        \"IPV4\": \"\",
        \"IPV6\": \"\",
        \"AMDATA\": true,
        \"DEFAULT\": \"TRUE\",
        \"UEcanSendSNSSAI\": \"FALSE\",
        \"AMBRUP\": 4000000,
        \"AMBRDW\": 4000000
    }" > /dev/null
done

# Test 4: HTTP 400 - Bad request (when there are exactly 10 UEs)
echo -e "${RED}Test 4: HTTP 400 - Bad request (when there are exactly 10 UEs)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/UE/get" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
