"""
Dusoma Foundation - African Poverty Reduction AI Prototype
Author: Mohamed Malik Turay (Executive Director & AI Lead, Dusoma Foundation / UPAN)

Target Environments:
  1. Primary: Hugging Face ZeroGPU Space (gradio SDK, spaces unpinned, @spaces.GPU decorator)
  2. Fallback: Render Free Tier (binds 0.0.0.0:$PORT, 512MB RAM safe, no GPU needed)
"""

import os
import sys
import re

# ==============================================================================
# 1. ZeroGPU & Fallback Compatibility Layer
# ==============================================================================
# HF ZeroGPU requires the 'spaces' package and the @spaces.GPU decorator.
# When running on Render or local CPU, we define a transparent fallback decorator.
try:
    import spaces
    gpu_decorator = spaces.GPU
    IS_ZEROGPU_AVAILABLE = True
except Exception:
    def gpu_decorator(func=None, **kwargs):
        if func is not None:
            return func
        def wrapper(f):
            return f
        return wrapper
    IS_ZEROGPU_AVAILABLE = False

import gradio as gr

# ==============================================================================
# 2. Grounded African Poverty Reduction Knowledge Base & Reasoning Engine
# ==============================================================================

SYSTEM_IDENTITY = """
You are the Dusoma Foundation Grounded AI Advisory Engine, engineered for rural African community uplift and poverty reduction.
Affiliated with the Dusoma Foundation and United People's Action Network (UPAN).
Executive Director & AI Lead: Mohamed Malik Turay.
Core Principles:
1. Prioritize zero-cost and ultra-low-cost practical methods using locally available resources.
2. Focus on climate resilience, rural food sovereignty, and community empowerment.
3. Align strictly with WHO, FAO, and Village Savings & Loan Associations (VSLA) field-tested standards.
"""

