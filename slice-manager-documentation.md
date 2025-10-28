

## 1. Network Slices

### 1.1 - Create Network Slice


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
| **HTTP 475** | ```{ "data": "data", "description": "<list_of_failed_commands>" } ``` | 
| **HTTP 405** | ```{ "errors": "<error_message>", "description": "<exception_string>" } ``` | 
| **HTTP 400** | ```{ "errors": "<exception_string>", "description": "Bad request" } ``` |




