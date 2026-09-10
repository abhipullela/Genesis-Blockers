# Investigation Flow

**Project:** Automated Blockchain Intelligence & VASP Attribution
Engine\
**SIH 2026 Problem Statement:** 26182\
**Version:** 1.0\
**Status:** MVP\
**Primary Blockchain:** Ethereum

------------------------------------------------------------------------

# 1. Purpose

This document describes the end-to-end investigation workflow used by
the VASP Attribution Engine.

The MVP takes an unknown or suspect Ethereum wallet and attempts to
identify the nearest known VASP connection through transaction analysis.

The result must be evidence-based and explainable.

------------------------------------------------------------------------

# 2. End-to-End Flow

``` text
                    +----------------------+
                    | Investigator         |
                    | enters wallet        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Validate Request     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Fetch Ethereum       |
                    | Transactions         |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Normalize Blockchain |
                    | Data                 |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Build Transaction     |
                    | Graph                |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Multi-hop Traversal  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Match Known VASP     |
                    | Addresses            |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Rank Candidate VASPs |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Confidence + Risk    |
                    | Scoring              |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Generate Evidence    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Investigator         |
                    | Dashboard            |
                    +----------------------+
```

------------------------------------------------------------------------

# 3. Step 1 --- Investigator Input

The investigator provides:

``` json
{
  "wallet": "0x1111111111111111111111111111111111111111",
  "chain": "ethereum",
  "max_hops": 5
}
```

For the MVP:

``` text
chain = ethereum
```

The wallet must be validated before analysis begins.

------------------------------------------------------------------------

# 4. Step 2 --- Input Validation

The backend validates:

-   Wallet address format.
-   Blockchain selection.
-   Maximum hop value.
-   Request structure.

Invalid input returns an appropriate API error.

Example:

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

# 5. Step 3 --- Blockchain Data Retrieval

The Investigation API requests transaction data from the Blockchain Data
Service.

``` text
Investigation API
       |
       v
Blockchain Data Service
       |
       v
Ethereum RPC / API Provider
```

The blockchain service is responsible for provider-specific
communication.

The rest of the system must not depend on the provider's response
format.

------------------------------------------------------------------------

# 6. Step 4 --- Transaction Normalization

Provider responses are converted into the common transaction model.

Example:

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

This normalized structure is passed to downstream services.

------------------------------------------------------------------------

# 7. Step 5 --- Graph Construction

The graph service converts transactions into a graph.

Example transaction:

``` text
Wallet A
   |
   | 1.25 ETH
   | TX-001
   v
Wallet B
```

becomes:

``` text
NODE A ---------------- EDGE TX-001 ----------------> NODE B
```

The transaction hash is retained as evidence.

------------------------------------------------------------------------

# 8. Step 6 --- Multi-hop Traversal

The system follows relevant transaction paths from the suspect wallet.

Example:

``` text
Suspect Wallet
      |
      v
Wallet A
      |
      v
Wallet B
      |
      v
Deposit Address
```

Hop calculation:

``` text
Suspect → Wallet A       = 1 hop
Wallet A → Wallet B      = 2 hops
Wallet B → Deposit       = 3 hops
```

Therefore:

``` text
distance_hops = 3
```

The maximum traversal depth is controlled by:

``` text
max_hops
```

------------------------------------------------------------------------

# 9. Step 7 --- VASP Address Matching

For each relevant address, the graph service checks the VASP
Intelligence layer.

``` text
Graph Address
      |
      v
VASP Intelligence Lookup
      |
      +---- Known ----> VASP Entity
      |
      +---- Unknown --> Continue Traversal
```

A known match may contain:

``` json
{
  "address": "0x444...",
  "vasp_id": "vasp_001",
  "address_type": "deposit_address",
  "confidence": 0.95,
  "source": "SOURCE-001"
}
```

The system must retain the intelligence source.

------------------------------------------------------------------------

# 10. Step 8 --- Candidate VASP Identification

If multiple VASPs are reached, the system creates candidate results.

Example:

``` text
Suspect Wallet
      |
      +---- 3 hops ----> VASP A
      |
      +---- 4 hops ----> VASP B
      |
      +---- 5 hops ----> VASP C
```

Candidates are passed to the scoring engine.

------------------------------------------------------------------------

# 11. Step 9 --- Confidence Scoring

The scoring engine evaluates available attribution features.

Example features:

``` text
Graph distance
Known address match
Address intelligence confidence
Path strength
Transaction relationship
```

Example:

``` text
VASP A
Confidence = 0.91

VASP B
Confidence = 0.64

VASP C
Confidence = 0.32
```

The score must be accompanied by reasons.

------------------------------------------------------------------------

# 12. Step 10 --- Risk Scoring

Risk is calculated separately from VASP attribution confidence.

Example:

``` text
Risk Score = 78
Risk Level = CRITICAL
```

The risk score should be explainable through contributing factors.

Important:

> A high attribution confidence does not automatically mean that the
> VASP itself is malicious.

The system is identifying a service/entity connection, while risk
concerns the analyzed wallet/activity.

------------------------------------------------------------------------

# 13. Step 11 --- Evidence Generation

The final result must contain evidence supporting the attribution.

Example:

``` json
{
  "type": "known_vasp_address",
  "description": "Destination matches a known VASP deposit address",
  "strength": 0.95,
  "transaction_hash": "0xaaaaaaaa...",
  "source": "SOURCE-001"
}
```

Possible evidence:

-   Known VASP address match.
-   Deposit address match.
-   Hot wallet match.
-   Graph distance.
-   Transaction path.
-   Transaction frequency.
-   Transaction volume.
-   Other validated intelligence.

