# Youtube Comment Analysis for Vercel

기존 로컬 `Youtube_comment_analysis` 프로젝트를 Vercel 배포용으로 재구성한 버전입니다.  
정적 프론트는 `public/index.html`에서 제공하고, 서버 기능은 Vercel Python Functions로 분리했습니다.

## 주요 기능

- YouTube 키워드 검색 기반 영상 카드 대시보드
- `구독자 대비 조회수 N배` 표시
- 상위 댓글 + 답글 수집
- 댓글 50개 초과 시 무작위 50개 샘플 분석
- 균형형 Strategic Insight 생성
- 긍정 대표 댓글 1개, 부정 대표 댓글 1개 표시
- 서버측 환경변수 기반 YouTube/A15T 프록시

## 프로젝트 구조

- `public/index.html`: 기존 UI와 클라이언트 로직을 이식한 정적 엔트리
- `api/config.py`: `youtubeConfigured`, `a15tConfigured` 상태 반환
- `api/youtube/[endpoint].py`: YouTube API 프록시
- `api/proxy/analyze.py`: A15T 분석 프록시
- `api/_lib/`: 공통 유틸
- `docs/`: 문서 자산용 디렉터리
- `.env.example`: 필요한 환경변수 이름만 정의한 예시

## 환경변수

로컬과 Vercel 모두 아래 두 값을 사용합니다.

```env
YOUTUBE_API_KEY=
A15T_API_KEY=
```

- `YOUTUBE_API_KEY`: YouTube 검색/댓글 조회 프록시용
- `A15T_API_KEY`: Strategic Insight 생성용

실제 키는 Git에 올리지 말고, 로컬 `.env.local` 또는 Vercel Project Environment Variables에만 넣습니다.

## 로컬 실행

### 1. Vercel CLI 설치

```powershell
npm install -g vercel
```

### 2. 프로젝트 폴더로 이동

```powershell
cd "C:\Codex\Youtube_comment_analysis_versel"
```

### 3. 환경변수 준비

`.env.example`를 참고해 `.env.local` 또는 `.env`를 생성합니다.

```env
YOUTUBE_API_KEY=your_youtube_api_key
A15T_API_KEY=your_a15t_api_key
```

### 4. 로컬 개발 서버 실행

```powershell
vercel dev
```

브라우저에서 표시된 로컬 주소로 접속합니다. 일반적으로 `http://localhost:3000`입니다.

## Vercel 배포

### 1. Vercel 프로젝트 연결

```powershell
vercel
```

### 2. Vercel 환경변수 설정

Vercel Dashboard 또는 CLI에서 아래 키를 설정합니다.

- `YOUTUBE_API_KEY`
- `A15T_API_KEY`

### 3. 프로덕션 배포

```powershell
vercel --prod
```

## API 계약

프론트는 아래 경로를 그대로 사용합니다.

- `GET /api/config`
- `GET /api/youtube/search`
- `GET /api/youtube/videos`
- `GET /api/youtube/channels`
- `GET /api/youtube/commentThreads`
- `GET /api/youtube/comments`
- `POST /api/proxy/analyze`

이 계약은 기존 로컬 프로젝트와 동일하게 유지됩니다.

## 검증 시나리오

배포 전후에 아래 항목을 확인합니다.

1. `GET /api/config`가 `youtubeConfigured`, `a15tConfigured`를 반환하는지 확인
2. 검색창에 키워드를 입력했을 때 영상 카드 목록이 정상 표시되는지 확인
3. 영상 카드 클릭 시 댓글과 답글이 수집되는지 확인
4. 댓글 수가 50개를 넘는 영상에서 샘플링 기반 분석이 유지되는지 확인
5. 분석 결과에 긍정 대표 댓글과 부정 대표 댓글이 모두 표시되는지 확인
6. 부정 댓글 비중이 높은 영상에서 부정적 인사이트가 실제로 반영되는지 확인
7. `A15T_API_KEY`가 없을 때 경고 토스트가 표시되는지 확인
8. YouTube API 오류가 발생할 때 프론트에 에러 메시지가 전달되는지 확인

## 스크린샷 정책

- README용 화면 캡처가 필요하면 `docs/` 아래에 저장합니다.
- 정적 앱 런타임은 `public/`을 기준으로 하며, 문서 이미지는 기능 동작과 분리합니다.

## 주의 사항

- 이 프로젝트는 Vercel Python Functions를 전제로 구성됩니다.
- 기존 로컬 `server.py` 실행 방식은 새 프로젝트에 적용되지 않습니다.
- 실제 API Key는 절대 저장소에 커밋하지 않습니다.
