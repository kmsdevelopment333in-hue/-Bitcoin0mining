# mining.py
# Mining engine for educational Bitcoin mining simulator

import threading
import time
import hashlib
from blockchain import Blockchain


class MiningEngine:
    """Handles the mining process in a separate thread"""
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.is_mining = False
        self.is_paused = False
        self.current_block = None
        self.current_nonce = 0
        self.total_hashes = 0
        self.blocks_found = 0
        self.start_time = None
        self.elapsed_time = 0
        self.pause_time = None
        self.difficulty = 4
        self.hashes_per_batch = 5000
        self.mining_thread = None
        self.stats_callback = None
        self.log_callback = None
    
    def set_difficulty(self, difficulty):
        """Set mining difficulty"""
        self.difficulty = difficulty
    
    def set_workload(self, hashes_per_batch):
        """Set CPU workload (hashes per batch)"""
        self.hashes_per_batch = hashes_per_batch
    
    def set_callbacks(self, stats_callback, log_callback):
        """Set callbacks for updating GUI"""
        self.stats_callback = stats_callback
        self.log_callback = log_callback
    
    def start_mining(self):
        """Start the mining process"""
        if not self.is_mining:
            self.is_mining = True
            self.is_paused = False
            if self.start_time is None:
                self.start_time = time.time()
            elif self.pause_time is not None:
                # Resume from pause
                self.start_time += (time.time() - self.pause_time)
                self.pause_time = None
            
            self.mining_thread = threading.Thread(target=self._mine, daemon=True)
            self.mining_thread.start()
            self._log("Mining started")
    
    def pause_mining(self):
        """Pause the mining process"""
        if self.is_mining and not self.is_paused:
            self.is_paused = True
            self.pause_time = time.time()
            self._log("Mining paused")
    
    def resume_mining(self):
        """Resume mining after pause"""
        if self.is_mining and self.is_paused:
            self.is_paused = False
            if self.pause_time is not None:
                self.start_time += (time.time() - self.pause_time)
                self.pause_time = None
            self._log("Mining resumed")
    
    def stop_mining(self):
        """Stop the mining process"""
        if self.is_mining:
            self.is_mining = False
            self.is_paused = False
            if self.mining_thread:
                self.mining_thread.join(timeout=2)
            self._log("Mining stopped")
    
    def reset(self):
        """Reset all mining statistics"""
        self.stop_mining()
        self.current_block = None
        self.current_nonce = 0
        self.total_hashes = 0
        self.blocks_found = 0
        self.start_time = None
        self.elapsed_time = 0
        self.pause_time = None
        self.blockchain.reset()
        self._log("Mining statistics reset")
    
    def _mine(self):
        """Main mining loop (runs in separate thread)"""
        while self.is_mining:
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            # Create new block if needed
            if self.current_block is None:
                block_data = f"Block {len(self.blockchain.chain)} - Educational Demo Transaction"
                self.current_block = self.blockchain.add_block(block_data, self.difficulty)
                self.current_nonce = 0
                self._log(f"Mining block {self.current_block.index}...")
            
            # Mine in batches to allow responsiveness
            target = "0" * self.difficulty
            batch_complete = False
            
            for _ in range(self.hashes_per_batch):
                if not self.is_mining or self.is_paused:
                    break
                
                self.current_block.nonce = self.current_nonce
                self.current_block.hash = self.current_block.calculate_hash()
                self.total_hashes += 1
                self.current_nonce += 1
                
                # Check if valid hash found
                if self.current_block.hash[:self.difficulty] == target:
                    self.current_block.status = "Mined"
                    self.blockchain.append_mined_block(self.current_block)
                    self.blocks_found += 1
                    self._log(f"✓ Block {self.current_block.index} found! Hash: {self.current_block.hash[:16]}...")
                    self.current_block = None
                    batch_complete = True
                    break
            
            # Update statistics
            if self.start_time:
                self.elapsed_time = time.time() - self.start_time
            
            if self.stats_callback:
                self.stats_callback()
            
            # Small delay to prevent CPU overload
            if not batch_complete:
                time.sleep(0.001)
    
    def get_hash_rate(self):
        """Calculate current hash rate"""
        if self.elapsed_time > 0:
            return self.total_hashes / self.elapsed_time
        return 0
    
    def get_demo_coins(self):
        """Calculate demo coins earned"""
        from config import BLOCK_REWARD
        return self.blocks_found * BLOCK_REWARD
    
    def _log(self, message):
        """Send log message to callback"""
        if self.log_callback:
            timestamp = time.strftime("%H:%M:%S")
            self.log_callback(f"[{timestamp}] {message}")
    
    def get_stats(self):
        """Get current mining statistics"""
        return {
            "block_number": self.current_block.index if self.current_block else len(self.blockchain.chain),
            "nonce": self.current_nonce,
            "hash": self.current_block.hash if self.current_block else "N/A",
            "hash_rate": self.get_hash_rate(),
            "total_hashes": self.total_hashes,
            "blocks_found": self.blocks_found,
            "elapsed_time": self.elapsed_time,
            "demo_coins": self.get_demo_coins()
        }
