import unittest
import sys
import os
import numpy as np
from web3 import Web3

# Add the parent directory to sys.path to import medshare
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medshare.blockchain import MedShareBlockchain

class TestBlockchainIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We assume Ganache is running on 8545 and contracts are deployed
        cls.blockchain = MedShareBlockchain(rpc_url="http://127.0.0.1:8545")
        cls.w3 = cls.blockchain.w3
        
    def test_01_connection(self):
        """Verify we are connected to the live Ganache instance."""
        self.assertTrue(self.blockchain.is_connected())
        print(f"Connected to Ganache. Network ID: {self.w3.eth.chain_id}")

    def test_02_create_task(self):
        """Create a new FL task with a real ETH bounty."""
        description = "Integration Test Task"
        min_clients = 1 # One client is enough to start training
        rounds = 3
        bounty_eth = 1.0 # 1 ETH bounty
        
        # Get balance before
        admin_bal_before = float(self.w3.from_wei(self.w3.eth.get_balance(self.w3.eth.accounts[0]), 'ether'))
        
        TestBlockchainIntegration.current_task_id = self.blockchain.create_task_with_bounty(description, min_clients, rounds, bounty_eth)
        
        self.assertIsNotNone(TestBlockchainIntegration.current_task_id)
        print(f"Created Task ID: {TestBlockchainIntegration.current_task_id}")
        
        # Verify balance decreased (plus gas)
        admin_bal_after = float(self.w3.from_wei(self.w3.eth.get_balance(self.w3.eth.accounts[0]), 'ether'))
        self.assertLess(admin_bal_after, admin_bal_before - float(bounty_eth))

    def test_03_participation_flow(self):
        """Full lifecycle: join, commit, finalize, payout."""
        task_id = TestBlockchainIntegration.current_task_id
        hospital_idx = 0 # Account 1
        
        # 1. Join Task
        success = self.blockchain.join_task(task_id, hospital_idx)
        self.assertTrue(success)
        print(f"Hospital {hospital_idx} joined task {task_id}")
        
        # 2. Post Commitment (Audit Hash)
        weights = [np.array([0.1, 0.2]), np.array([0.3])]
        gas = self.blockchain.post_commitment(task_id, 1, weights, hospital_idx)
        self.assertIsNotNone(gas)
        self.assertGreater(gas, 0)
        print(f"Posted commitment for round 1. Gas used: {gas}")
        
        # 3. Finalize and Payout
        # Get hospital balance before payout
        hosp_acc = self.w3.eth.accounts[hospital_idx + 1]
        bal_before = self.w3.from_wei(self.w3.eth.get_balance(hosp_acc), 'ether')
        
        # Finalize (hashes weights and releases bounty)
        success_final = self.blockchain.finalize_task(task_id, weights)
        self.assertTrue(success_final)
        
        # 4. Claim Reward (Withdrawal)
        success_claim = self.blockchain.claim_reward(hospital_idx)
        self.assertTrue(success_claim)
        
        # 5. Verify Payout
        bal_after = self.w3.from_wei(self.w3.eth.get_balance(hosp_acc), 'ether')
        self.assertGreater(bal_after, bal_before)
        print(f"Bounty payout verified. Balance increased from {bal_before} to {bal_after} ETH")

    def test_04_reputation(self):
        """Verify reputation scoring works on-chain."""
        hospital_idx = 1 # Account 2
        
        # Get initial
        score_before = self.blockchain.get_reputation(hospital_idx)
        
        # Update (Reward)
        self.blockchain.update_reputation(hospital_idx, 50, "Consistent performance")
        
        # Check after
        score_after = self.blockchain.get_reputation(hospital_idx)
        self.assertEqual(score_after, score_before + 50)
        print(f"Reputation updated from {score_before} to {score_after}")

if __name__ == '__main__':
    unittest.main()
