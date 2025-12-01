"""
NexSupply AI - Analysis Page (v2.0)
- Refactored for a clean, professional UI using the new Global Theme.
- All inline CSS has been removed and replaced with centralized styles.
- Layout is structured with st.container and the 'glass-container' class.
"""
import streamlit as st
import re
from utils.theme import GLOBAL_THEME_CSS
from config.locales import DEFAULT_LANG
from dotenv import load_dotenv
import time

load_dotenv()

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NexSupply AI - Analyze",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="collapsed"
)

# --- 2. APPLY GLOBAL THEME ---
st.markdown(GLOBAL_THEME_CSS, unsafe_allow_html=True)

# --- 3. EMAIL VERIFICATION ---
if not st.session_state.get('user_email'):
    st.warning("📧 Email required. Please return to the landing page to enter your email.")
    if st.button("← Back to Landing Page"):
        st.switch_page("app.py")
    st.stop()

# --- 3. SESSION STATE INITIALIZATION ---
if 'language' not in st.session_state:
    st.session_state.language = DEFAULT_LANG
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'shipment_input' in st.session_state:
    # If returning from the results page, restore the previous input
    st.session_state.user_input = st.session_state.shipment_input.get('user_input', '')


# --- 4. PAGE HEADER & INSTRUCTIONS ---
st.title("📦 AI-Powered Landed Cost Estimator")
st.markdown(
    "**AI가 계산하는 예상 수입 원가, 마진, 그리고 리스크.**\n\n*정확한 최종 견적은 반드시 전문가의 검토가 필요합니다.*"
)
st.markdown("---")

with st.container(border=True):
    st.markdown("""
    **How it works:**
    1.  **Describe your shipment** in the text box below.
    2.  **(Optional)** Add details like HTS codes or unit weight in the advanced options.
    3.  **Click "Analyze"** to get a complete breakdown.
    """)
    st.markdown("---")
    st.markdown("💡 **Example Input:**")
    st.code("I want to import 5,000 bags of shrimp chips from South Korea. FOB price is $0.30 per unit. I plan to sell them for $4 each on Amazon FBA in the US.", language=None)

# "Try Example" button is more prominent now
if st.button("⚡ Try Example", use_container_width=True, type="secondary", help="Load the example input to see how it works"):
    st.session_state.user_input = "I want to import 5,000 bags of shrimp chips from South Korea. FOB price is $0.30 per unit. I plan to sell them for $4 each on Amazon FBA in the US."
    st.rerun()

st.markdown("---")
with st.container(border=True):
    st.markdown("##### 👔 부장님의 조언 (A Tip from the Manager)")
    st.markdown("""
    AI는 당신이 제공한 정보를 바탕으로 똑똑하게 계산합니다. 하지만 **'쓰레기가 들어가면 쓰레기가 나온다'**는 말을 기억하세요.
    - **상세한 설명:** '전자제품'보다는 '블루투스 스피커 모델명 X'처럼 구체적으로.
    - **정확한 숫자:** 대략적인 수량과 가격이라도 정확할수록 결과가 현실에 가까워집니다.
    
    **이 AI 분석은 당신의 비즈니스를 위한 강력한 시작점입니다.** 최종 결정 전에는 반드시 저희 전문가 팀과 현장 상황을 점검하여 리스크를 최소화하세요.
    """)

# --- 5. MAIN INPUT & VALIDATION ---
def validate_input(text):
    """Provides real-time, experience-based feedback on the user's input."""
    if not text or len(text.strip()) < 10:
        st.warning("부장님 한마디: '보고서는 좀 더 상세하게.' (10자 이상 입력해주세요)", icon="👔")
        return False

    text_lower = text.lower()
    missing = []
    # More specific keywords for product
    if not any(kw in text_lower for kw in ['product', 'item', 'unit', 'bag', 'box', 'chip', 'speaker', 'toy']):
        missing.append("어떤 **상품**인지 알려주셔야 규제와 관세를 정확히 볼 수 있습니다.")
    # More specific keywords for origin
    if not any(kw in text_lower for kw in ['from', 'korea', 'china', 'vietnam', '한국', '중국', '베트남']):
        missing.append("**어느 나라**에서 오는지에 따라 물류비와 리스크가 크게 달라집니다.")
    # More specific keywords for destination
    if not any(kw in text_lower for kw in ['to', 'usa', 'us', 'europe', '미국', '유럽']):
        missing.append("**도착 국가**를 알려주셔야 정확한 관세 계산이 가능합니다.")
    # Price check
    if not (re.search(r'\d', text) and any(kw in text_lower for kw in ['$', '¥', '€', '원', 'dollar', 'price', 'cost'])):
        missing.append("단가가 빠졌네요. **가격** 정보는 수익성 분석의 핵심입니다.")
    # Quantity check
    if not re.search(r'\d{2,}', text) or not any(kw in text_lower for kw in ['quantity', '개', '장', '박스', 'units']):
        missing.append("가장 중요한 **수량**이 빠지면 총비용을 계산할 수 없습니다.")
        
    if missing:
        # Show one suggestion at a time to not overwhelm the user
        st.info(f"💡 **현장 전문가 조언:** {missing[0]}", icon="💡")
        return True # Still valid to proceed, but with suggestions
    
    st.success("✅ 좋습니다. 핵심 정보가 포함되어 분석의 정확도가 올라갑니다.", icon="👍")
    return True

