---
title: Dusoma AI - Poverty Reduction Advisory
emoji: 🌍
colorFrom: green
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: mit
short_description: Grounded African rural advisory engine for poverty reduction
---

# 🌍 Dusoma Foundation &bull; Poverty Reduction AI Prototype

An open-access, grounded artificial intelligence advisory engine engineered specifically for rural African communities, smallholder farmers, and grassroots cooperatives.

Developed by **Mohamed Malik Turay** (Founder & Executive Director, Dusoma Foundation / AI Lead) in strategic partnership with **UPAN (United People's Action Network)**.

---

## 🎯 Focus Domains

1. **🌾 Climate-Smart Agriculture:** Organic foliar pest control (Neem leaf extract, wood ash for fall armyworm), zero-chemical post-harvest hermetic storage (PICS bags), and drought-hardy staples (cassava, sorghum, millet).
2. **💧 Clean Water & Sanitation (WASH):** Zero-cost Solar Water Disinfection (SODIS in clear PET bottles), DIY gravity bio-sand filters, and 5-person village borehole maintenance committees.
3. **💰 Grassroots Microfinance:** Village Savings and Loan Associations (VSLA) governance, 3-lockbox protocols, and avoiding predatory high-interest digital lending traps.
4. **🩺 Community Health & First Triage:** WHO standard homemade Oral Rehydration Salts (ORS) formulation, malaria fever triage, and maternal emergency warning signs.
5. **📚 Offline Education:** Kiwix/Kolibri internet-free digital classroom hubs, community solar study lamp programs, and youth technical apprenticeships.

---

## 🚀 Deployment Specifications

### 1. Primary: Hugging Face ZeroGPU Space
- **SDK:** `gradio`
- **Hardware:** ZeroGPU (dynamic NVIDIA A10G/A100 allocation)
- **Function Wrapping:** Uses `@spaces.GPU` decorator on the core responder.
- **Dependencies:** Unpinned `spaces` and `gradio` to allow the HF container orchestrator to resolve dependencies cleanly.

### 2. Fallback: Render Free Tier
- **Footprint:** Consumes `< 120 MB RAM` (comfortably within the 512 MB ceiling).
- **Binding:** Binds dynamically to `0.0.0.0:$PORT`.
- **CPU Fallback:** Includes a safe passthrough decorator if `spaces` is unavailable.

---

## 👥 Strategic Horizon
- **Milestones:** Relaunch operational rollout following October 16 legal deadline.
- **Key Target:** Funding Evaluation Decision on **January 5, 2027**.
- **Contact:** [Dusoma Foundation](mailto:contact@dusoma.org)
