# NexSupply AI - B2B 소싱 컨설턴트 플랫폼

AI 네이티브 B2B 소싱 컨설턴트 애플리케이션입니다. 텍스트나 이미지를 입력하면 Gemini 1.5 Flash가 분석하여 구조화된 소싱 리포트를 생성합니다.

## 🚀 빠른 시작

### Streamlit 앱 실행

#### 1. API 키 설정

`.env` 파일을 열고 실제 Gemini API 키로 수정하세요:

```
GEMINI_API_KEY=your_actual_api_key_here
```

API 키는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급받을 수 있습니다.

#### 2. 패키지 설치

```powershell
python -m pip install -r requirements.txt
```

#### 3. 앱 실행

```powershell
python -m streamlit run app.py
```

### Next.js 랜딩 페이지 실행

```bash
cd landing-page

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 📁 프로젝트 구조

```
Nexsupply-ai/
├── app.py                 # 메인 Streamlit 앱
├── requirements.txt       # Python 패키지 목록
├── Procfile               # 배포 설정
├── runtime.txt            # Python 버전
├── .env                   # API 키 설정 (직접 생성/수정)
├── pages/                 # Streamlit 페이지들
│   ├── Analyze.py
│   ├── Analyze_Results.py
│   └── Results.py
├── services/              # 비즈니스 로직
├── core/                   # 핵심 엔진
├── src/                    # AI 파이프라인
├── utils/                  # 유틸리티
├── data/                   # 데이터 파일 (CSV, JSON)
└── landing-page/          # Next.js 랜딩 페이지
    ├── app/
    ├── components/
    └── public/
```

## ✨ 주요 기능

### Streamlit 앱
- **텍스트/이미지 입력**: 비구조화된 텍스트나 제품 이미지 업로드
- **AI 분석**: Gemini 1.5 Flash가 자동으로 언어를 감지하고 JSON 리포트 생성
- **비용 분석**: Plotly 도넛 차트로 제조비용, 배송비, 관세 시각화
- **가정 표시**: AI가 가정한 수량(MOQ) 및 타겟 시장 정보
- **리스크 분석**: Safe/Caution/Danger 레벨 및 상세 노트
- **시장 인사이트**: 소매가 범위 및 경쟁 상황 분석

### Next.js 랜딩 페이지
- **Hero Section**: 메인 헤드라인과 제품 분석 입력
- **Value Proposition**: 3가지 타겟 페르소나 (Brands, FBA, Enterprise)
- **Core Features**: True Landed Cost, Regulatory Shield, Supplier Vetting
- **Dashboard Preview**: Mission Control 대시보드 미리보기
- **Pricing**: 3가지 가격 티어 (Starter, Growth, Corporate)

## 🔧 기술 스택

### Backend (Streamlit)
- **Frontend**: Streamlit
- **AI**: Google Gemini 1.5 Flash
- **Visualization**: Plotly
- **Database**: SQLite3

### Frontend (Landing Page)
- **Framework**: Next.js 16 (App Router)
- **UI**: React 19, TypeScript
- **Styling**: Tailwind CSS v4

## 📝 참고사항

- 모든 파싱은 LLM에만 의존하며, 하드코딩된 정규식이나 파싱 로직이 없습니다.
- 데이터베이스는 자동으로 초기화되며 `nexsupply.db` 파일에 저장됩니다.
- API 키는 절대 Git에 커밋하지 마세요. `.env` 파일은 `.gitignore`에 포함되어 있습니다.

## 🚢 배포

### Streamlit Cloud
1. GitHub 저장소에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 앱 배포
3. Secrets에 `GEMINI_API_KEY` 추가

### Next.js (Vercel)
```bash
cd landing-page
npm run build
```
