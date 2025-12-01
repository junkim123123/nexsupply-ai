# NexSupply Landing Page

NexSupply 랜딩 페이지 - B2B 글로벌 소싱 플랫폼

## 기술 스택

- **Next.js 16** (App Router)
- **React 19**
- **TypeScript**
- **Tailwind CSS v4**

## 시작하기

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 프로젝트 구조

```
landing-page/
├── app/
│   ├── page.tsx          # 메인 페이지
│   ├── layout.tsx        # 레이아웃
│   └── globals.css       # 전역 스타일
├── components/
│   ├── NavigationBar.tsx      # 네비게이션 바
│   ├── HeroSection.tsx        # 히어로 섹션
│   ├── ValueProposition.tsx   # 가치 제안
│   ├── CoreFeatures.tsx       # 핵심 기능
│   ├── DashboardPreview.tsx   # 대시보드 미리보기
│   ├── SocialProof.tsx        # 소셜 프루프
│   ├── Pricing.tsx            # 가격 정책
│   └── Footer.tsx             # 푸터
└── public/                    # 정적 파일
```

## 주요 섹션

1. **Global Navigation Bar** - 로고, 메뉴, CTA 버튼
2. **Hero Section** - 메인 헤드라인과 제품 분석 입력
3. **Value Proposition** - 3가지 타겟 페르소나 (Brands, FBA, Enterprise)
4. **Core Features** - True Landed Cost, Regulatory Shield, Supplier Vetting
5. **Dashboard Preview** - Mission Control 대시보드 미리보기
6. **Social Proof** - 글로벌 리더 기업 로고
7. **Pricing** - 3가지 가격 티어 (Starter, Growth, Corporate)
8. **Footer** - 링크 및 저작권 정보

## 디자인 시스템

- **Primary Colors**: Deep Navy (#111827), Steel Grey (#1f2937)
- **Accent Colors**: Blue (#3b82f6), Cyan (#06b6d4), Purple (#a855f7)
- **Font**: Inter (Google Fonts)

## 빌드

```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```