KB_DOMAINS = {
    "agriculture": {
        "keywords": [
            "crop", "crops", "farm", "farming", "maize", "cassava", "pest", "armyworm", 
            "fertilizer", "soil", "harvest", "seed", "weevil", "storage", "drought", 
            "sorghum", "millet", "cowpea", "neem", "irrigation", "plant", "planting", 
            "compost", "agriculture", "farmer", "yield", "insects", "caterpillar", "grain"
        ],
        "responses": [
            {
                "triggers": ["armyworm", "caterpillar", "worm", "insect", "eating leaf", "stem borer"],
                "title": "🌾 Fall Armyworm & Foliar Pest Control (Zero-Cost / Organic)",
                "content": """### Grassroots Action Plan: Armyworm & Leaf Pests
**Context:** Chemical insecticides are prohibitively expensive for smallholders, hazardous without protective masks/gloves, and quickly trigger pesticide resistance.

1. **Immediate Physical Intervention (Zero Cost):**
   - **Wood Ash / Dry Sand:** Drop a small pinch (1/2 teaspoon) of clean, dry wood ash or dry fine river sand directly into the funnel (whorl) of young maize plants. The abrasive mineral particles physically lacerate and desiccate young caterpillar skin within 24–48 hours without harming plant tissue.
   - **Early Morning Handpicking:** Collect caterpillars at dawn (6:00–7:00 AM) when they feed on tender outer leaves. Drop them into a container with soapy water.

2. **Botanical Neem Leaf Bio-Spray (Low / Zero Cost):**
   - **Recipe:** Collect 500g of fresh, mature neem (*Azadirachta indica*) leaves or seeds. Pound thoroughly in a traditional wooden mortar.
   - **Steeping:** Soak the paste in 5 liters of clean water for 24 hours in a shaded location.
   - **Application:** Strain liquid through clean muslin/cotton cloth. Add 1 teaspoon of shaved local laundry bar soap (serves as a wetting/sticking agent). Spray thoroughly into plant whorls once weekly in late afternoon to avoid direct sunlight breakdown.

3. **Ecological "Push-Pull" Intercropping:**
   - Intercrop maize with silverleaf or greenleaf *Desmodium* (repels stemborer moths and suppresses Striga weed) while planting *Napier grass* around the farm perimeter (attracts moths away from maize)."""
            },
            {
                "triggers": ["storage", "weevil", "grain", "pics", "bag", "rot", "post-harvest", "keep maize", "corn weevil"],
                "title": "🌾 Post-Harvest Grain Protection Without Toxic Chemicals",
                "content": """### Grassroots Action Plan: Zero-Chemical Grain Preservation
**Context:** Smallholder farmers lose up to 30–40% of their harvested grain to weevils (*Sitophilus zeamais*) and larger grain borers, forcing distress sales at low prices.

1. **Sun-Drying & Moisture Verification ("The Salt Test"):**
   - Dry grain thoroughly on clean tarpaulins or raised platforms for 4–5 full sunny days. Never dry on bare soil.
   - **Village Salt Test:** Put 2 tablespoons of dry grain into a clean, dry glass jar with 1 teaspoon of common table salt. Shake for 1 minute. If salt clumps or coats the glass, moisture is above 13% and grain will rot—continue sun-drying until salt remains powdery.

2. **Hermetic Storage (PICS - Purdue Improved Crop Storage Bags):**
   - Use triple-layer hermetic bags (two heavy inner polyethylene liners inside an outer woven polypropylene bag).
   - Pack grain tightly to exclude excess air. Tie the innermost liner tightly with twine, repeat for the middle liner, then tie the outer bag.
   - Trapped insects consume residual oxygen within 24–48 hours and asphyxiate naturally without any toxic chemical dusts (e.g., Actellic Super).

3. **Traditional Bio-Protectants:**
   - If hermetic bags are unavailable, blend fine, sifted dry wood ash (2kg ash per 50kg grain) or dried crushed chili peppers (*Capsicum*) before sealing in clean airtight plastic or clay drums."""
            },
            {
                "triggers": ["drought", "dry", "no rain", "water short", "cassava", "sorghum", "millet", "erratic rain"],
                "title": "🌾 Climate-Resilient & Drought-Hardy Farming",
                "content": """### Grassroots Action Plan: Drought Mitigation & Food Security
**Context:** Erratic rainfall cycles demand a shift away from high-water mono-cropping toward climate-hardy indigenous staples.

1. **Drought-Hardy Crop Portfolio:**
   - **Improved Cassava:** Varieties with early bulking (e.g., TME 419, TMS varieties) resist Cassava Mosaic Disease and survive up to 6 months of severe drought under the soil.
   - **Sorghum & Finger Millet:** Require 40% less water than maize and tolerate high soil temperatures.
   - **Cowpeas & Groundnuts:** Deep root systems harvest subsoil moisture while fixing nitrogen to naturally rejuvenate depleted land.

2. **Zai Pits & Water Harvesting Basins:**
   - Dig shallow planting pits (20cm deep, 30cm wide) spaced 75cm apart along natural field contours.
   - Add two handfuls of compost or animal manure to the bottom before the rains. Pits collect runoff water, concentrating moisture around root zones for weeks after rains stop."""
            }
        ]
    },
    "water": {
        "keywords": [
            "water", "well", "borehole", "clean", "dirty", "purify", "drink", "drinking", 
            "cholera", "filter", "sodis", "rain", "rainwater", "sanitation", "wash", 
            "latrine", "diarrhea", "chlorine", "muddy", "sediment", "boil"
        ],
        "responses": [
            {
                "triggers": ["purify", "dirty water", "muddy", "clean water", "sodis", "filter", "boil", "turbid"],
                "title": "💧 Low-Cost Household Water Purification & SODIS Method",
                "content": """### Grassroots Action Plan: Solar Water Disinfection (SODIS) & Filtration
**Context:** Boiling water requires scarce firewood, contributes to local deforestation, and creates indoor air pollution. SODIS is a zero-cost WHO-approved alternative.

1. **SODIS (Solar Water Disinfection) Protocol (Zero Cost):**
   - **Bottles:** Obtain clear, transparent PET plastic beverage bottles (0.5L to 2L, clear plastic without deep tint or heavy scratches).
   - **Pre-Filtering:** If water is turbid/muddy, filter through a clean folded 4-layer cotton cloth or allow sediment to settle in a bucket for 2 hours before decanting. SODIS requires clear water for UV penetration.
   - **Aeration:** Fill bottle 3/4 full, recap, and shake vigorously for 20 seconds to oxygenate. Then fill to the top and cap tightly.
   - **Sun Exposure:** Lay bottles horizontally on a corrugated corrugated iron/tin roof in direct sunlight for **6 full continuous hours** (or **2 consecutive days** if sky is more than 50% cloudy).
   - Solar UVA radiation combined with water heating destroys >99.9% of bacterial pathogens, viruses, and cholera vibrios.

2. **Three-Stage Bio-Sand Gravity Filter:**
   - Utilize 3 clean food-grade 20L plastic buckets stacked or linked.
   - Layer 1 (Top): Coarse gravel (5cm) to trap large debris.
   - Layer 2 (Middle): Clean, washed fine river sand (20cm) to trap microorganisms and create a biological purification layer (*Schmutzdecke*).
   - Layer 3 (Bottom): Clean reservoir with a tight spigot tap for safe dispensing."""
            },
            {
                "triggers": ["borehole", "well", "maintenance", "committee", "breakdown", "pump", "hand pump"],
                "title": "💧 Community Borehole Maintenance & Water Committee Protocol",
                "content": """### Grassroots Action Plan: Sustainable Village Water Points
**Context:** Over 40% of rural African hand pumps fail within 24 months due to lack of local preventative maintenance and absence of emergency repair funds.

1. **Forming a 5-Person Village WASH Committee:**
   - **Community Representation:** At least 3 committee members must be women (the primary managers of household water).
   - **Key Roles:** Chairperson, Secretary, Trained Caretaker (equipped with basic wrenches and grease), and 2 Box Keepers.

2. **Maintenance & Hygiene Schedule:**
   - **Weekly:** Apply food-grade grease to handle pivot pins; tighten foundation anchor bolts.
   - **Monthly:** Count pump strokes needed to draw water (if >10 strokes, the internal leather cup seal is worn and needs replacement).
   - **Sanitary Perimeter:** Build a 10-meter thorn or timber fence around the borehole apron to prevent cattle, pigs, and goats from defecating near the water table."""
            }
        ]
    },
    "microfinance": {
        "keywords": [
            "money", "loan", "savings", "vsla", "finance", "debt", "interest", "bank", 
            "credit", "capital", "cooperative", "fund", "invest", "momo", "orange money", 
            "mpesa", "cash", "business", "small business"
        ],
        "responses": [
            {
                "triggers": ["vsla", "savings", "village", "group", "cooperative", "start group", "box"],
                "title": "💰 Setting Up a Village Savings & Loan Association (VSLA)",
                "content": """### Grassroots Action Plan: Organizing a Village Savings & Loan Group
**Context:** Traditional commercial banks demand physical collateral that rural families do not possess. VSLAs create community-owned capital and mutual security.

1. **Group Structure & Member Selection:**
   - Form an association of **15 to 25 self-selected, trusted community members** (frequently women farmers and traders).
   - Elect officers for a 1-year cycle: Chairperson, Record Keeper, Box Keeper, and 2 Money Counters.
   - **The 3-Padlock Safety Rule:** The group purchases a sturdy lockable metal box with 3 distinct padlocks. The 3 keys are held by 3 distinct members who do NOT live in the same house as the Box Keeper. The box is only unlocked during formal group meetings in plain view of all members.

2. **Share-Purchase Mechanism:**
   - Fix a modest unit share value agreed upon by all (e.g., 5,000 to 20,000 Leones / equivalent).
   - At weekly meetings, each member purchases between 1 and 5 shares.
   - Maintain a separate **Social / Emergency Fund** (small fixed weekly contribution) used for non-repayable grants during childbirth, bereavement, or sudden medical emergencies.

3. **Loan Allocation & Annual Share-Out:**
   - Members borrow up to 3x their accumulated share balance for short-term productive income activities.
   - Repayment is due in 1 to 3 months with a modest monthly service fee (e.g., 5% or 10%).
   - After a 9–12 month cycle (aligned with school fee or planting season), 100% of the accumulated funds (savings + interest earned) are completely distributed back to members based on their shares."""
            },
            {
                "triggers": ["debt", "predatory", "momo loan", "loan app", "interest", "high interest", "borrow"],
                "title": "💰 Escaping Debt Traps & Managing Digital Micro-Loans",
                "content": """### Grassroots Advisory: Avoiding High-Interest Predatory Debt
**Context:** Digital lending apps and informal money lenders frequently charge effective annualized interest rates of 150%–300%, locking rural entrepreneurs in cycles of debt.

1. **Golden Rule of Rural Borrowing:** Borrow money strictly for **productive assets** (certified seeds, bulk trade goods, pump rentals) where anticipated returns exceed the loan fee. Never borrow at high commercial interest to pay for routine consumption.
2. **Prioritize Community Funds First:** Always exhaust internal VSLA loans or family solidarity circles before taking commercial smartphone loans.
3. **Structured Negotiation Protocol:** If a borrower falls into distress, the VSLA or cooperative committee should intervene directly to freeze compounding penalties and negotiate a flat principal repayment schedule."""
            }
        ]
    },
    "health": {
        "keywords": [
            "health", "sick", "fever", "malaria", "ors", "diarrhea", "baby", "child", 
            "doctor", "clinic", "medicine", "pregnant", "blood", "headache", "wound", 
            "vomiting", "dehydration", "hospital", "infant"
        ],
        "responses": [
            {
                "triggers": ["ors", "diarrhea", "dehydration", "vomit", "water stool", "rehydration"],
                "title": "🩺 Emergency Homemade ORS (Oral Rehydration Salts) Preparation",
                "content": """### Life-Saving Health Advisory: WHO Standard Homemade ORS
**Critical Notice:** Severe dehydration from acute diarrhea can be fatal to young children within 24 hours. Rehydration must begin immediately at home before travel to a clinic.

1. **Exact Homemade Formulation:**
   - **Clean Water:** Exactly **1 Liter** of safe drinking water (boiled and cooled, or SODIS-treated).
   - **Granulated Sugar:** **6 level teaspoons** (provides rapid energy and sodium absorption across intestinal walls).
   - **Table Salt:** **Half (1/2) level teaspoon** (replaces lost essential electrolytes).
   - Stir thoroughly until dissolved. *Taste test:* It should taste no saltier than human tears.

2. **Dosage & Administration:**
   - **Children under 2 years:** 50–100 ml (1/4 to 1/2 standard cup) after every loose stool. Administer slowly with a clean spoon.
   - **Children 2 to 10 years:** 100–200 ml (1/2 to 1 full cup) after every loose stool.
   - If the child vomits, pause for 10 minutes, then resume slowly at one teaspoon every 2 minutes.

3. **Urgent Danger Signs Requiring Immediate Clinic Referral:**
   - Sunken eyes, inability to drink or breastfeed, extreme lethargy or unresponsiveness, skin pinch on abdomen retracts slowly (>2 seconds), or blood in stool."""
            },
            {
                "triggers": ["malaria", "fever", "mosquito", "bednet", "shivering", "chills", "high temperature"],
                "title": "🩺 Community Malaria Triage & Bednet Care",
                "content": """### Community Health Advisory: Malaria Prevention & Fever Management
**Context:** Malaria accounts for the highest rate of preventable under-five mortality across Sub-Saharan Africa.

1. **Treated Bednet (LLIN) Protection:**
   - Sleep under long-lasting insecticide-treated mosquito nets every night, in all seasons.
   - Tuck net edges firmly beneath mattresses or sleeping mats before sunset.
   - Wash gently in cold water with mild soap. **Never dry nets in direct harsh sunlight** (UV radiation breaks down the deltamethrin/permethrin insecticide molecules); dry in shaded outdoor breezes.

2. **Fever Triage in Remote Communities:**
   - Sponge a feverish child with **tepid (lukewarm) water** on the forehead, neck, and groins. Avoid cold water or alcohol, which causes shivering and raises core body temperature.
   - Obtain a Rapid Diagnostic Test (RDT) at the nearest health post within 24 hours of fever onset.
   - If positive, complete the full 3-day course of Artemisinin-based Combination Therapy (ACT), even if the fever disappears after day one."""
            }
        ]
    },
    "education": {
        "keywords": [
            "education", "school", "learn", "study", "student", "teacher", "offline", 
            "book", "reading", "skills", "vocational", "youth", "solar lamp", "kiwix", 
            "kolibri", "textbook", "job", "apprentice"
        ],
        "responses": [
            {
                "triggers": ["offline", "kiwix", "kolibri", "computer", "digital", "no internet", "tablet", "hotspot"],
                "title": "📚 Low-Cost Offline Digital Classrooms (Kiwix / Kolibri)",
                "content": """### Grassroots Action Plan: Internet-Free Digital Learning
**Context:** Rural African schools face severe connectivity and electricity limitations. Waiting for national grid fiber leaves rural students behind.

1. **Deploying Kiwix & Kolibri Offline Hubs:**
   - **How it Works:** Kiwix stores encyclopedias, African curriculum guides, and open textbooks as compressed `.zim` archives.
   - **Hardware Setup:** A single low-cost Raspberry Pi or refurbished old laptop acts as a local Wi-Fi hotspot. Up to 30 low-cost mobile phones or tablets in the classroom can browse thousands of textbooks without cellular data, internet cables, or recurring subscriptions.

2. **Community Solar Study Hubs:**
   - Install a central 100W solar panel and battery bank at the primary school or community hall.
   - Charge portable LED study lamps during daylight hours. Students check out charged lamps each evening, replacing hazardous kerosene wick lamps that harm eyesight and respiratory health."""
            },
            {
                "triggers": ["vocational", "youth", "jobs", "skills", "apprentice", "carpentry", "solar repair", "kekeh", "mechanic"],
                "title": "📚 High-Impact Rural Vocational Apprenticeships",
                "content": """### Grassroots Action Plan: Technical Youth Livelihoods
**Context:** Young people in rural communities require rapid, income-generating technical competencies tailored to rural economic needs.

1. **Top Vocational Tracks with Immediate Rural Demand:**
   - **Solar Installation & Battery Reconditioning:** Maintaining 12V domestic solar systems, replacing inverter fuses, and testing lead-acid/lithium cells.
   - **Small-Engine & Kekeh (Tricycle) Maintenance:** 2-stroke and 4-stroke engine servicing for transport of farm produce to regional markets.
   - **Agricultural Machinery Fabrication:** Assembling manual cassava graters, treadle irrigation pumps, and hand-operated groundnut shellers using local scrap steel."""
            }
        ]
    }
}

