# blockchain.py
# Blockchain implementation for educational Bitcoin mining simulator

import hashlib
import time
from datetime import datetime


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index, previous_hash, timestamp, data, nonce=0, difficulty=4):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()
        self.status = "Pending"
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of block contents"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block by finding a valid nonce"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        self.status = "Mined"
        return self.nonce
    
    def is_valid(self, difficulty):
        """Check if block hash meets difficulty requirements"""
        target = "0" * difficulty
        return self.hash[:difficulty] == target
    
    def to_dict(self):
        """Convert block to dictionary for display"""
        return {
            "Block": self.index,
            "Previous Hash": self.previous_hash[:16] + "...",
            "Nonce": self.nonce,
            "Hash": self.hash[:16] + "...",
            "Difficulty": self.difficulty,
            "Timestamp": datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "Status": self.status
        }
    
    def get_full_details(self):
        """Get complete block information"""
        return {
            "Block Number": self.index,
            "Previous Hash": self.previous_hash,
            "Timestamp": datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "Data": self.data,
            "Nonce": self.nonce,
            "Hash": self.hash,
            "Difficulty": self.difficulty,
            "Status": self.status
        }


class Blockchain:
    """Manages the blockchain and validation"""
    
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", 0, 1)
        genesis_block.hash = genesis_block.calculate_hash()
        genesis_block.status = "Genesis"
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data, difficulty):
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            previous_hash=previous_block.hash,
            timestamp=time.time(),
            data=data,
            nonce=0,
            difficulty=difficulty
        )
        return new_block
    
    def append_mined_block(self, block):
        """Append a successfully mined block to the chain"""
        self.chain.append(block)
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False, f"Block {i}: Hash mismatch"
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False, f"Block {i}: Previous hash mismatch"
            
            # Check if block meets difficulty requirement
            if not current_block.is_valid(current_block.difficulty):
                return False, f"Block {i}: Does not meet difficulty requirement"
        
        return True, "Blockchain is valid"
    
    def tamper_block(self, block_index, new_data):
        """Tamper with a block's data (for educational demonstration)"""
        if 0 < block_index < len(self.chain):
            block = self.chain[block_index]
            block.data = new_data
            block.hash = block.calculate_hash()
            block.status = "Tampered"
            return True
        return False
    
    def get_all_blocks(self):
        """Get all blocks in the chain"""
        return self.chain
    
    def get_block(self, index):
        """Get a specific block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def reset(self):
        """Reset the blockchain"""
        self.chain = []
        self.create_genesis_block()
