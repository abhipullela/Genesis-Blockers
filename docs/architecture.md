# System Architecture

**Project:** Automated Blockchain Intelligence & VASP Attribution
Engine\
**SIH 2026 Problem Statement:** 26182\
**Organization:** Ministry of Home Affairs\
**Department:** Indian Cyber Crime Coordination Centre (I4C)\
**Theme:** Blockchain & Cybersecurity\
**Category:** Software\
**Document Version:** 1.0\
**Status:** MVP Architecture

------------------------------------------------------------------------

## 1. Purpose

This document defines the high-level software architecture of the
Automated Blockchain Intelligence & VASP Attribution Engine.

The system is intended to help authorized law-enforcement investigators
analyze an unknown or suspect cryptocurrency wallet, trace relevant
blockchain transactions, identify connections to known Virtual Asset
Service Providers (VASPs), calculate attribution confidence and risk,
and present the evidence through an investigator dashboard.

The architecture is designed around a working Ethereum MVP and must
remain extensible to additional blockchains and future SAHYOG
integration.

------------------------------------------------------------------------

## 2. MVP Scope

The first implementation supports **Ethereum only**.

The MVP must complete the following flow:

``` text
Unknown / Suspect Wallet
        |
        v
Ethereum Transaction Data
        |
        v
Transaction Normalization
        |
        v
Transaction Graph
        |
        v
Multi-hop Tracing
        |
        v
Known VASP / Deposit Address Matching
        |
        v
Nearest VASP Identification
        |
        v
Confidence + Risk Scoring
        |
        v
Evidence Generation
        |
        v
Investigator Dashboard
```

The team must complete this vertical slice before implementing advanced
multi-chain or ML features.

------------------------------------------------------------------------

## 3. Architectural Goals

The system should provide:

1.  Automated blockchain transaction retrieval.
2.  Standardized transaction data independent of blockchain provider.
3.  Graph-based multi-hop transaction tracing.
4.  Evidence-based VASP attribution.
5.  Explainable confidence and risk scores.
6.  Investigator-friendly visualization.
7.  Clear separation between modules.
8.  Parallel development by all six team members.
9.  Extensibility for additional blockchains.
10. A future integration point for the SAHYOG ecosystem.

------------------------------------------------------------------------

## 4. High-Level Architecture

``` text
                         +----------------------+
                         |   LEA Investigator    |
                         |      Dashboard        |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |   Investigation API   |
                         |   /api/v1/investigate|
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Investigation         |
                         | Orchestrator          |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
     +----------------+    +------------------+   +----------------+
     | Blockchain     |    | Graph &          |   | Scoring        |
     | Data Service   |    | Attribution      |   | Engine         |
     +-------+--------+    +--------+---------+   +-------+--------+
             |                      |                     |
             v                      v                     |
     +----------------+    +------------------+          |
     | Ethereum RPC / |    | VASP Intelligence|<---------+
     | Blockchain API |    | Database         |
     +----------------+    +------------------+
```

------------------------------------------------------------------------

## 5. Component Responsibilities

### 5.1 Investigation API / Orchestrator

**Owner:** Abhinav

Responsibilities:

-   Accept investigator requests.
-   Validate incoming requests.
-   Create an investigation ID.
-   Coordinate blockchain, graph, VASP intelligence, and scoring
    modules.
-   Aggregate module outputs.
-   Return a single investigation result to the frontend.
-   Handle errors and partial failures.
-   Provide the main integration boundary.

The orchestrator should not contain provider-specific blockchain logic
or scoring algorithms.

------------------------------------------------------------------------

### 5.2 Blockchain Data Service

**Owner:** Trishanu

Responsibilities:

-   Validate Ethereum wallet addresses.
-   Retrieve transaction history.
-   Communicate with Ethereum RPC/API providers.
-   Normalize provider responses.
-   Handle pagination and API limits.
-   Handle failed, missing, or duplicate transactions.

Output must conform to the normalized transaction contract defined in
`data-model.md`.

------------------------------------------------------------------------

### 5.3 Graph & Attribution Service

**Owner:** Disen

Responsibilities:

-   Convert normalized transactions into a transaction graph.
-   Represent wallets and relevant entities as graph nodes.
-   Represent transactions as graph edges.
-   Perform configurable multi-hop traversal.
-   Query VASP intelligence for known addresses.
-   Identify candidate VASPs.
-   Calculate graph distance.
-   Return transaction paths and attribution evidence.

The graph module must not invent VASP identities. VASP identities must
originate from the VASP intelligence layer.

------------------------------------------------------------------------

### 5.4 VASP Intelligence Layer

**Owner:** Geethika

Responsibilities:

-   Maintain known VASP entities.
-   Maintain known blockchain addresses.
-   Identify address types.
-   Store intelligence-source references.
-   Store data confidence and verification metadata.
-   Provide address/entity lookup functionality.

Examples of address types:

-   `deposit_address`
-   `hot_wallet`
-   `exchange_wallet`
-   `custodial_wallet`
-   `treasury`
-   `unknown`

------------------------------------------------------------------------

### 5.5 Confidence & Risk Scoring Engine

**Owner:** Siddharth

Responsibilities:

-   Receive attribution features.
-   Calculate VASP confidence.
-   Calculate wallet/transaction risk.
-   Rank VASP candidates.
-   Provide explanations for scores.

The MVP should use an explainable rule-based or hybrid scoring approach.

Machine-learning models may be introduced later after sufficient labeled
data and evaluation methodology are available.

------------------------------------------------------------------------

### 5.6 Investigator Dashboard

**Owner:** Dhairya

