# tests/test_blockchain.py
# Unit tests for blockchain functionality

import unittest
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blockchain import Block, Blockchain
import hashlib


class TestBlock(unittest.TestCase):
    """Test Block class functionality"""
    
    def test_block_creation(self):
        """Test basic block creation"""
        block = Block(0, "0", time.time(), "Test Block", 0, 2)
        self.assertEqual(block.index, 0)
        self.assertEqual(block.previous_hash, "0")
        self.assertEqual(block.data, "Test Block")
        self.assertEqual(block.nonce, 0)
        self.assertEqual(block.difficulty, 2)
    
    def test_hash_calculation(self):
        """Test SHA-256 hash calculation"""
        block = Block(0, "0", 1234567890, "Test Block", 0, 2)
        hash1 = block.calculate_hash()
        
        # Hash should be 64 characters (256 bits in hex)
        self.assertEqual(len(hash1), 64)
        
        # Same data should produce same hash
        hash2 = block.calculate_hash()
        self.assertEqual(hash1, hash2)
        
        # Different nonce should produce different hash
        block.nonce = 1
        hash3 = block.calculate_hash()
        self.assertNotEqual(hash1, hash3)
    
    def test_hash_is_sha256(self):
        """Verify hash is valid SHA-256"""
        block = Block(0, "0", 1234567890, "Test Block", 100, 2)
        block_hash = block.calculate_hash()
        
        # Manual SHA-256 calculation
        block_string = f"{block.index}{block.previous_hash}{block.timestamp}{block.data}{block.nonce}"
        expected_hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        self.assertEqual(block_hash, expected_hash)
    
    def test_mining(self):
        """Test block mining with difficulty"""
        block = Block(0, "0", time.time(), "Test Block", 0, 2)
        
        # Mine the block
        final_nonce = block.mine_block(2)
        
        # Hash should start with 2 zeros
        self.assertTrue(block.hash.startswith("00"))
        self.assertEqual(block.status, "Mined")
        self.assertGreater(final_nonce, 0)
    
    def test_difficulty_validation(self):
        """Test difficulty validation"""
        block = Block(0, "0", time.time(), "Test Block", 0, 3)
        
        # Before mining, should not be valid
        self.assertFalse(block.is_valid(3))
        
        # After mining, should be valid
        block.mine_block(3)
        self.assertTrue(block.is_valid(3))
        self.assertTrue(block.hash.startswith("000"))
    
    def test_to_dict(self):
        """Test block serialization to dictionary"""
        block = Block(0, "0", time.time(), "Test Block", 100, 2)
        block_dict = block.to_dict()
        
        self.assertIn("Block", block_dict)
        self.assertIn("Previous Hash", block_dict)
        self.assertIn("Nonce", block_dict)
        self.assertIn("Hash", block_dict)
        self.assertIn("Difficulty", block_dict)
        self.assertIn("Timestamp", block_dict)
        self.assertIn("Status", block_dict)


