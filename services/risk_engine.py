"""
Real-World Risk Engine - Phase 3 Survival Upgrade
Provides specific, actionable risk warnings based on product characteristics.
Now integrates detailed compliance rules from compliance_rules_us.json
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class RiskWarning:
    """Single risk warning with details"""
    category: str
    risk_level: RiskLevel
    title: str
    description: str
    actions: List[str]  # Recommended actions


class RiskEngine:
    """
    Real-World Risk Engine
    
    Analyzes product, market, and timing to generate specific risk warnings.
    Integrates detailed compliance rules from compliance_rules_us.json
    """
    
    # Famous brand names for IP/Trademark detection
    FAMOUS_BRANDS = [
        "pororo", "뽀로로", "disney", "디즈니", "marvel", "marvel",
        "nintendo", "pokemon", "포켓몬", "hello kitty", "헬로키티",
        "sanrio", "san-x", "rilakkuma", "리락쿠마", "moomin", "무민"
    ]
    
    def __init__(self):
        """Load compliance rules from JSON file"""
        self.compliance_rules = self._load_compliance_rules()
    
    def _load_compliance_rules(self) -> Dict[str, Any]:
        """
        Load compliance rules from JSON file.
        
        Returns:
            Dictionary with compliance rules, or empty dict if file not found
        """
        try:
            # Try multiple possible paths
            possible_paths = [
                "data/compliance_rules_us.json",
                "compliance_rules_us.json",
                os.path.join(os.path.dirname(__file__), "..", "data", "compliance_rules_us.json")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
            
            # If file not found, return empty structure
            return {"categories": []}
        except Exception as e:
            # Log error but continue with hardcoded rules
            print(f"Warning: Could not load compliance_rules_us.json: {e}")
            return {"categories": []}
    
    def analyze_regulatory_risks(
        self,
        product_name: str,
        product_category: Optional[str] = None,
        market: Optional[str] = None
    ) -> List[RiskWarning]:
        """
        Analyze regulatory risks for food/candy/toys/electronics.
        
        Args:
            product_name: Product name
            product_category: Product category
            market: Target market
            
        Returns:
            List of RiskWarning objects
        """
        warnings: List[RiskWarning] = []
        search_text = f"{product_name} {product_category or ''}".lower()
        
        # Use detailed compliance rules from JSON if available
        compliance_rules = self.compliance_rules.get("categories", [])
        
        # Check each compliance rule category
        for category_data in compliance_rules:
            category_name = category_data.get("category", "")
            rules = category_data.get("rules", [])
            
            for rule in rules:
                trigger_keywords = rule.get("trigger_keywords", [])
                
                # Check if any keyword matches
                if any(keyword.lower() in search_text for keyword in trigger_keywords):
                    # Determine risk level
                    risk_level_str = rule.get("risk_level", "HIGH")
                    if risk_level_str == "HIGH" or risk_level_str == "High":
                        risk_level = RiskLevel.HIGH
                    elif risk_level_str == "CRITICAL" or risk_level_str == "Critical":
                        risk_level = RiskLevel.CRITICAL
                    elif risk_level_str == "MEDIUM" or risk_level_str == "Medium":
                        risk_level = RiskLevel.MEDIUM
                    else:
                        risk_level = RiskLevel.LOW
                    
                    warnings.append(RiskWarning(
                        category="Regulatory",
                        risk_level=risk_level,
                        title=rule.get("title", f"{category_name} Compliance Required"),
                        description=rule.get("warning_message", ""),
                        actions=[
                            f"Check {category_name} regulations",
                            "Consult compliance professional",
                            "Budget for certification/testing"
                        ]
                    ))
        
        # Fallback to hardcoded rules if JSON not loaded or no matches
        if not warnings:
            # Food/Candy Regulatory Risks (Fallback)
            if any(keyword in search_text for keyword in ["food", "candy", "snack", "chocolate", "beverage", "drink", "식품", "과자", "음료"]):
                warnings.append(RiskWarning(
                    category="Regulatory",
                    risk_level=RiskLevel.HIGH,
                    title="🔴 FDA Facility Registration & Prior Notice Required",
                    description=(
                        "Food products imported to USA require:\n"
                        "• FDA Facility Registration (Foreign Supplier Verification Program - FSVP)\n"
                        "• Prior Notice submission for each shipment\n"
                        "• Food Safety Modernization Act (FSMA) compliance\n"
                        "• Labeling requirements (allergens, nutrition facts)\n"
                        "• Potential FDA inspection hold at port"
                    ),
                    actions=[
                        "Obtain FDA Registration before shipping",
                        "Partner with FSVP-compliant supplier",
                        "Budget 2-4 weeks for FDA clearance",
                        "Consult FDA-registered broker"
                    ]
                ))
        
        # Toys/Children's Products - CPSC
        if any(keyword in search_text for keyword in ["toy", "kid", "child", "children", "baby", "infant", "장난감", "어린이"]):
            warnings.append(RiskWarning(
                category="Regulatory",
                risk_level=RiskLevel.HIGH,
                title="CPSC/CPC Certification Required",
                description=(
                    "Children's products require:\n"
                    "• Children's Product Certificate (CPC) from manufacturer\n"
                    "• CPSC testing by accredited lab (lead, phthalates, mechanical hazards)\n"
                    "• Tracking labels on product packaging\n"
                    "• Age grading requirements\n"
                    "• Potential CPSC recall if non-compliant"
                ),
                actions=[
                    "Get CPC from supplier before shipping",
                    "Verify CPSC testing documentation",
                    "Ensure tracking labels are compliant",
                    "Budget for lab testing ($500-$2000 per product)"
                ]
            ))
        
        # Electronics - FCC/UL
        if any(keyword in search_text for keyword in ["electronic", "battery", "charger", "power", "wireless", "bluetooth", "전자제품", "배터리"]):
            warnings.append(RiskWarning(
                category="Regulatory",
                risk_level=RiskLevel.MEDIUM,
                title="FCC/UL Certification Required",
                description=(
                    "Electronic devices require:\n"
                    "• FCC Part 15 certification (radio frequency devices)\n"
                    "• UL/CE marking for safety compliance\n"
                    "• Battery safety testing (if lithium battery included)\n"
                    "• Amazon requires FCC ID in product listing"
                ),
                actions=[
                    "Obtain FCC ID before listing on Amazon",
                    "Verify UL/CE certification documents",
                    "Test battery safety if applicable",
                    "Budget 4-8 weeks for certification"
                ]
            ))
        
        return warnings
    
    def analyze_logistics_risks(
        self,
        product_name: str,
        market: Optional[str] = None,
        estimated_lead_time: Optional[str] = None
    ) -> List[RiskWarning]:
        """
        Analyze logistics risks including peak season surcharges.
        
        Args:
            product_name: Product name
            market: Target market
            estimated_lead_time: Estimated lead time string
            
        Returns:
            List of RiskWarning objects
        """
        warnings: List[RiskWarning] = []
        
        # Q4/Holiday Season Warning
        from datetime import datetime
        current_month = datetime.now().month
        
        if current_month >= 10 or current_month <= 1:  # Oct, Nov, Dec, Jan
            warnings.append(RiskWarning(
                category="Logistics",
                risk_level=RiskLevel.HIGH,
                title="Peak Season Surcharge (PSS) & Port Congestion Warning",
                description=(
                    "Q4/Holiday season logistics challenges:\n"
                    "• Peak Season Surcharge (PSS): +$500-$2000 per container\n"
                    "• Port congestion delays: +7-14 days at LA/Long Beach ports\n"
                    "• Carrier capacity constraints - booking guaranteed space required\n"
                    "• Higher freight rates (20-50% premium)\n"
                    "• Extended customs clearance times"
                ),
                actions=[
                    "Book container space 4-6 weeks in advance",
                    "Budget 20-50% higher freight costs",
                    "Plan for 2-week buffer in lead time",
                    "Consider air freight for urgent orders (+$5-10/unit cost)"
                ]
            ))
        
        # Market-specific logistics risks
        if market == "USA":
            warnings.append(RiskWarning(
                category="Logistics",
                risk_level=RiskLevel.MEDIUM,
                title="US Port Congestion Risk",
                description=(
                    "Common US port challenges:\n"
                    "• LA/Long Beach: Frequent congestion (2-5 day delays)\n"
                    "• New York/NJ: Peak season delays\n"
                    "• Inland rail congestion affecting drayage\n"
                    "• Chassis shortages at port terminals"
                ),
                actions=[
                    "Book guaranteed container space",
                    "Consider alternative ports (Savannah, Charleston)",
                    "Budget for demurrage/detention fees",
                    "Work with experienced customs broker"
                ]
            ))
        
        return warnings
    
    def analyze_ip_risks(
        self,
        product_name: str,
        product_category: Optional[str] = None
    ) -> List[RiskWarning]:
        """
        Detect IP/Trademark risks for famous brand names.
        
        Args:
            product_name: Product name
            product_category: Product category
            
        Returns:
            List of RiskWarning objects
        """
        warnings: List[RiskWarning] = []
        search_text = f"{product_name} {product_category or ''}".lower()
        
        # Check for famous brands
        detected_brands = []
        for brand in self.FAMOUS_BRANDS:
            if brand in search_text:
                detected_brands.append(brand)
        
        if detected_brands:
            brand_list = ", ".join(set(detected_brands))
            warnings.append(RiskWarning(
                category="IP/Trademark",
                risk_level=RiskLevel.CRITICAL,
                title="🚨 IP/Trademark License Verification REQUIRED",
                description=(
                    f"Detected potential IP/trademark usage: {brand_list}\n\n"
                    "⚠️ CRITICAL RISKS:\n"
                    "• Amazon will REMOVE listing without proper license\n"
                    "• Legal action from IP holder (cease & desist)\n"
                    "• Customs seizure at port if unlicensed\n"
                    "• Financial penalties and inventory loss\n"
                    "• Permanent Amazon seller account suspension"
                ),
                actions=[
                    "Verify IP/Trademark license BEFORE ordering",
                    "Obtain written authorization from IP holder",
                    "Check with Amazon Brand Registry",
                    "Consult IP attorney if unsure",
                    "DO NOT proceed without license documentation"
                ]
            ))
        
        return warnings
    
    def generate_all_risks(
        self,
        product_name: str,
        product_category: Optional[str] = None,
        market: Optional[str] = None,
        estimated_lead_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate all risk warnings for a product.
        
        Args:
            product_name: Product name
            product_category: Product category
            market: Target market
            estimated_lead_time: Estimated lead time
            
        Returns:
            Dictionary with categorized risk warnings
        """
        all_warnings = []
        
        # Regulatory risks
        all_warnings.extend(self.analyze_regulatory_risks(product_name, product_category, market))
        
        # Logistics risks
        all_warnings.extend(self.analyze_logistics_risks(product_name, market, estimated_lead_time))
        
        # IP/Trademark risks
        # IP/Trademark risks
        all_warnings.extend(self.analyze_ip_risks(product_name, product_category))
        
        # --- Mitsubishi/Alibaba Style Macro Analysis ---
        macro_risks = self.analyze_macro_risks(product_name, product_category, market)
        all_warnings.extend(macro_risks)

        # Convert to dictionary format
        return {
            "warnings": [
                {
                    "category": w.category,
                    "risk_level": w.risk_level.value,
                    "title": w.title,
                    "description": w.description,
                    "actions": w.actions
                }
                for w in all_warnings
            ],
            "summary": {
                "total_warnings": len(all_warnings),
                "critical_count": sum(1 for w in all_warnings if w.risk_level == RiskLevel.CRITICAL),
                "high_count": sum(1 for w in all_warnings if w.risk_level == RiskLevel.HIGH),
                "medium_count": sum(1 for w in all_warnings if w.risk_level == RiskLevel.MEDIUM),
                "low_count": sum(1 for w in all_warnings if w.risk_level == RiskLevel.LOW)
            },
            "macro_analysis": self.get_macro_analysis_scores(market, product_category)
        }

    def detect_regulatory_risks(
        self,
        product_name: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simplified keyword-based regulatory risk detection (Phase 4 spec).
        
        Args:
            product_name: Product name
            category: Product category
            
        Returns:
            Dictionary with regulatory_risk level and warnings
        """
        search_text = f"{product_name} {category or ''}".lower()
        warnings = []
        regulatory_risk_level = "LOW"
        
        # Food/Supplements
        if any(keyword in search_text for keyword in ["candy", "snack", "vitamin", "food", "식품", "과자"]):
            regulatory_risk_level = "HIGH"
            warnings.append({
                "category": "Food/Supplements",
                "warning": "FDA Facility Registration (21 CFR 1.225), Prior Notice, FSVP required."
            })
        
        # Children/Toys
        if any(keyword in search_text for keyword in ["toy", "plush", "kid", "child", "children", "장난감"]):
            regulatory_risk_level = "HIGH"
            warnings.append({
                "category": "Children/Toys",
                "warning": "CPSIA Compliance, ASTM F963 Testing, CPC (Children's Product Certificate) required."
            })
        
        # Electronics
        if any(keyword in search_text for keyword in ["battery", "led", "wireless", "electronic", "전자제품"]):
            regulatory_risk_level = "MEDIUM"
            warning_msg = "FCC Authorization, UL Standards."
            if "lithium" in search_text or "li-ion" in search_text or "battery" in search_text:
                warning_msg += " If Lithium: UN38.3 required."
            warnings.append({
                "category": "Electronics",
                "warning": warning_msg
            })
        
        # Cosmetics
        if any(keyword in search_text for keyword in ["cream", "skin", "serum", "cosmetic", "beauty", "화장품"]):
            regulatory_risk_level = "MEDIUM"
            warnings.append({
                "category": "Cosmetics",
                "warning": "FDA MoCRA Facility Registration & Listing required."
            })
        
        # Textile
        if any(keyword in search_text for keyword in ["shirt", "apparel", "cloth", "textile", "의류"]):
            regulatory_risk_level = "LOW"
            warnings.append({
                "category": "Textile",
                "warning": "Flammable Fabrics Act, FTC 'Made in USA' labeling rules."
            })
        
        # If no match, return LOW risk
        if not warnings:
            return {
                "regulatory_risk": "LOW",
                "warnings": [{"category": "General", "warning": "Standard General Cargo Risks"}]
            }
        
        return {
            "regulatory_risk": regulatory_risk_level,
            "warnings": warnings
        }

    def get_macro_analysis_scores(self, market: Optional[str], product_category: Optional[str]) -> Dict[str, Any]:
        """
        Generates quantitative scores for macro analysis factors with sub-factor transparency.
        """
        # Define base scores and sub-factors for transparency
        geo_risk = {"score": 30, "factors": {"무역 분쟁": 20, "정치 안정성": 50, "규제 변화": 60}}
        sup_stability = {"score": 70, "factors": {"납기 준수율": 75, "품질 클레임": 65, "업력": 70}}
        mkt_volatility = {"score": 40, "factors": {"원자재": 30, "환율": 50, "유가": 40}}

        # Adjust scores based on market and product
        if market and "china" in market.lower():
            geo_risk = {"score": 80, "factors": {"미중 무역분쟁": 90, "정치 안정성": 60, "자국 우선주의 규제": 85}}
            sup_stability["score"] = 60
        elif market and "vietnam" in market.lower():
            geo_risk = {"score": 40, "factors": {"중국 의존도": 50, "정치 안정성": 70, "노동법규 변화": 60}}
            sup_stability["score"] = 65

        if product_category and any(keyword in product_category.lower() for keyword in ["electronic", "chip", "battery"]):
            sup_stability = {"score": 50, "factors": {"핵심 부품 수급": 40, "기술 유출": 60, "인증 요구사항": 50}}
            mkt_volatility = {"score": 75, "factors": {"반도체 사이클": 80, "희귀 광물 가격": 70, "환율": 75}}
        
        return {
            "geopolitical_risk": geo_risk,
            "supplier_stability": sup_stability,
            "market_volatility": mkt_volatility
        }

    def analyze_macro_risks(
        self,
        product_name: str,
        product_category: Optional[str] = None,
        market: Optional[str] = None
    ) -> List[RiskWarning]:
        """
        Analyzes macro-level risks like geopolitical issues, supplier reliability, and market volatility.
        This simulates the expertise of a global trading company.
        """
        warnings: List[RiskWarning] = []
        search_text = f"{product_name} {product_category or ''}".lower()
        
        # 1. Geopolitical Risk (e.g., US-China Trade War)
        if market and "china" in market.lower():
            warnings.append(RiskWarning(
                category="Geopolitical",
                risk_level=RiskLevel.HIGH,
                title="📈 지정학적 리스크: 미-중 무역 분쟁",
                description="중국산 제품에 대한 미국의 추가 관세(Section 301) 부과 가능성이 상존합니다. 이는 예측 원가에 포함되지 않은 갑작스러운 비용 증가로 이어질 수 있습니다.",
                actions=["대체 원산지(베트남, 멕시코 등) 검토", "관세 변동에 대비한 가격 협상 조항 삽입", "정치/무역 뉴스 모니터링"]
            ))

        # 2. Supplier Reliability Risk (Alibaba-style)
        if market and any(c in market.lower() for c in ["china", "vietnam"]):
             warnings.append(RiskWarning(
                category="Supplier",
                risk_level=RiskLevel.MEDIUM,
                title="🏭 공급망 리스크: 공급업체 신뢰도",
                description="첫 거래 시, 소량 발주를 통해 품질, 납기 준수, 커뮤니케이션 능력을 반드시 검증해야 합니다. Alibaba의 Gold Supplier 등급도 실제와는 차이가 있을 수 있습니다.",
                actions=["공장 실사 또는 제3자 검수 진행", "단계별 대금 지급 조건(예: 선금 30%, 잔금 70%) 설정", "샘플과 양산품의 품질 일치 여부 확인"]
            ))
# 3. Market Volatility Risk
if any(keyword in search_text for keyword in ["oil", "plastic", "steel", "chip", "원유", "플라스틱", "철강"]):
    warnings.append(RiskWarning(
        category="Market",
        risk_level=RiskLevel.HIGH,
        title="💹 시장 리스크: 원자재 가격 변동성",
        description="이 제품은 원자재 가격 변동에 민감하여, 생산 중 원가가 상승할 리스크가 있습니다. 이는 마진을 급격히 감소시킬 수 있습니다.",
        actions=["고정 가격 계약 체결 시도", "원자재 가격 상승 시 원가 분담 조건 협의", "선물 거래를 통한 헷징(Hedging) 고려"]
    ))

# 4. Category-Specific Nuances (Feedback #088)
if "mango" in search_text or "asparagus" in search_text:
    warnings.append(RiskWarning(
        category="Regulatory",
        risk_level=RiskLevel.MEDIUM,
        title="🌿 특별 검역 대상 품목",
        description="망고, 아스파라거스 등 특정 신선 농산물은 통관 시 특별 검역 절차를 거치므로, 일반 농산물 대비 3~5일의 추가 시간이 소요될 수 있습니다.",
        actions=["통관사에 특별 검역 필요 여부 사전 문의", "유통기한을 고려하여 항공 운송 검토"]
    ))

return warnings
        # 4. Category-Specific Nuances (Feedback #088)
        if "mango" in search_text or "asparagus" in search_text:
            warnings.append(RiskWarning(
                category="Regulatory",
                risk_level=RiskLevel.MEDIUM,
                title="🌿 특별 검역 대상 품목",
                description="망고, 아스파라거스 등 특정 신선 농산물은 통관 시 특별 검역 절차를 거치므로, 일반 농산물 대비 3~5일의 추가 시간이 소요될 수 있습니다.",
                actions=["통관사에 특별 검역 필요 여부 사전 문의", "유통기한을 고려하여 항공 운송 검토"]
            ))
        
        if "battery" in search_text or "lithium" in search_text:
            warnings.append(RiskWarning(
                category="Cost",
                risk_level=RiskLevel.MEDIUM,
                title="💰 숨겨진 비용: 위험물 취급",
                description="리튬 배터리는 위험물로 분류되어, 일반 화물에 없는 추가 비용이 발생합니다: UN38.3 테스트(약 $500-2000), 위험물 취급 수수료, 특수 포장 비용 등.",
                actions=["공급업체에 UN38.3 테스트 리포트 요청", "포워더에게 위험물 운송 할증료 확인"]
            ))

        return warnings

    def get_macro_analysis_scores(self, market: Optional[str], product_category: Optional[str]) -> Dict[str, Any]:
        """
        Generates quantitative scores for macro analysis factors.
        """
        scores = {
            "geopolitical_risk": 30, # Base score
            "supplier_stability": 70, # Base score
            "market_volatility": 40 # Base score
        }
        
        if market and "china" in market.lower():
            scores["geopolitical_risk"] = 80
            scores["supplier_stability"] = 60
        elif market and "vietnam" in market.lower():
            scores["geopolitical_risk"] = 40
            scores["supplier_stability"] = 65

        if product_category and any(keyword in product_category.lower() for keyword in ["electronic", "chip", "battery"]):
            scores["supplier_stability"] = 50
            scores["market_volatility"] = 75

        return scores


# Singleton instance
risk_engine = RiskEngine()

# Expose main function
generate_all_risks = risk_engine.generate_all_risks
detect_regulatory_risks = risk_engine.detect_regulatory_risks