# ==============================================================================
# 3. Response Generation Logic
# ==============================================================================

def check_language_greetings(text_lower):
    """Detects African regional greetings to provide culturally grounded greetings."""
    if any(w in text_lower for w in ["kushe", "wetin", "how di bodi", "krio"]):
        return "Kushe! Welkam to Dusoma Foundation AI advisory. Wi de ya fɔ elp yu fɔ agrikɔlchɔ, klin wata, famili wɛlbɔdi, microfinance, ɛn skul tin dɛn fɔ tek pɔsin kɔmɔt na powa.\n\n"
    elif any(w in text_lower for w in ["jambo", "habari", "shikamoo", "karibu"]):
        return "Jambo! Karibu kwenye mfumo wa Dusoma AI wa kupunguza umaskini vijijini. Tuko hapa kukusaidia katika kilimo, maji safi, afya, na akiba za jamii (VSLA).\n\n"
    elif any(w in text_lower for w in ["sannu", "ina kwana", "ba wani"]):
        return "Sannu da zuwa! Wannan ita ce Dusoma AI domin taimaka wa manoma, ruwa mai kyau, lafiya, da kasuwancin karkara.\n\n"
    elif any(w in text_lower for w in ["bonjour", "salut", "comment allez-vous"]):
        return "Bonjour et bienvenue sur Dusoma AI. Nous vous accompagnons pour l'agriculture durable, l'eau potable, la santé et la microfinance rurale.\n\n"
    return ""

