# Data Model

**Project:** Automated Blockchain Intelligence & VASP Attribution
Engine\
**SIH 2026 Problem Statement:** 26182\
**Version:** 1.0\
**Status:** MVP\
**Primary Blockchain:** Ethereum

------------------------------------------------------------------------

# 1. Purpose

This document defines the common data structures used across the system.

The data model separates:

-   Blockchain transactions
-   Wallet/address entities
-   Graph nodes and edges
-   VASP entities
-   VASP-known addresses
-   Attribution results
-   Risk and confidence scores
-   Evidence
-   Investigations

The purpose is to ensure that every team member uses compatible data
structures.

------------------------------------------------------------------------

# 2. Identifier Conventions

## 2.1 Wallet / Address

Blockchain addresses are represented as strings.

Ethereum example:

``` text
0x1111111111111111111111111111111111111111
```

Address comparisons should be performed consistently using the
normalization rules of the selected blockchain.

------------------------------------------------------------------------

## 2.2 Transaction Hash

A transaction hash is represented as a string.

Example:

``` text
0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

------------------------------------------------------------------------

## 2.3 VASP ID

VASP entities use an internal stable identifier.

Example:

``` text
vasp_001
```

The internal ID must not depend on the display name.

------------------------------------------------------------------------

## 2.4 Investigation ID

Each investigation receives a unique identifier.

Example:

``` text
INV-2026-0001
```

------------------------------------------------------------------------

# 3. Normalized Transaction

This is the most important shared structure between the blockchain and
downstream services.

``` json
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
```

## Fields

  Field            Type              Required   Description
  ---------------- ----------------- ---------- ------------------------------
  `tx_hash`        string            Yes        Blockchain transaction hash
  `block_number`   integer           Yes        Block containing transaction
  `timestamp`      ISO-8601 string   Yes        Transaction timestamp
  `from`           string            Yes        Sender address
  `to`             string            Yes        Receiver address
  `asset`          string            Yes        Asset symbol
  `amount`         number            Yes        Transferred amount
  `status`         string            Yes        Transaction status

------------------------------------------------------------------------

# 4. Wallet / Address Entity

A blockchain address can be represented as:

``` json
{
  "address": "0x1111111111111111111111111111111111111111",
  "chain": "ethereum",
  "type": "wallet"
}
```

## Address Types

``` text
wallet
contract
deposit_address
hot_wallet
exchange_wallet
custodial_wallet
treasury
vasp
unknown
```

An address type is an intelligence classification and should not be
assumed solely from the address format.

------------------------------------------------------------------------

# 5. Graph Node

Graph nodes represent relevant blockchain addresses or known entities.

``` json
{
  "node_id": "0x1111111111111111111111111111111111111111",
  "address": "0x1111111111111111111111111111111111111111",
  "chain": "ethereum",
  "type": "wallet",
  "label": null
}
```

For a known VASP-related address:

``` json
{
  "node_id": "0x4444444444444444444444444444444444444444",
  "address": "0x4444444444444444444444444444444444444444",
  "chain": "ethereum",
  "type": "deposit_address",
  "label": "Demo VASP"
}
```

------------------------------------------------------------------------

# 6. Graph Edge

Edges represent transfers between addresses.

``` json
{
  "tx_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "from": "0x1111111111111111111111111111111111111111",
  "to": "0x2222222222222222222222222222222222222222",
  "amount": 1.25,
  "asset": "ETH",
  "timestamp": "2026-09-10T00:00:00Z"
}
```

A graph edge must retain the transaction hash so the path can be traced
back to blockchain evidence.

------------------------------------------------------------------------

# 7. VASP Entity

``` json
{
  "vasp_id": "vasp_001",
  "name": "Demo VASP",
  "country": "IN",
  "supported_chains": [
    "ethereum"
  ]
}
```

## Fields

  Field                Type     Description
  -------------------- -------- --------------------------------------
  `vasp_id`            string   Stable internal identifier
  `name`               string   VASP/entity display name
  `country`            string   Country/region code where applicable
  `supported_chains`   array    Known supported blockchains

------------------------------------------------------------------------

# 8. VASP Address Intelligence

A known address associated with a VASP should be represented as:

``` json
{
  "address": "0x4444444444444444444444444444444444444444",
  "chain": "ethereum",
  "vasp_id": "vasp_001",
  "address_type": "deposit_address",
  "confidence": 0.95,
  "source": "SOURCE-001",
  "last_verified": "2026-09-10T00:00:00Z"
}
```

## Fields

  Field             Type              Description
  ----------------- ----------------- -----------------------------------------
  `address`         string            Blockchain address
  `chain`           string            Blockchain
  `vasp_id`         string            Associated VASP
  `address_type`    string            Type of known address
  `confidence`      number            Intelligence confidence from 0.0 to 1.0
  `source`          string            Internal source/reference ID
  `last_verified`   ISO-8601 string   Last verification time

------------------------------------------------------------------------

# 9. Intelligence Source

Sources should be represented using a stable internal reference.

``` json
{
  "source_id": "SOURCE-001",
  "name": "Verified Intelligence Source",
  "type": "public",
  "reference": "source-reference",
  "verified_at": "2026-09-10T00:00:00Z"
}
```

The actual source URL or reference must be stored according to the
project's data-handling and authorization requirements.

------------------------------------------------------------------------

# 10. Attribution Candidate

``` json
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
```

------------------------------------------------------------------------

# 11. Confidence Score

Confidence is represented as a decimal between:

``` text
0.0 and 1.0
```

Examples:

``` text
0.91 = 91%
0.64 = 64%
0.32 = 32%
```

Confidence represents the system's strength of attribution evidence, not
certainty that a VASP legally owns or controls an address.

------------------------------------------------------------------------

# 12. Risk Score

Risk is represented as an integer between:

``` text
0 and 100
```

Recommended MVP levels:

      Score Level
  --------- ----------
      0--24 LOW
     25--49 MEDIUM
     50--74 HIGH
    75--100 CRITICAL

The scoring team may refine the formula while maintaining this output
format.

------------------------------------------------------------------------

# 13. Evidence

Evidence must be structured and traceable.

``` json
{
  "type": "known_vasp_address",
  "description": "Destination matches a known VASP deposit address",
  "strength": 0.95,
  "transaction_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "source": "SOURCE-001"
}
```

## Evidence Types

``` text
known_vasp_address
deposit_address_match
hot_wallet_match
exchange_wallet_match
graph_distance
transaction_frequency
transaction_volume
behavioral_pattern
entity_label
```

Evidence should describe the reason for an attribution rather than
merely state the conclusion.

------------------------------------------------------------------------

# 14. Investigation

A complete investigation can be represented as:

``` json
{
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
    "level": "CRITICAL"
  },

  "transaction_path": [
    "0x1111111111111111111111111111111111111111",
    "0x2222222222222222222222222222222222222222",
    "0x3333333333333333333333333333333333333333",
    "0x4444444444444444444444444444444444444444"
  ],

  "evidence": [],

  "transactions_analyzed": 25,

  "timestamp": "2026-09-10T00:00:00Z"
}
```

> Note: The example risk level is `CRITICAL` because the recommended
> range places a score of 78 in the 75--100 range. Implementations must
> use the same mapping consistently.

------------------------------------------------------------------------

# 15. Candidate VASP List

When multiple VASPs are identified:

``` json
{
  "candidate_vasps": [
    {
      "vasp_id": "vasp_001",
      "vasp_name": "VASP A",
      "confidence": 0.91,
      "distance_hops": 3
    },
    {
      "vasp_id": "vasp_002",
      "vasp_name": "VASP B",
      "confidence": 0.64,
      "distance_hops": 4
    },
    {
      "vasp_id": "vasp_003",
      "vasp_name": "VASP C",
      "confidence": 0.32,
      "distance_hops": 5
    }
  ]
}
```

Candidates should be ordered by descending confidence.

------------------------------------------------------------------------

# 16. Null / Unknown Values

When information is unavailable, use:

``` json
null
```

Do not use arbitrary placeholder strings such as:

``` text
"N/A"
"unknown_vasp"
"not_found"
```

unless the field is explicitly defined as an enum/status field.

------------------------------------------------------------------------

# 17. Data Integrity Rules

1.  Transaction hashes must remain linked to their source transaction.
2.  VASP IDs must remain stable.
3.  Evidence should identify its source where available.
4.  Confidence values must remain between `0.0` and `1.0`.
5.  Risk scores must remain between `0` and `100`.
6.  Hop distance must be a non-negative integer.
7.  Timestamps should use ISO-8601 format.
8.  Blockchain addresses must be validated according to the selected
    blockchain.
9.  Provider-specific fields may be stored separately but must not
    replace the common schema.
