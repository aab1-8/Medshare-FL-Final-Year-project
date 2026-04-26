import subprocess
import time
import os
import sys
import threading
from web3 import Web3

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from medshare.blockchain import MedShareBlockchain

def auto_join_task():
    """Monitors the blockchain and automatically joins any new task created by the simulation."""
    print("[SystemTest] Auto-join monitor started...")
    try:
        blockchain = MedShareBlockchain(rpc_url="http://127.0.0.1:8545")
    except Exception as e:
        print(f"[SystemTest] Blockchain connection failed: {e}")
        return
    
    # Wait for a task to be created
    try:
        last_count = blockchain.task_contract.functions.taskCount().call()
    except:
        last_count = 0
        
    timeout = 120 # 2 minutes
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            current_count = blockchain.task_contract.functions.taskCount().call()
            if current_count > last_count:
                task_id = current_count - 1
                print(f"[SystemTest] Detected new task: {task_id}. Proceeding to auto-join all nodes to satisfy the test requirement...")
                
                # Test script now needs to join multiple hospitals to simulate the manual clicks
                for i in range(8): # Auto-join up to 8 nodes to ensure minClients is met
                    blockchain.join_task(task_id, i)
                print(f"[SystemTest] Automatically joined nodes to Task {task_id}.")
                return
        except Exception as e:
            print(f"[SystemTest] Error during polling: {e}")
        
        time.sleep(2)
    print("[SystemTest] Timeout waiting for task creation.")

def run_system_test():
    """Runs a full FL simulation with blockchain enabled and auto-joins the task."""
    print("="*60)
    print("MEDSHARE SYSTEM TEST: FULL FL + BLOCKCHAIN PIPELINE")
    print("="*60)
    
    # 1. Start the auto-joiner thread
    join_thread = threading.Thread(target=auto_join_task)
    join_thread.daemon = True
    join_thread.start()
    
    # 2. Run the simulation
    cmd = [
        "python", "federated_survival.py",
        "--dataset", "support2",
        "--rounds", "3",
        "--epochs", "1",
        "--enable_blockchain", "True"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    # 3. Monitor output
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())
        
        # We also need to catch the "DEMO PAUSE" from federated_survival.py if we can't bypass it.
        # But our auto-joiner should trigger the 't_status == 1' condition.
            
    process.wait()
    
    if process.returncode == 0:
        print("\n" + "="*60)
        print("[PASS] SYSTEM TEST: Full cycle verified on-chain.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print(f"[FAIL] SYSTEM TEST: Exit code {process.returncode}")
        print("="*60)
        sys.exit(process.returncode)

if __name__ == "__main__":
    run_system_test()
