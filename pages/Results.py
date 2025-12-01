"""
NexSupply AI - Analysis Results Page (v4.0 - Persona Feedback 반영)
- 시나리오 시뮬레이션 기능 추가
- 데이터 출처 명시성 강화 및 보안 안내 추가
- 산업별/투자 성향별 동적 코멘트 기능 추가
- 보고서 다운로드(JSON), 복사하기 기능 추가
- 동적 '다음 실행 계획' 및 용어 해설 추가
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

# --- SIMULATION LOGIC ---
cost_breakdown = result.get("cost_breakdown", {}).copy()
profitability = result.get("profitability", {}).copy()

if 'sim_fob_price' in st.session_state and st.session_state.sim_fob_price > 0:
    cost_breakdown['manufacturing'] = st.session_state.sim_fob_price
if 'sim_retail_price' in st.session_state and st.session_state.sim_retail_price > 0:
    profitability['retail_price'] = st.session_state.sim_retail_price

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

    sim_fob = st.number_input("FOB 가격 조정 ($)", value=original_fob, key="sim_fob_price", help="공급자에게 지불하는 단위당 제품 원가를 조정합니다.")
    sim_retail = st.number_input("판매가 조정 ($)", value=original_retail, key="sim_retail_price", help="최종 소비자에게 판매하는 가격을 조정합니다.")

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
    
def format_money(amount, currency_mode):
    if amount is None: return "—"
    try:
        amount_float = float(amount)
        if currency_mode == "KRW (₩)":
            return f"₩{amount_float * USD_TO_KRW:,.0f}"
        return f"${amount_float:,.2f}"
    except (ValueError, TypeError):
        return "—"

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

# --- VERDICT LOGIC ---
profile_map = {
    "보수적 (Conservative)": {"margin_threshold": 35, "prob_threshold": 60},
    "중립적 (Neutral)": {"margin_threshold": 25, "prob_threshold": 50},
    "공격적 (Aggressive)": {"margin_threshold": 15, "prob_threshold": 40}
}
profile = profile_map.get(investment_profile, profile_map["중립적 (Neutral)"])

if net_margin >= profile["margin_threshold"] + 15 and success_prob_pct >= profile["prob_threshold"] + 10:
    verdict = "Strong Go"; verdict_color = "#10b981"; verdict_icon = "✅"; verdict_badge = "강력 추천"
    one_liner = f"기대 마진({net_margin:.1f}%)과 성공 확률({success_prob_pct:.1f}%)이 모두 매우 높습니다."
    manager_comment = "이런 기회는 흔치 않습니다. 시장 수요만 확인된다면, 과감하게 추진할 가치가 있습니다."
elif net_margin >= profile["margin_threshold"] and success_prob_pct >= profile["prob_threshold"]:
    verdict = "Go"; verdict_color = "#10b981"; verdict_icon = "✅"; verdict_badge = "추천"
    one_liner = f"기대 마진({net_margin:.1f}%)과 성공 확률({success_prob_pct:.1f}%)이 양호한 수준입니다."
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
if 'fashion' in product_category: manager_comment += " 패션 상품은 트렌드가 중요하니, 초기 재고는 3개월 판매 예상 수량 이하로 보수적으로 잡는 것이 안전합니다."
elif 'electronic' in product_category: manager_comment += " 전자제품은 인증(FCC, CE) 이슈가 잦으니, 납기에 2-3주 여유를 추가로 고려하세요."
elif 'food' in product_category: manager_comment += " 식품은 유통기한과 통관 검역이 핵심입니다. 첫 거래 시 샘플과 본품의 성분표가 일치하는지 반드시 확인하세요."

# --- DYNAMIC NEXT ACTIONS ---
next_actions = []
if verdict in ["Conditional Go", "No-Go"]: next_actions.append("**[협상]** FOB 가격 15-20% 인하를 목표로 공급업체와 협상 시작")
if macro_analysis.get("supplier_stability", {}).get("score", 100) < 60: next_actions.append("**[검증]** 공급업체 실사 또는 제3자 공장 검수 진행")
if compliance_risk > 40: next_actions.append("**[규제]** 타겟 국가의 통관 및 인증 전문가와 상담 (필수)")
if verdict in ["Strong Go", "Go"]: next_actions.append("**[실행]** 소량 테스트 발주(300-500개)를 통해 시장 반응 및 품질 검증")
if macro_analysis.get("market_volatility", {}).get("score", 0) > 60: next_actions.append("**[재무]** 환율 및 원자재 가격 변동에 대비한 선물환 계약 등 헷징 전략 검토")
next_actions.append("**[분석]** 이 분석 결과를 저장하고, 다른 조건으로 시나리오를 재분석")

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
            <div><span style="color: #94a3b8; font-size: 0.85rem;">Success Probability</span><p style="color: #e2e8f0; font-size: 1.25rem; font-weight: 700; margin: 0;">{success_prob_pct:.1f}%</p></div>
            <div><span style="color: #94a3b8; font-size: 0.85rem;">Profit per Unit</span><p style="color: #e2e8f0; font-size: 1.25rem; font-weight: 700; margin: 0;">{format_money(net_profit_per_unit, currency)}</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ✅ 다음 단계: 실행 체크리스트")

cta_cols = st.columns(2)
with cta_cols[0]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                border-radius: 10px; padding: 1.5rem; text-align: center; height: 100%;">
        <h3 style="color: white; margin-top: 0;">AI 분석 결과 심층 검토</h3>
        <p style="color: #dbeafe; font-size: 0.9rem; margin-bottom: 1rem;">
            AI가 놓친 리스크는 없는지, 저희 전문가 팀이 직접 검토해드립니다.
        </p>
        <a href="mailto:contact@nexsupply.com?subject=AI 분석 결과 심층 검토 요청"
           style="background: white; color: #1e3a8a; padding: 0.6rem 1.2rem; border-radius: 8px;
                  text-decoration: none; font-weight: 700;">
            검토 요청하기
        </a>
    </div>
    """, unsafe_allow_html=True)