def synthesize_domain_advisory(user_message):
    """Matches user prompt against prioritized practical playbooks."""
    text_lower = user_message.lower().strip()
    greeting_prefix = check_language_greetings(text_lower)

    matched_entries = []

    # Match across all 5 domains
    for domain_name, data in KB_DOMAINS.items():
        domain_keywords = data["keywords"]
        has_domain_affinity = any(re.search(rf"\b{re.escape(kw)}\b", text_lower) for kw in domain_keywords)

        for entry in data["responses"]:
            triggers = entry["triggers"]
            score = 0
            for t in triggers:
                if t in text_lower:
                    score += 4
            if has_domain_affinity:
                score += 1

            if score > 0:
                matched_entries.append((score, domain_name, entry))

    if matched_entries:
        # Prioritize highest match
        matched_entries.sort(key=lambda x: x[0], reverse=True)
        top_entry = matched_entries[0][2]
        
        response_text = f"{greeting_prefix}{top_entry['content']}\n\n---\n"
        response_text += "**Dusoma Advisory Note:** *Share this guidance with your local community elders or agricultural extension officer. Always seek medical professionals for severe clinical emergencies.*"
        return response_text

    # Default overview guidance
    fallback = f"""{greeting_prefix}### Dusoma Foundation Advisory Engine (Poverty Alleviation Focus)

I provide grounded, low-cost action plans tailored to rural African communities across 5 key pillars:

1. **🌾 Climate-Smart Agriculture:** Organic pest control (Neem leaves, wood ash), PICS hermetic grain storage without chemicals, drought-hardy cassava/sorghum.
2. **💧 Clean Water & WASH:** Solar Water Disinfection (SODIS in clear PET bottles), bio-sand filtration, and community borehole committees.
3. **💰 Grassroots Microfinance:** Village Savings and Loan Associations (VSLA) setup, 3-key cash boxes, avoiding predatory digital loans.
4. **🩺 Community Health:** WHO homemade Oral Rehydration Salts (ORS) formula, malaria triage, and maternal warning signs.
5. **📚 Offline Education:** Kiwix/Kolibri offline knowledge boxes for schools without internet, solar study lamps, youth apprenticeships.

**Try asking:**
- *"Fall armyworm has attacked my maize. What zero-cost remedy works?"*
- *"What is the exact ratio of sugar, salt, and water for homemade ORS?"*
- *"How do we organize a 3-key cash box for our women's VSLA savings group?"*
- *"How can our village purify murky water using plastic bottles and sunlight?"*"""
    return fallback


