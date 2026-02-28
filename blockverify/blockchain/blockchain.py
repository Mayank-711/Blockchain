"""
blockchain/blockchain.py
Pure Python educational blockchain implementation.

Contains Block and Blockchain classes for storing
certificate hashes and student metadata securely.
"""

import hashlib
import json
import time
import threading


class Block:
    """
    Represents a single block in the blockchain.

    Attributes:
        index (int): Position of the block in the chain.
        timestamp (float): Unix timestamp when block was created.
        data (dict): Certificate hash + student info.
        previous_hash (str): Hash of the previous block.
        current_hash (str): SHA-256 hash of this block.
        nonce (int): Proof-of-work nonce value.
    """

    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block contents.
        Combines index, timestamp, data, previous_hash, and nonce.
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        """Convert block to dictionary for serialization."""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'current_hash': self.current_hash,
            'nonce': self.nonce,
        }

    def __repr__(self):
        return (
            f"Block(index={self.index}, "
            f"hash={self.current_hash[:16]}...)"
        )


class Blockchain:
    """
    Simple blockchain implementation for certificate storage.

    This is a singleton — one chain exists for the entire application.
    Thread-safe for concurrent Django request handling.

    Methods:
        add_block(data): Add a new block with certificate data.
        get_block(index): Retrieve a block by its index.
        find_by_hash(certificate_hash): Find block by cert hash.
        is_chain_valid(): Validate the entire chain integrity.
        get_chain_length(): Return number of blocks.
        get_latest_block(): Return the most recent block.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern — only one blockchain instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the blockchain with a genesis block."""
        if self._initialized:
            return
        self.chain = []
        self._chain_lock = threading.Lock()
        self._create_genesis_block()
        self._initialized = True

    def _create_genesis_block(self):
        """Create the first block in the chain (genesis block)."""
        genesis_data = {
            'certificate_hash': '0' * 64,
            'student_name': 'Genesis',
            'student_id': '0',
            'certificate_type': 'genesis',
            'institution': 'BlockVerify System',
        }
        genesis_block = Block(0, genesis_data, '0' * 64)
        self.chain.append(genesis_block)

    def add_block(self, data):
        """
        Add a new block to the blockchain.

        Args:
            data (dict): Must contain at minimum:
                - certificate_hash: SHA-256 hash of the certificate
                - student_name: Name of the student
                - student_id: Unique student identifier
                - certificate_type: Type of certificate

        Returns:
            Block: The newly created and added block.
        """
        with self._chain_lock:
            previous_block = self.chain[-1]
            new_block = Block(
                index=len(self.chain),
                data=data,
                previous_hash=previous_block.current_hash
            )
            # Simple proof-of-work (educational, not heavy)
            while not new_block.current_hash.startswith('0'):
                new_block.nonce += 1
                new_block.current_hash = new_block.calculate_hash()

            self.chain.append(new_block)
            return new_block

    def get_block(self, index):
        """
        Retrieve a block by its index.

        Args:
            index (int): Block index to retrieve.

        Returns:
            Block or None: The block if found, None otherwise.
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def find_by_hash(self, certificate_hash):
        """
        Find a block that contains the given certificate hash.

        Args:
            certificate_hash (str): SHA-256 hash to search for.

        Returns:
            Block or None: Matching block, or None if not found.
        """
        for block in self.chain:
            if block.data.get('certificate_hash') == certificate_hash:
                return block
        return None

    def is_chain_valid(self):
        """
        Validate the integrity of the entire blockchain.

        Checks:
            1. Each block's hash matches its recalculated hash.
            2. Each block's previous_hash matches prior block's hash.

        Returns:
            bool: True if chain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify current block's hash
            if current.current_hash != current.calculate_hash():
                return False

            # Verify chain linkage
            if current.previous_hash != previous.current_hash:
                return False

        return True

    def get_chain_length(self):
        """Return the total number of blocks in the chain."""
        return len(self.chain)

    def get_latest_block(self):
        """Return the most recently added block."""
        return self.chain[-1]

    def get_all_blocks(self):
        """Return list of all blocks as dictionaries."""
        return [block.to_dict() for block in self.chain]

    def reset(self):
        """Reset blockchain (for testing only)."""
        with self._chain_lock:
            self.chain = []
            self._create_genesis_block()
