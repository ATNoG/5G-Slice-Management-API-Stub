#!/bin/bash
# @Author: Test Suite
# @Date:   2025-11-05
# Test script for GET /productOrder/get endpoint
# Tests all response codes: 200 (success), 404, 400, 401

# Base URL and credentials
BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================================="
echo "Testing GET /productOrder/get - Get All Network Slices"
echo "=================================================="
echo ""

# Clear and setup test data
echo -e "${YELLOW}Setting up test data...${NC}"
curl -s --request POST "http://${BASE_URL}/clear/all" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" > /dev/null

# Create some test slices
for i in {1..3}; do
    curl -s --request POST "http://${BASE_URL}/productOrder/post" \
    --header 'Content-Type: application/json' \
    --header "${AUTH_HEADER}" \
    --data "{
        \"id\": \"test_slice_${i}\", 
        \"name\": \"test${i}\",
        \"administrative_state\": \"UNLOCKED\", 
        \"operational_state\": \"ENABLED\", 
        \"coverage_area\": [\"IT\"], 
        \"sst\": 1, 
        \"sd\": \"22222${i}\", 
        \"dnn\": \"test${i}.eu\", 
        \"prioritylabel\": 100,
        \"reliability\": 99.9, 
        \"dllatency\": 20, 
        \"ullatency\": 20,
        \"delaytolerance\": \"NOT_SUPPORTED\", 
        \"dldeterministiccomm\": \"NOT_SUPPORTED\", 
        \"uldeterministiccomm\": \"NOT_SUPPORTED\",
        \"ulguathptperue\": 20000,
        \"ulmaxthptperue\": 50000,
        \"dlguathptperue\": 20000,
        \"dlmaxthptperue\": 50000,
        \"n6protection\":[{\"type\":\"PCC Rule\",\"name\":\"rule_any\"}] 
    }" > /dev/null
done
echo ""

# Test 1: HTTP 200 - Success (Get all)
echo -e "${GREEN}Test 1: HTTP 200 - Get all slices${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 2: HTTP 200 - Success with fields filter
echo -e "${GREEN}Test 2: HTTP 200 - Get slices with fields filter (id, name, DNN)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get?fields=id,name,DNN" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 3: HTTP 200 - Success with pagination (offset and limit)
echo -e "${GREEN}Test 3: HTTP 200 - Get slices with pagination (offset=1, limit=2)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get?offset=1&limit=2" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 4: HTTP 404 - No slices found
echo -e "${YELLOW}Test 4: HTTP 404 - No slices found${NC}"
echo "-------------------------------------------"
curl -s --request POST "http://${BASE_URL}/clear/slice" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" > /dev/null

curl -s --request GET "http://${BASE_URL}/productOrder/get" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Recreate slices for remaining tests
for i in {1..3}; do
    curl -s --request POST "http://${BASE_URL}/productOrder/post" \
    --header 'Content-Type: application/json' \
    --header "${AUTH_HEADER}" \
    --data "{
        \"id\": \"test_slice_${i}\", 
        \"name\": \"test${i}\",
        \"administrative_state\": \"UNLOCKED\", 
        \"operational_state\": \"ENABLED\", 
        \"coverage_area\": [\"IT\"], 
        \"sst\": 1, 
        \"sd\": \"22222${i}\", 
        \"dnn\": \"test${i}.eu\", 
        \"prioritylabel\": 100,
        \"reliability\": 99.9, 
        \"dllatency\": 20, 
        \"ullatency\": 20,
        \"delaytolerance\": \"NOT_SUPPORTED\", 
        \"dldeterministiccomm\": \"NOT_SUPPORTED\", 
        \"uldeterministiccomm\": \"NOT_SUPPORTED\",
        \"ulguathptperue\": 20000,
        \"ulmaxthptperue\": 50000,
        \"dlguathptperue\": 20000,
        \"dlmaxthptperue\": 50000,
        \"n6protection\":[{\"type\":\"PCC Rule\",\"name\":\"rule_any\"}] 
    }" > /dev/null
done

# Test 5: HTTP 400 - Bad request (negative offset)
echo -e "${RED}Test 5: HTTP 400 - Bad request (negative offset)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get?offset=-1" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 6: HTTP 400 - Bad request (negative limit)
echo -e "${RED}Test 6: HTTP 400 - Bad request (negative limit)${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get?limit=-5" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 7: HTTP 401 - Invalid credentials
echo -e "${RED}Test 7: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
curl -s --request GET "http://${BASE_URL}/productOrder/get" \
--header 'Content-Type: application/json' \
--header "${INVALID_AUTH_HEADER}" | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
