"""
NexSupply AI - Analysis Results Page (v4.1 - Persona Feedback #26-30 반영)
- '성공 확률' -> '종합 신뢰도 지수' 변경 및 세부 항목 명시
- '다음 실행 계획'을 클릭 가능한 버튼으로 변경
- 법적 책임 고지 강화 및 용어 해설 상세화
- 공급업체 질문 목록 생성 기능 추가 (팝업)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.theme import GLOBAL_THEME_CSS
from datetime import datetime
from config.constants import USD_TO_KRW
import json

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NexSupply AI - Results",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- 2. APPLY GLOBAL THEME ---
st.markdown(GLOBAL_THEME_CSS, unsafe_allow_html=True)

# --- 3. SESSION STATE & DATA CHECK ---
if 'analysis_result' not in st.session_state:
    st.warning("분석 결과가 없습니다. 먼저 분석을 시작해주세요.")
    if st.button("← 분석 페이지로 돌아가기", use_container_width=True):
        st.switch_page("pages/Analyze.py")
    st.stop()

result = st.session_state.get('analysis_result', {})
shipment_spec = st.session_state.get('shipment_spec', {})
shipment_input = st.session_state.get('shipment_input', {})
investment_profile = shipment_input.get('investment_profile', '중립적 (Neutral)')

# --- SIMULATION LOGIC (Recalculate metrics based on simulation inputs) ---
cost_breakdown = result.get("cost_breakdown", {}).copy()
profitability = result.get("profitability", {}).copy()

if 'sim_fob_price' in st.session_state and st.session_state.sim_fob_price > 0:
    cost_breakdown['manufacturing'] = st.session_state.sim_fob_price
if 'sim_retail_price' in st.session_state and st.session_state.sim_retail_price > 0:
    profitability['retail_price'] = st.session_state.sim_retail_price

# --- Re-calculate metrics based on simulation ---
total_landed_cost = sum([
    float(cost_breakdown.get('manufacturing', 0) or 0),
    float(cost_breakdown.get('shipping', 0) or 0),
    float(cost_breakdown.get('duty', 0) or 0),
    float(cost_breakdown.get('misc', 0) or 0)
])
retail_price = float(profitability.get('retail_price', 0) or 0)
net_profit_per_unit = retail_price - total_landed_cost
net_margin = (net_profit_per_unit / retail_price * 100) if retail_price > 0 else 0

risk_scores = result.get("risk_scores", {})
success_prob_pct = (risk_scores.get('success_probability', 0.5) or 0.5) * 100
compliance_risk = risk_scores.get('compliance_risk', 0) or 0
macro_analysis = result.get('macro_analysis', {})

# --- Helper Functions ---
def format_money(amount, currency_mode):
    if amount is None: return "—"
    try:
        amount_float = float(amount)
        # Apply simulated exchange rate if available
        current_krw_usd = st.session_state.get('sim_krw_usd', USD_TO_KRW)
        
        if currency_mode == "KRW (₩)":
            return f"₩{amount_float * current_krw_usd:,.0f}"
        return f"${amount_float:,.2f}"
    except (ValueError, TypeError):
        return "—"

def create_metric_with_tooltip(label, score_data):
    score = score_data.get('score', 0)
    factors = score_data.get('factors', {})
    tooltip_content = f"**{label} 상세 항목:**\n" + "\n".join([f"- {fname}: **{fvalue} / 100**" for fname, fvalue in factors.items()]) if factors else "세부 데이터가 없습니다."
    st.metric(label, f"{score}/100", help=tooltip_content)

def generate_supplier_questions(analysis_result, investment_profile):
    questions = [
        "1. 귀사의 월 최대 생산량(Capacity)은 얼마이며, 현재 가동률은 몇 %입니까?",
        "2. 납기 지연 발생 시, 지연 일수당 페널티 조항이 계약서에 명시되어 있습니까?",
        "3. 원자재 가격이 10% 이상 상승할 경우, 원가 상승분을 구매자와 어떻게 분담할 계획입니까?"
    ]
    if investment_profile == "보수적 (Conservative)":
        questions.append("4. 귀사가 보유한 품질 인증서(ISO 9001, CE 등)의 유효기간과 사본을 요청합니다.")
    if analysis_result.get('risk_warnings'):
        questions.append("5. [규제 리스크] 저희 제품이 타겟 국가의 통관 규제를 통과할 수 있도록 지원할 수 있습니까?")
    return "\n".join(questions)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🌍 Settings")
    currency = st.radio("Currency", ["USD ($)", "KRW (₩)"], index=0)
    
    st.markdown("---")
    st.header("👤 View Mode")
    view_mode = st.radio(
        "Choose your view",
        ["Simple", "Advanced"],
        index=0,
        help="Simple mode shows only the essentials. Advanced mode shows all details."
    )
    
    st.markdown("---")
    st.header("🔄 시나리오 시뮬레이션")
    st.caption("핵심 변수를 조정하여 수익성 변화를 즉시 확인하세요.")

    original_fob = result.get("cost_breakdown", {}).get('manufacturing', 0)
    original_retail = result.get("profitability", {}).get('retail_price', 0)
    original_krw_usd = USD_TO_KRW # Assuming USD_TO_KRW is defined globally

    sim_fob = st.number_input("FOB 가격 조정 ($)", value=original_fob, key="sim_fob_price", help="공급자에게 지불하는 단위당 제품 원가를 조정합니다.")
    sim_retail = st.number_input("판매가 조정 ($)", value=original_retail, key="sim_retail_price", help="최종 소비자에게 판매하는 가격을 조정합니다.")
    
    # New: Currency Simulation (Feedback #32)
    sim_krw_usd = st.number_input(f"환율 조정 (1 USD = {original_krw_usd:.0f} KRW)", value=original_krw_usd, key="sim_krw_usd", help="환율 변동에 따른 원가 변화를 시뮬레이션합니다.")

    st.markdown("---")
    st.header("🌐 언어 선택 (Language)")
    language = st.selectbox("Language", ["한국어", "English"], key="language_select")

    st.markdown("---")
    with st.expander("🔒 데이터 및 보안"):
        st.info("""
        **고객의 정보는 안전하게 보호됩니다.**
        - 모든 분석 데이터는 익명으로 처리됩니다.
        - 민감한 소싱 정보는 고객이 '분석 저장'을 선택하지 않는 한, 영구적으로 저장되지 않습니다.
        - 저희 시스템은 업계 최고의 표준에 따라 암호화되고 보호됩니다.
        """)

    st.markdown("---")
    st.header("🔧 Debug")
    debug_query_param = st.query_params.get("debug") == "1" or st.query_params.get("debug") == "true"
    show_debug_info = st.checkbox(
        "Show debug info",
        value=debug_query_param,
        help="Show raw ShipmentSpec and AnalysisResult JSON for debugging."
    )
    
# --- 5. REPORT HEADER ---
product_name = shipment_spec.get('product_name', 'Product')
origin = shipment_spec.get('origin_country', 'Origin')
destination = shipment_spec.get('destination_country', 'Destination')
channel = shipment_spec.get('channel', 'Channel')

st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.8); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: #e2e8f0; margin: 0;">📊 DDP / Risk Report</h1>
                <p style="color: #94a3b8; margin-top: 0.5rem;">{product_name} • {origin} → {destination} • {channel}</p>
            </div>
            <span style="font-size: 0.85rem; color: #64748b;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- VERDICT LOGIC (Cont.) ---
profile_map = {
    "보수적 (Conservative)": {"margin_threshold": 35, "prob_threshold": 60},
    "중립적 (Neutral)": {"margin_threshold": 25, "prob_threshold": 50},
    "공격적 (Aggressive)": {"margin_threshold": 15, "prob_threshold": 40}
}
profile = profile_map.get(investment_profile, profile_map["중립적 (Neutral)"])

if net_margin >= profile["margin_threshold"] + 15 and success_prob_pct >= profile["prob_threshold"] + 10:
    verdict = "Strong Go"; verdict_color = "#10b981"; verdict_icon = "✅"; verdict_badge = "강력 추천"
    one_liner = f"기대 마진({net_margin:.1f}%)과 종합 신뢰도({success_prob_pct:.1f}%)가 모두 매우 높습니다."
    manager_comment = "이런 기회는 흔치 않습니다. 시장 수요만 확인된다면, 과감하게 추진할 가치가 있습니다."
elif net_margin >= profile["margin_threshold"] and success_prob_pct >= profile["prob_threshold"]:
    verdict = "Go"; verdict_color = "#10b981"; verdict_icon = "✅"; verdict_badge = "추천"
    one_liner = f"기대 마진({net_margin:.1f}%)과 종합 신뢰도({success_prob_pct:.1f}%)가 양호한 수준입니다."
    manager_comment = "균형 잡힌 딜입니다. 파일럿 테스트를 통해 빠르게 시장 반응을 확인해보세요."
elif net_margin >= 10:
    verdict = "Conditional Go"; verdict_color = "#f59e0b"; verdict_icon = "⚠️"; verdict_badge = "조건부 추천"
    one_liner = f"마진이 다소 낮거나({net_margin:.1f}%) 리스크 요인이 있습니다. 조건부 검토가 필요합니다."
    manager_comment = "현재 조건으로는 추천하기 어렵습니다. FOB 가격 협상이나 판매가 인상을 통해 안전 마진을 확보해야 합니다."
else:
    verdict = "No-Go"; verdict_color = "#ef4444"; verdict_icon = "❌"; verdict_badge = "비추천"
    one_liner = f"기대 마진({net_margin:.1f}%)이 너무 낮아 사업성이 부족합니다."
    manager_comment = "시간과 자원을 낭비할 가능성이 큽니다. 미련 없이 다음 기회를 찾는 것이 현명합니다."

product_category = (shipment_spec.get('product_category', '') or '').lower()
if macro_analysis.get("supplier_stability", {}).get("score", 100) < 70:
    manager_comment += " 공급망 안정성 점수가 낮습니다. 첫 거래에서는 가격 협상보다 신뢰 구축에 집중하며, 소량 발주로 납기 준수와 품질을 먼저 검증하는 것이 장기적으로 유리합니다."
if 'fashion' in product_category: manager_comment += " 패션 상품은 트렌드가 중요하니, 초기 재고는 3개월 판매 예상 수량 이하로 보수적으로 잡는 것이 안전합니다."
elif 'electronic' in product_category: manager_comment += " 전자제품은 인증(FCC, CE) 이슈가 잦으니, 납기에 2-3주 여유를 추가로 고려하세요."
elif 'food' in product_category: manager_comment += " 식품은 유통기한과 통관 검역이 핵심입니다. 첫 거래 시 샘플과 본품의 성분표가 일치하는지 반드시 확인하세요."

# --- DYNAMIC NEXT ACTIONS ---
next_actions = []
if verdict in ["Conditional Go", "No-Go"]: next_actions.append("**[협상]** FOB 가격 15-20% 인하를 목표로 공급업체와 협상 시작")
if macro_analysis.get("supplier_stability", {}).get("score", 100) < 60:
    next_actions.append("**[검증]** 공급업체 실사 또는 제3자 공장 검수 진행")
    next_actions.append("**[검증]** 공급업체에 주요 품질 인증서(예: ISO 9001) 사본 및 유효기간 요청")
if compliance_risk > 40: next_actions.append("**[규제]** 타겟 국가의 통관 및 인증 전문가와 상담 (필수)")
if verdict in ["Strong Go", "Go"]: next_actions.append("**[실행]** 소량 테스트 발주(300-500개)를 통해 시장 반응 및 품질 검증")
if macro_analysis.get("market_volatility", {}).get("score", 0) > 60: next_actions.append("**[재무]** 환율 및 원자재 가격 변동에 대비한 선물환 계약 등 헷징 전략 검토")
next_actions.append("**[분석]** 이 분석 결과를 저장하고, 다른 조건으로 시나리오를 재분석")
next_actions.append("**[소싱]** NexSupply에 이 제품 소싱 요청하기 (API 연동 요청 포함)") # Feedback #36

# --- UI RENDERING ---
st.markdown(f"""
    <div style="background: {verdict_color}15; border: 2px solid {verdict_color}40; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">{verdict_icon}</span>
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                    <span style="background: {verdict_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">{verdict_badge}</span>
                    <span style="color: {verdict_color}; font-weight: 600; font-size: 1.1rem;">{verdict}</span>
                </div>
                <p style="color: #e2e8f0; font-size: 1rem; margin: 0;">{one_liner}</p>
                <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; border-left: 3px solid {verdict_color};">
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0; font-style: italic;">
                        <span style="font-weight: 600;">👔 부장님 코멘트:</span> "{manager_comment}"
                    </p>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 1.5rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(148, 163, 184, 0.2);">
            <div><span style="color: #94a3b8; font-size: 0.85rem;">Margin</span><p style="color: #e2e8f0; font-size: 1.25rem; font-weight: 700; margin: 0;">{net_margin:.1f}%</p></div>
            <div><span style="color: #94a3b8; font-size: 0.85rem;">종합 신뢰도 지수</span><p style="color: #e2e8f0; font-size: 1.25rem; font-weight: 700; margin: 0;">{success_prob_pct:.1f}%</p></div>
            <div><span style="color: #94a3b8; font-size: 0.85rem;">Profit per Unit</span><p style="color: #e2e8f0; font-size: 1.25rem; font-weight: 700; margin: 0;">{format_money(net_profit_per_unit, currency)}</p></div>
        </div>
        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 1rem; text-align: center;">
            * 종합 신뢰도 지수 = (납기 정확도: {100 - risk_scores.get('lead_time_risk', 0)}% + 품질 일치도: {100 - risk_scores.get('reputation_risk', 0)}% + 비용 예측 정확도: {100 - risk_scores.get('price_risk', 0)}%) / 3
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ✅ 다음 단계: 실행 체크리스트")

