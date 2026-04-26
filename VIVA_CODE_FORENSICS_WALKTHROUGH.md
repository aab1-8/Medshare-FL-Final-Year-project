# 🛡️ MedShare-FL: THE COMPLETE REPOSITORY ENCYCLOPEDIA
*Every file. Every line. Every connection. Full Project Mastery.*

---

## 🐍 SECTION 1: THE AI CORE (Python)
*The engine that powers the federated clinical learning.*

### 1. `medshare/engine.py` (The "AI Guts")
**Mission**: Executes the mathematical training on the GPU/CPU.
- **[Line 16 (FedProx Anchor)](./medshare/engine.py#L16)**: `global_params` captures the initial weights at the start of a round to calculate the "Proximal Penalty."
- **[Line 30 (DP-SGD Injection)](./medshare/engine.py#L30)**: Integrates `opacus.make_private` to wrap the optimizer in a privacy-preserving shell.
- **[Line 58 (Stability Guard)](./medshare/engine.py#L58)**: Uses `nan_to_num(0.5)` and `clamp` to prevent the model from crashing if Differential Privacy noise becomes too volatile.
- **[Line 67 (Proximal Math)](./medshare/engine.py#L67)**: The exact L2-distance formula that keeps local models from drifting too far from the global consensus.
- **[Line 139 (AUC Scorer)](./medshare/engine.py#L139)**: Calculates the Area Under Curve (ROC), the industry-standard for clinical risk ranking.

### 2. `medshare/strategy.py` (The "Security Filter")
**Mission**: The server-side brain that aggregates hospital updates.
- **[Line 36 (NaN Scrubbing)](./medshare/strategy.py#L36)**: Proactively excludes nodes that send corrupted (NaN/Inf) weights before they touch the global average.
- **[Line 57 (Robust-MAD Filter)](./medshare/strategy.py#L57)**: The core defense. Calculates the **Median Absolute Deviation** of weight norms to detect poisoning.
- **[Line 81 (Sashing Transaction)](./medshare/strategy.py#L81)**: Triggers an on-chain reputation penalty (`update_reputation`) if an anomaly is detected.
- **[Line 145 (State Checkpointing)](./medshare/strategy.py#L145)**: Maps NumPy arrays back to a PyTorch `state_dict` and saves the best-performing model to `best_model.pth`.

### 3. `medshare/client.py` (The "Hospital Node")
**Mission**: The representative of a single hospital node.
- **[Line 24 (GPU Handshake)](./medshare/client.py#L24)**: Dynamically detects `cuda:0` to leverage vLab's GPU hardware for faster clinical training.
- **[Line 29 (Label Flip Attack)](./medshare/client.py#L29)**: Simulates a malicious hospital by reversing patient labels (0 -> 1) to test system robustness.
- **[Line 83 (SHA-256 Audit)](./medshare/client.py#L83)**: Posts weight fingerprints to Ethereum *before* the server sees them.
- **[Line 94 (Double Masking)](./medshare/client.py#L94)**: Implements **Secure Aggregation** by adding secret pairwise masks to hide raw weights.

### 4. `medshare/data.py` (The "Clinical Fuel")
**Mission**: Fetches and prepares real clinical data (SUPPORT2, CDC, etc.).
- **[Line 161 (SMOTE)](./medshare/data.py#L161)**: The **Synthetic Minority Over-sampling Technique** used to fix class imbalance in rare diseases.
- **[Line 221 (Heterogeneity Simulation)](./medshare/data.py#L221)**: Sorts data by label or feature to simulate "Non-IID" (Skewed) real-world hospitals.
- **[Line 262 (Global Scaler)](./medshare/data.py#L262)**: Uses `MinMaxScaler` to ensure clinical features (like Blood Pressure) don't dominate the neural learning process.

### 5. `medshare/models.py` (The "Brain")
**Mission**: The architecture of the clinical AI model.
- **[Line 5 (Weight Serialization)](./medshare/models.py#L5)**: The `get_parameters` function. It strips the PyTorch tensors off the GPU and converts them to raw NumPy arrays so they can be transmitted over the internet via Flower.
- **[Line 13 (Weight Hydration)](./medshare/models.py#L13)**: The `set_parameters` function. It receives NumPy arrays from the Global Server and strictly loads them back into the local Neural Network (`strict=True` guards against dimension mismatch).
- **[Line 26 (Clinical MLP)](./medshare/models.py#L26)**: The `SurvivalMLP` architecture. Maps inputs -> 256 nodes -> ReLU -> 128 nodes -> ReLU -> Output. Chosen specifically for tabular clinical data where CNNs/RNNs would fail.
- **[Line 43 (Adaptive Output)](./medshare/models.py#L43)**: Automatically appends a `Sigmoid` layer for binary classification tasks.

### 6. `medshare/utils.py` (The "Audit Logger")
**Mission**: Calculates metrics and logs gas/latency to CSVs.
- **[Line 45 (MI-Gap Scoring)](./medshare/utils.py#L45)**: The Yeom-formula implementation for measuring **Membership Inference** privacy leakage.
- **[Line 128 (Dashboard Sync)](./medshare/utils.py#L128)**: The bridge that writes real-time training telemetry to `training_history.json` for the web interface.
- **[Line 147 (Pairwise Mask Gen)](./medshare/utils.py#L147)**: Generates the cryptographically secure additive noise used in Secure Aggregation.

---

## 💎 SECTION 2: THE TRUST LAYER (Blockchain)
*The decentralized judge that manages rewards and audits.*

### 7. `contracts/MedShareTask.sol` (The "Law")
**Mission**: The main contract governing the study lifecycle.
- **[Line 104 (Honest Filter)](./contracts/MedShareTask.sol#L104)**: The `completeTask` function uses an internal `honestHospitals` array to ensure only nodes with positive reputation receive a share of the ETH bounty.
- **[Line 132 (Bounty Escrow)](./contracts/MedShareTask.sol#L132)**: Implements the **Pull Pattern** by crediting `pendingWithdrawals` rather than sending ETH directly. This prevents "Denial of Service" attacks during payout.
- **[Line 158 (Secure Claim)](./contracts/MedShareTask.sol#L158)**: The `claimReward` function, which ensures only the rightful owner of a wallet can withdraw their clinical research rewards.

### 8. `contracts/CommitmentRegistry.sol` (The "Audit Vault")
**Mission**: Stores SHA-256 model fingerprints.
- **[Line 46 (postCommitment)](./contracts/CommitmentRegistry.sol#L46)**: An immutable mapping that links a `taskId`, `roundNum`, and `modelHash`. Once posted, this cannot be deleted or changed.
- **[Line 75 (postFinalWeights)](./contracts/CommitmentRegistry.sol#L75)**: Records the final aggregated global model fingerprint for post-study scientific verification.

### 9. `contracts/Reputation.sol` (The "Credit Score")
**Mission**: Permanent trust scores for nodes.
- **[Line 34 (updateReputation)](./contracts/Reputation.sol#L34)**: The `onlyAdmin` function that applies the rewards (+1) or slashes (-10) based on the AI core's Robust-MAD analysis.

### 10. `medshare/blockchain.py` (The "Python-Web3 Bridge")
**Mission**: Translates Python AI commands into Ethereum transactions.
- **[Line 115 (SHA-256 Logic)](./medshare/blockchain.py#L115)**: The `hash_weights` function that converts multi-dimensional NumPy arrays into a flat byte stream for hashing.
- **[Line 186 (post_commitment)](./medshare/blockchain.py#L186)**: The Web3 wrapper that calculates the **Gas Used** for each audit transaction.
- **[Line 221 (Task Escrowing)](./medshare/blockchain.py#L221)**: The logic that converts "Bounty ETH" into "Wei" before funding a task.
- **[Line 282 (finalize_task)](./medshare/blockchain.py#L282)**: Triggers the final bounty release and cross-checks the final model hash.

---

## 🎨 SECTION 3: THE INTERFACE (Frontend)
*The visualization and interaction dashboard.*

### 11. `frontend/index.html` (The "Skin")
**Mission**: The visual layout of the dashboard.
- **[Line 34 (Audit Selector)](./frontend/index.html#L34)**: The `<select>` element that allows switching between the "Live Simulation" and "Pre-calculated SOTA Benchmarks."
- **[Line 60 (View Toggles)](./frontend/index.html#L60)**: A group of control buttons that drive the `setupViewToggle()` logic in `main.js`.
- **[Line 86 (Node Mapping)](./frontend/index.html#L86)**: The selection box that maps your browser session to one of the 10 Ganache blockchain wallets.

### 12. `frontend/src/main.js` (The "UI Pulse")
**Mission**: Orchestrates the UI logic and view switching.
- **[Line 12 (Data Fetcher)](./frontend/src/main.js#L12)**: Uses `Promise.all` to concurrently load the stats, baselines, and history, ensuring a smooth "Loading" experience.
- **[Line 151 (Audit Jumper)](./frontend/src/main.js#L151)**: A helper function that automatically navigates the UI when a user clicks a "View Audit" button in the marketplace.
- **[Line 208 (Safety Reset)](./frontend/src/main.js#L208)**: Triggers the custom modal that clears `localStorage` to reset the simulation for a fresh demo.

### 13. `frontend/src/marketplace.js` (The "Study Manager")
**Mission**: Manages bounty creation and dataset linking.
- **[Line 158 (Join Logic)](./frontend/src/marketplace.js#L158)**: Verifies that a hospital node is "Logged In" and "Dataset Linked" before allowing them to participate in a study.
- **[Line 245 (Form Handler)](./frontend/src/marketplace.js#L245)**: Captures input from the researcher form and triggers the blockchain `createTask` transaction.

### 14. `frontend/src/charts.js` (The "Visual Evidence")
**Mission**: Renders the SOTA accuracy comparisons.
- **[Line 177 (Bar Logic)](./frontend/src/charts.js#L177)**: A Chart.js implementation that draws the three bars (Local, Centralized, Federated) for direct comparison.
- **[Line 35 (Theme Awareness)](./frontend/src/charts.js#L35)**: Dynamically checks if `light-mode` is active to swap grid and label colors for high visibility.

### 15. `frontend/src/blockchain.js` (The "Browser-Web3 Bridge")
**Mission**: Connects the Dashboard directly to Ganache via Ethers.js.
- **[Line 55 (Contract Proxy)](./frontend/src/blockchain.js#L55)**: Uses `getTaskContract()` to create a local Ethers object for sending real money (Bounty ETH) to the chain.
- **[Line 144 (Claim Transaction)](./frontend/src/blockchain.js#L144)**: Signs the withdrawal transaction with the hospital's private key to pull funds from the escrow.

---

## 🧪 SECTION 4: THE DATA BRIDGES (JSON)
*The communication files between sections.*

### 16. `frontend/src/data/deploy_info.json` (The "Map")
**Mission**: Lists the Ethereum addresses for all contracts.
- **[Link to file](./frontend/src/data/deploy_info.json)**: Crucial for the UI to know *where* to find the "Law" on the blockchain.

### 17. `frontend/src/data/comparison_stats.json` (The "Proof")
**Mission**: Stores the final SOTA benchmark results.
- **[Link to file](./frontend/src/data/comparison_stats.json)**: Feeds the main benchmark chart in the UI.

---

## 🛠️ SECTION 5: INFRA & AUDITS (Tests/Config)
*The backbone of the repository.*

### 18. `test/run_tests.py` (The "Sanity Check")
**Mission**: Verifies the entire repo is functional.
- **[Line 65 (Syntax Audit)](./test/run_tests.py#L65)**: Proves no broken code is in the repository.

### 19. `test/plot_results.py` (The "Science Auditor")
**Mission**: Generates the final audit plots for the report.
- **[Line 45 (MI Gap Chart)](./test/plot_results.py#L45)**: Visualizes the privacy/utility trade-off.

### 20. `federated_survival.py` (The "Orchestrator")
**Mission**: The main execution script for the entire demo.
- **[Line 406 (Baseline Suite)](./federated_survival.py#L406)**: Runs the "Triple Baseline" (Local, Central, Fed).

### 21. `hardhat.config.js` (The "Chain Config")
**Mission**: Configures the Ethereum network settings.
- **[Line 25 (Port 8545)](./hardhat.config.js#L25)**: The hard-coded anchor for the local blockchain.

### 22. `requirements.txt` (The "Dependency DNA")
**Mission**: The reproducibility anchor for the entire project.
- **[Link to file](./requirements.txt)**: Specifies `torch` (AI), `flwr` (Federated), `opacus` (Privacy), and `web3` (Blockchain).
- **Defense**: *"This file ensures environment parity. By locking versions of Opacus and PyTorch, we guarantee that the Differential Privacy epsilon calculations are mathematically identical across any deployment."*

---

## 🏗️ SECTION 6: DEPLOYMENT & PERSISTENCE
*The engines that build the network and remember the results.*

### 23. `scripts/deploy_colab.py` (The "Architect")
**Mission**: The main deployment script that compiles the contracts and generates the ABIs.
- **Connection**: It creates the "Law" on the blockchain before any training starts.

### 24. `frontend/src/data/MedShareTask.json` (The "API Protocol")
**Mission**: The Application Binary Interface (ABI) for the main task contract.
- **Connection**: It tells the Javascript exactly which functions (like `joinTask`) are available on the blockchain.

### 25. `frontend/src/data/CommitmentRegistry.json` (The "Audit Protocol")
**Mission**: The ABI for the model hash registry.
- **Logic**: Defines how the UI reads the cryptographic fingerprints of previous rounds.

### 26. `frontend/src/data/Reputation.json` (The "Trust Protocol")
**Mission**: The ABI for the reputation scoring contract.
- **Logic**: Defines how the UI queries the current trust score of a hospital.

### 27. `frontend/src/data/training_history.json` (The "Memory")
**Mission**: Stores the live accuracy and loss logs from the Python simulation.
- **Persistence**: This is how the dashboard "Remembers" the chart data even after a page refresh.

---

## 🎨 SECTION 7: THE VISUAL IDENTITY (CSS)
*The styling system that gives the project a premium clinical feel.*

### 28. `frontend/src/style.css` (The "Design System")
**Mission**: Implements the Glassmorphism and Dark Mode theme.
- **[Line 12 (Color Tokens)](./frontend/src/style.css#L12)**: Defines the `#58a6ff` Blue and `#2eafb2` Teal accents used in the charts.
- **[Line 330 (View Transitions)](./frontend/src/style.css#L330)**: Smooth animations for switching between Hospital and Researcher views.

---

## 🧪 SECTION 8: DEEP INTEGRATION TESTS (Python)
*The proof that the Python code and Ethereum contracts are perfectly synchronized.*

### 29. `test/test_blockchain.py` (The "Gas Auditor")
**Mission**: Verifies that smart contract functions don't cost too much ETH.
- **[Link to file](./test/test_blockchain.py)**: Tests the deployment efficiency of the Reputation contract.

### 30. `test/test_integration_blockchain.py` (The "Handshake Check")
**Mission**: Proves Python can successfully send a model hash to Ethereum.
- **[Link to file](./test/test_integration_blockchain.py)**: Mocks a training round to verify the end-to-end audit trail.

### 31. `test/system_test_runner.py` (The "Stress Tester")
**Mission**: Runs the AI engine against edge cases (Zero data, NaN weights).
- **[Link to file](./test/system_test_runner.py)**: Ensures the system doesn't crash during a live demo.

---

## 📦 SECTION 9: THE PACKAGE SPINE (JSON)
*The configuration files that build the environment.*

### 32. `package.json` (The Root - Hardhat Config)
**Mission**: Manages the Solidity development environment.
- **Connection**: Used for compiling the contracts and running the local Ganache node.

### 33. `frontend/package.json` (The UI - Vite Config)
**Mission**: Manages the Dashboard development server.
- **Connection**: Uses `Vite` for the fast-refresh dashboard you use in the demo.

---

## 📂 SECTION 10: THE PROJECT CENSUS (Non-Logic Assets)
*Files you might see in the folder that aren't "Code," but are part of the project evidence.*

### 34. `test/*.png` (The Visual Evidence)
**Mission**: The 5 final audit plots (Gas, Privacy, Latency, etc.) generated by `plot_results.py`.
- **Viva Use**: Show these to the examiners as the scientific proof of your findings.

### 35. `test/baseline_*.json` (The Performance Cache)
**Mission**: Stores the pre-calculated results of the "Gold Standard" (Centralized) models.
- **Viva Use**: Explain that these prevent the need to re-train the expensive centralized model every single time.

### 36. `MedShare_FINAL_new.ipynb` (The AI Playground)
**Mission**: A Jupyter Notebook used for initial model prototyping and testing the clinical logic in isolation.

### 37. `MedShare_Viva_Presentation.pptx` (The Deck)
**Mission**: Your actual presentation slides for the MEng defense.

## 🧪 SECTION 4: THE ORCHESTRATION (Main)
*The glue that binds AI, Blockchain, and Data.*

### 16. `federated_survival.py` (The "Commander")
**Mission**: The entry point for all simulations and experiments.
- **[Line 125 (Hardware Calibration)](./federated_survival.py#L125)**: The `get_adaptive_experiment_config` function. It detects if you are in vLab vs. local and scales the rounds/epochs to ensure scientific convergence.
- **[Line 210 (Reputation Gatekeeper)](./federated_survival.py#L210)**: Filters the hospital list by querying the blockchain. If a node's reputation is < 0, it is physically removed from the training round.
- **[Line 255 (Handshake Pause)](./federated_survival.py#L255)**: A blocking loop that waits for you to link hospitals in the Dashboard before starting the AI engine.
- **[Line 355 (VRAM Safety Zone)](./federated_survival.py#L355)**: Limits parallel GPU usage to 10GB (out of 15GB) to prevent vLab environment crashes during high-concurrency 10-node runs.

---

## 📊 SECTION 5: THE AUDIT PIPELINE (Results)
*The post-processing and plotting scripts.*

### 17. `test/plot_results.py` (The "Artist")
**Mission**: Converts CSV logs into the PNG charts in your presentation.
- **[Line 126 (Robustness Renderer)](./test/plot_results.py#L126)**: Reads the attack data and renders the Red vs. Cyan bar chart comparing vulnerable FedAvg against your Robust-MAD defense.
- **[Line 233 (Privacy Audit Math)](./test/plot_results.py#L233)**: Renders the highly technical "Yeom 2018 Accuracy Gap" and "Nasr 2019 AUC Gap" metrics side-by-side to prove DP-SGD effectively stops information leakage.
- **[Line 206 (Gas Normalization)](./test/plot_results.py#L206)**: Uses `set_useOffset(False)` to stop Matplotlib from switching to scientific notation, ensuring Gas costs are printed as whole integer EVM units.

---

## ⛓️ SECTION 6: THE DEPLOYMENT (Infra)
*Solidity compilation and wallet setup.*

### 18. `scripts/deploy_colab.py` (The "Builder")
**Mission**: Automates the compilation and deployment of the 3 smart contracts to Ganache.
- **[Line 42 (Contract Orchestration)](./scripts/deploy_colab.py#L42)**: Triggers the deployment of the Task, Registry, and Reputation contracts sequentially.
- **[Line 55 (Contract Linking)](./scripts/deploy_colab.py#L55)**: Injects the address of the Reputation contract into the Task contract, completing the trust loop.
- **[Line 69 (Pre-Authorization)](./scripts/deploy_colab.py#L69)**: Automatically authorizes all 10 Ganache wallets so they can immediately participate in the UI without manual setup.
- **[Line 97 (ABI Sync)](./scripts/deploy_colab.py#L97)**: Pushes the newly generated Ethereum `deploy_info.json` directly into the frontend's data folder.

### 19. `hardhat.config.js` (The "Compiler")
**Mission**: Configures the Solidity compiler and network.
- **[Line 3 (EVM Versioning)](./hardhat.config.js#L3)**: Pins the compiler to `0.8.20` to use the latest Ethereum security features like `cancun` opcodes.
- **[Line 7 (Optimizer Runs)](./hardhat.config.js#L7)**: Enables the compiler optimizer (`runs: 200`) to reduce the gas cost of your smart contracts.
- **[Line 13 (Ganache Port)](./hardhat.config.js#L13)**: Hardcodes the network port to `8546` so the UI and python backends know exactly where the blockchain lives.

---

## 🖼️ SECTION 7: VISUAL IDENTITY (Styling)
*The CSS and Image assets.*

### 22. `frontend/src/style.css` (The "Gloss")
**Mission**: Defines the "Glassmorphism" UI.
- **[Line 12 (Color System)](./frontend/src/style.css#L12)**: Defines the HSL variables for the Dark Mode / Light Mode toggle.

### 23. `frontend/src/assets/` (The "Branding")
**Mission**: Visual logos and favicons.
- **`logo.png`**: The primary branding for the "MedShare-FL" dashboard header.

---

## 🧪 SECTION 8: THE SAFETY NET (Testing)
*Unit tests and requirements.*

### 24. `test/run_tests.py` (AI Unit Test & System Integrator)
**Mission**: Verifies that the MLP, DP-SGD, and data pipelines work as intended.
- **[Line 101 (Convergence Test)](./test/run_tests.py#L101)**: Creates a mock 300-patient dataset and physically tests if the model's weights change (ensuring the model accuracy actually improves and learns during training).
- **[Line 62 (Syntax Audit)](./test/run_tests.py#L62)**: Uses the Python AST (Abstract Syntax Tree) to mathematically prove your main files have no compilation errors.
- **[Line 206 (SecAgg Math Check)](./test/run_tests.py#L206)**: An algebraic proof that your pairwise masks correctly cancel out to exactly 0 (within `1e-7` tolerance).

### 25. `test/test_blockchain.py` (Chain Unit Test)
**Mission**: Validates contract interaction and reputation logic.
- **[Line 74 (Penalty Logic)](./test/test_blockchain.py#L74)**: Confirms that a call to `update_reputation` correctly passes the punishment delta (e.g., -10) to the contract.
- **[Line 122 (Bounty Creation)](./test/test_blockchain.py#L122)**: Proves that `create_task_with_bounty` successfully locks ETH into the escrow for later payout.

### 26. `requirements.txt` (The Manifest)
**Mission**: The "Dependency DNA" of the project.
- **`flwr`**: The backbone for the federated communication.
- **`opacus`**: The differential privacy engine from Meta AI.


---

## 🧬 SECTION 9: THE PACKAGE SPINE (Init)
*Python package definitions and ABIs.*

### 27. `medshare/__init__.py` (The Namespace)
**Mission**: Makes the folder a valid Python module.

### 26-31. `frontend/src/data/*.json` (The ABIs & The Cache)
**Mission**: The "Rosetta Stone" and "Static Memory" for the Javascript dashboard.

**The ABIs** (`MedShareTask.json`, `CommitmentRegistry.json`, `Reputation.json`, `deploy_info.json`):
- **`MedShareTask.json`**: Contains the ABI string that Ethers.js uses to call the `joinTask` function.
> *"When the `deploy_colab.py` script compiles the Solidity smart contracts, it automatically generates ABI (Application Binary Interface) JSON files. My Javascript dashboard reads these files to know exactly what functions exist on the blockchain and how to format data to call them."*

**The Cache** (`baseline.json`, `comparison_stats.json`, `training_history.json`):
> *"Because running a full 50-round federated simulation on 253,000 patients takes hours, I ran the Gold Standard sweeps beforehand. The UI loads these static JSON caches to instantly render the benchmark charts when the 'Sync' button is clicked."*

**The "Generalization" Flex** (e.g., `maternal_risk_audit.json`, `training_history_support2.json`):
> *"If you ask if my system only works on one disease, the answer is no. I designed the architecture to be dataset-agnostic. I ran full audits on CDC Diabetes, SUPPORT2, and Maternal Health. The system generated separate JSON caches for each of them. When a user selects a different study in the dashboard dropdown, the UI dynamically swaps which JSON cache it reads from, proving the model generalizes across disparate medical fields."*

---

## 📦 SECTION 10: NON-LOGIC ASSETS (Artifacts)
*Files you need for your Viva presentation.*

- **`VIVA_PRESENTATION.pptx`**: Your final slide deck explaining the "Triad of Privacy."
- **`test/*.png`**: The generated audit plots (e.g., `audit_dp_accuracy.png`).
- **`test/*.csv`**: The raw evidence logs for the Gas and Latency benchmarks.

---

**Status: 100% REPOSITORY TRANSPARENCY ACHIEVED. 31 LOGIC FILES + 10 SECTIONS FULLY MAPPED.** 👋🛡️🎓🚀

---
---

# 📖 SECTION 11: EXHAUSTIVE CODE BLOCK EXPLANATIONS
*This section breaks down every major function and code block across the 19 primary logic files. Use this to explain EXACTLY what any piece of code does during your Viva if asked "How does this file work under the hood?"*

## 🔬 PART 1: THE AI CORE (Python)

### 1. `medshare/engine.py` (The Training Engine)
* **`train()`**: This is the heart of the neural network learning process.
  - **DP-SGD Block**: If privacy is enabled, it wraps the model in Opacus's `PrivacyEngine`, adding mathematically calibrated Gaussian noise to the gradients.
  - **FedProx Block**: Calculates the L2 distance between the current hospital's weights and the global server's weights. It adds this as a "Proximal Term" to the loss function to prevent hospitals with skewed data from drifting too far.
  - **Loss & Optimizer**: Uses `Adam` to update weights and `BCEWithLogitsLoss` (for binary) or `CrossEntropyLoss` (for multiclass) to measure how "wrong" the model's predictions are.
  - **Memory Guard (Hidden Gem)**: Uses `del` and `torch.cuda.empty_cache()` inside the loop. Without this, the massive tensor graphs created by Opacus would cause a VRAM memory leak and crash the simulation.
* **`test()`**: Evaluates the model on unseen patient data.
  - **Metrics Block**: Calculates standard Accuracy and the AUC-ROC (Area Under the Receiver Operating Characteristic Curve), which is crucial in clinical settings to measure False Positive/Negative rates.

### 2. `medshare/strategy.py` (The Aggregation & Defense)
* **`AnomalyMonitoringStrategy.__init__()`**: Configures the Flower Strategy. It sets up the baseline weights and initializes the blockchain connection.
* **`aggregate_fit()`**: The most critical security function in the project.
  - **Weight Extraction**: Pulls the NumPy arrays from every hospital that just finished training.
  - **Norm Calculation**: Measures the Euclidean length (Norm) of every hospital's weight update.
  - **Robust-MAD Filter**: Calculates the Median Absolute Deviation of all norms. If a hospital's update is beyond `median + 3.0 * (MAD + 0.1 * median)`, it is flagged as an anomaly.
  - **Slashing Block**: If a hospital is flagged, its weights are discarded, and a call is made to the blockchain to slash its reputation by 10 points.
  - **FedAvg**: The surviving, honest weights are averaged together to create the new Global Model.

### 3. `medshare/client.py` (The Hospital Node)
* **`FlowerSurvivalClient.fit()`**: Triggered when the server asks a hospital to train.
  - **Adversarial Simulation**: If `is_malicious` is true, it triggers a `Label Flip Attack` (reversing 0s to 1s) or a `Gradient Scale Attack` (multiplying weights by 100) before sending them back.
  - **SecAgg Masking**: Adds the cryptographically generated `mask_add` and subtracts `mask_sub` to the raw weights before transmission, hiding the true data from the central server.
  - **Blockchain Audit**: Calls `post_commitment()` to record the SHA-256 hash of the weights on Ethereum.

### 4. `medshare/data.py` (The Clinical Pipeline)
* **[get_data_cached()](./medshare/data.py#L283)** (Hidden Gem): Intercepts data loading. If the processed dataset exists as a binary `.pt` file, it loads it directly into PyTorch. This is the *only* reason the massive 253,680-row CDC dataset can load instantly without blowing up the vLab RAM.
* **[load_tabular_data()](./medshare/data.py#L85)**: Reads the raw CSVs (SUPPORT2, CDC Diabetes).
* **[Scientific Integrity Drop](./medshare/data.py#L211)** (Hidden Gem): Specifically calls `df.dropna(subset=[target])` *before* median imputation. This prevents missing clinical outcomes from being accidentally filled with the "average" outcome, preserving medical science integrity.
* **[SMOTE Block](./medshare/data.py#L168)**: Uses the Synthetic Minority Over-sampling Technique to synthetically generate new patient records for underrepresented classes (e.g., rare diseases), preventing the model from just guessing the majority class.
* **[DataLoader Pin Memory](./medshare/data.py#L280)** (Hidden Gem): Uses `pin_memory=torch.cuda.is_available()`. This extreme performance optimization locks data in RAM, allowing the CPU to bypass standard limits and transfer batches to the GPU via Direct Memory Access (DMA) up to 2x faster.
* **[Non-IID Partitioning](./medshare/data.py#L221)**: Sorts the dataset by labels or features and chunks it. This proves your system works when Hospital A has mostly healthy patients and Hospital B has mostly sick patients.
* **[MinMaxScaler](./medshare/data.py#L259)**: Squeezes all clinical features (Age, Blood Pressure, etc.) into a 0-to-1 range so high-value features don't mathematically drown out low-value features.

### 5. `medshare/models.py` (The Architecture)
* **`get_parameters()` & `set_parameters()`**: The FL Translators. They convert PyTorch GPU Tensors into NumPy arrays (for internet travel) and back into Tensors.
* **`SurvivalMLP`**: Defines the Multi-Layer Perceptron. Input Layer -> 256 Nodes -> ReLU Activation -> 128 Nodes -> ReLU -> Output Node (with Sigmoid for binary prediction).

### 6. `medshare/utils.py` (The Math Toolkit)
* **`Yeom / Nasr Privacy Audit`**: Mathematically calculates the difference between `Train Accuracy` and `Test Accuracy`. If the model performs significantly better on training data, it has "memorized" it (Information Leakage).
* **`generate_pairwise_masks()`**: Generates seeded random numbers for the Secure Aggregation protocol that mathematically cancel each other out when summed at the server.

---

## 💎 PART 2: THE TRUST LAYER (Blockchain)

### 7. `contracts/MedShareTask.sol` (The Task Manager)
* **[createTask()](./contracts/MedShareTask.sol#L70)**: Takes an ETH deposit from a researcher and locks it in the contract.
* **[joinTask()](./contracts/MedShareTask.sol#L85)**: Hospitals call this to register for a study.
  - **[O(1) Scalability](./contracts/MedShareTask.sol#L93)** (Hidden Gem): Uses a nested mapping (`hasJoined[_taskId][msg.sender]`) instead of iterating through an array to check if a hospital already joined. This prevents the contract from running out of Gas (Denial of Service) if thousands of hospitals try to join simultaneously.
* **[completeTask()](./contracts/MedShareTask.sol#L104)**: Called by the Python server. It iterates through the hospitals, checks their reputation, and divides the locked ETH bounty equally among the honest participants.
  - **[Dust Protection](./contracts/MedShareTask.sol#L136)** (Hidden Gem): Calculates the remainder of the integer division (`bounty - distributed`) and routes the leftover "Dust" back to the researcher, preventing ETH from getting permanently locked in the contract forever.
* **[claimReward()](./contracts/MedShareTask.sol#L158)**: The "Pull Pattern" security block. Hospitals call this to transfer their earned ETH to their wallet, preventing re-entrancy attacks.

### 8. `contracts/CommitmentRegistry.sol` (The Audit Trail)
* **`postCommitment()`**: Maps `TaskID -> Round -> Hospital Address -> SHA-256 Hash`. This ensures a hospital can never go back and change what they submitted if an audit occurs.
* **`postFinalWeights()`**: Records the ultimate outcome of the study.

### 9. `contracts/Reputation.sol` (The Credit Score)
* **`updateReputation()`**: Adds +1 for a successful, honest round. Subtracts 10 if the Robust-MAD filter catches them cheating.

### 10. `medshare/blockchain.py` (The Python Wrapper)
* **`hash_weights()`**: Uses Python's `hashlib` to convert 100,000+ floating-point numbers into a single 32-byte cryptographic string.
* **`Gas Tracking`**: Wraps the Web3 `transact()` calls and reads the `receipt.gasUsed` to power the latency and cost charts.

---

## 🎨 PART 3: THE DASHBOARD (Frontend)

### 11. `frontend/index.html` (The DOM)
* **`<select id="audit-selector">`**: The dropdown that changes the UI from live-simulation mode to viewing pre-calculated CSV benchmarks.
* **`data-view` sections**: The HTML containers that `main.js` hides or shows to create the "Single Page Application" feel.

### 12. `frontend/src/main.js` (The State Manager)
* **`Promise.all` Loader**: The block that fetches `baseline.json`, `comparison_stats.json`, and `training_history.json` concurrently from the local disk so the UI doesn't freeze.
* **`setInterval` Polling (Hidden Gem)**: Creates a "Live Pulse" by pinging the disk every 3 seconds to check for new training data. This creates a real-time, WebSocket-like experience without the heavy infrastructure.
* **`updateUI()`**: Maps the JSON data to the DOM elements, changing colors to green/red depending on performance improvements.

### 13. `frontend/src/marketplace.js` (The Study Creator)
* **`Schema Guard`**: Ensures that if a researcher requests a "Survival" study, a hospital cannot join using "Diabetes" data.
* **`Form Submit Block`**: Reads the ETH bounty amount from the UI, validates it, and triggers the Web3 transaction.

### 14. `frontend/src/charts.js` (The Visualizer)
* **`Chart.js Blocks`**: Initializes the HTML5 Canvas elements.
* **`SOTA Rendering`**: The specific logic that draws the 3 comparative bars (Local, Centralized, Federated) side-by-side to visually prove the Federated model is superior to the Local models.

### 15. `frontend/src/blockchain.js` (The Web3 Injector)
* **[connectToProvider()](./frontend/src/blockchain.js#L9)** (Hidden Gem): Loops through standard Ganache ports (`8545, 8546, 7545`) as a multi-port fallback sequence. If the main port dies, the UI seamlessly hunts for a backup port without throwing errors to the user.
* **[JsonRpcProvider](./frontend/src/blockchain.js#L14)**: Connects the browser's javascript engine directly to your local Ganache port.
* **[ethers.parseEther()](./frontend/src/blockchain.js#L63)** (Hidden Gem): Used when creating a task to securely format ETH balances. Javascript physically cannot calculate 18-decimal numbers accurately (floating-point overflow), so this delegates the math safely to the Ethers library.
* **[Signer Block](./frontend/src/blockchain.js#L39)**: Simulates MetaMask by using the hospital's private keys to sign transactions before sending them.

### 16. `frontend/src/style.css` (The Glassmorphism)
* **`backdrop-filter: blur(10px)`**: The CSS rule that gives all the cards their modern, frosted-glass look.

---

## ⚙️ PART 4: ORCHESTRATION & INFRASTRUCTURE

### 17. `federated_survival.py` (The Master Loop)
* **`get_adaptive_experiment_config()`**: Detects if you have 15GB of GPU VRAM (vLab) or a local CPU, and scales the batch sizes and epochs accordingly so the system never crashes.
* **`backend_config` Slicing (Hidden Gem)**: Uses `{num_gpus: 0.13}` to mathematically slice the 15GB vLab GPU into fractional chunks. This allows 10 hospital nodes to train in parallel on a single GPU without throwing Out-Of-Memory errors.
* **`Simulation Boot`**: Triggers `flwr.simulation.run_simulation`, spinning up the simulated hospital nodes.

### 18. `test/plot_results.py` (The Chart Generator)
* **`plot_dp()`**: Uses Matplotlib to plot the curve of Accuracy going down as DP Noise (Sigma) goes up.
* **`plot_mi()`**: Calculates the Yeom Privacy math and plots the dual-bar chart showing Information Leakage dropping to 0%.

### 19. `scripts/deploy_colab.py` (The Blockchain Compiler)
* **`deploy_contract()`**: Reads the compiled Solidity bytecode and pushes it to Ganache.
* **`ABI Sync Block`**: Copies the resulting `deploy_info.json` directly into the frontend folder so the UI knows where the contracts live.

### 20. `hardhat.config.js` (The Config)
* **`solidity: "0.8.20"`**: Pins the compiler.
* **`optimizer: { runs: 200 }`**: Forces the compiler to optimize the Solidity code, making it cheaper to run.

### 21. `medshare/__init__.py`
* **Empty File**: Its only job is to tell Python that the `medshare/` folder is a package that can be imported from.