# ZeroGPU Decorator wraps the core responder
@gpu_decorator
def dusoma_chat_responder(message, history):
    """
    Core responder function.
    Decorated with @spaces.GPU for Hugging Face ZeroGPU compatibility.
    Runs identically on Render CPU instances.
    """
    if not message or not str(message).strip():
        return "Please enter a question regarding agriculture, clean water, health, microfinance, or education."
    
    return synthesize_domain_advisory(str(message))


# ==============================================================================
# 4. Gradio Interface Construction
# ==============================================================================

# Custom styling injected directly into the HTML header
CUSTOM_HEADER = f"""
<style>
  .dusoma-header {{
    background: linear-gradient(135deg, #065f46 0%, #0d9488 50%, #1e3a8a 100%);
    color: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 16px;
    box-shadow: 0 8px 16px -2px rgba(6, 95, 70, 0.2);
  }}
  .dusoma-header h1 {{
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    color: #ffffff;
  }}
  .dusoma-header p {{
    font-size: 0.95rem;
    color: #ccfbf1;
    margin: 0 0 12px 0;
  }}
  .badge-tag {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
</style>

<div class="dusoma-header">
  <h1>🌍 Dusoma Foundation &bull; Poverty Reduction AI Prototype</h1>
  <p>Grounded Rural African Advisory Engine &bull; Climate Agriculture, WASH, Microfinance, Health &amp; Education</p>
  <div>
    <span class="badge-tag">Executive Director: Mohamed Malik Turay</span>
    <span class="badge-tag" style="background: rgba(16, 185, 129, 0.35);">UPAN Initiative</span>
    <span class="badge-tag" style="background: rgba(245, 158, 11, 0.35);">{'ZeroGPU Enabled' if IS_ZEROGPU_AVAILABLE else '512MB RAM Edge Mode'}</span>
    <span class="badge-tag">Jan 5 Funding Horizon</span>
  </div>
</div>
"""