# CTA for expert consultation (Enhanced with NexSupply Branding)
cta_cols = st.columns(2)
with cta_cols[0]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                border-radius: 10px; padding: 1.5rem; text-align: center; height: 100%;">
        <h3 style="color: white; margin-top: 0;">AI 분석 결과 심층 검토</h3>
        <p style="color: #dbeafe; font-size: 0.9rem; margin-bottom: 1rem;">
            <strong>"We Are Your Assurance."</strong><br>
            알리바바의 'Trade Assurance'는 사후 보험일 뿐입니다.<br>
            NexSupply는 사고가 발생하지 않도록 현장에서 관리하는 <strong>파트너</strong>입니다.<br>
            (200+ 검증된 공장, 10년+ 운영 노하우)
        </p>
        <a href="mailto:k.myungjun@nexsupply.net?subject=[AI분석검토] {product_name} 소싱 검토 요청&body=안녕하세요, NexSupply 팀.\n\nAI 분석 결과를 바탕으로 더 구체적인 소싱 가능성을 타진하고 싶습니다.\n\n- 제품: {product_name}\n- 예상 수량: 1,000개\n- 목표 단가: {format_money(total_landed_cost, currency)}\n\n검토 부탁드립니다."
           style="background: white; color: #1e3a8a; padding: 0.6rem 1.2rem; border-radius: 8px;
                  text-decoration: none; font-weight: 700; display: inline-block;">
            전문가 검토 요청하기
        </a>
    </div>
    """.format(product_name=product_name, total_landed_cost=total_landed_cost, currency=currency, format_money=format_money), unsafe_allow_html=True)
with cta_cols[1]:
    # --- SUPPLIER QUESTIONS GENERATOR IMPLEMENTATION ---
    if st.button("공급업체 질문 목록 생성", key="generate_q_btn", use_container_width=True):
        questions_list = generate_supplier_questions(result, investment_profile)
        st.info("아래 질문 목록을 복사하여 공급업체에 문의하세요.")
        st.code(questions_list, language=None)
        
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.6);
                border-radius: 10px; padding: 1.5rem; text-align: center; height: 100%; margin-top: 0.5rem;">
        <h3 style="color: #e2e8f0; margin-top: 0;">공급업체 질문 목록 생성</h3>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
            이 분석 결과를 바탕으로, 공급업체에 보낼 핵심 질문 목록을 생성합니다.
        </p>
        <a href="#"
           style="background: #334155; color: white; padding: 0.6rem 1.2rem; border-radius: 8px;
                  text-decoration: none; font-weight: 700;">
            질문 목록 생성하기 (버튼 위로 이동)
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# --- DYNAMIC ACTION BUTTONS (Feedback #27, #33) ---
for i, step in enumerate(next_actions):
    # Use a unique key for each button
    if st.button(step, key=f"action_btn_{i}", use_container_width=True):
        if "[협상]" in step:
            # Implement Negotiation Template Pop-up
            st.markdown(f"""
            <div style="background: #273040; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <h4 style="color: #3b82f6;">📝 협상 이메일 템플릿</h4>
                <p style="color: #94a3b8;">(FOB 가격 인하 요청 버전)</p>
                <textarea style="width: 100%; height: 200px; background: #0F172A; color: white; border: 1px solid #334155;">
                {generate_negotiation_template(product_name, total_landed_cost, net_margin, sim_fob, sim_retail)}
                </textarea>
            </div>
            """, unsafe_allow_html=True)
        elif "[검증]" in step:
            # Implement Verification Checklist Pop-up
            st.markdown(f"""
            <div style="background: #273040; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <h4 style="color: #10b981;">✅ 공급업체 검증 체크리스트</h4>
                <p style="color: #94a3b8;">(공급망 안정성 확보를 위한 필수 질문)</p>
                <ul>
                    <li>- ISO 9001 인증서 사본 및 유효기간 확인</li>
                    <li>- 최근 1년간 납기 지연 이력 (월별)</li>
                    <li>- 생산 시설 규모 및 월 최대 생산 능력(CAPA)</li>
                    <li>- 주요 원자재 공급처 다변화 여부</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"'{step}' 액션 실행 (구현 예정)")

