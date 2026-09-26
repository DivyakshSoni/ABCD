import hashlib
from typing import List, Optional

class MerkleNode:
    def __init__(self, left: Optional['MerkleNode'], right: Optional['MerkleNode'], data: Optional[bytes] = None, hash_val: Optional[str] = None):
        self.left = left
        self.right = right
        if hash_val:
            self.hash = hash_val
        elif data:
            self.hash = hashlib.sha256(data).hexdigest()
        else:
            # Combine left and right hashes
            assert left is not None and right is not None
            combined = left.hash.encode('utf-8') + right.hash.encode('utf-8')
            self.hash = hashlib.sha256(combined).hexdigest()

class MerkleTree:
    def __init__(self, leaves_data: List[bytes]):
        self.leaves = [MerkleNode(None, None, data=d) for d in leaves_data]
        self.root = self._build_tree(self.leaves) if self.leaves else None

    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        if len(nodes) == 1:
            return nodes[0]
        
        parents = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left # Duplicate last node if odd
            parents.append(MerkleNode(left, right))
            
        return self._build_tree(parents)

    def get_root_hash(self) -> Optional[str]:
        return self.root.hash if self.root else None

# An append-only log backed by a simple sqlite table, to be integrated later.
