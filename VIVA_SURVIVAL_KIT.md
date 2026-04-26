# 🛡️ MedShare-FL: VIVA SURVIVAL KIT 🚀

> **"In battle, if you break your sword, use your dagger. If you break your dagger, use your teeth."**  
> Keep this open on a second monitor or print it for your desk.

---

## ⚡ 1. THE COMMAND CHAIN (30s SETUP)
*Run these in 3 separate terminals from the project root.*

1. **Terminal 1 (Blockchain)**: `npx ganache --port 8545`
2. **Terminal 2 (Dashboard)**: `cd frontend && npm run dev`
3. **Terminal 3 (Aggregator/Engine)**: `python federated_survival.py --enable_blockchain`

---

## 🚒 2. THE PANIC STATIONS (TROUBLESHOOTING)

| Symptom | Quick Fix |
| :--- | :--- |
| **"Ganache/Node Connection Error"** | In **Terminal 1**, run `ctrl+c` and then `python scripts/deploy_colab.py`. This redeploys the contracts and re-authorizes the 10 hospital wallets. |
| **"Frontend is Blank/Spinning"** | Hard refresh with `Ctrl + F5`. Check if the backend terminal shows `[Blockchain] Connected to http://127.0.0.1:8545`. |
| **"Python Out of Memory (OOM)"** | Add `--batch_size 16` to your run command to reduce VRAM pressure. |
| **"Inspector is bored / Tech is slow"** | **THE ESCAPE HATCH**: Stop the live train and show the **"📈 Analytics"** tab. It will show the pre-computed high-accuracy results from your 50-round audits. |

---

## 📊 3. THE "IMPACT" NUMBERS (MEMORIZE THESE)

| Metric | Your Gold Standard Stat | Why It Matters |
| :--- | :--- | :--- |
| **Population Size** | **253,680 Clinical Records** | Proves scalability for the entire NHS. |
| **Accuracy (Binary)** | **86.74%** | Beats Chowdhury (2023) SOTA baseline of 85.16%. |
| **Privacy Multiplier** | **$\sigma = 1.0$ ($\epsilon \approx 1.57$)** | Proves "Strong Privacy" with minimal accuracy cost. |
| **Blockchain Cost** | **~120,500 Gas per Round** | Proves economic sustainability (approx. $0.05). |

---

## 🖱️ 4. THE "WOW" MOMENT HOTKEYS (DASHBOARD)
1. **The Reputation Ledger**: Click the "Hospitals" tab. Show the "Penalties" (negative numbers).   
   *Explain: "This is the active deterrent against poisoned gradients."*
2. **The Epsilon Gauge**: Point to the "Privacy Budget" chart.   
   *Explain: "This is the live Moments Accountant tracking our GDPR compliance."*
3. **The Audit Trail**: Click "View Transaction".   
   *Explain: "This link goes directly to our local Ethereum block, proving the training was non-repudiable."*

---

> **"You have the code. You have the math. You have the guide. Go get your Distinction."** 👋🛡️🎓🚀

**The demo will last 20min and will consist of:
1. 15-20 minutes talk about your project (e.g. rough idea, achievements,
etc.) and
2. 5 minutes for a couple of questions/discussion about your project
The 30 minutes includes the time the inspector will need for recording the outcome of the meeting.
So in practice I think each inspection will last slightly less.
Some staff are likely taking this into account in the way they distribute their meetings.**