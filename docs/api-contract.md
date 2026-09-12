# API Contract

**Project:** Automated Blockchain Intelligence & VASP Attribution
Engine\
**SIH 2026 Problem Statement:** 26182\
**Version:** 1.0\
**Status:** MVP\
**Primary Blockchain:** Ethereum

------------------------------------------------------------------------

## 1. API Conventions

### Base URL

Development:

``` text
http://localhost:8000/api/v1
```

All APIs use:

``` text
Content-Type: application/json
```

### API Versioning

All MVP endpoints use:

``` text
/api/v1/
```

Breaking API changes should use a new API version.

------------------------------------------------------------------------

## 2. Common Response Format

### Successful Response

``` json
{
  "success": true,
  "data": {},
  "error": null
}
```

### Error Response

``` json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_WALLET",
    "message": "Invalid Ethereum wallet address"
  }
}
```

------------------------------------------------------------------------

# 3. Investigation API

**Owner:** Abhinav

The Investigation API is the main entry point for the frontend.

## 3.1 Start Investigation

### Endpoint

``` http
POST /api/v1/investigate
```

### Request

``` json
{
  "wallet": "0x1111111111111111111111111111111111111111",
  "chain": "ethereum",
  "max_hops": 5
}
```

### Request Fields

  Field        Type      Required   Description
  ------------ --------- ---------- ----------------------------------------
  `wallet`     string    Yes        Wallet/address to investigate
  `chain`      string    Yes        Blockchain identifier
  `max_hops`   integer   No         Maximum graph traversal depth
  `case_id`    string    No         Existing investigation/case identifier

For the MVP, `chain` must be `ethereum`.

------------------------------------------------------------------------

## 3.2 Investigation Response

``` json
{
  "success": true,
  "data": {
    "investigation_id": "INV-2026-0001",

    "input": {
      "wallet": "0x1111111111111111111111111111111111111111",
      "chain": "ethereum",
      "max_hops": 5
    },

    "attribution": {
      "vasp_id": "vasp_001",
      "vasp_name": "Demo VASP",
      "confidence": 0.91,
      "distance_hops": 3
    },

    "risk": {
      "score": 78,
      "level": "HIGH"
    },

    "transaction_path": [
      "0x1111111111111111111111111111111111111111",
      "0x2222222222222222222222222222222222222222",
      "0x3333333333333333333333333333333333333333",
      "0x4444444444444444444444444444444444444444"
    ],

    "evidence": [
      {
        "type": "known_vasp_address",
        "description": "Destination matches a known VASP deposit address",
        "strength": 0.95
      }
    ],

    "transactions_analyzed": 25,
    "timestamp": "2026-09-10T00:00:00Z"
  },
  "error": null
}
```

------------------------------------------------------------------------

# 4. Blockchain Data API

**Owner:** Trishanu

The Blockchain Data API retrieves blockchain transactions and returns
normalized transaction objects.

## 4.1 Get Wallet Transactions

### Endpoint

``` http
GET /api/v1/blockchain/{chain}/wallet/{address}/transactions
```

### Example

``` http
GET /api/v1/blockchain/ethereum/wallet/0x1111111111111111111111111111111111111111/transactions
```

### Optional Query Parameters

``` text
limit
page
start_time
end_time
```

Example:

``` http
GET /api/v1/blockchain/ethereum/wallet/0x111.../transactions?limit=100
```

------------------------------------------------------------------------

## 4.2 Response

``` json
{
  "success": true,
  "data": {
    "wallet": "0x1111111111111111111111111111111111111111",
    "chain": "ethereum",
    "transactions": [
      {
        "tx_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "block_number": 12345678,
        "timestamp": "2026-09-10T00:00:00Z",
        "from": "0x1111111111111111111111111111111111111111",
        "to": "0x2222222222222222222222222222222222222222",
        "asset": "ETH",
        "amount": 1.25,
        "status": "success"
      }
    ],
    "total": 1
  },
  "error": null
}
```

The service must return normalized data rather than provider-specific
responses.

------------------------------------------------------------------------

# 5. Graph & Attribution API

**Owner:** Disen

The Graph API receives normalized transactions, constructs a transaction
graph, performs multi-hop analysis, and identifies candidate VASPs.

## 5.1 Analyze Graph

### Endpoint

``` http
POST /api/v1/graph/analyze
```

### Request

``` json
{
  "wallet": "0x1111111111111111111111111111111111111111",
  "chain": "ethereum",
  "max_hops": 5,
  "transactions": [
    {
      "tx_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "block_number": 12345678,
      "timestamp": "2026-09-10T00:00:00Z",
      "from": "0x1111111111111111111111111111111111111111",
      "to": "0x2222222222222222222222222222222222222222",
      "asset": "ETH",
      "amount": 1.25,
      "status": "success"
    }
  ]
}
```

## 5.2 Response