------------------------------------------------------------------------

# 14. Step 12 --- Final Investigation Result

The orchestrator combines all outputs.

Conceptually:

``` text
Blockchain Data
      +
Graph Analysis
      +
VASP Intelligence
      +
Scoring
      |
      v
Investigation Result
```

Example:

``` json
{
  "investigation_id": "INV-2026-0001",

  "input": {
    "wallet": "0x111...",
    "chain": "ethereum"
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
    "0x111...",
    "0x222...",
    "0x333...",
    "0x444..."
  ],

  "evidence": []
}
```

------------------------------------------------------------------------

# 15. Step 13 --- Dashboard Visualization

The frontend should present:

## Investigation Summary

``` text
Wallet
Blockchain
Investigation ID
Transactions analyzed
```

## VASP Attribution

``` text
Nearest VASP
Confidence
Hop distance
Candidate VASPs
```

## Risk

``` text
Risk Score
Risk Level
Risk Factors
```

## Transaction Path

``` text
Suspect Wallet
      ↓
Wallet A
      ↓
Wallet B
      ↓
VASP Deposit Address
      ↓
VASP
```

## Evidence

Each evidence item should be independently viewable.

------------------------------------------------------------------------

# 16. No VASP Found Flow

Not every wallet will connect to a known VASP.

The system must support:

``` text
Wallet
  |
  v
Transactions
  |
  v
Graph
  |
  v
No known VASP within max_hops
  |
  v
Valid investigation result
```

Example:

``` json
{
  "success": true,
  "data": {
    "input_wallet": "0x111...",
    "candidate_vasps": [],
    "attribution": null,
    "message": "No known VASP identified within the configured hop limit."
  },
  "error": null
}
```

This is not a system failure.

------------------------------------------------------------------------

# 17. Invalid Wallet Flow

``` text
Wallet Input
     |
     v
Validation
     |
     X
Invalid
     |
     v
Return INVALID_WALLET
```

No blockchain request should be made after validation fails.

------------------------------------------------------------------------

# 18. Blockchain Provider Failure Flow

``` text
Investigation
     |
     v
Blockchain Service
     |
     v
Provider Failure
     |
     v
BLOCKCHAIN_API_ERROR
```

The error should be returned without exposing API keys, internal
credentials, or unnecessary provider details.

------------------------------------------------------------------------

# 19. Investigation State Model

For a future asynchronous implementation, investigations may use:

``` text
CREATED
   |
   v
FETCHING_TRANSACTIONS
   |
   v
BUILDING_GRAPH
   |
   v
ANALYZING_VASP
   |
   v
SCORING
   |
   v
COMPLETED
```

Failure states:

``` text
FAILED
```

The MVP may implement the pipeline synchronously if execution time is
acceptable.

------------------------------------------------------------------------

# 20. Example Complete Investigation

Suppose:

``` text
Input:
0xSuspect
```

The blockchain service returns:

``` text
0xSuspect → 0xWalletA
0xWalletA → 0xWalletB
0xWalletB → 0xDeposit
```

The VASP intelligence service identifies:

``` text
0xDeposit → VASP XYZ
```

The graph service returns:

``` text
VASP XYZ
Distance = 3 hops
```

The scoring engine returns:

``` text
Confidence = 0.91
Risk Score = 78
Risk Level = CRITICAL
```

The final system displays:

``` text
+--------------------------------------+
| INVESTIGATION RESULT                 |
+--------------------------------------+
| Wallet: 0xSuspect                    |
| Chain: Ethereum                      |
|                                      |
| Nearest VASP: VASP XYZ               |
| Confidence: 91%                      |
| Distance: 3 hops                     |
|                                      |
| Risk Score: 78                       |
| Risk Level: CRITICAL                 |
+--------------------------------------+

Transaction Path:

Suspect
   ↓
Wallet A
   ↓
Wallet B
   ↓
Deposit Address
   ↓
VASP XYZ

Evidence:
✓ Known VASP deposit address
✓ 3-hop transaction path
✓ Verified intelligence source
```

------------------------------------------------------------------------

# 21. MVP Completion Criteria

The MVP investigation flow is complete when:

-   [ ] Investigator can submit an Ethereum wallet.
-   [ ] Wallet validation works.
-   [ ] Ethereum transactions are retrieved.
-   [ ] Transactions are normalized.
-   [ ] Transaction graph is constructed.
-   [ ] Multi-hop traversal works.
-   [ ] Known VASP addresses can be identified.
-   [ ] Candidate VASPs can be ranked.
-   [ ] Nearest VASP can be identified.
-   [ ] Confidence score is generated.
-   [ ] Risk score is generated.
-   [ ] Score explanations are generated.
-   [ ] Transaction path is displayed.
-   [ ] Evidence is displayed.
-   [ ] No-VASP cases are handled.
-   [ ] Provider/API errors are handled.
-   [ ] Final result is displayed on the investigator dashboard.

------------------------------------------------------------------------

# 22. Future Investigation Flow

After the Ethereum MVP is stable:

``` text
Multi-chain Transactions
        |
        v
Cross-chain Address / Entity Correlation
        |
        v
Exchange Clusters
        |
        v
DeFi / Bridge Analysis
        |
        v
Advanced Behavioral Analysis
        |
        v
ML-assisted Risk Detection
        |
        v
Automated Alerts
        |
        v
Investigation Reports
        |
        v
SAHYOG Integration
```

These features must be implemented only after the core Ethereum
investigation flow is stable.
