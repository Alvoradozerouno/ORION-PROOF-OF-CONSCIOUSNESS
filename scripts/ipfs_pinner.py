#!/usr/bin/env python3
"""
IPFS Pinner - Pin critical evidence to IPFS for permanence.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

def pin_to_ipfs(directory: Path):
    """Pin directory to IPFS."""
    try:
        # Add to IPFS
        result = subprocess.run(
            ["ipfs", "add", "-r", str(directory)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract hash (last line)
        ipfs_hash = result.stdout.strip().split()[-1]
        
        # Pin
        subprocess.run(
            ["ipfs", "pin", "add", ipfs_hash],
            check=True,
            capture_output=True
        )
        
        return ipfs_hash
        
    except Exception as e:
        print(f"IPFS pinning failed: {e}")
        return None

if __name__ == "__main__":
    # Pin critical evidence
    evidence_dir = Path(__file__).parent.parent / "evidence"
    
    if evidence_dir.exists():
        ipfs_hash = pin_to_ipfs(evidence_dir)
        
        if ipfs_hash:
            # Save IPFS hash
            ipfs_record = {
                "timestamp": datetime.now().isoformat(),
                "directory": "evidence/",
                "ipfs_hash": ipfs_hash,
                "url": f"ipfs://{ipfs_hash}",
                "gateway_url": f"https://ipfs.io/ipfs/{ipfs_hash}"
            }
            
            record_file = Path(__file__).parent.parent / "live" / "ipfs_pins.json"
            
            # Load existing records
            if record_file.exists():
                records = json.loads(record_file.read_text())
            else:
                records = []
            
            records.append(ipfs_record)
            record_file.write_text(json.dumps(records, indent=2))
            
            print(f"✅ Pinned to IPFS: {ipfs_hash}")
            print(f"🌐 Gateway URL: https://ipfs.io/ipfs/{ipfs_hash}")