Responsibilities:

-   Investigator authentication interface.
-   Wallet and blockchain input.
-   Investigation initiation.
-   Investigation status.
-   VASP attribution result.
-   Confidence visualization.
-   Risk visualization.
-   Transaction graph.
-   Transaction timeline.
-   Evidence display.
-   Investigation report view.

The frontend communicates with the main Investigation API rather than
directly calling blockchain providers.

------------------------------------------------------------------------

## 6. Data Flow

### Step 1 --- Investigator Input

The investigator submits:

``` json
{
  "wallet": "0x...",
  "chain": "ethereum",
  "max_hops": 5
}
```

### Step 2 --- Blockchain Retrieval

The blockchain service retrieves transactions for the wallet.

### Step 3 --- Normalization

Provider-specific blockchain responses are converted to the common
transaction schema.

### Step 4 --- Graph Construction

The graph service creates wallet/address nodes and transaction edges.

### Step 5 --- VASP Matching

Graph traversal identifies addresses that match known VASP intelligence.

### Step 6 --- Candidate Ranking

Candidate VASPs are ranked using graph distance and available evidence.

### Step 7 --- Scoring

The scoring engine calculates confidence and risk.

### Step 8 --- Evidence Aggregation

The orchestrator combines transaction paths, matched addresses, source
information, and score explanations.

### Step 9 --- Dashboard

The final investigation result is returned to the investigator
dashboard.

------------------------------------------------------------------------

## 7. Architectural Boundaries

The following boundaries must be maintained:

``` text
Blockchain Service
    |
    +--> Provides normalized transactions

Graph Service
    |
    +--> Provides graph paths and candidate VASPs

VASP Intelligence
    |
    +--> Provides known entity/address intelligence

Scoring Engine
    |
    +--> Provides confidence, risk, and explanations

Investigation API
    |
    +--> Orchestrates and aggregates the above

Frontend
    |
    +--> Displays the final investigation result
```

Internal implementation can change without affecting other modules as
long as the API contracts remain compatible.

------------------------------------------------------------------------

## 8. Initial Technology Direction

### Backend

-   Python
-   FastAPI

### Frontend

-   React
-   TypeScript recommended

### Database

-   PostgreSQL

### Graph

For the MVP, the graph can initially be implemented using an in-memory
graph structure or PostgreSQL-backed representation.

A dedicated graph database may be introduced later if required by scale
or query complexity.

### Containerization

-   Docker
-   Docker Compose for local development

### Blockchain

-   Ethereum for MVP

------------------------------------------------------------------------

## 9. Scalability Strategy

Blockchain-specific logic must be isolated behind a common interface.

Conceptually:

``` text
Blockchain Provider Interface
          |
     +----+----+----+----+
     |         |         |
 Ethereum   Bitcoin    Tron ...
```

The investigation and scoring layers should not need major changes when
a new blockchain is added.

Future blockchain adapters:

-   Ethereum
-   Bitcoin
-   Tron
-   BNB Chain
-   Solana
-   Polygon

------------------------------------------------------------------------

## 10. Security Architecture

The system is intended for authorized investigation use.

Security requirements include:

-   Authentication.
-   Authorization.
-   Input validation.
-   API rate limiting.
-   Secure secret management.
-   No hardcoded API keys.
-   Audit logging.
-   Controlled access to investigation data.
-   Validation of external API responses.
-   Protection against malformed wallet/address input.
-   Secure error handling without exposing secrets.

Detailed security testing is owned by Geethika.

------------------------------------------------------------------------

## 11. Auditability

An investigation should have a unique identifier.

Example:

``` text
INV-2026-0001
```

The system should preserve sufficient metadata to reconstruct how an
attribution result was produced, including:

-   Input wallet.
-   Blockchain.
-   Investigation timestamp.
-   Transactions analyzed.
-   Graph path.
-   Matched VASP address.
-   Intelligence source.
-   Confidence score.
-   Risk score.
-   Scoring reasons.

------------------------------------------------------------------------

## 12. MVP vs Future Architecture

### MVP

``` text
Ethereum
   |
Normalized Transactions
   |
Graph
   |
Known VASP Address
   |
Nearest VASP
   |
Rule-based Confidence/Risk
   |
Dashboard
```

### Future

``` text
Multiple Blockchains
        |
Cross-chain Correlation
        |
Entity / Cluster Intelligence
        |
Advanced Graph Analytics
        |
ML-assisted Detection
        |
Alerts
        |
Investigation Reports
        |
SAHYOG Integration
```

Advanced capabilities must not delay the working MVP.

------------------------------------------------------------------------

## 13. Architectural Principles

### Principle 1 --- Vertical Slice First

A complete working investigation is more important than partially
implemented advanced features.

### Principle 2 --- Contract First

Modules communicate through documented contracts.

### Principle 3 --- Provider Independence

External blockchain provider responses must be normalized before
entering the core system.

### Principle 4 --- Explainability

Every VASP attribution should have traceable evidence and an explanation
for its confidence.

### Principle 5 --- Replaceable Components

Blockchain providers, graph implementations, and scoring models should
be replaceable without redesigning the whole system.

### Principle 6 --- Parallel Development

Every team member should be able to work with mock data when dependent
modules are incomplete.

------------------------------------------------------------------------

## 14. Ownership

  Component                      Owner
  ------------------------------ -----------
  Architecture & Integration     Abhinav
  Blockchain Data                Trishanu
  Graph & Attribution            Disen
  Confidence & Risk              Siddharth
  Frontend                       Dhairya
  VASP Intelligence & Security   Geethika
