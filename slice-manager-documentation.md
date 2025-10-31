# Authentication

All Slice Manager's endpoints are protected (basic auth). Therefore, the request should be made with this in mind. See the example below.

```python
# Make a GET request with Basic Auth
response = requests.get(url, auth=HTTPBasicAuth(username, password))
```

# Requests

## 1. Network Slices

### 1.1 - Create Network Slice (CSMF Product Create)


`POST http://{{slice_manager_url}}/productOrder/post`

**Payload:**

``` json
{
    "id": "test", // str not allowed [,;="']
    "name": "test",
    "administrative_state": "UNLOCKED", //LOCKED - UNLOCKED - SHUTTINGDOWN
    "operational_state": "ENABLED", // ENABLED - DISABLED
    "coverage_area": ["IT"], //["IT","PDA"]
    "sst": 1, // int 0 - 255
    "sd": "222222", //str "6 numbers" 
    // usar o mesmo sd para as slices dinamicas
    "dnn": "test", //str
    "prioritylabel": 95, //int 0 - 100
    
    "reliability": 99, //float 0-100
    "dllatency": 5, //int milliseconds
    "ullatency": 5, //int milliseconds
    
    // ------- Input from André Perdigão is Needed --------- //
    "delaytolerance": "NOT_SUPPORTED", //str SUPPORTED - NOT_SUPPORTED
    "dldeterministiccomm": "NOT_SUPPORTED", //str SUPPORTED - NOT_SUPPORTED
    "uldeterministiccomm": "NOT_SUPPORTED", //str SUPPORTED - NOT_SUPPORTED
    // ----------------------------------------------------- //
    
    "ulguathptperue": 30000,//int kbit/s -> (30mbit/s)
    "ulmaxthptperue": 30000,//int kbit/s -> (30mbit/s)
    "dlguathptperue": 30000,//int kbit/s -> (30mbit/s)
    "dlmaxthptperue": 30000,//int kbit/s -> (30mbit/s)
    
    "n6protection":[{"type":"PCC Rule","name":"rule_any"}] //default rule allows all types of communications
}
```

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 201** | ``` {"description":"Success","data":{"id":"test","name":"test","DNN":"test","administrative_state":"UNLOCKED","operational_state":"ENABLED","sst":"1","sd":"222222","dllatency":"5","ullatency":"5","dlguathptperue":"30000.0","ulguathptperue":"30000.0","dlmaxthptperue":"30000.0","ulmaxthptperue":"30000.0","delaytolerance":"NOT_SUPPORTED","reliability":"99.0","dldeterministiccomm":"NOT_SUPPORTED","uldeterministiccomm":"NOT_SUPPORTED","coverage_area":{"IT":"RAN in IT two cells"},"n6protections":[{"type":"PCC Rule","name":"rule_any"}],"kpis":[]}}``` |

**[Errors]**



| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 476** | ```{ "description": "The maximum number of slices created was reached.", "data": "Slice number reached the limit." } ``` |
| **HTTP 475** | ```{ "description": "<failed_commands>", "data": "<body_payload>" } ``` |
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed during Product order creation", "data": "<similar_to_201_response_payload>" } ``` | 
| **HTTP 405** | ```{ "description": "<operation_not_allowed_exception_string>", "errors": "<error_message_for_why_the_operation_was_not_allowed (e.g. 'Slice ID reserved.', 'This DNN cannot be used outside of standard slice.', 'This sst and sd combination cannot be used outside of standard slice.', 'Rule name {} is reserved.', 'NetworkSlice ID already exists.', 'NetworkSlice ID created by serviceOrder, ProductOrder has no permissions.')>" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |


-----

### 1.2 - Get Network Slices (CSMF Get Products)


`GET http://{{slice_manager_url}}/productOrder/get` [`?fields=f1,f2,f3&offset=2&limit=3`] (no query parameters used for example)

