from typing import Dict, Any, List

class TrustNode:
    def __init__(self, node_id: str, node_type: str, initial_trust: float = 0.2):
        self.node_id = node_id
        self.node_type = node_type
        self.trust_score = initial_trust
        self.crypto_locked = False
        
    def update_trust(self, confirming_evidence: float, disconfirming_evidence: float):
        if self.crypto_locked:
            return
            
        new_trust = self.trust_score + confirming_evidence - disconfirming_evidence
        self.trust_score = max(0.0, min(1.0, new_trust))
        
    def lock_crypto(self):
        self.crypto_locked = True
        self.trust_score = 0.0

class TrustGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, node: TrustNode):
        self.nodes[node.node_id] = node
        
    def add_edge(self, source_id: str, target_id: str, relationship: str):
        self.edges.append({
            "source": source_id,
            "target": target_id,
            "relationship": relationship
        })
        
    def get_downstream_nodes(self, node_id: str) -> List[str]:
        downstream = []
        for edge in self.edges:
            if edge["source"] == node_id:
                downstream.append(edge["target"])
        return downstream
