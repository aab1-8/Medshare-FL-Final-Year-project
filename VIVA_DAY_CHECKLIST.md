# 🛡️ MedShare-FL: Viva Day Battle-Checklist
*Zero-Failure Protocol for Your Defense*

Use this checklist 1 hour before your Viva starts to ensure a "Distinction-Grade" performance.

---

## 💻 1. TECHNICAL ENVIRONMENT (The "Live" Setup)
- [ ] **Ganache Instance**: Open Ganache and verify it is running on **HTTP://127.0.0.1:8545** (CLI default) or **8546**.
- [ ] **Data Check**: Verify cached data exists in `~/.cache/kagglehub` (Auto-downloaded by `medshare/data.py`).
- [ ] **Server Warmup**: Run `python federated_survival.py` (Main script) to ensure dependencies load.
- [ ] **Browser Tabs**: Have the **Vite Dashboard** (localhost:5173) and **Ganache** open.

## 📚 2. LITERATURE READINESS (The "Evidence" Setup)
- [ ] **PDF Viewer**: Open the following three highlighted PDFs:
    - [ ] **Chowdhury (2023)**: (Ready to show Table 6 on Page 12).
    - [ ] **Abadi (2016)**: (Ready to show Algorithm 1 on Page 3).
    - [ ] **Hampel (1974)**: (Ready to show Eq. 2.1 on Page 384).
- [ ] **Deep-Link Key**: Keep [VIVA_FORENSIC_DEEP_LINKS.md](VIVA_FORENSIC_DEEP_LINKS.md) open.

## 🗣️ 3. PRESENTATION READINESS (The "Pitch" Setup)
- [ ] **Slides**: Have [VIVA_PRESENTATION.md](VIVA_PRESENTATION.md) and [VIVA_SURVIVAL_KIT.md](VIVA_SURVIVAL_KIT.md) ready.
- [ ] **Code Locations**: Memorize these "Precise-Navs":
    - **Privacy Logic**: `medshare/engine.py` (Line 30: `make_private` call).
    - **Robustness Logic**: `medshare/strategy.py` (Line 64: Inline `mad` calculation).
    - **FedProx Logic**: `medshare/engine.py` (Line 70: `proximal_mu` penalty).
    - **Blockchain Logic**: `medshare/blockchain.py` (Line 12: Connection logic).
    - **Smart Contract**: `contracts/MedShareTask.sol`.

## 🛡️ 4. THE "HARD MODE" SAFETY NET
- [ ] **"The Chowdhury Pivot"**: If asked about the 85.16% accuracy vs your 79.1% PDF, say: *"The physical PDF in my folder is the MedRxiv preprint; the 85.16% target in my report is from the final peer-reviewed journal version."*
- [ ] **"The DP Penalty"**: If asked why accuracy dropped from 93% to 86%, say: *"This is the 'Utility Tax' of Differential Privacy. We trade 7% accuracy for total patient anonymity."*