**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":[{"id":"huawei.com","name":"huawei.com","DNN":"huawei.com","administrative_state":"UNLOCKED","operational_state":"ENABLED","plmnid":"1","sst":"1","sd":"010101","coverage_area":{"IT":"RAN in IT two cells","PDA":"RAN Porto de Aveiro"},"n6protections":[{"type":"filter","name":"rule_any"}],"kpis":[]},{"id":"5gasp.eu","name":"5gasp.eu","DNN":"5gasp.eu","administrative_state":"UNLOCKED","operational_state":"ENABLED","plmnid":"1","sst":"1","sd":"030303","coverage_area":{"IT":"RAN in IT two cells","PDA":"RAN Porto de Aveiro"},"n6protections":[{"type":"filter","name":"rule_any"}],"kpis":[]},{"id":"test","name":"test","DNN":"test","administrative_state":"UNLOCKED","operational_state":"ENABLED","sst":"1","sd":"222222","dllatency":"5","ullatency":"5","dlguathptperue":"30000.0","ulguathptperue":"30000.0","dlmaxthptperue":"30000.0","ulmaxthptperue":"30000.0","delaytolerance":"NOT_SUPPORTED","reliability":"99.0","dldeterministiccomm":"NOT_SUPPORTED","uldeterministiccomm":"NOT_SUPPORTED","coverage_area":{"IT":"RAN in IT two cells"},"n6protections":[{"type":"PCC Rule","name":"rule_any"}],"kpis":[]}]}``` |

- Headers: `{ X-Result-Count": "3", "X-Total-Count": "3" }`

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

-----

### 1.3 - Get Network Slice By ID (CSMF Get Product by ID)


`GET http://{{slice_manager_url}}/productOrder/{{id}}/get` [`?fields=f1,f2,f3`] (no query parameters used for example)

In the examples below, id = "test"

**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":{"id":"test","name":"test","DNN":"test","administrative_state":"UNLOCKED","operational_state":"ENABLED","sst":"1","sd":"222222","dllatency":"5","ullatency":"5","dlguathptperue":"30000.0","ulguathptperue":"30000.0","dlmaxthptperue":"30000.0","ulmaxthptperue":"30000.0","delaytolerance":"NOT_SUPPORTED","reliability":"99.0","dldeterministiccomm":"NOT_SUPPORTED","uldeterministiccomm":"NOT_SUPPORTED","coverage_area":{"IT":"RAN in IT two cells"},"n6protections":[{"type":"PCC Rule","name":"rule_any"}],"kpis":[]}}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |


-----

### 1.4 - Patch Network Slice (CSMF Patch Product)

`PATCH http://{{slice_manager_url}}/productOrder/{{id}}/patch`

In the examples below, id = "test". 
The examples consider the patching of the `test` network slice created in request 1.1.

**Payload:**

