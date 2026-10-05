# main.py
# Educational Bitcoin Mining Simulator - Main GUI Application

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from blockchain import Blockchain
from mining import MiningEngine
from config import *


class BitcoinMiningSimulator:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        
        # Initialize blockchain and mining engine
        self.blockchain = Blockchain()
        self.mining_engine = MiningEngine(self.blockchain)
        self.mining_engine.set_callbacks(self.update_stats, self.add_log)
        
        # GUI update timer
        self.update_timer = None
        
        # Create GUI
        self.create_gui()
        
        # Start GUI update loop
        self.schedule_update()
    
    def create_gui(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Warning banner
        self.create_warning_banner(main_frame)
        
        # Control panel (left side)
        self.create_control_panel(main_frame)
        
        # Statistics panel (right side)
        self.create_stats_panel(main_frame)
        
        # Blockchain viewer (bottom)
        self.create_blockchain_viewer(main_frame)
        
        # Mining log (bottom right)
        self.create_mining_log(main_frame)
    
    def create_warning_banner(self, parent):
        """Create warning banner at top"""
        banner_frame = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=2)
        banner_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        warning_label = ttk.Label(
            banner_frame,
            text=EDUCATIONAL_WARNING,
            font=("Arial", 14, "bold"),
            foreground="red"
        )
        warning_label.pack(pady=5)
        
        mode_label = ttk.Label(
            banner_frame,
            text="24-HOUR RUN MODE",
            font=("Arial", 10, "bold")
        )
        mode_label.pack()
        
        runtime_warning = ttk.Label(
            banner_frame,
            text=RUNTIME_WARNING,
            font=("Arial", 8),
            foreground="orange",
            wraplength=APP_WIDTH - 40
        )
        runtime_warning.pack(pady=5)
    
    def create_control_panel(self, parent):
        """Create control panel with buttons and settings"""
        control_frame = ttk.LabelFrame(parent, text="Mining Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 5))
        
        # Mining buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(
            button_frame,
            text="⛏ Start Mining",
            command=self.start_mining,
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self.pause_mining,
            width=15,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop_mining,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_button = ttk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset_mining,
            width=15
        )
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        # Difficulty selector
        diff_frame = ttk.Frame(control_frame)
        diff_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(diff_frame, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=list(DIFFICULTY_LEVELS.keys()),
            state="readonly",
            width=15
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        difficulty_combo.bind("<<ComboboxSelected>>", self.on_difficulty_change)
        
        # CPU workload selector
        cpu_frame = ttk.Frame(control_frame)
        cpu_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cpu_frame, text="CPU Workload:").pack(side=tk.LEFT, padx=5)
        self.workload_var = tk.StringVar(value="Medium")
        workload_combo = ttk.Combobox(
            cpu_frame,
            textvariable=self.workload_var,
            values=list(CPU_WORKLOAD.keys()),
            state="readonly",
            width=15
        )
        workload_combo.pack(side=tk.LEFT, padx=5)
        workload_combo.bind("<<ComboboxSelected>>", self.on_workload_change)
        
        # Tamper demonstration
        tamper_frame = ttk.LabelFrame(control_frame, text="Educational Features", padding="10")
        tamper_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            tamper_frame,
            text="🔧 Tamper Test",
            command=self.tamper_demo,
            width=20
        ).pack(pady=2)
        
        ttk.Button(
            tamper_frame,
            text="✓ Validate Blockchain",
            command=self.validate_blockchain,
            width=20
        ).pack(pady=2)
    
    def create_stats_panel(self, parent):
        """Create statistics display panel"""
        stats_frame = ttk.LabelFrame(parent, text="Mining Statistics", padding="10")
        stats_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), padx=(5, 0))
        
        # Statistics labels
        self.stats_labels = {}
        stats_data = [
            ("Current Block:", "block_number"),
            ("Current Nonce:", "nonce"),
            ("Current Hash:", "hash"),
            ("Hash Rate:", "hash_rate"),
            ("Total Hashes:", "total_hashes"),
            ("Blocks Found:", "blocks_found"),
            ("Runtime:", "runtime"),
            (DEMO_COINS_LABEL + ":", "demo_coins")
        ]
        
        for i, (label_text, key) in enumerate(stats_data):
            label_frame = ttk.Frame(stats_frame)
            label_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(
                label_frame,
                text=label_text,
                font=("Arial", 9, "bold"),
                width=20,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            value_label = ttk.Label(
                label_frame,
                text="0",
                font=("Arial", 9),
                anchor=tk.W
            )
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.stats_labels[key] = value_label
    
    def create_blockchain_viewer(self, parent):
        """Create blockchain viewer with treeview"""
        viewer_frame = ttk.LabelFrame(parent, text="Blockchain Viewer", padding="10")
        viewer_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Create treeview
        columns = ("Block", "Previous Hash", "Nonce", "Hash", "Difficulty", "Timestamp", "Status")
        self.tree = ttk.Treeview(viewer_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ["Block", "Nonce", "Difficulty"]:
                self.tree.column(col, width=80, anchor=tk.CENTER)
            elif col == "Status":
                self.tree.column(col, width=100, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=150, anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(viewer_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to show block details
        self.tree.bind("<Double-1>", self.show_block_details)
        
        # Initial population
        self.update_blockchain_viewer()
    
    def create_mining_log(self, parent):
        """Create mining log display"""
        log_frame = ttk.LabelFrame(parent, text="Mining Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            width=100,
            font=("Courier", 8),
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial log
        self.add_log("Educational Bitcoin Mining Simulator initialized")
        self.add_log("This is a demonstration only - no real Bitcoin mining occurs")
    
    def start_mining(self):
        """Start mining process"""
        self.mining_engine.start_mining()
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
    
    def pause_mining(self):
        """Pause/resume mining"""
        if self.mining_engine.is_paused:
            self.mining_engine.resume_mining()
            self.pause_button.config(text="⏸ Pause")
        else:
            self.mining_engine.pause_mining()
            self.pause_button.config(text="▶ Resume")
    
    def stop_mining(self):
        """Stop mining process"""
        self.mining_engine.stop_mining()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="⏸ Pause")
        self.stop_button.config(state=tk.DISABLED)
    
    def reset_mining(self):
        """Reset mining statistics"""
        if messagebox.askyesno("Reset", "Reset all mining statistics and blockchain?"):
            self.mining_engine.reset()
            self.update_stats()
            self.update_blockchain_viewer()
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, text="⏸ Pause")
            self.stop_button.config(state=tk.DISABLED)
    
    def on_difficulty_change(self, event):
        """Handle difficulty change"""
        difficulty_name = self.difficulty_var.get()
        difficulty = DIFFICULTY_LEVELS[difficulty_name]
        self.mining_engine.set_difficulty(difficulty)
        self.add_log(f"Difficulty changed to: {difficulty_name} ({difficulty} leading zeros)")
    
    def on_workload_change(self, event):
        """Handle CPU workload change"""
        workload_name = self.workload_var.get()
        workload = CPU_WORKLOAD[workload_name]
        self.mining_engine.set_workload(workload)
        self.add_log(f"CPU workload changed to: {workload_name}")
    
    def update_stats(self):
        """Update statistics display"""
        stats = self.mining_engine.get_stats()
        
        self.stats_labels["block_number"].config(text=str(stats["block_number"]))
        self.stats_labels["nonce"].config(text=f"{stats['nonce']:,}")
        
        hash_display = stats["hash"][:32] + "..." if stats["hash"] != "N/A" else "N/A"
        self.stats_labels["hash"].config(text=hash_display)
        
        self.stats_labels["hash_rate"].config(text=f"{stats['hash_rate']:,.2f} H/s")
        self.stats_labels["total_hashes"].config(text=f"{stats['total_hashes']:,}")
        self.stats_labels["blocks_found"].config(text=str(stats["blocks_found"]))
        
        # Format runtime
        elapsed = int(stats["elapsed_time"])
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.stats_labels["runtime"].config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        self.stats_labels["demo_coins"].config(
            text=f"{stats['demo_coins']:.2f}",
            foreground="green",
            font=("Arial", 9, "bold")
        )
    
    def update_blockchain_viewer(self):
        """Update blockchain viewer with current chain"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add all blocks
        for block in self.blockchain.get_all_blocks():
            block_dict = block.to_dict()
            self.tree.insert(
                "",
                tk.END,
                values=(
                    block_dict["Block"],
                    block_dict["Previous Hash"],
                    block_dict["Nonce"],
                    block_dict["Hash"],
                    block_dict["Difficulty"],
                    block_dict["Timestamp"],
                    block_dict["Status"]
                )
            )
    
    def show_block_details(self, event):
        """Show detailed information for selected block"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            block_number = item["values"][0]
            block = self.blockchain.get_block(block_number)
            
            if block:
                details = block.get_full_details()
                detail_text = "\n".join([f"{key}: {value}" for key, value in details.items()])
                messagebox.showinfo(f"Block {block_number} Details", detail_text)
    
    def add_log(self, message):
        """Add message to mining log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Limit log size to prevent memory issues
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 1000:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete('1.0', '100.0')
            self.log_text.config(state=tk.DISABLED)
    
    def schedule_update(self):
        """Schedule periodic GUI updates"""
        self.update_stats()
        self.update_blockchain_viewer()
        self.update_timer = self.root.after(GUI_UPDATE_INTERVAL, self.schedule_update)
    
    def tamper_demo(self):
        """Demonstrate tampering with blockchain"""
        blocks = self.blockchain.get_all_blocks()
        if len(blocks) < 2:
            messagebox.showinfo("Tamper Test", "Mine at least one block first!")
            return
        
        # Tamper with block 1
        success = self.blockchain.tamper_block(1, "TAMPERED DATA - Educational Demo")
        if success:
            self.add_log("⚠ Block 1 has been tampered with for demonstration")
            self.update_blockchain_viewer()
            messagebox.showwarning(
                "Tamper Test",
                "Block 1 data has been changed!\n\n"
                "Notice:\n"
                "1. Block 1's hash changed\n"
                "2. Block 2's 'Previous Hash' no longer matches\n"
                "3. The chain is now INVALID\n\n"
                "Use 'Validate Blockchain' to verify."
            )
    
    def validate_blockchain(self):
        """Validate the entire blockchain"""
        is_valid, message = self.blockchain.is_chain_valid()
        self.add_log(f"Blockchain validation: {message}")
        
        if is_valid:
            messagebox.showinfo("Blockchain Validation", "✓ " + message)
        else:
            messagebox.showerror("Blockchain Validation", "✗ " + message)
    
    def on_closing(self):
        """Handle window close event"""
        if self.mining_engine.is_mining:
            if messagebox.askokcancel("Quit", "Mining is active. Stop and quit?"):
                self.mining_engine.stop_mining()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = BitcoinMiningSimulator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
