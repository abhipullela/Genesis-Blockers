from typing import List

import networkx as nx
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.mock_vasps import check_mock_vasp


router = APIRouter(
    prefix="/graph",
    tags=["Graph"],
)


class Transaction(BaseModel):
    tx_hash: str
    block_number: int
    timestamp: str

    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")

    asset: str
    amount: float
    status: str

    model_config = {
        "populate_by_name": True
    }


class GraphAnalyzeRequest(BaseModel):
    wallet: str
    chain: str = "ethereum"
    max_hops: int = Field(default=5, ge=1, le=20)
    transactions: List[Transaction]


def find_wallet_path(
    graph: nx.DiGraph,
    source: str,
    target: str,
):
    try:
        return nx.shortest_path(
            graph,
            source=source,
            target=target,
        )
    except nx.NetworkXNoPath:
        return []


def find_reachable_wallets(
    graph: nx.DiGraph,
    wallet: str,
    max_hops: int,
):
    return nx.single_source_shortest_path_length(
        graph,
        wallet,
        cutoff=max_hops,
    )


@router.post("/analyze")
def analyze_graph(request: GraphAnalyzeRequest):

    graph = nx.DiGraph()

    # ---------------------------------------------------------
    # 1. Build transaction graph
    # ---------------------------------------------------------

    for transaction in request.transactions:

        graph.add_node(
            transaction.from_address,
            address=transaction.from_address,
            chain=request.chain,
            type="wallet",
        )

        graph.add_node(
            transaction.to_address,
            address=transaction.to_address,
            chain=request.chain,
            type="wallet",
        )

        graph.add_edge(
            transaction.from_address,
            transaction.to_address,
            tx_hash=transaction.tx_hash,
            block_number=transaction.block_number,
            amount=transaction.amount,
            asset=transaction.asset,
            timestamp=transaction.timestamp,
            status=transaction.status,
        )

    # ---------------------------------------------------------
    # 2. Multi-hop traversal
    # ---------------------------------------------------------

    reachable_wallets = find_reachable_wallets(
        graph,
        request.wallet,
        request.max_hops,
    )

    # ---------------------------------------------------------
    # 3. Find known VASP addresses
    # ---------------------------------------------------------

    vasp_matches = []

    for address, distance in reachable_wallets.items():

        vasp = check_mock_vasp(address)

        if not vasp["known"]:
            continue

        path = find_wallet_path(
            graph,
            request.wallet,
            address,
        )

        path_transactions = []

        for i in range(len(path) - 1):

            source = path[i]
            target = path[i + 1]

            edge_data = graph.get_edge_data(
                source,
                target,
            )

            if edge_data:
                path_transactions.append({
                    "from": source,
                    "to": target,
                    "tx_hash": edge_data["tx_hash"],
                    "block_number": edge_data["block_number"],
                    "amount": edge_data["amount"],
                    "asset": edge_data["asset"],
                    "timestamp": edge_data["timestamp"],
                    "status": edge_data["status"],
                })

        # -----------------------------------------------------
        # 4. Graph evidence/features for scoring
        # -----------------------------------------------------

        transaction_count = len(path_transactions)

        # Simple factual path-strength indicator.
        # Lower hop distance means stronger graph proximity.
        path_strength = 1.0 / (1.0 + distance)

        vasp_matches.append({
            "address": address,
            "graph_distance": distance,
            "transaction_count": transaction_count,
            "address_confidence": vasp["confidence"],
            "path_strength": path_strength,
            "path": path,
            "transactions": path_transactions,
            "vasp": vasp,
        })

    # ---------------------------------------------------------
    # 5. Return graph analysis
    # ---------------------------------------------------------

    return {
        "success": True,
        "data": {
            "input_wallet": request.wallet,
            "chain": request.chain,
            "max_hops": request.max_hops,
            "node_count": graph.number_of_nodes(),
            "edge_count": graph.number_of_edges(),
            "reachable_wallet_count": len(reachable_wallets),
            "reachable_wallets": reachable_wallets,
            "vasp_matches": vasp_matches,
        },
        "error": None,
    }