```json
{
    "id": "test",
    "name": "test",
    "administrative_state": "UNLOCKED", 
    "operational_state": "ENABLED",
    "coverage_area": ["IT"],
    "sst": 1, 
    "sd": "222222", 
    "dnn": "test", 
    "prioritylabel": 95, 
    "reliability": 99,
    "dllatency": 5,
    "ullatency": 5,
    "delaytolerance": "NOT_SUPPORTED", 
    "dldeterministiccomm": "NOT_SUPPORTED", 
    "uldeterministiccomm": "NOT_SUPPORTED",
    "ulguathptperue": 50000, // updated
    "ulmaxthptperue": 50000, // updated
    "dlguathptperue": 50000, // updated
    "dlmaxthptperue": 50000, // updated
    "n6protection":[{"type":"PCC Rule","name":"rule_any"}] 
}
```

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Updated","data":{"id":"test","name":"test","DNN":"test","administrative_state":"UNLOCKED","operational_state":"ENABLED","sst":"1","sd":"222222","dllatency":"5","ullatency":"5","dlguathptperue":"50000.0","ulguathptperue":"50000.0","dlmaxthptperue":"50000.0","ulmaxthptperue":"50000.0","delaytolerance":"NOT_SUPPORTED","reliability":"99.0","dldeterministiccomm":"NOT_SUPPORTED","uldeterministiccomm":"NOT_SUPPORTED","coverage_area":{"IT":"RAN in IT two cells"},"n6protections":[{"type":"PCC Rule","name":"rule_any"}],"kpis":[]}}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 475** | ```{ "description": "<failed_commands>", "data": "<body_payload_including_id>" } ``` |
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed during ProductOrder update" } ``` |
| **HTTP 405** | ```{ "description": "<operation_not_allowed_exception_string>", "errors": "<error_message_for_why_the_operation_was_not_allowed (e.g. 'Standard slice cannot be updated.', 'This DNN cannot be used outside of standard slice.', 'This sst and sd combination cannot be used outside of standard slice.', 'Rule name {} is reserved.')>" } ``` | 
| **HTTP 404** | ```{ "description": "Not Found", "errors": "NetworkSlice ID does not exists in ProductOrders" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

-----

### 1.5 - Network Slice Ips Pool 

`GET http://{{slice_manager_url}}/OrderIPs/{{id}}/get`

In the examples below, id = "test". 

**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":"10.16.9.37-10.16.9.54"}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

-----

### 1.6 - Delete all Network Slice UEs 

`DELETE http://{{slice_manager_url}}/UE/{{slice}}/delete_slice`

In the examples below, slice = "test"

**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** | **Headers** |
|------------------|----------------------|----------------------|
| **HTTP 204** | - | ``` {"description":"Deleted"} ``` |

**[Errors]**

| **Status Code** | **Response Payload**                                                            |
|------------------|---------------------------------------------------------------------------------|
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed when deleting UEs" } ``` |
| **HTTP 404** | ```{ "description": "Not Found" }```                                            |
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ```         |


---

### 1.7 - Delete Network Slice 

`DELETE http://{{slice_manager_url}}/productOrder/{{id}}/delete`

In the examples below, id = "test"

**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** | **Headers** |
|------------------|----------------------|----------------------|
| **HTTP 204** | - | ``` {"description":"Deleted"} ``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed during Product order deletion" } ``` |
| **HTTP 405** | ```{ "description": "<operation_not_allowed_exception_string>", "errors": "<error_message_for_why_the_operation_was_not_allowed (e.g. 'Standard slice cannot be deleted.')>" } ``` |
| **HTTP 404** | ```{ "description": "Not Found", "errors": "NetworkSlice does not exists" OR "NetworkSlice only existed in ProductOrder, it is deleted now" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |


## 2. UE

### 2.1 - Create UE

`POST http://{{slice_manager_url}}/UE/post`


**Payload:**

```json
{
    "IMSI": 999080100001125, // int IMSI number
    "numIMSIs":1, // int numero de consecutivos IMSIs min 1
    "slice": "test", //str name given to product in CSMF or service in NSMF
    //"slice": "first_slice",
    "IPV4": "", //str IP of UE needs to be inside the slice pool
    "IPV6": "", //str IPv6 of UE
    "AMDATA": true, //bool decide if UE uses access management data of this slice, each UE can only use AMDATA from 1 slice
                    //if a second slice is configure with AMDATA it will overwritten the first one
    "DEFAULT": "TRUE",  //TRUE-FALSE defines when multiple slices have the same DNN and different SNSSAI which slice is used by default when
                        //when accessing network
    "UEcanSendSNSSAI": "FALSE",   //TRUE-FALSE defines  if UE can select SNSSAI when same DNN has multiple SNSSAIs.
                                // only affects if AMDATA is true
    "AMBRUP": 4000000,  //int defines maximum throughput of UE in Uplink only works if AMDATA is true
    "AMBRDW": 4000000   //int defines maximum throughput of UE in Downlink only works if AMDATA is true
}
```

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 201** | ```{"description":"Created","data":{"id":20,"IMSI":999080100001125,"slice":"test","operational_state":"ENABLED","AMDATA":true,"SNSSAI":"1-222222","DNN":"test","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"test999080100001125","numIMSIs":1}}``` |

