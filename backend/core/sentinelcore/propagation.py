from backend.core.sentinelcore.trust_graph import TrustGraph, TrustNode

def propagate_trust(graph: TrustGraph, start_node_id: str, trust_delta: float):
    """
    Propagates trust changes downstream.
    If a dataset's trust drops significantly, it affects the model trained on it, 
    and inferences generated from that model.
    """
    # Simple BFS propagation
    queue = [start_node_id]
    visited = set([start_node_id])
    
    while queue:
        current_id = queue.pop(0)
        downstream = graph.get_downstream_nodes(current_id)
        
        for next_id in downstream:
            if next_id not in visited:
                node = graph.nodes[next_id]
                if not node.crypto_locked:
                    # Apply a dampening factor for propagation
                    node.trust_score = max(0.0, min(1.0, node.trust_score + (trust_delta * 0.5)))
                visited.add(next_id)
                queue.append(next_id)
