# 🛡️ MedShare-FL: COMPLETE VIVA GUIDE — PART 5
*The Forensic Appendices (100% Completion Buffer)*

---

# SECTION V: SCIENTIFIC JUSTIFICATION (The "Why")
*From VIVA_CODE_TRACEABILITY.md — Use these for "Why did you implement it this way?" questions.*

| Feature | Scientific Justification (The "Why") |
| :--- | :--- |
| **Robust-MAD** | "Standard mean/FedAvg is vulnerable to a single outlier. MAD provides a 50% breakdown point, ensuring one malicious hospital cannot deviate the global model." |
| **FedProx (μ)** | "Hospitals have Non-IID data. μ=0.01 adds a proximal term that 'anchors' local gradients, preventing local models from drifting into overfitted local minima." |
| **DP-SGD noise** | "Neutralizes Membership Inference Attacks. It ensures the statistical presence of any single patient record is mathematically undetectable." |
| **Per-Sample Clip** | "Mandatory for DP. We must bound the sensitivity of each individual record before adding noise, otherwise a single extreme patient could leak their identity." |
| **LR Attenuation** | "DP noise adds high-frequency variance. Reducing the Learning Rate by 75% acts as a dampener, ensuring the model converges despite the noise." |
| **SHA-256 Hashing** | "Provides 'Proof of Ethical Participation.' It ensures hospitals cannot retroactively change their updates if they are later audited for poisoning." |
| **SMOTE (k=5)** | "Medical datasets are heavily imbalanced (e.g. fewer stroke cases). SMOTE ensures the model doesn't just learn to predict 'Healthy' for everyone." |
| **Global Scaler** | "Unifies the 'Feature Language' across hospitals. Without it, the Robust-MAD filter would incorrectly reject honest hospitals due to coordinate shifts." |

---

# SECTION W: LITERATURE "TRAP" QUESTIONS
*From VIVA_LITERATURE_GUIDE.md — Use these for the Scientific Discussion phase.*

| Paper | The "Inspector's Trap" Question | Your Defense Script |
| :--- | :--- | :--- |
| **Abadi (2016)** | "Why not use a standard ε instead of RDP?" | "Standard ε composition is too loose. RDP provides a tighter bound for multi-round training (O(q√T) vs O(qT))." |
| **Chowdhury (2023)** | "If SOTA is 85.16%, isn't 86% impossible for DP?" | "No. Chowdhury's LightGBM was tuned for generality; my MLP is specifically optimized for this BRFSS distribution." |
| **Bagdasaryan (2020)**| "Can't attackers hide inside your DP noise?" | "Yes, that is the 'Robustness Paradox.' I mitigate this by adaptively calibrating the MAD threshold to the noise floor." |
| **Nasr (2019)** | "Is FL actually private without DP?" | "No. Nasr proved that white-box gradients expose raw data. My system implements DP to explicitly solve the Nasr-leakage." |
| **Li et al. (2020)** | "Why is μ=0.01? Why not 1.0?" | "1.0 is too aggressive; it prevents learning. 0.01 was empirically found to stabilize divergence without blocking convergence." |

---

# SECTION X: EXPERIMENTAL CONSTANTS (The "Gold Standard")
*From VIVA_DEFENSE_PROOFS.md — If asked "What were your exact settings?"*

| Constant | Value | Role |
| :--- | :--- | :--- |
| **Learning Rate** | **0.001 (Base)** | Standard Adam optimization step. |
| **DP-LR** | **0.00025** | Attenuated step for DP-SGD stability. |
| **Batch Size** | **32** | Balanced between memory and gradient quality. |
| **Noise Sigma (σ)**| **1.0** | Calibrated for ε ≈ 1.57 privacy guarantee. |
| **Clip Norm (C)** | **1.0** | Per-sample sensitivity bound. |
| **FedProx (μ)** | **0.01** | Non-IID stabilization constant. |
| **Rounds** | **50** | Sufficient for clinical convergence. |
| **Epochs** | **5 - 10** | Local training intensity. |

---

# SECTION Y: CLINICAL GROUP NAMES (SUPPORT2)
*If asked "Who are these hospitals?", name these 8 groups:*

1.  **ARDS** (Acute Respiratory Distress Syndrome)
2.  **CHF** (Congestive Heart Failure)
3.  **COPD** (Chronic Obstructive Pulmonary Disease)
4.  **Cirrhosis**
5.  **Coma**
6.  **Colon Cancer**
7.  **Lung Cancer**
8.  **MOSF** (Multiple Organ System Failure)

---

# SECTION Z: THE "TRIPLE BASELINE" TRUTH
*From VIVA_PRESENTATION.md — The exact results for the SUPPORT2 demo:*

*   **Centralized (Pooled Data)**: **78.5%** Accuracy (The "Upper Bound")
*   **Local (Siloed Data)**: **75.2%** Accuracy (Average per-hospital)
*   **Federated (MedShare)**: **78.9%** Accuracy (The "Winner")

**Q: "Why is Federated higher than Centralized?"**
> *" aggregation acts as a natural ensemble regularizer. While the Centralized model gets 'distracted' by global noise, our federated model averages local specialists, leading to 0.4% superior generalization on the held-out test set."*

---

**Status: FORENSIC CONSOLIDATION 100% COMPLETE. NO FURTHER INFORMATION REMAINS IN THE 11 SOURCE FILES.** 🛡️🎓🚀
