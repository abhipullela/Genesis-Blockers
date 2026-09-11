import json
import random
from pathlib import Path

random.seed(42)

DATA_DIR = Path("data/dummy")
DATA_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_SCENARIOS = [
    # Strong direct match
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 1,
        "address_confidence": 0.98,
        "label": 1,
    },

    # Strong direct match with multiple transactions
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 5,
        "address_confidence": 0.95,
        "label": 1,
    },

    # Strong but indirect match
    {
        "graph_distance": 4,
        "path_strength": 0.20,
        "transaction_count": 8,
        "address_confidence": 0.92,
        "label": 1,
    },

    # Medium-distance strong match
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 4,
        "address_confidence": 0.88,
        "label": 1,
    },

    # Direct but weak VASP evidence
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 1,
        "address_confidence": 0.40,
        "label": 0,
    },

    # Many transactions but weak VASP evidence
    {
        "graph_distance": 3,
        "path_strength": 0.25,
        "transaction_count": 10,
        "address_confidence": 0.45,
        "label": 0,
    },

    # Far away with weak confidence
    {
        "graph_distance": 5,
        "path_strength": 0.1667,
        "transaction_count": 6,
        "address_confidence": 0.35,
        "label": 0,
    },

    # Close competition: moderately strong candidate
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 3,
        "address_confidence": 0.82,
        "label": 1,
    },

    # Close competition: nearly identical but weaker candidate
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 3,
        "address_confidence": 0.75,
        "label": 0,
    },

    # High confidence but distant
    {
        "graph_distance": 5,
        "path_strength": 0.1667,
        "transaction_count": 12,
        "address_confidence": 0.90,
        "label": 1,
    },

    # Low confidence but many transactions
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 12,
        "address_confidence": 0.50,
        "label": 0,
    },

    # Ambiguous / no convincing candidate
    {
        "graph_distance": 4,
        "path_strength": 0.20,
        "transaction_count": 2,
        "address_confidence": 0.40,
        "label": 0,
    },
]


def make_candidate(case_id, candidate_number, scenario):
    vasp_id = f"vasp_{candidate_number:03d}"

    address = (
        f"0x"
        f"{case_id}"
        f"{candidate_number:02d}"
        f"{'a' * 36}"
    )

    return {
        "address": address,
        "graph_distance": scenario["graph_distance"],
        "transaction_count": scenario["transaction_count"],
        "address_confidence": scenario["address_confidence"],
        "path_strength": scenario["path_strength"],
        "path": [],
        "transactions": [],
        "vasp": {
            "known": True,
            "vasp_id": vasp_id,
            "vasp_name": f"Synthetic VASP {candidate_number:03d}",
        },
        "_label": scenario["label"],
    }


def generate_case(case_id, scenario_pair):
    candidates = []

    for candidate_number, scenario in enumerate(
        scenario_pair,
        start=1,
    ):
        candidates.append(
            make_candidate(
                case_id,
                candidate_number,
                scenario,
            )
        )

    graph_response = {
        "success": True,
        "data": {
            "input_wallet": (
                f"0x{'f' * 40}"
            ),
            "chain": "ethereum",
            "max_hops": 5,
            "node_count": 10,
            "edge_count": 12,
            "reachable_wallet_count": 5,
            "reachable_wallets": [],
            "vasp_matches": candidates,
        },
    }

    return graph_response


def main():
    # Remove old synthetic graph files.
    for file_path in DATA_DIR.glob("graph_response_*.json"):
        file_path.unlink()

    labels = []

    scenario_pairs = []

    # Create 60 investigation cases.
    for _ in range(60):
        scenario_1 = random.choice(FEATURE_SCENARIOS)
        scenario_2 = random.choice(FEATURE_SCENARIOS)

        # Avoid cases where both candidates are exactly the same.
        while scenario_1 == scenario_2:
            scenario_2 = random.choice(FEATURE_SCENARIOS)

        scenario_pairs.append(
            [scenario_1, scenario_2]
        )

    for case_number, scenario_pair in enumerate(
        scenario_pairs,
        start=1,
    ):
        case_id = f"{case_number:03d}"

        graph_response = generate_case(
            case_id,
            scenario_pair,
        )

        graph_file = (
            DATA_DIR
            / f"graph_response_{case_id}.json"
        )

        with open(
            graph_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                graph_response,
                file,
                indent=2,
            )

        for candidate in graph_response["data"]["vasp_matches"]:
            labels.append(
                {
                    "case_id": case_id,
                    "candidate_vasp_id": candidate["vasp"]["vasp_id"],
                    "label": candidate["_label"],
                }
            )

            # Do not store the development label
            # inside the graph response.
            del candidate["_label"]

        # Rewrite file after removing labels.
        with open(
            graph_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                graph_response,
                file,
                indent=2,
            )

    labels_file = DATA_DIR / "labels.csv"

    with open(
        labels_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            "case_id,candidate_vasp_id,label\n"
        )

        for row in labels:
            file.write(
                f"{row['case_id']},"
                f"{row['candidate_vasp_id']},"
                f"{row['label']}\n"
            )

    print(
        f"Generated {len(scenario_pairs)} cases."
    )
    print(
        f"Generated {len(labels)} candidate labels."
    )


if __name__ == "__main__":
    main()