with gr.Blocks(title="Dusoma AI - Poverty Reduction Advisory") as demo:
    gr.HTML(CUSTOM_HEADER)

    # Standard ChatInterface compatible with Gradio 4, 5, and 6
    chat = gr.ChatInterface(
        fn=dusoma_chat_responder,
        examples=[
            "Fall armyworm has attacked our maize. We cannot afford chemicals. What can we do?",
            "How do we prepare homemade ORS for a child suffering from severe diarrhea?",
            "How do we purify muddy well water using plastic bottles and sunlight (SODIS)?",
            "How do we set up a 3-key cash box for a community VSLA savings group?",
            "What offline digital resources like Kiwix can we run in an off-grid rural school?"
        ],
        textbox=gr.Textbox(
            placeholder="Ask about agriculture, clean water, health triage, microfinance, or offline education...",
            container=False,
            scale=7
        )
    )

    with gr.Accordion("ℹ️ Project Context & Architecture (Dusoma Foundation / UPAN)", open=False):
        gr.Markdown("""
        ### About the Dusoma Foundation Poverty Reduction Prototype
        - **Leadership:** Mohamed Malik Turay (Founder & AI Lead), in collaboration with UPAN.
        - **Target Milestones:** Operational relaunch following October 16 legal deadline, targeting the **January 5, 2027 funding decision**.
        - **Deployment Dual-Mode:**
          - **Primary:** Hugging Face ZeroGPU Space (`@spaces.GPU` wrapped, Gradio SDK, dynamic GPU allocation).
          - **Fallback:** Render Free Tier (512 MB RAM / 0.1 CPU, bound to `0.0.0.0:$PORT`).
        - **Architecture:** Lightweight domain retrieval engine delivering actionable, low-cost, and zero-cost rural interventions.
        """)

# ==============================================================================
# 5. Application Launch
# ==============================================================================
if __name__ == "__main__":
    # Render passes port via $PORT; Hugging Face Spaces defaults to 7860
    server_port = int(os.environ.get("PORT", 7860))
    print(f"Starting Dusoma AI Prototype on 0.0.0.0:{server_port}...")
    print(f"ZeroGPU Environment detected: {IS_ZEROGPU_AVAILABLE}")

    demo.launch(
        server_name="0.0.0.0",
        server_port=server_port
    )