``` json
{
  "success": true,
  "data": {
    "input_wallet": "0x1111111111111111111111111111111111111111",
    "nodes_count": 4,
    "edges_count": 3,

    "candidate_vasps": [
      {
        "vasp_id": "vasp_001",
        "vasp_name": "Demo VASP",
        "distance_hops": 3,
        "matched_address": "0x4444444444444444444444444444444444444444",
        "path": [
          "0x1111111111111111111111111111111111111111",
          "0x2222222222222222222222222222222222222222",
          "0x3333333333333333333333333333333333333333",
          "0x4444444444444444444444444444444444444444"
        ]
      }
    ]
  },
  "error": null
}
```

------------------------------------------------------------------------

# 6. VASP Intelligence API

**Owner:** Geethika

The VASP Intelligence API provides known address and entity information.

## 6.1 Lookup Address

### Endpoint

``` http
GET /api/v1/vasp/address/{address}
```

### Example

``` http
GET /api/v1/vasp/address/0x4444444444444444444444444444444444444444
```

## 6.2 Known Address Response

``` json
{
  "success": true,
  "data": {
    "address": "0x4444444444444444444444444444444444444444",
    "chain": "ethereum",
    "known": true,

    "vasp": {
      "vasp_id": "vasp_001",
      "name": "Demo VASP",
      "country": "IN"
    },

    "address_type": "deposit_address",
    "confidence": 0.95,
    "source": "SOURCE-001"
  },
  "error": null
}
```

## 6.3 Unknown Address Response

``` json
{
  "success": true,
  "data": {
    "address": "0x9999999999999999999999999999999999999999",
    "chain": "ethereum",
    "known": false,
    "vasp": null,
    "address_type": null,
    "confidence": 0,
    "source": null
  },
  "error": null
}
```

------------------------------------------------------------------------

# 7. Scoring API

**Owner:** Siddharth

The scoring API calculates explainable attribution confidence and risk.

## 7.1 Calculate Score

### Endpoint

``` http
POST /api/v1/scoring/calculate
```

### Request

``` json
{
  "input_wallet": "0x1111111111111111111111111111111111111111",

  "candidate_vasp": {
    "vasp_id": "vasp_001",
    "vasp_name": "Demo VASP"
  },

  "features": {
    "graph_distance": 3,
    "known_address_match": true,
    "address_confidence": 0.95,
    "path_strength": 0.87,
    "transaction_count": 4
  }
}
```

## 7.2 Response

``` json
{
  "success": true,
  "data": {
    "vasp_id": "vasp_001",
    "vasp_name": "Demo VASP",

    "confidence": 0.91,

    "risk_score": 78,

    "risk_level": "HIGH",

    "reasons": [
      {
        "factor": "known_address_match",
        "description": "Destination matches a known VASP deposit address",
        "contribution": 0.40
      },
      {
        "factor": "graph_distance",
        "description": "VASP address is reachable within 3 hops",
        "contribution": 0.25
      },
      {
        "factor": "address_confidence",
        "description": "Known address intelligence has high confidence",
        "contribution": 0.20
      }
    ]
  },
  "error": null
}
```

------------------------------------------------------------------------

# 8. Standard Error Codes

  Code                       HTTP Status Meaning
  ------------------------ ------------- -----------------------------
  `INVALID_WALLET`                   400 Invalid wallet/address
  `INVALID_REQUEST`                  400 Invalid request body
  `UNSUPPORTED_CHAIN`                400 Blockchain not supported
  `WALLET_NOT_FOUND`                 404 Wallet/data not found
  `NO_TRANSACTIONS`                  404 No transactions found
  `NO_VASP_FOUND`                    200 No known VASP identified
  `BLOCKCHAIN_API_ERROR`             502 Blockchain provider error
  `BLOCKCHAIN_TIMEOUT`               504 Blockchain provider timeout
  `RATE_LIMITED`                     429 External API rate limit
  `INTERNAL_ERROR`                   500 Internal server error

`NO_VASP_FOUND` is a valid investigation result and must not be treated
as a server failure.

------------------------------------------------------------------------

# 9. API Ownership

  API                                  Owner       Primary Consumer
  ------------------------------------ ----------- ------------------
  `POST /investigate`                  Abhinav     Frontend
  `GET /blockchain/.../transactions`   Trishanu    Backend / Graph
  `POST /graph/analyze`                Disen       Backend
  `GET /vasp/address/{address}`        Geethika    Graph / Scoring
  `POST /scoring/calculate`            Siddharth   Backend

------------------------------------------------------------------------

# 10. Contract Change Rules

Any breaking change to an API contract must be agreed upon before
implementation.

When changing a contract:

1.  Update this document.
2.  Update the corresponding mock JSON.
3.  Inform dependent team members.
4.  Update the implementation.
5.  Update tests.
6.  Verify frontend compatibility.

Internal implementation may change freely as long as the public contract
remains compatible.
