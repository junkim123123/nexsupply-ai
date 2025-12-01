"""
NexSupply AI - Analysis Processing Page
This page handles the actual AI analysis and redirects to Results page.
"""
import streamlit as st
from utils.error_handler import handle_error_with_retry_button
from utils.theme import LOADING_ANIMATION_CSS
from config.constants import (
    STATUS_CONNECTING, STATUS_AUTHENTICATING, STATUS_PARSING,
    STATUS_ANALYZING, STATUS_PROCESSING, STATUS_COMPLETE,
    COLOR_BLUE, COLOR_CYAN, COLOR_GREEN
)
import time

# Page configuration
st.set_page_config(
    page_title="NexSupply AI - Analyzing...",
    layout="centered",
    page_icon="⏳",
    initial_sidebar_state="collapsed"
)

# Apply dark theme
from utils.theme import GLOBAL_THEME_CSS
st.markdown(GLOBAL_THEME_CSS, unsafe_allow_html=True)

# Check if we have shipment input
if 'shipment_input' not in st.session_state:
    st.error("No shipment data found. Please go back to the Analyze page.")
    if st.button("← Back to Analyze"):
        st.switch_page("pages/Analyze.py")
    st.stop()

shipment_input = st.session_state.shipment_input
user_input = shipment_input.get('user_input', '')

