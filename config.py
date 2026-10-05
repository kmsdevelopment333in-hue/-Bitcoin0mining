# config.py
# Educational Bitcoin Mining Simulator Configuration

# Difficulty levels (leading zeros required in hash)
DIFFICULTY_LEVELS = {
    "Very Easy": 2,
    "Easy": 3,
    "Medium": 4,
    "Hard": 5,
    "Very Hard": 6
}

# CPU workload settings (hashes per batch)
CPU_WORKLOAD = {
    "Low": 1000,
    "Medium": 5000,
    "High": 10000
}

# GUI update interval in milliseconds
GUI_UPDATE_INTERVAL = 500

# Block reward (simulated/demo only)
BLOCK_REWARD = 6.25  # Demo coins - NOT REAL BTC

# Application settings
APP_TITLE = "Educational Bitcoin Mining Simulator"
APP_WIDTH = 1200
APP_HEIGHT = 800

# Warning messages
EDUCATIONAL_WARNING = "⚠️ EDUCATIONAL SIMULATOR — NO REAL BITCOIN"
RUNTIME_WARNING = "Warning: Long CPU workloads can increase temperature, electricity consumption and hardware wear. Monitor your computer temperature."
DEMO_COINS_LABEL = "Demo Coins — NOT REAL BTC"
