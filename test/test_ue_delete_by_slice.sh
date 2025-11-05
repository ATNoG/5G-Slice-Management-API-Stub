#!/bin/bash
# @Author: Test Suite
# @Date:   2025-11-05
# Test script for DELETE /UE/{slice}/delete_slice endpoint
# Tests all response codes: 204 (success), 475, 404, 400, 401

BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "Testing DELETE /UE/{slice}/delete_slice - Delete UEs by Slice"
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
    "id": "test_ue_deletion", 
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

# Create UEs on the slice
curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "slice_id": "test_ue_deletion",
    "imsi": "999700000000001",
    "msisdn": "351999000001",
    "static_ip": "192.168.0.10"
}' > /dev/null

curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "slice_id": "test_ue_deletion",
    "imsi": "999700000000002",
    "msisdn": "351999000002",
    "static_ip": "192.168.0.11"
}' > /dev/null

# Create another test slice for command failure
curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "delete", 
    "name": "delete_test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222223", 
    "dnn": "delete.eu", 
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

curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "slice_id": "delete",
    "imsi": "999700000000003",
    "msisdn": "351999000003",
    "static_ip": "192.168.0.12"
}' > /dev/null
echo ""

# Test 1: HTTP 204 - Success
echo -e "${GREEN}Test 1: HTTP 204 - Successful UE deletion${NC}"
echo "-------------------------------------------"
echo "Response:"
curl -i -s --request DELETE "http://${BASE_URL}/UE/test_ue_deletion/delete_slice" \
--header "${AUTH_HEADER}" | grep -E "HTTP|description"
echo ""
echo ""

# Test 2: HTTP 475 - Command failure
echo -e "${YELLOW}Test 2: HTTP 475 - Command failure during UE deletion${NC}"
echo "-------------------------------------------"
curl -s --request DELETE "http://${BASE_URL}/UE/fail_475_0/delete_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 3: HTTP 404 - Slice not found
echo -e "${YELLOW}Test 3: HTTP 404 - NetworkSlice does not exist${NC}"
echo "-------------------------------------------"
curl -s --request DELETE "http://${BASE_URL}/UE/nonexistent/delete_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 4: HTTP 400 - Bad request
echo -e "${RED}Test 4: HTTP 400 - Bad request${NC}"
echo "-------------------------------------------"

curl -s --request DELETE "http://${BASE_URL}/UE/fail_400_0/delete_slice" \
--header "${AUTH_HEADER}" | jq .
echo ""
echo ""

# Test 5: HTTP 401 - Invalid credentials
echo -e "${RED}Test 5: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
# Create another slice for auth test
curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_auth_ue", 
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222225", 
    "dnn": "auth.eu", 
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

curl -s --request POST "http://${BASE_URL}/UE/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "slice_id": "test_auth_ue",
    "imsi": "999700000000005",
    "msisdn": "351999000005",
    "static_ip": "192.168.0.14"
}' > /dev/null

curl -s --request DELETE "http://${BASE_URL}/UE/test_auth_ue/delete_slice" \
--header "${INVALID_AUTH_HEADER}" | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
