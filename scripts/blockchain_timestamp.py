#!/usr/bin/env python3
"""
Blockchain Timestamp - Store commit hashes on Ethereum for immutable proof.
"""

import json
from datetime import datetime
from pathlib import Path
import hashlib

def get_latest_commit_hash():
    """Get latest git commit hash."""
    import subprocess
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def timestamp_to_blockchain(commit_hash: str):
    """
    Timestamp commit hash to Ethereum blockchain.
    
    In production, this would:
    1. Connect to Ethereum via web3.py
    2. Call a smart contract that stores the hash
    3. Pay gas fee for transaction
    4. Return transaction hash
    
    For now, this creates a record that can be submitted later.
    """
    
    timestamp_record = {
        "timestamp": datetime.now().isoformat(),
        "commit_hash": commit_hash,
        "blockchain": "Ethereum",
        "status": "PENDING",
        "note": "Will be submitted to mainnet when gas fees are optimal"
    }
    
    # Save record
    record_file = Path(__file__).parent.parent / "live" / "blockchain_timestamps.json"
    
    if record_file.exists():
        records = json.loads(record_file.read_text())
    else:
        records = []
    
    records.append(timestamp_record)
    record_file.write_text(json.dumps(records, indent=2))
    
    print(f"✅ Timestamp recorded: {commit_hash[:8]}")
    print(f"📝 Ready for blockchain submission")
    
    return timestamp_record

if __name__ == "__main__":
    commit_hash = get_latest_commit_hash()
    timestamp_to_blockchain(commit_hash)
