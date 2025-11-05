#!/bin/bash
# @Author: Miguel Figueiredo (Test Suite generated with AI)
# @Date:   2025-11-05
# Test script for PATCH /productOrder/{id}/patch endpoint
# Tests all response codes: 200 (success), 475, 405, 404, 400, 401

BASE_URL="127.0.0.1:8000"
AUTH_HEADER="Authorization: Basic YWRtaW46cGFzc3dvcmQ="
INVALID_AUTH_HEADER="Authorization: Basic YWRtaW46YWRtaW4="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "Testing PATCH /productOrder/{id}/patch - Update Network Slice"
echo "=================================================="
echo ""

# Setup
echo -e "${YELLOW}Setting up test data...${NC}"
curl -s --request POST "http://${BASE_URL}/clear/all" --header "${AUTH_HEADER}" > /dev/null

curl -s --request POST "http://${BASE_URL}/productOrder/post" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
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
echo ""

# Test 1: HTTP 200 - Success
echo -e "${GREEN}Test 1: HTTP 200 - Successful update${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
    "name": "test_updated",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT", "PDA"], 
    "sst": 1, 
    "sd": "222222", 
    "dnn": "test.eu", 
    "prioritylabel": 95,
    "reliability": 99.5, 
    "dllatency": 25, 
    "ullatency": 25,
    "delaytolerance": "NOT_SUPPORTED", 
    "dldeterministiccomm": "NOT_SUPPORTED", 
    "uldeterministiccomm": "NOT_SUPPORTED",
    "ulguathptperue": 30000,
    "ulmaxthptperue": 60000,
    "dlguathptperue": 30000,
    "dlmaxthptperue": 60000,
    "n6protection":[{"type":"PCC Rule","name":"rule_any"}] 
}' | jq .
echo ""
echo ""

# Test 2: HTTP 475 - Command failure (returns data request payload back with id)
echo -e "${YELLOW}Test 2: HTTP 475 - Command failure during update (name = fail_475_0) [returns data request payload back with id]${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
    "name": "fail_475_0",
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
}' | jq .
echo ""
echo ""

# Test 3: HTTP 475 - Command failure (returns only message)
echo -e "${YELLOW}Test 3: HTTP 475 - Command failure during update (name = fail_475_1) [returns only message]${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update",
    "name": "fail_475_1",
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
}' | jq .
echo ""
echo ""

# Test 4: HTTP 405 - Reserved DNN
echo -e "${YELLOW}Test 4: HTTP 405 - Reserved DNN${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "222222", 
    "dnn": "operator", 
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
}' | jq .
echo ""
echo ""

# Test 5: HTTP 405 - Reserved SST/SD combination
echo -e "${YELLOW}Test 5: HTTP 405 - Reserved SST/SD combination${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED", 
    "coverage_area": ["IT"], 
    "sst": 1, 
    "sd": "010101", 
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
}' | jq .
echo ""
echo ""

# Test 6: HTTP 405 - Reserved rule name
echo -e "${YELLOW}Test 6: HTTP 405 - Reserved rule name${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
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
    "n6protection":[{"type":"PCC Rule","name":"admin_rule"}] 
}' | jq .
echo ""
echo ""

# Test 7: HTTP 405 - Standard slice cannot be updated (slice1 is a standard slice)
echo -e "${YELLOW}Test 7: HTTP 405 - Standard slice cannot be updated${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/slice1/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "slice1", 
    "name": "slice1",
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
}' | jq .
echo ""
echo ""

# Test 8: HTTP 404 - Slice not found
echo -e "${YELLOW}Test 8: HTTP 404 - NetworkSlice ID does not exist${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/nonexistent/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "nonexistent", 
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
}' | jq .
echo ""
echo ""

# Test 9: HTTP 400 - Bad request (name = fail_400_0)
echo -e "${RED}Test 9: HTTP 400 - Bad request (name = fail_400_0)${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${AUTH_HEADER}" \
--data '{
    "id": "test_update", 
    "name": "fail_400_0",
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
}' | jq .
echo ""
echo ""

# Test 10: HTTP 401 - Invalid credentials
echo -e "${RED}Test 10: HTTP 401 - Invalid authentication credentials${NC}"
echo "-------------------------------------------"
curl -s --request PATCH "http://${BASE_URL}/productOrder/test_update/patch" \
--header 'Content-Type: application/json' \
--header "${INVALID_AUTH_HEADER}" \
--data '{
    "id": "test_update", 
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
}' | jq .
echo ""
echo ""

echo "=================================================="
echo "Testing Complete"
echo "=================================================="