with st.container(border=True):
    st.subheader("📝 Describe Your Shipment")
    user_input = st.text_area(
        label="Shipment Description",
        value=st.session_state.user_input,
        placeholder="e.g., I want to import 5,000 bags of shrimp chips from South Korea. FOB price is $0.30 per unit. I plan to sell them for $4 each on Amazon FBA in the US.",
        height=150,
        label_visibility="collapsed",
        key="main_input"
    )
    st.session_state.user_input = user_input
    
    # Display validation feedback
    is_valid_input = validate_input(user_input)

# --- 6. ADVANCED OPTIONS ---
with st.expander("⚙️ 전문가 설정 (Advanced Options)"):
    st.info("이 옵션들은 AI의 분석 정확도를 더욱 높여줍니다. 확실하지 않다면 그냥 넘어가셔도 좋습니다.", icon="💡")
    
    adv_col1, adv_col2 = st.columns(2)
    with adv_col1:
        st.selectbox("운송 방식 (Freight Mode)", ["Auto-detect", "Ocean", "Air"], key="freight_mode")
        st.text_input("HS/HTS Code", placeholder="e.g., 1905.90", key="hts_code")
        st.selectbox("Incoterm", ["FOB", "CIF", "EXW", "DDP"], key="incoterm")
    with adv_col2:
        st.number_input("개당 무게 (Unit Weight in kg)", min_value=0.0, step=0.1, value=None, key="unit_weight")
        st.radio(
            "투자 성향 (Investment Profile)",
            ["보수적 (Conservative)", "중립적 (Neutral)", "공격적 (Aggressive)"],
            index=1,
            key="investment_profile",
            help="선택한 성향에 따라 최종 Verdict와 전문가 코멘트의 톤이 조절됩니다."
        )

# Analyze Button - Prominent CTA
is_loading = st.session_state.get('is_analyzing', False)
user_input_clean = (st.session_state.get('user_input', '') or '').strip()
min_chars = 10
button_disabled = len(user_input_clean) < min_chars or is_loading

# Analyze Button with better visual feedback
# Single button centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 Get Full Analysis",
        key="analyze_btn",
        type="primary",
        use_container_width=True,
        disabled=button_disabled,
        help="Calculates landed cost, profit margin, and risks based on your input."
    )
    
    if button_disabled and len(user_input_clean) < min_chars:
        st.caption("💡 Please enter more details to activate the analysis.", help="A good description includes the product, quantity, origin, destination, and target price.")


# --- 7. FORM SUBMISSION LOGIC ---
if analyze_button:
    user_input_clean = (st.session_state.get('user_input', '') or '').strip()
    
    if not user_input_clean:
        st.error("Please enter a shipment description to start the analysis.")
    else:
        # Phase 1: Parse user input using new NLP parser
        try:
            from core.nlp_parser import parse_user_input
            shipment_spec = parse_user_input(user_input_clean)
            
            # Store ShipmentSpec in session state
            st.session_state["shipment_spec"] = shipment_spec.model_dump()
            
            # Also store legacy format for backward compatibility
            from config.constants import DEFAULT_RETAIL_PRICE
            hts_code_input = st.session_state.get('hts_code', '') or ''
            st.session_state["shipment_input"] = {
                'user_input': user_input_clean,
                'retail_price': shipment_spec.target_retail_price or DEFAULT_RETAIL_PRICE,
                'include_fba': "fba" in user_input_clean.lower() or shipment_spec.channel and "fba" in shipment_spec.channel.lower(),
                'hts_code': hts_code_input.strip() if hts_code_input else '',
                'investment_profile': st.session_state.get('investment_profile', '중립적 (Neutral)')
            }
            
        except Exception as e:
            # Fallback to legacy format if parsing fails
            import logging
            logging.warning(f"Phase 1 parser failed, using legacy format: {e}")
            from config.constants import DEFAULT_RETAIL_PRICE
            hts_code_input = st.session_state.get('hts_code', '') or ''
            st.session_state["shipment_input"] = {
                'user_input': user_input_clean,
                'retail_price': DEFAULT_RETAIL_PRICE,
                'include_fba': "fba" in user_input_clean.lower(),
                'hts_code': hts_code_input.strip() if hts_code_input else '',
            }
        
        # Set status and switch to the results page
        st.session_state["analysis_status"] = "running"
        st.switch_page("pages/Analyze_Results.py")

# --- 8. FOOTER ---
st.markdown("""
    <hr>
    <div style="text-align: center; color: var(--color-text-secondary); font-size: 0.875rem;">
        <p>NexSupply © 2025 | A new era of B2B Sourcing</p>
    </div>
""", unsafe_allow_html=True)