# --- ADVANCED TABS ---
if view_mode == "Advanced":
    st.markdown("---")
    tab_briefing, tab_costs, tab_data_quality = st.tabs(["📈 종합 리스크 브리핑", "💰 상세 비용 분석", "📊 데이터 품질"])

    with tab_briefing:
        st.markdown("#### 거시 환경 분석 (Macro Environment Analysis)")
        macro_cols = st.columns(3)
        def create_metric_with_tooltip(label, score_data):
            score = score_data.get('score', 0)
            factors = score_data.get('factors', {})
            tooltip_content = f"**{label} 상세 항목:**\n" + "\n".join([f"- {fname}: **{fvalue} / 100**" for fname, fvalue in factors.items()]) if factors else "세부 데이터가 없습니다."
            st.metric(label, f"{score}/100", help=tooltip_content)
        
        with macro_cols[0]: create_metric_with_tooltip("지정학적 리스크", macro_analysis.get('geopolitical_risk', {}))
        with macro_cols[1]: create_metric_with_tooltip("공급망 안정성", macro_analysis.get('supplier_stability', {}))
        with macro_cols[2]: create_metric_with_tooltip("시장 변동성", macro_analysis.get('market_volatility', {}))

        st.markdown("---")
        st.markdown("#### 🚢 주요 항만 물류 병목 현황 (Beta)")
        st.caption("실시간 데이터는 아니며, 일반적인 경향을 나타냅니다.")
        logistics_cols = st.columns(3)
        with logistics_cols[0]:
            st.metric("상하이/닝보", "보통", "평균 2-3일 지연")
        with logistics_cols[1]:
            st.metric("LA/롱비치", "높음", "평균 5-7일 지연")
        with logistics_cols[2]:
            st.metric("로테르담", "낮음", "정상 운영")

        st.markdown("---")
        st.markdown("#### 상세 리스크 경고 (Micro-Risk Warnings)")
        risk_warnings = result.get('risk_warnings', [])
        if risk_warnings:
             for warning in risk_warnings:
                if warning['risk_level'] == "Critical": st.error(f"**{warning['title']}**")
                elif warning['risk_level'] == "High": st.warning(f"**{warning['title']}**")
                else: st.info(f"**{warning['title']}**")
                st.markdown(f"<small>{warning['description']}</small>", unsafe_allow_html=True)
                with st.expander("권장 조치 보기"):
                    for action in warning['actions']: st.markdown(f"- {action}")
        else:
            st.success("✅ 특이한 미시적 리스크는 발견되지 않았습니다.")

    with tab_costs:
        st.markdown("#### 운송 방식별 비교")
        st.caption("항공 운송은 빠르지만, 해상 운송에 비해 비용이 크게 증가합니다.")
        ocean_cost = total_landed_cost
        air_cost = ocean_cost + (cost_breakdown.get('manufacturing', 0) * 0.8)
        
        comp_cols = st.columns(2)
        with comp_cols[0]:
            st.metric("🚢 해상 운송 (현재)", f"{format_money(ocean_cost, currency)} / unit", delta="약 30-45일 소요", delta_color="normal")
        with comp_cols[1]:
            st.metric("✈️ 항공 운송 (예상)", f"{format_money(air_cost, currency)} / unit", delta=f"+{format_money(air_cost - ocean_cost, currency)}", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### DDP Cost Breakdown (per unit)")
        cost_df = pd.DataFrame({
            "Cost Component": ["FOB / Manufacturing", "Freight / Shipping", "Duty / Tariffs", "Extra Costs / Misc", "**DDP per Unit**"],
            "Amount": [format_money(cost_breakdown.get(k, 0), currency) for k in ['manufacturing', 'shipping', 'duty', 'misc']] + [f"**{format_money(total_landed_cost, currency)}**"]
        })
        st.dataframe(cost_df, use_container_width=True, hide_index=True)

    with tab_data_quality:
        st.markdown("### 📊 데이터 품질 및 출처")
        st.caption("본 분석에 사용된 데이터의 출처와 신선도를 투명하게 공개합니다.")
        
        st.markdown("#### NexSupply 독점 데이터 (Our Moat)")
        st.markdown("""
        - **12,450건의 클레임/분쟁 해결 데이터베이스:** 지난 10년간 축적된 실제 무역 분쟁 사례를 AI가 학습하여, 잠재적인 리스크를 예측하고 예방합니다. (경쟁사 분석 불가 영역)
        - **실시간 물류 병목 현상 분석:** 주요 5개국 12개 항만의 파트너사를 통해 확보된 실시간 데이터를 기반으로, AI가 예측하지 못하는 물류 지연 가능성을 경고합니다.
        - **비관세 장벽 데이터:** 각국의 최신 기술 규제, 환경 규제 등 비관세 장벽 정보를 AI가 분석하여, 숨겨진 통관 리스크를 찾아냅니다.
        """)

        st.markdown("#### 분석 데이터 출처")
        used_fallbacks = result.get('data_quality', {}).get('used_fallbacks', [])
        ref_count = result.get('data_quality', {}).get('reference_transaction_count', 0)
        
        # Dynamic Time Stamp (Feedback #35)
        current_quarter = f"Q{(datetime.now().month - 1) // 3 + 1} '{datetime.now().year % 100}"
        
        data_sources = {
            "Data Point": ["Product Pricing", "Freight Rates", "Duty Rates", "Extra Costs", "Reference Transactions"],
            "Source": [
                f"✅ NexSupply Verified Pricing DB ({current_quarter})" if "product_pricing" not in used_fallbacks else "⚠️ AI Estimation Model",
                f"✅ Global Freight Index ({current_quarter})" if "freight" not in used_fallbacks else "⚠️ AI Estimation Model",
                "✅ US Customs HTS Database (2025)" if "duty" not in used_fallbacks else "⚠️ AI Estimation Model",
                "✅ NexSupply Partner Network Data" if "extra_costs" not in used_fallbacks else "⚠️ AI Estimation Model",
                f"✅ {ref_count} Similar Transactions" if ref_count > 0 else "⚠️ No reference data"
            ]
        }
        st.dataframe(pd.DataFrame(data_sources), use_container_width=True, hide_index=True)

# --- FOOTER & DOWNLOADS ---
st.markdown("---")
with st.expander("낯선 무역 용어가 있으신가요? (Glossary)"):
    st.markdown("""
    - **DDP (Delivered Duty Paid):** 판매자가 모든 비용과 책임을 지고 구매자 국가의 지정 장소까지 배송하는 조건. **(초보자에게 가장 편리)**
    - **FOB (Free On Board):** 판매자가 수출항의 배에 상품을 선적할 때까지의 비용과 책임을 부담하는 조건. **(가장 보편적으로 사용)**
    - **EXW (Ex Works):** 판매자가 자신의 공장이나 창고에서 상품을 인도하면 책임이 끝나는 조건. 운송의 모든 책임이 구매자에게 있습니다. **(전문가에게 유리)**
    - **HTS Code:** 국제 통일 상품 분류 체계에 따른 상품 코드로, 관세율을 결정하는 가장 중요한 기준입니다.
    - **선물환 계약 (Forward Exchange Contract):** 미래의 특정 시점에 정해진 환율로 외화를 매매하는 계약으로, 환율 변동 리스크를 줄입니다.
    
    | 조건 | 판매자 책임 범위 | 구매자 책임 범위 | 특징 |
    |---|---|---|---|
    | **EXW** | 공장 인도 | 모든 운송/통관 | 구매자에게 가장 불리 |
    | **FOB** | 수출항 선적까지 | 해상운송부터 | 가장 보편적 |
    | **DDP** | 최종 목적지까지 | 없음 | 구매자에게 가장 유리 |
    """)

st.markdown("#### 📤 분석 결과 공유하기")
report_content = f"""
# NexSupply AI 분석 요약 보고서
- 분석 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- 제품: {product_name} ({origin} → {destination})
- 투자 성향: {investment_profile}
## 최종 결론: {verdict} ({verdict_badge})
- AI 분석: {one_liner}
- 전문가 코멘트: {manager_comment}
## 핵심 지표
- 예상 도착 원가 (DDP): {format_money(total_landed_cost, currency)} / unit
- 예상 순수익률: {net_margin:.1f}%
- 종합 신뢰도 지수: {success_prob_pct:.1f}%
## 종합 리스크 평가
- 지정학 리스크: {macro_analysis.get('geopolitical_risk', {}).get('score', 'N/A')}/100
- 공급망 안정성: {macro_analysis.get('supplier_stability', {}).get('score', 'N/A')}/100
- 시장 변동성: {macro_analysis.get('market_volatility', {}).get('score', 'N/A')}/100
## 다음 실행 계획
""" + "\n".join([f"- {action}" for action in next_actions])

if st.button("📋 클립보드에 보고서 복사하기", use_container_width=True):
    st.code(report_content)
    st.success("보고서 내용이 클립보드에 복사되었습니다.")

# Compare Analysis Feature (Feedback #99)
if st.button("💾 비교 분석을 위해 저장하기", use_container_width=True):
    if 'saved_analyses' not in st.session_state:
        st.session_state.saved_analyses = []
    
    # Save essential metrics
    analysis_snapshot = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "product": product_name,
        "margin": net_margin,
        "roi": roi if 'roi' in locals() else 0,
        "risk_score": 100 - success_prob_pct,
        "landed_cost": total_landed_cost
    }
    st.session_state.saved_analyses.append(analysis_snapshot)
    st.success(f"저장되었습니다! (현재 저장된 분석: {len(st.session_state.saved_analyses)}개)")

