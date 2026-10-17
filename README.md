# Dusoma Foundation 🌍
### Grounded AI & Sustainable Poverty Reduction for Africa

[![GitHub Pages](https://img.shields.io/badge/Website-GitHub%20Pages-065f46?style=for-the-badge&logo=github)](https://mohamtur1.github.io/dusoma-website/)
[![Gradio Prototype](https://img.shields.io/badge/AI%20Prototype-ZeroGPU%20Ready-1e3a8a?style=for-the-badge&logo=huggingface)](prototype/)
[![Partnership](https://img.shields.io/badge/Alliance-UPAN-f59e0b?style=for-the-badge)](https://mohamtur1.github.io/dusoma-website/#mission)

**Dusoma Foundation** is an African non-profit development initiative relaunching to bridge the grassroots knowledge and advisory gap across rural Sub-Saharan communities. Working in strategic alliance with **United People's Action Network (UPAN)**, Dusoma Foundation delivers actionable, zero-cost, and low-cost community solutions paired with lightweight artificial intelligence.

Executive Director & AI Lead: **Mohamed Malik Turay**  
Key Milestone Horizon: **January 5, 2027 Funding Decision**

---

## 📁 Repository Contents

| File / Folder | Purpose | Target Platform |
| :--- | :--- | :--- |
| **`index.html`** | Standalone responsive website (no build step, pure HTML/CSS/JS) | **GitHub Pages** |
| **`app.py`** | Grounded rural advisory AI prototype (dual-mode ZeroGPU / Render) | **HF ZeroGPU / Render** |
| **`requirements.txt`** | Pinned dependencies for lightweight 512 MB RAM deployment | **Render Free Tier** |
| **`requirements-zerogpu.txt`** | Unpinned dependencies for Hugging Face ZeroGPU runtime | **Hugging Face Spaces** |
| **`prototype/`** | Isolated prototype package ready to mirror directly to an HF Space | **Hugging Face Space** |

---

## 🌐 1. Live Website (GitHub Pages)

The website is engineered with zero build tools or dependencies, using clean semantic HTML5, modern CSS3, responsive mobile layouts, and an African-inspired color palette (emerald green, deep navy, warm gold).

### Enabling GitHub Pages (1-Minute Setup)
1. In this repository, go to **Settings** &rarr; **Pages** (under "Code and automation" on the left menu).
2. Under **Build and deployment > Source**, select **Deploy from a branch**.
3. Under **Branch**, choose `main` and folder `/ (root)`.
4. Click **Save**.
5. Within 60 seconds, your site is live at:  
   👉 **`https://mohamtur1.github.io/dusoma-website/`**

---

## 🤖 2. Grounded AI Prototype

The Dusoma AI prototype provides practical, non-hallucinatory guidance across five essential poverty alleviation pillars:

1. **🌾 Climate-Smart Agriculture:** Organic pest control (Neem leaf extract & wood ash for fall armyworm), zero-chemical hermetic grain storage (PICS bags), and drought-hardy staples (cassava, sorghum, millet).
2. **💧 Clean Water & WASH:** Solar Water Disinfection (SODIS in clear PET bottles), DIY gravity bio-sand filters, and community borehole maintenance committees.
3. **💰 Grassroots Microfinance:** Village Savings and Loan Associations (VSLA) governance, 3-lockbox security protocols, and protection against predatory debt.
4. **🩺 Rural Health First Response:** WHO standard homemade Oral Rehydration Salts (ORS) formula, malaria fever triage, and maternal emergency indicators.
5. **📚 Offline Education:** Kiwix/Kolibri internet-free classroom digital servers, solar study lamp rotations, and technical youth apprenticeships.

### Deployment Options:

#### Option A: Hugging Face ZeroGPU Space (Primary Target)
1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Gradio** as SDK and **ZeroGPU** as hardware.
3. Upload the contents of the [`prototype/`](prototype/) folder:
   - `app.py` (uses `@spaces.GPU` decorator)
   - `requirements.txt` (unpinned `spaces` and `gradio`)
   - `README.md` (with Gradio metadata front matter)
4. Your space will build and launch automatically with dynamic GPU allocation.

#### Option B: Render Free Tier (Fallback)
1. Go to [Render](https://dashboard.render.com/) &rarr; **New +** &rarr; **Web Service**.
2. Connect this repository (`mohamtur1/dusoma-website`).
3. Set configuration:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Instance Type:** `Free` (512 MB RAM / 0.1 CPU)
4. Render automatically supplies the `$PORT` environment variable, which `app.py` binds to `0.0.0.0`.

---

## 👥 The "Dream Team" Roadmap

Ahead of the **January 5 funding decision**, Dusoma Foundation is structuring four core technical and field roles:
* **Mohamed Malik Turay:** Executive Director & AI Lead (System Architecture & Strategy)
* **Machine Learning & Edge Engineer:** Quantization, embedding indexing, and offline containerization
* **Data Curator & Dialect Specialist:** African vernacular agronomy corpora and translations (Krio, Swahili, Hausa, French)
* **Field Operations Lead (UPAN Network):** Direct community pilot validation with rural cooperatives and VSLA groups

---

## 📄 License & Attribution

Developed by **Mohamed Malik Turay** for the **Dusoma Foundation** in partnership with **UPAN**.  
Open-source under the [MIT License](LICENSE).