**[Errors]**

| **Status Code** | **Response Payload**                                                                                                                                                                                                                |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed when creating UEs", "data": "<UE_data_similar_to_201_response_payload>" } ```                                                                                                |
| **HTTP 405** | ```{ "description": "<operation_not_allowed_exception_string>", "errors": "<error_message_for_why_the_operation_was_not_allowed (e.g. 'UE association already exists.', 'Slice does not exist.', 'IPV4 outside of IPpool.')>" } ``` |
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ```                                                                                                                                                             |

---

### 2.2 - Get UE by Slice

`GET http://{{slice_manager_url}}/UE/{{slice}}/get_slice`

In the examples below, slice = "test". 


**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":[{"id":20,"IMSI":999080100001125,"slice":"test","operational_state":"ENABLED","AMDATA":true,"SNSSAI":"1-222222","DNN":"test","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"test999080100001125","numIMSIs":1}]}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

---

### 2.3 - Get UE by IMSI

`GET http://{{slice_manager_url}}/UE/{{IMSI}}/get_IMSI`

In the examples below, IMSI = 999080100001125. 


**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":[{"id":20,"IMSI":999080100001125,"slice":"test","operational_state":"ENABLED","AMDATA":true,"SNSSAI":"1-222222","DNN":"test","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"test999080100001125","numIMSIs":1}]}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

---

### 2.4 - Get UE by ID

`GET http://{{slice_manager_url}}/UE/{{id}}/get`

In the examples below, id = 20. 


**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":{"id":20,"IMSI":999080100001125,"slice":"test","operational_state":"ENABLED","AMDATA":true,"SNSSAI":"1-222222","DNN":"test","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"test999080100001125","numIMSIs":1}}``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

---

### 2.5 - Get All UE

`GET http://{{slice_manager_url}}/UE/get`


**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 200** | ```{"description":"Success","data":[{"id":5,"IMSI":999080100001122,"slice":"huawei.com","operational_state":"DISABLED","AMDATA":false,"SNSSAI":"1-010101","DNN":"huawei.com","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"huawei.com999080100001122","numIMSIs":1},{"id":19,"IMSI":999080100001140,"slice":"huawei.com","operational_state":"DISABLED","AMDATA":true,"SNSSAI":"1-010101","DNN":"huawei.com","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"huawei.com999080100001140","numIMSIs":1},{"id":20,"IMSI":999080100001125,"slice":"test","operational_state":"ENABLED","AMDATA":true,"SNSSAI":"1-222222","DNN":"test","DEFAULT":"TRUE","UEcanSendSNSSAI":"FALSE","IMSIGroupNAME":"test999080100001125","numIMSIs":1}]}``` |

- Headers: `{ X-Result-Count": "3", "X-Total-Count": "3" }`

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

---

### 2.6 - Delete UE By IMSI

`DELETE http://{{slice_manager_url}}/UE/{{IMSI}}/delete_IMSI`

In the examples below, IMSI = 999080100001125. 


**Payload:**

*None*

**Responses:**

**[Success]**

| **Status Code** | **Response Payload** | **Headers** |
|------------------|----------------------|----------------------|
| **HTTP 204** | - | ``` {"description":"Deleted"} ``` |

**[Errors]**

| **Status Code** | **Response Payload** |
|------------------|----------------------|
| **HTTP 475** | ```{ "description": "<failed_commands> commands failed when deleting UEs" }``` (headers: ``` {"description":"Deleted"} ```) |
| **HTTP 404** | ```{ "description": "Not Found" } ``` | 
| **HTTP 400** | ```{ "description": "Bad request", "errors": "<exception_string>" } ``` |