# Show loading state with improved UX
st.markdown(LOADING_ANIMATION_CSS, unsafe_allow_html=True)
st.markdown("""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <h1 class="loading-title">베테랑 무역 전문가가 AI와 함께 분석 중...</h1>
        <p class="status-text">잠시만 기다려주세요. 보통 10-20초 정도 소요됩니다. 저희는 지금:</p>
        <ul style="text-align: left; max-width: 500px; margin: 1rem auto; color: #94a3b8; font-size: 0.9rem;">
            <li>Landed cost breakdown</li>
            <li>Profit margin analysis</li>
            <li>Risk assessment</li>
            <li>Success probability</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

progress_bar = st.progress(0)
status_text = st.empty()
progress_hints = st.empty()

# Run analysis
try:
    # Check if analysis is already running or done
    if st.session_state.get('analysis_status') == 'running':
        # Helper function for status updates with improved UX
        def update_status(message, progress, color=COLOR_BLUE, hint=None):
            status_text.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <p style="font-size: 1.2rem; color: {color}; font-weight: 600; margin-bottom: 0.5rem;">{message}</p>
                </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(progress / 100)
            if hint:
                progress_hints.markdown(f"""
                    <div style="text-align: center; padding: 0.75rem; background: rgba(30, 41, 59, 0.3); border-radius: 8px; margin-top: 1rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                        <p style="font-size: 0.9rem; color: #94a3b8; margin: 0;">💡 {hint}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        import time
        start_time = time.time()
        
        # Step 1: Initializing
        update_status(STATUS_CONNECTING, 10, hint="고객님의 요청사항을 분석하며, 수십 년의 무역 데이터를 대조하고 있습니다.")
        
        # Get API key (optimized: check once)
        # Priority: external_api.gemini_api_key → GEMINI_API_KEY → environment variable
        api_key = None
        if hasattr(st, 'secrets'):
            try:
                # Try external_api section first
                if 'external_api' in st.secrets and 'gemini_api_key' in st.secrets['external_api']:
                    api_key = st.secrets['external_api']['gemini_api_key']
                # Fallback to root level
                elif 'GEMINI_API_KEY' in st.secrets:
                    api_key = st.secrets['GEMINI_API_KEY']
            except Exception as e:
                import logging
                logging.warning(f"Could not read API key from secrets: {e}")
        
        if not api_key:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please configure it in Streamlit Secrets or .env file.")
        
        # Step 2: Authenticating
        update_status(STATUS_AUTHENTICATING, 20, hint="Parsing your shipment details")
        
        # Step 3: Parsing input (Phase 1: Use new NLP parser if available)
        update_status(STATUS_PARSING, 35, COLOR_CYAN, hint="전 세계 물류망과 관세 규정을 확인하여, 예상치 못한 비용을 찾아내고 있습니다.")
        
        # Step 4: AI Analysis (Phase 1: Use new analysis engine if available)
        update_status(STATUS_ANALYZING, 50, COLOR_CYAN, hint="AI의 분석에 현장 전문가의 노하우를 더해, 최종 리포트를 작성하고 있습니다.")
        
        # Phase 4: Use new analysis engine (parse_user_input + run_analysis)
        result = None
        try:
            from core.nlp_parser import parse_user_input
            from core.analysis_engine import run_analysis
            from core.models import ShipmentSpec
            
            # Step 3: Parse user input to ShipmentSpec
            update_status(STATUS_PARSING, 40, COLOR_CYAN, hint="Extracting product details")
            
            # Check if we already have a parsed spec, otherwise parse now
            shipment_spec_dict = st.session_state.get('shipment_spec')
            if shipment_spec_dict and isinstance(shipment_spec_dict, dict):
                try:
                    shipment_spec = ShipmentSpec(**shipment_spec_dict)
                except Exception:
                    # If cached spec is invalid, re-parse
                    shipment_spec = parse_user_input(user_input, api_key=api_key)
                    st.session_state['shipment_spec'] = shipment_spec.model_dump()
            else:
                # Parse fresh
                shipment_spec = parse_user_input(user_input, api_key=api_key)
                st.session_state['shipment_spec'] = shipment_spec.model_dump()
            
            # Step 4: Run analysis with new engine
            update_status(STATUS_ANALYZING, 60, COLOR_CYAN, hint="Calculating costs and risks")
            result = run_analysis(shipment_spec, api_key=api_key)
            
        except Exception as e:
            import logging
            logging.error(f"New analysis engine failed: {e}", exc_info=True)
            # User-friendly error message (Customer Service feedback)
            error_msg = str(e)
            if "API" in error_msg or "key" in error_msg.lower():
                user_friendly_msg = "⚠️ API connection issue. Please check your API key settings or try again later."
            elif "parse" in error_msg.lower() or "input" in error_msg.lower():
                # More specific feedback for parsing errors
                missing_info = []
                if "product" not in user_input.lower(): missing_info.append("제품명")
                if "quantity" not in user_input.lower() and not any(char.isdigit() for char in user_input): missing_info.append("수량")
                if "price" not in user_input.lower() and "$" not in user_input and "원" not in user_input: missing_info.append("가격")
                if "from" not in user_input.lower(): missing_info.append("출발 국가")
                if "to" not in user_input.lower(): missing_info.append("도착 국가")
                
                if missing_info:
                    user_friendly_msg = f"⚠️ **입력 정보 부족:** AI가 '{', '.join(missing_info)}' 정보를 찾지 못했습니다. 더 자세한 정보를 포함하여 다시 시도해주세요."
                else:
                    user_friendly_msg = "⚠️ **입력 이해 불가:** 문장을 조금 더 명확하게 작성해주시면 AI가 더 정확하게 분석할 수 있습니다. (예: 5,000개의 XX를 한국에서 미국으로...)"
            elif "timeout" in error_msg.lower():
                user_friendly_msg = "⏱️ 분석 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."
            else:
                user_friendly_msg = "⚠️ 알 수 없는 오류가 발생했습니다. 입력 내용을 확인하시거나, 잠시 후 다시 시도해주세요."
            
            # Fallback to legacy AI analysis if new engine fails
            update_status(user_friendly_msg, 50, COLOR_CYAN)
            try:
                from src.ai import analyze_input
        result = analyze_input(
            text=user_input,
            api_key=api_key,
            use_pipeline=True
        )
            except Exception as fallback_error:
                logging.error(f"Legacy analysis also failed: {fallback_error}")
                # Show final user-friendly error
                st.error(f"❌ **Analysis Failed**: {user_friendly_msg}")
                st.info("💡 **Tips to fix this**:\n- Check your internet connection\n- Verify your input includes: product name, quantity, origin country, destination country, and target price\n- Try refreshing the page")
                raise fallback_error
        
        elapsed_time = time.time() - start_time
        
        # Step 5: Processing results
        if elapsed_time > 20:
            update_status(STATUS_PROCESSING, 80, COLOR_GREEN, hint="복잡한 건이라 조금 더 시간이 걸리고 있습니다. 거의 다 됐습니다!")
        else:
            update_status(STATUS_PROCESSING, 80, COLOR_GREEN, hint="최종 리포트를 생성하고 있습니다. 거의 다 됐습니다!")
        
        # Step 6: Complete
        update_status(STATUS_COMPLETE, 100, COLOR_GREEN)
        
        # Reassurance message
        if elapsed_time < 20:
            progress_hints.markdown("""
                <div style="text-align: center; padding: 1rem; margin-top: 1rem;">
                    <p style="font-size: 0.85rem; color: #64748b;">Typical analyses finish under 15–20 seconds.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Store result in session state
        st.session_state['analysis_result'] = result
        st.session_state['analysis_status'] = 'done'
        
        # Phase 4: Store shipment_spec if we have it
        if 'shipment_spec' not in st.session_state and 'shipment_spec' in locals():
            st.session_state['shipment_spec'] = shipment_spec.model_dump()
        
        # PostgreSQL: Save analysis log to database
        try:
            from utils.postgres_db import insert_analysis_log, is_postgresql_available
            
            if is_postgresql_available():
                # Extract data from result for logging
                cost_breakdown = result.get("cost_breakdown", {})
                profitability = result.get("profitability", {})
                risk_scores = result.get("risk_scores", {})
                data_quality = result.get("data_quality", {})
                
                # Insert analysis log
                log_id = insert_analysis_log(
                    user_input=user_input,
                    user_email=st.session_state.get('user_email'),
                    product_name=shipment_spec.product_name if hasattr(shipment_spec, 'product_name') else None,
                    origin_country=shipment_spec.origin_country if hasattr(shipment_spec, 'origin_country') else None,
                    destination_country=shipment_spec.destination_country if hasattr(shipment_spec, 'destination_country') else None,
                    quantity=shipment_spec.quantity if hasattr(shipment_spec, 'quantity') else None,
                    target_retail_price=float(shipment_spec.target_retail_price) if hasattr(shipment_spec, 'target_retail_price') and shipment_spec.target_retail_price else None,
                    target_retail_currency=getattr(shipment_spec, 'target_retail_currency', 'USD') if hasattr(shipment_spec, 'target_retail_currency') else 'USD',
                    landed_cost_per_unit=float(cost_breakdown.get('total_landed_cost', 0)) if cost_breakdown.get('total_landed_cost') else None,
                    net_margin_percent=float(profitability.get('net_profit_percent', 0)) if profitability.get('net_profit_percent') else None,
                    success_probability=float(risk_scores.get('success_probability', 0)) if risk_scores.get('success_probability') else None,
                    overall_risk_score=int(risk_scores.get('overall_risk_score', 0)) if risk_scores.get('overall_risk_score') else None,
                    price_risk=int(risk_scores.get('price_risk', 0)) if risk_scores.get('price_risk') else 0,
                    lead_time_risk=int(risk_scores.get('lead_time_risk', 0)) if risk_scores.get('lead_time_risk') else 0,
                    compliance_risk=int(risk_scores.get('compliance_risk', 0)) if risk_scores.get('compliance_risk') else 0,
                    reputation_risk=int(risk_scores.get('reputation_risk', 0)) if risk_scores.get('reputation_risk') else 0,
                    verdict=result.get("verdict") or result.get("risk_analysis", {}).get("level", "Unknown"),
                    used_fallbacks=data_quality.get('used_fallbacks', []),
                    reference_transaction_count=data_quality.get('reference_transaction_count', 0),
                    full_result=result,
                    status="success"
                )
                
                if log_id:
                    logging.info(f"Analysis log saved to PostgreSQL: {log_id}")
        except Exception as db_error:
            # PostgreSQL 로그 저장 실패해도 앱은 계속 진행
            logging.warning(f"Failed to save analysis log to PostgreSQL: {db_error}")
        
        # Small delay before redirect
        time.sleep(0.3)
        
        # Redirect to Results page
        st.switch_page("pages/Results.py")
        
    elif st.session_state.get('analysis_status') == 'done':
        # Already done, redirect immediately
        st.switch_page("pages/Results.py")
    else:
        # Start analysis
        st.session_state['analysis_status'] = 'running'
        st.rerun()
        
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Analysis failed: {e}", exc_info=True)
    
    progress_bar.progress(100)
    status_text.text("❌ Analysis failed")
    
    # Show error with retry option
    try:
        error_info = handle_error_with_retry_button(
        error=e,
            retry_callback=lambda: st.session_state.update({'analysis_status': None}),
            lang="ko"
    )
    
        # Display error information
        st.error(f"**{error_info.get('title', '오류 발생')}**")
        st.warning(error_info.get('message', str(e)))
        
        if error_info.get('suggestion'):
            st.info(f"💡 {error_info['suggestion']}")
        
        # Retry button if applicable
        if error_info.get('can_retry') and error_info.get('retry_callback'):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 다시 시도", type="primary"):
                    error_info['retry_callback']()
                    st.rerun()
            with col2:
                if st.button("← Analyze로 돌아가기"):
                    st.switch_page("pages/Analyze.py")
        else:
            if st.button("← Analyze로 돌아가기"):
                st.switch_page("pages/Analyze.py")
    except Exception as inner_e:
        # Fallback error display
        logger.error(f"Error handling failed: {inner_e}", exc_info=True)
        st.error(f"**예상치 못한 오류가 발생했습니다**")
        st.warning(f"오류 내용: {str(e)}")
        st.info("💡 페이지를 새로고침하거나 잠시 후 다시 시도해주세요.")
        
        if st.button("← Analyze로 돌아가기"):
        st.switch_page("pages/Analyze.py")

