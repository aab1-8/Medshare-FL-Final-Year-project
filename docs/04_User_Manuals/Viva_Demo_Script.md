# MedShare-FL: Live Demonstration Script

*This document outlines the exact, step-by-step procedure to execute a flawless live demonstration of the MedShare-FL platform for your MEng examiners. Keep this sheet open alongside your terminals.*

---

## **Phase 1: Environment Initialization (Pre-Demo)**
Before the examiners arrive, ensure your backend infrastructure is fully booted and wiped clean.

1. **Start the Ganache Blockchain Server:**
   Open a new terminal in your project directory (e.g., `bxp267`) and run:
   ```bash
   npx -y ganache --port 8545 --accounts 10 --gasLimit 6721975 --mnemonic "test test test test test test test test test test test junk"
   ```
   *(Leave this terminal visible on the side. The examiners will love seeing the Ethereum transactions stream in real-time.)*

2. **Deploy the Smart Contracts:**
   Open a **second** terminal and run the deployment script to push your Solidity code to Ganache:
   ```bash
   python scripts/deploy_colab.py
   ```

3. **Start the Dashboard:**
   In the **same second terminal** (or a third), start the Vite UI server:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Wipe Browser Memory (Safety Check):**
   * Open `http://localhost:5173/` in your browser.
   * Scroll to the very bottom and click: **"Developer: Clear Local Simulation Progress"**
   * Click **"Reset Everything"** on the popup.
   * Your dashboard will reload and be 100% mathematically clean.

---

## **Phase 2: The Live Demonstration (Examiner Present)**

### **Step 1: Launch the Federated AI Engine**
Tell the examiners: *"I am now going to launch a federated training run across 8 isolated nodes, secured by an Ethereum Smart Contract."*
* Open a terminal containing your python environment and run:
  ```bash
  python federated_survival.py --enable_blockchain True --rounds 3 --epochs 1
  ```
* **What happens:** The script will initialize your dataset, post the Escrow Transaction of **0.05 ETH** to the blockchain, and print a massive `🚨 DEMO PAUSE 🚨` message. 
* Tell the examiners: *"The AI engine has intentionally frozen itself. It is waiting for all 8 clinical participants to manually sign the legal Smart Contract using the UI."*

### **Step 2: Execute the Dashboard Handshake**
* Navigate to your **Frontend Dashboard window**.
* You will instantly see the new **"TRAIN SUPPORT2-DEATH"** Study task appear dynamically from the blockchain.
* Sequentially select **Hospitals 1 through 7** and click **`🔗 Link & Participate`** for each.
* For Hospital 1, tell the examiners: *"I'm acting as Hospital 1. I've linked my local survival dataset and I'm now registering as a participant. This calls the joinTask function on the MedShareTask smart contract."*
* **The Climax**: Select **Hospital 8** and click **`🔗 Link & Participate`**.
* Tell the examiners: *"I have just cryptographically signed the final data commitment. Let’s look back at the terminal."*

### **Step 3: Watch the Engine Evaluate**
* Immediately open your Python Terminal.
* You will see that the script has automatically detected the 8th handshake and **resumed training!** 
* Tell the examiners: *"Because all 8 hospital nodes are now committed, the smart contract has transitioned to the 'Training' state, releasing the lock on the AI engine."*
* Let the 3 rounds complete. At Round 3, you will see it execute `completeTask()` and close itself.

### **Step 4: Claim the 0.0063 ETH Reward**
* Navigate back to the **Frontend Dashboard**.
* Click **`↻ Refresh`** on your browser.
* Point to your Hospital Earnings. The `0.000` balance has instantly skyrocketed to **`0.0063 ETH`**.
* The **`🔗 Claim Reward`** button is now unlocked!
* Explain the math: *"The contract held a rigid 0.05 ETH. Because 8 nodes contributed honestly, 0.05 split 8 ways equals 0.00625. Our dashboard perfectly detected the 0.0063 ETH allocation directly from the Ethereum state."*

### **Step 5: Inspect Final Assets**
* Point to the Request Card. It now proudly displays **"FINALIZED"** and **"STUDY FULFILLED"**.
* Click the blue **"📊 View Study Assets"** button to proudly show the final Global Model weights and audit parameters!

**End of Demo!** 🎉
