import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import numpy as np

# Add the parent directory to sys.path to import medshare
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medshare.blockchain import MedShareBlockchain

class TestBlockchainLogic(unittest.TestCase):
    @patch('medshare.blockchain.Web3')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"MedShareTask": "0x1", "CommitmentRegistry": "0x2", "Reputation": "0x3", "abi": []}')
    def setUp(self, mock_file, mock_exists, mock_web3):
        # Setup mocks
        mock_exists.return_value = True
        
        # Mock Web3 instance
        self.mock_w3 = MagicMock()
        mock_web3.return_value = self.mock_w3
        self.mock_w3.eth.accounts = ['0xAdmin', '0xHosp1', '0xHosp2']
        self.mock_w3.eth.contract.return_value = MagicMock()
        
        # Mock connection check
        self.mock_w3.is_connected.return_value = True
        
        # Initialize the blockchain class
        # We need to mock the json.load inside the class too for ABIs
        with patch('json.load') as mock_json:
            mock_json.side_effect = [
                {"MedShareTask": "0x1", "CommitmentRegistry": "0x2", "Reputation": "0x3"}, # deploy_info
                {"abi": []}, # MedShareTask ABI
                {"abi": []}, # CommitmentRegistry ABI
                {"abi": []}  # Reputation ABI
            ]
            self.blockchain = MedShareBlockchain(rpc_url="http://mock:8545")

    def test_connection_heartbeat(self):
        """Test the is_connected heartbeat."""
        self.assertTrue(self.blockchain.is_connected())

    def test_hash_weights(self):
        """Test the internal weight hashing logic (SHA-256)."""
        weights = [np.array([1.0, 2.0]), np.array([3.0])]
        h = self.blockchain.hash_weights(weights)
        self.assertIsInstance(h, bytes)
        self.assertEqual(len(h), 32) # SHA-256 is 32 bytes

    @patch('medshare.blockchain.int')
    def test_post_commitment(self, mock_int):
        """Test posting a commitment (calls contract function)."""
        weights = [np.array([0.1])]
        task_id = 0
        round_num = 1
        client_id = 0
        
        # Mock the contract function call
        mock_func = self.blockchain.registry_contract.functions.postCommitment
        mock_func.return_value.transact.return_value = b'tx_hash'
        
        # Mock receipt as an object with gasUsed attribute
        mock_receipt = MagicMock()
        mock_receipt.gasUsed = 100000
        self.mock_w3.eth.wait_for_transaction_receipt.return_value = mock_receipt
        
        gas = self.blockchain.post_commitment(task_id, round_num, weights, client_id)
        
        self.assertEqual(gas, 100000)
        mock_func.assert_called_once()
        self.mock_w3.eth.wait_for_transaction_receipt.assert_called_once_with(b'tx_hash')

    def test_update_reputation(self):
        """Test reputation update transaction flow."""
        mock_func = self.blockchain.reputation_contract.functions.updateReputation
        self.blockchain.update_reputation(0, 10, "Great work")
        
        # Verify it uses account 1 (admin is 0, hospitals start at 1)
        mock_func.assert_called_with(self.mock_w3.eth.accounts[1], 10, "Great work")

    def test_authorize_hospital(self):
        """Test the multi-contract authorization flow."""
        mock_auth_task = self.blockchain.task_contract.functions.authorizeHospital
        mock_auth_reg = self.blockchain.registry_contract.functions.authorizeHospital
        
        # Mock that hospital is NOT authorized
        self.blockchain.task_contract.functions.authorizedHospitals.return_value.call.return_value = False
        
        self.blockchain.authorize_hospital(0)
        
        mock_auth_task.assert_called_with(self.mock_w3.eth.accounts[1], True)
        mock_auth_reg.assert_called_with(self.mock_w3.eth.accounts[1], True)

    def test_join_task(self):
        """Test joining a task with auto-authorization."""
        mock_join = self.blockchain.task_contract.functions.joinTask
        
        # Mock that hospital is already authorized
        self.blockchain.task_contract.functions.authorizedHospitals.return_value.call.return_value = True
        
        success = self.blockchain.join_task(0, 0)
        
        self.assertTrue(success)
        mock_join.assert_called_with(0)

    def test_create_task_with_bounty(self):
        """Test creating a task and funding it with ETH."""
        mock_create = self.blockchain.task_contract.functions.createTask
        self.blockchain.task_contract.functions.taskCount.return_value.call.return_value = 5 # 4+1
        
        # Mock wait_for_transaction_receipt
        mock_receipt = MagicMock()
        mock_receipt.transactionHash.hex.return_value = "0xabcdef1234"
        self.mock_w3.eth.wait_for_transaction_receipt.return_value = mock_receipt

        task_id = self.blockchain.create_task_with_bounty("Test Task", 3, 10, 0.5)
        
        self.assertEqual(task_id, 4)
        mock_create.assert_called_with("Test Task", 3, 10)
        
    def test_finalize_task(self):
        """Test the end-to-end task finalization and payout."""
        mock_complete = self.blockchain.task_contract.functions.completeTask
        weights = [np.array([0.5])]
        
        success = self.blockchain.finalize_task(0, weights)
        
        self.assertTrue(success)
        mock_complete.assert_called_once()
        # Verify hash was passed as hex string
        args, kwargs = mock_complete.call_args
        self.assertIsInstance(args[1], str)
        self.assertEqual(len(args[1]), 64) # SHA256 hex is 64 chars

if __name__ == '__main__':
    unittest.main()