# Confidence & Risk Scoring Service

## Overview

The Confidence & Risk Scoring Service is the ML and decision-support component of the Genesis-Blockers blockchain intelligence system.

Its purpose is to evaluate the strength of attribution between an unknown or suspect cryptocurrency wallet and candidate Virtual Asset Service Providers (VASPs), and to calculate an associated wallet or transaction risk score.

The service does **not** discover VASPs.

VASP discovery and transaction-graph traversal are handled by the Graph & Attribution Service. This service consumes the evidence produced by those components, converts it into numerical features, evaluates the evidence using explainable scoring models, and returns confidence, risk, and reasons.

---

## Position in the System

```text
                    Blockchain Data Service
                              |
                              v
                 Transaction Normalization
                              |
                              v
                    Graph & Attribution Service
                              |
                 Candidate VASPs + Evidence
                              |
                              v
                 +---------------------------+
                 |     SCORING SERVICE       |
                 |                           |
                 |  1. Feature Builder       |
                 |  2. Rule Baseline         |
                 |  3. ML Predictor          |
                 |  4. Calibration           |
                 |  5. Score Fusion          |
                 |  6. Risk Scoring          |
                 |  7. Explanation           |
                 +---------------------------+
                              |
                              v
              Confidence + Risk + Explanation
                              |
                              v
                    Investigation API
                              |
                              v
                    Investigator Dashboard
```

---

## Responsibilities

The scoring service is responsible for:

1. Receiving candidate VASP attribution evidence.
2. Extracting and calculating scoring features.
3. Calculating a transparent rule-based baseline score.
4. Running trained ML models for attribution scoring.
5. Calibrating ML probabilities where appropriate.
6. Combining graph, VASP intelligence, and ML evidence.
7. Calculating a risk score and risk level.
8. Generating human-readable explanations.
9. Returning structured results through the scoring API.
10. Supporting future replacement of the ML model without changing the API contract.

---

## Non-Responsibilities

The scoring service does **not**:

- Discover unknown VASPs.
- Crawl the blockchain directly.
- Build the transaction graph.
- Perform multi-hop graph traversal.
- Invent or assign VASP identities.
- Replace the VASP Intelligence database.
- Make an absolute legal claim that a wallet belongs to a particular entity.

The output represents the **strength of available evidence**, not definitive ownership.

---

## Scoring Pipeline

```text
Graph Service Response
        |
        v
Candidate Evidence
        |
        v
Feature Builder
        |
        +-------------------+
        |                   |
        v                   v
Rule Baseline          ML Predictor
        |                   |
        |                   v
        |              Calibration
        |                   |
        +---------+---------+
                  |
                  v
             Score Fusion
                  |
                  v
          Confidence Score
                  |
                  +-------> Risk Scoring
                  |
                  +-------> Explanation
                  |
                  v
            Final API Response
```

---

## File Structure

```text
scoring-service/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── scoring.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── scoring.py
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── graph.py
│   │   ├── transaction.py
│   │   └── behavioral.py
│   │
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   ├── risk.py
│   │   └── fusion.py
│   │
│   └── explainability/
│       ├── __init__.py
│       └── reasons.py
│
├── data/
│   ├── dummy/
│   │   ├── graph_response_001.json
│   │   ├── graph_response_002.json
│   │   └── labels.csv
│   │
│   └── processed/
│
├── training/
│   ├── train.py
│   ├── evaluate.py
│   └── split.py
│
├── models/
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_features.py
│   └── test_model.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Directory Responsibilities

| Directory / File | Responsibility |
|---|---|
| `app/main.py` | FastAPI application entry point |
| `app/api/` | REST API endpoints |
| `app/schemas/` | Request and response validation |
| `app/features/` | Feature extraction and engineering |
| `app/scoring/baseline.py` | Explainable rule-based attribution scoring |
| `app/scoring/risk.py` | Risk score and risk-level calculation |
| `app/scoring/fusion.py` | Combines ML, graph, and intelligence evidence |
| `app/explainability/` | Generates human-readable scoring explanations |
| `data/dummy/` | Synthetic development and testing data |
| `data/processed/` | Processed feature datasets |
| `training/` | ML training and evaluation scripts |
| `models/` | Saved trained model artifacts |
| `tests/` | Unit, API, and model tests |
| `requirements.txt` | Python dependencies |

> **Note:** The file structure represents the planned architecture. Files will be implemented incrementally as development progresses.

---

## Input

The initial API contract accepts:

```json
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

The initial contract is intentionally small.

As the feature pipeline develops, additional evidence can be incorporated without changing the fundamental responsibility of the scoring service.

---

## Feature Engineering

Features will be divided into several categories.

### 1. Graph Features

Examples:

- `graph_distance`
- `path_strength`
- `number_of_paths`
- `shortest_path_length`
- `candidate_reachable`
- wallet degree
- weighted degree
- graph centrality where useful

### 2. Transaction Features

Examples:

- `transaction_count`
- incoming transaction count
- outgoing transaction count
- total transaction volume
- average transaction value
- median transaction value
- maximum transaction value

### 3. Behavioral Features

Examples:

- wallet age
- active days
- transactions per day
- average time between transactions
- incoming/outgoing ratio
- repeat counterparty ratio

### 4. VASP Interaction Features

Examples:

- direct VASP interaction
- VASP interaction count
- percentage of outgoing transactions to VASP
- percentage of incoming transactions from VASP
- unique known VASP addresses interacted with

### 5. Candidate-Specific Features

Examples:

- candidate graph distance
- candidate path strength
- candidate address confidence
- candidate interaction count
- candidate transaction volume share

---

## Scoring Strategy

The service will use a staged approach.

### Stage 1: Rule-Based Baseline

A transparent rule-based score will be implemented first.

Example evidence:

```text
Known VASP address match       -> strong positive evidence
High address confidence        -> positive evidence
Short graph distance           -> positive evidence
Strong transaction path        -> positive evidence
Repeated interaction           -> positive evidence
Weak or indirect connection    -> weaker evidence
```

The baseline provides:

- a working scoring system before ML training data exists
- an interpretable benchmark
- a fallback mechanism
- a reference against which ML models can be evaluated

---

### Stage 2: Logistic Regression

Logistic Regression will be implemented as the first ML baseline.

It provides:

- probability-like output
- simple interpretation
- low computational requirements
- a strong baseline for tabular features

---

### Stage 3: Tree-Based ML

A tree-based model such as Random Forest or XGBoost will then be evaluated.

The model will be selected based on validation performance rather than assuming that a more complicated model is automatically better.

---

### Stage 4: Probability Calibration

ML outputs should represent meaningful confidence values.

Calibration techniques such as:

- Platt scaling
- isotonic regression

may be evaluated.

The objective is that a predicted confidence such as `0.90` should correspond approximately to a 90% empirical success rate on suitable evaluation data.

---

## Hybrid Scoring

The final attribution confidence may combine multiple sources of evidence:

```text
Final Score =
    ML Evidence
    + Graph Evidence
    + VASP Intelligence Evidence
```

The exact weights will be configurable and evaluated experimentally.

For example:

```text
ML score                 40%
Graph evidence           35%
VASP intelligence        25%
```

These values are initial design placeholders, not final scientific conclusions.

High-confidence verified VASP intelligence should not be blindly overridden by an ML model.

---

## Confidence Interpretation

The service should support an `INCONCLUSIVE` outcome.

It must not force every wallet to be attributed to a VASP.

Example initial interpretation:

```text
0.90 - 1.00   Very Strong Evidence
0.75 - 0.89   Strong Evidence
0.50 - 0.74   Moderate Evidence
0.25 - 0.49   Weak Evidence
0.00 - 0.24   Very Weak Evidence
```

The final thresholds will be determined through evaluation and calibration.

If multiple candidates have similar scores, the system should be able to report that the attribution is uncertain rather than assuming that the highest score is automatically correct.

---

## Risk Scoring

Risk scoring is separate from attribution confidence.

A wallet may have:

```text
High attribution confidence
+
High transaction risk
```

or:

```text
High attribution confidence
+
Low transaction risk
```

Therefore, the system maintains two separate concepts.

### Attribution Confidence

> How strongly does the available evidence support the relationship between the wallet and candidate VASP?

### Risk Score

> How concerning is the observed wallet or transaction behavior according to the defined risk indicators?

The risk score will be based on available evidence such as transaction behavior, graph characteristics, and other approved risk indicators.

---

## Explainability

Every scoring result should contain human-readable reasons.

Example:

```json
{
  "confidence": 0.87,
  "risk_score": 72,
  "risk_level": "HIGH",
  "reasons": [
    "Candidate VASP address is directly matched",
    "Known address has high intelligence confidence",
    "Candidate is reachable within 2 graph hops",
    "Multiple transactions connect the wallet to the candidate"
  ]
}
```

For ML models, feature contributions may later be exposed using techniques such as SHAP where appropriate.

The objective is that an investigator can understand **why** a score was produced rather than receiving an unexplained number.

---

## Synthetic Development Data

The initial development dataset will contain small, clearly labelled synthetic investigation cases.

Synthetic data is used for:

- API development
- feature engineering
- unit testing
- model pipeline testing
- demonstrations

Synthetic records must not be presented as real blockchain attribution evidence.

Example scenarios:

```text
Case 1:
Wallet -> VASP A
Direct known-address interaction
Expected: Strong attribution

Case 2:
Wallet -> Intermediate Wallet -> VASP A
Short path with strong evidence
Expected: Strong/Moderate attribution

Case 3:
Wallet -> several intermediaries -> VASP B
Longer and weaker connection
Expected: Weak attribution

Case 4:
Wallet has no known VASP connection
Expected: Inconclusive
```

The synthetic data should imitate the structure of real Graph Service responses so that real graph results can later replace the dummy data without redesigning the feature pipeline.

---

## Machine Learning Data Pipeline

```text
Synthetic / Real Investigation Cases
                |
                v
         Feature Extraction
                |
                v
          Feature Matrix
                |
                v
       Train / Validation / Test
                |
                v
          Model Training
                |
                v
             Evaluation
                |
                v
           Calibration
                |
                v
         Saved Model Version
                |
                v
             Inference
```

---

## Model Evaluation

Models will be evaluated using appropriate classification and ranking metrics.

Primary metrics:

- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC
- Top-1 candidate accuracy
- Top-3 candidate accuracy
- Top-5 candidate accuracy
- Brier Score
- Calibration Error

The system should compare:

```text
Graph-only baseline
        vs
Rule-based scoring
        vs
Logistic Regression
        vs
Tree-based ML
        vs
Hybrid scoring
```

Where possible, train/validation/test splitting should avoid leakage between related wallets or entities.

---

## API

### Calculate Score

```http
POST /api/v1/scoring/calculate
```

### Request

```json
{
  "input_wallet": "0x...",
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

### Response

```json
{
  "vasp_id": "vasp_001",
  "vasp_name": "Demo VASP",
  "confidence": 0.91,
  "risk_score": 78,
  "risk_level": "CRITICAL",
  "reasons": [
    "High-confidence known VASP address match",
    "Strong graph connection",
    "Multiple supporting transactions"
  ]
}
```

Risk thresholds must remain consistent with the project-wide API contract and will be finalized before implementation.

---

## Development Roadmap

### Phase 1: Service Foundation

- [ ] Create FastAPI scoring service
- [ ] Implement `/api/v1/scoring/calculate`
- [ ] Define request/response schemas
- [ ] Add health check
- [ ] Add basic tests

### Phase 2: Feature Engineering

- [ ] Implement graph features
- [ ] Implement transaction features
- [ ] Implement behavioral features
- [ ] Implement VASP interaction features
- [ ] Build unified Feature Builder
- [ ] Add feature tests

### Phase 3: Synthetic Dataset

- [ ] Create synthetic Graph Service responses
- [ ] Create labelled investigation cases
- [ ] Build feature matrix
- [ ] Validate feature distributions

### Phase 4: Baseline Scoring

- [ ] Implement rule-based attribution score
- [ ] Implement risk score
- [ ] Implement explanation generation
- [ ] Establish baseline metrics

### Phase 5: Machine Learning

- [ ] Train Logistic Regression
- [ ] Train Random Forest
- [ ] Evaluate XGBoost
- [ ] Compare against baseline
- [ ] Select appropriate model
- [ ] Version the trained model

### Phase 6: Calibration & Hybrid Scoring

- [ ] Calibrate ML probabilities
- [ ] Implement score fusion
- [ ] Handle inconclusive attribution
- [ ] Add candidate ranking
- [ ] Add model explanations

### Phase 7: Integration

- [ ] Connect to Graph Service
- [ ] Test real Graph Service responses
- [ ] Integrate with Investigation API
- [ ] Validate frontend compatibility
- [ ] Perform end-to-end testing

---

## Design Principles

### Explainability First

The system is intended to support investigators. Scores should be explainable.

### Candidate Attribution, Not Absolute Ownership

The service measures the strength of evidence supporting a candidate VASP. It does not claim legal ownership of a wallet.

### Replaceable Models

The API and feature pipeline should not depend on one specific ML algorithm.

### Real Data Compatibility

Synthetic data is only for development. Feature extraction must be designed around the normalized evidence structure used by the actual system.

### No Forced Attribution

When evidence is insufficient or candidates are too close in score, the system should report uncertainty.

### Version Everything

Model versions, feature versions, and scoring configurations should be identifiable in scoring results.

---

## Current Implementation Status

| Component | Status |
|---|---|
| Service folder | Ready |
| README / Architecture | Complete |
| API contract | Defined |
| FastAPI endpoint | Pending |
| Feature Builder | Pending |
| Synthetic dataset | Pending |
| Rule baseline | Pending |
| Logistic Regression | Pending |
| Tree-based ML | Pending |
| Calibration | Pending |
| Hybrid scoring | Pending |
| Risk scoring | Pending |
| Explainability | Pending |
| Graph integration | Pending |