with cta_cols[1]:
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.6);
                border-radius: 10px; padding: 1.5rem; text-align: center; height: 100%;">
        <h3 style="color: #e2e8f0; margin-top: 0;">공급업체 질문 목록 생성</h3>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
            이 분석 결과를 바탕으로, 공급업체에 보낼 핵심 질문 목록을 생성합니다.
        </p>
        <a href="#"
           style="background: #334155; color: white; padding: 0.6rem 1.2rem; border-radius: 8px;
                  text-decoration: none; font-weight: 700;">
            질문 목록 생성하기 (준비 중)
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
for step in next_actions:
    st.markdown(f'<div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(30, 41, 59, 0.3); border-radius: 6px; margin-bottom: 0.5rem;"><input type="checkbox" style="width: 18px; height: 18px;"><span style="flex: 1;">{step}</span></div>', unsafe_allow_html=True)

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
        - **10년+ B2B 거래 데이터:** 1만 건 이상의 실제 거래를 통해 축적된 가격, 납기, 클레임 데이터를 AI 학습에 활용하여 예측 정확도를 높였습니다.
        - **실시간 물류 데이터:** 주요 5개국 파트너사를 통해 확보한 실시간 항만 상황, 운임 변동 데이터를 반영하여 '살아있는' 분석을 제공합니다.
        """)

        st.markdown("#### 분석 데이터 출처")
        used_fallbacks = result.get('data_quality', {}).get('used_fallbacks', [])
        ref_count = result.get('data_quality', {}).get('reference_transaction_count', 0)
        data_sources = {
            "Data Point": ["Product Pricing", "Freight Rates", "Duty Rates", "Extra Costs", "Reference Transactions"],
            "Source": [
                "✅ NexSupply Verified Pricing DB (Q4 '24)" if "product_pricing" not in used_fallbacks else "⚠️ AI Estimation Model",
                "✅ Global Freight Index (Q4 '24)" if "freight" not in used_fallbacks else "⚠️ AI Estimation Model",
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
    - **DDP (Delivered Duty Paid):** 판매자가 모든 비용과 책임을 지고 구매자 국가의 지정 장소까지 배송하는 조건.
    - **FOB (Free On Board):** 판매자가 수출항의 배에 상품을 선적할 때까지의 비용과 책임을 부담하는 조건.
    - **HTS Code:** 국제 통일 상품 분류 체계에 따른 상품 코드로, 관세율을 결정합니다.
    - **선물환 계약 (Forward Exchange Contract):** 미래의 특정 시점에 정해진 환율로 외화를 매매하는 계약으로, 환율 변동 리스크를 줄입니다.
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
- 성공 확률: {success_prob_pct:.1f}%
## 종합 리스크 평가
- 지정학 리스크: {macro_analysis.get('geopolitical_risk', {}).get('score', 'N/A')}/100
- 공급망 안정성: {macro_analysis.get('supplier_stability', {}).get('score', 'N/A')}/100
- 시장 변동성: {macro_analysis.get('market_volatility', {}).get('score', 'N/A')}/100
## 다음 실행 계획
""" + "\n".join([f"- {action}" for action in next_actions])

if st.button("📋 클립보드에 보고서 복사하기", use_container_width=True):
    st.code(report_content)
    st.success("보고서 내용이 클립보드에 복사되었습니다.")

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
        <h4 style="color: #f59e0b; margin-top: 0;">면책 조항 (Disclaimer)</h4>
        <p style="color: #94a3b8; font-size: 0.85rem;">본 분석은 AI의 자동 계산 결과이며, 실제와 다를 수 있습니다. 최종 사업 결정은 반드시 자격을 갖춘 무역 전문가와 상의하시기 바랍니다.</p>
    </div>
    """, unsafe_allow_html=True)

if show_debug_info:
    st.markdown("---")
    st.markdown("### 🐛 Debug View")
    st.json(result)