class TestBlockchain(unittest.TestCase):
    """Test Blockchain class functionality"""
    
    def setUp(self):
        """Create a fresh blockchain for each test"""
        self.blockchain = Blockchain()
    
    def test_genesis_block(self):
        """Test genesis block creation"""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0")
        self.assertEqual(genesis.status, "Genesis")
    
    def test_add_block(self):
        """Test adding new blocks"""
        block1 = self.blockchain.add_block("Block 1", 2)
        self.assertEqual(block1.index, 1)
        self.assertEqual(block1.previous_hash, self.blockchain.get_latest_block().hash)
        
        # Mine and add the block
        block1.mine_block(2)
        self.blockchain.append_mined_block(block1)
        
        self.assertEqual(len(self.blockchain.chain), 2)
    
    def test_chain_linking(self):
        """Test that blocks are properly linked"""
        # Add and mine multiple blocks
        for i in range(3):
            block = self.blockchain.add_block(f"Block {i+1}", 2)
            block.mine_block(2)
            self.blockchain.append_mined_block(block)
        
        # Verify chain length
        self.assertEqual(len(self.blockchain.chain), 4)  # Genesis + 3 blocks
        
        # Verify links
        for i in range(1, len(self.blockchain.chain)):
            current = self.blockchain.chain[i]
            previous = self.blockchain.chain[i-1]
            self.assertEqual(current.previous_hash, previous.hash)
    
    def test_blockchain_validation(self):
        """Test blockchain validation"""
        # Add some valid blocks
        for i in range(2):
            block = self.blockchain.add_block(f"Block {i+1}", 2)
            block.mine_block(2)
            self.blockchain.append_mined_block(block)
        
        # Chain should be valid
        is_valid, message = self.blockchain.is_chain_valid()
        self.assertTrue(is_valid)
        self.assertIn("valid", message.lower())
    
    def test_tamper_detection(self):
        """Test that tampering is detected"""
        # Add some blocks
        for i in range(3):
            block = self.blockchain.add_block(f"Block {i+1}", 2)
            block.mine_block(2)
            self.blockchain.append_mined_block(block)
        
        # Tamper with block 1
        success = self.blockchain.tamper_block(1, "TAMPERED DATA")
        self.assertTrue(success)
        
        # Chain should now be invalid
        is_valid, message = self.blockchain.is_chain_valid()
        self.assertFalse(is_valid)
        self.assertIn("Block 1", message)  # Should detect issue at block 1
    
    def test_hash_recalculation_after_tamper(self):
        """Test that hash changes when data is tampered"""
        # Add a block
        block = self.blockchain.add_block("Original Data", 2)
        block.mine_block(2)
        original_hash = block.hash
        self.blockchain.append_mined_block(block)
        
        # Tamper with it
        self.blockchain.tamper_block(1, "Tampered Data")
        tampered_hash = self.blockchain.chain[1].hash
        
        # Hash should be different
        self.assertNotEqual(original_hash, tampered_hash)
    
    def test_get_block(self):
        """Test retrieving specific blocks"""
        # Add blocks
        for i in range(3):
            block = self.blockchain.add_block(f"Block {i+1}", 2)
            block.mine_block(2)
            self.blockchain.append_mined_block(block)
        
        # Get specific blocks
        block0 = self.blockchain.get_block(0)
        self.assertIsNotNone(block0)
        self.assertEqual(block0.index, 0)
        
        block2 = self.blockchain.get_block(2)
        self.assertIsNotNone(block2)
        self.assertEqual(block2.index, 2)
        
        # Invalid index
        block99 = self.blockchain.get_block(99)
        self.assertIsNone(block99)
    
    def test_reset(self):
        """Test blockchain reset"""
        # Add blocks
        for i in range(5):
            block = self.blockchain.add_block(f"Block {i+1}", 2)
            block.mine_block(2)
            self.blockchain.append_mined_block(block)
        
        self.assertEqual(len(self.blockchain.chain), 6)
        
        # Reset
        self.blockchain.reset()
        
        # Should only have genesis block
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].status, "Genesis")
    
    def test_increasing_difficulty(self):
        """Test that higher difficulty requires more hashes"""
        block_easy = Block(0, "0", time.time(), "Easy", 0, 2)
        nonce_easy = block_easy.mine_block(2)
        
        block_hard = Block(0, "0", time.time(), "Hard", 0, 4)
        nonce_hard = block_hard.mine_block(4)
        
        # Harder difficulty should generally require more attempts
        # (Not always true due to randomness, but likely)
        self.assertGreater(nonce_hard, nonce_easy)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete mining workflow"""
    
    def test_complete_mining_workflow(self):
        """Test complete mining process from start to finish"""
        blockchain = Blockchain()
        
        # Mine 3 blocks
        for i in range(1, 4):
            block = blockchain.add_block(f"Transaction {i}", 3)
            block.mine_block(3)
            blockchain.append_mined_block(block)
        
        # Verify chain
        self.assertEqual(len(blockchain.chain), 4)  # Genesis + 3
        
        # All blocks should be valid
        is_valid, message = blockchain.is_chain_valid()
        self.assertTrue(is_valid)
        
        # All mined blocks should start with 3 zeros
        for block in blockchain.chain[1:]:
            self.assertTrue(block.hash.startswith("000"))
            self.assertEqual(block.status, "Mined")
    
    def test_tamper_and_validate_workflow(self):
        """Test tamper detection workflow"""
        blockchain = Blockchain()
        
        # Mine blocks
        for i in range(1, 4):
            block = blockchain.add_block(f"Transaction {i}", 2)
            block.mine_block(2)
            blockchain.append_mined_block(block)
        
        # Should be valid
        is_valid, _ = blockchain.is_chain_valid()
        self.assertTrue(is_valid)
        
        # Tamper with middle block
        blockchain.tamper_block(2, "TAMPERED")
        
        # Should be invalid
        is_valid, message = blockchain.is_chain_valid()
        self.assertFalse(is_valid)
        self.assertIn("Block 2", message)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBlock))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchain))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
