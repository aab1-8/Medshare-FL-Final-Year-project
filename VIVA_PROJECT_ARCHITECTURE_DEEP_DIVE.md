# 🛡️ MedShare-FL: COMPLETE PROJECT ARCHITECTURE DEEP DIVE
*The Master Encyclopedia of every file, function, and logic block.*

---

## 📂 1. THE PYTHON ENGINE (`medshare/`)
*The mathematical core of the federated learning system.*

### 📄 `medshare/engine.py` (The AI Powerhouse)
**Purpose**: Executes the actual PyTorch training and testing logic.
- **`train()`**: The main loop. It takes a model and patient data, calculates the error (Loss), and nudges the weights to improve.
    - **FedProx (Line 16)**: Anchors the model to prevent "local overfitting."
    - **DP-SGD (Line 30)**: Uses Opacus to inject noise, guaranteeing privacy.
- **`test()`**: Evaluates the model on unseen data to calculate **Accuracy** and **AUC-ROC**.

### 📄 `medshare/strategy.py` (The Security Orchestrator)
**Purpose**: The "Brain" of the central server. It decides how to merge hospital updates.
- **`AnomalyMonitoringStrategy`**: A custom Flower strategy.
- **`aggregate_fit()`**: The most important security function. It uses **Robust-MAD** (Median Absolute Deviation) to filter out malicious hospitals before averaging the weights.
- **Reputation Integration**: If a hospital update is an outlier, this file calls the blockchain to "Slash" their reputation score.

### 📄 `medshare/blockchain.py` (The Python-Web3 Bridge)
**Purpose**: Allows the Python AI code to "talk" to the Ethereum blockchain.
- **`BlockchainManager`**: A class using `Web3.py`.
- **`post_commitment()`**: Sends a SHA-256 hash of the model weights to the blockchain.
- **`create_task_with_bounty()`**: Sends real ETH into an escrow contract for hospitals to earn.

---

## 💎 2. THE SMART CONTRACTS (`contracts/`)
*The "Rules of Law" etched into Ethereum.*

### 📄 `contracts/MedShareTask.sol` (The Master Contract)
**Purpose**: Manages the lifecycle of a medical study.
- **`createTask()`**: Researcher locks ETH and defines how many hospitals are needed.
- **`joinTask()`**: Hospitals register their intent to contribute.
- **`completeTask()`**: Finalizes the study and triggers the payout algorithm.
- **`claimReward()`**: The **Pull Payment** pattern—hospitals withdraw their earned ETH safely.

### 📄 `contracts/Reputation.sol` (The Trust Ledger)
**Purpose**: Tracks the "Credit Score" of every hospital.
- **`updateReputation()`**: Permanently records if a hospital was honest (+1) or malicious (-10).
- **Security**: Only the authorized Strategy node can call this.

---

## 🎨 3. THE DASHBOARD (`frontend/`)
*The JavaScript/HTML/CSS layer that visualizes the network.*

### 📄 `frontend/index.html` (The Structure)
**Purpose**: The single-page architecture for the dashboard.
- **Tabs**: Logic for "Researcher Portal," "Hospital Portal," and "📈 Analytics."
- **Glassmorphism**: Premium CSS styling for a futuristic "Medical-Tech" feel.

### 📄 `frontend/src/blockchain.js` (The JS-Web3 Bridge)
**Purpose**: Uses `Ethers.js` to connect your browser to the blockchain.
- **`blockchain_joinTask()`**: This is what runs when a hospital clicks "Link & Participate."
- **`blockchain_claimReward()`**: Handles the secure withdrawal of ETH bounties.

### 📄 `frontend/src/marketplace.js` (The Application Logic)
**Purpose**: Manages the local "Marketplace" view.
- **`participateRequest()`**: Validates that the hospital is linking the **correct data type** (e.g., you can't join a Diabetes study with Stroke data).
- **`renderRequestCard()`**: Dynamically builds the UI for every study found on the blockchain.

---

## 📊 4. THE LOGIC JSONs & CONFIG
*The "Glue" that binds Python, Solidity, and JavaScript.*

### 📄 `frontend/src/data/deploy_info.json` (The Address Map)
**Purpose**: Stores the exact Ethereum addresses of your contracts.
- **Why it matters**: When the deployment script runs, it saves the addresses here so the Dashboard knows exactly "where" the blockchain lives.

### 📄 `frontend/src/data/MedShareTask.json` (The ABI)
**Purpose**: The "Application Binary Interface."
- **Why it matters**: It’s like a "Menu" of functions. It tells the JavaScript what functions (like `joinTask`) are available on the Smart Contract.

### 📄 `requirements.txt` & `package.json`
**Purpose**: The "Shopping Lists" for the project.
- **`requirements.txt`**: Lists Python tools (PyTorch, Flower, Web3).
- **`package.json`**: Lists JavaScript tools (Vite, Ethers, Chart.js).

---

## 🛠️ 5. THE AUDIT SUITE (`test/`)
*The scientific proof that the project works.*

### 📄 `test/plot_results.py` (The Forensic Scientist)
**Purpose**: Automatically audits the training logs to generate Accuracy vs. Rounds charts.
- **Leakage Audit**: Calculates the **AUC Gap** to prove that patients are safe from Membership Inference Attacks.

### 📄 `test/run_tests.py` (The Integrity Guard)
**Purpose**: A one-click script that verifies the syntax and logic of all 24 files before the demo.

---

**Status: FULL PROJECT ENCYCLOPEDIA COMPLETE.** 👋🛡️🎓🚀