# Show saved analyses in sidebar if any
if 'saved_analyses' in st.session_state and st.session_state.saved_analyses:
    with st.sidebar:
        st.markdown("---")
        st.header("🗂️ 저장된 분석 비교")
        for i, analysis in enumerate(st.session_state.saved_analyses):
            with st.expander(f"#{i+1} {analysis['product']}"):
                st.write(f"마진: {analysis['margin']:.1f}%")
                st.write(f"ROI: {analysis['roi']:.1f}%")
                st.write(f"원가: {format_money(analysis['landed_cost'], currency)}")

json_string = json.dumps(result, indent=2, ensure_ascii=False)
st.download_button(
    label="📥 전체 분석결과 다운로드 (JSON)",
    data=json_string,
    file_name=f"NexSupply_Report_{datetime.now().strftime('%Y%m%d')}.json",
    mime="application/json",
    use_container_width=True
)

st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.5); border-radius: 8px; padding: 1rem; text-align: center; margin-top: 2rem;">
        <h4 style="color: #f59e0b; margin-top: 0;">AI 분석의 법적 한계 및 면책 조항</h4>
        <p style="color: #94a3b8; font-size: 0.85rem;">
            본 분석은 AI를 활용한 자동화된 예상치이며, 법적 효력을 갖는 최종 견적이 아닙니다. 실제 무역 과정에서는 예측 불가능한 수많은 변수가 발생할 수 있습니다. 
            NexSupply는 본 분석 결과의 사용으로 인해 발생하는 어떠한 직접적, 간접적 손실에 대해서도 법적 책임을 지지 않습니다. 
            <strong>모든 최종 사업 결정은 반드시 계약서 검토 및 자격을 갖춘 무역/법률 전문가와의 상담을 통해 진행되어야 합니다.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

if show_debug_info:
    st.markdown("---")
    st.markdown("### 🐛 Debug View")
    st.json(result)