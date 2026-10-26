# BuildLog 개발 환경 기준 (Phase 0 확인 결과)

이 문서는 실제 개발을 시작하기 전에 확인하고 정한 환경 값들을 기록합니다.
개발이 진행되며 바뀌는 내용이 있으면 이 문서를 함께 수정합니다.

> 2026-10-26 업데이트: 백엔드를 Django에서 **FastAPI**로, 프론트엔드를 Django 템플릿에서 **React**로 바꾸고, 데이터베이스를 개발·테스트용 **SQLite**와 운영용 **Supabase(PostgreSQL)**로 나누기로 결정해 전체 내용을 다시 작성했습니다.

## 1. 문서 간 범위 확인

- [PRD.md](./PRD.md), [spec.md](./spec.md), [plan.md](./plan.md) 세 문서의 기능 범위를 비교했습니다.
- 세 문서 모두 같은 기능 범위(회원가입·로그인, 공부 기록, 할 일, 오류 기록, 공개·비공개, 검색, 댓글·좋아요, 신고)를 다루고 있고, 서로 충돌하는 내용은 없습니다.
- `spec.md`는 기술 구현 방법이 아닌 사용자 행동과 화면 결과 중심으로 작성되어 있어, 백엔드·프론트엔드 기술을 바꿔도 내용을 수정할 필요가 없습니다.
- 이번 MVP에서 만들지 않는 기능도 세 문서에서 동일합니다.
  - 이메일 인증
  - 비밀번호 찾기
  - 할 일 마감일, 중요도
  - 할 일(내 할 일) 검색
  - 댓글 답글

## 2. 전체 구조

BuildLog는 화면(프론트엔드)과 서버(백엔드)를 분리된 프로젝트로 만듭니다. 화면은 서버가 제공하는 API를 호출해서 데이터를 가져오고 저장합니다.

```text
사용자 브라우저
   │
   ▼
React (frontend) ──API 요청(JSON)──▶ FastAPI (backend) ──▶ 데이터베이스
                                                             (개발·테스트: SQLite)
                                                             (운영: Supabase/PostgreSQL)
```

## 3. 사용할 언어·프레임워크·버전

### 3.1 백엔드

| 항목 | 값 | 비고 |
| --- | --- | --- |
| Python | 3.14.6 | 실행 명령: `py -3.14`. 컴퓨터에 3.15.1도 있지만, 더 널리 쓰이고 안정적으로 확인된 3.14.6을 사용합니다. |
| 서버 프레임워크 | FastAPI 0.162.0 | API 서버를 가볍고 빠르게 만들 수 있습니다. |
| ASGI 서버 | Uvicorn 0.54.0 | FastAPI 앱을 실제로 실행하는 서버입니다. |
| ORM(데이터베이스 다루는 도구) | SQLAlchemy 2.0.55 | SQLite와 PostgreSQL(Supabase)을 같은 코드로 다룰 수 있게 해줍니다. 가장 널리 쓰이는 2.0 계열을 사용합니다. |
| 마이그레이션 도구 | Alembic 1.20.1 | 데이터 구조가 바뀔 때 SQLite와 Supabase에 같은 방식으로 반영합니다. |
| 데이터 검증 | Pydantic 2.14.1 | FastAPI가 기본으로 사용하는 입력값 검증 도구입니다. |
| 비밀번호 암호화 | passlib 1.7.4 + bcrypt 5.0.0 | 비밀번호를 안전하게 저장합니다. |
| 로그인 토큰 | PyJWT 2.15.1 | 로그인 상태를 유지하는 토큰(JWT)을 만들고 확인합니다. |
| PostgreSQL 연결 드라이버 | psycopg 3.3.6 | 운영 환경에서 Supabase(PostgreSQL)에 연결할 때 사용합니다. 개발·테스트 중에는 필요하지 않습니다. |
| 환경변수 읽기 | python-dotenv 1.2.4 | `.env` 파일의 값을 읽어옵니다. |
| 테스트 도구 | pytest 9.1.1 + httpx 0.28.1 | API 동작을 자동으로 테스트합니다. |

### 3.2 프론트엔드

| 항목 | 값 | 비고 |
| --- | --- | --- |
| Node.js | 24.22.1 | 컴퓨터에 설치된 버전을 사용합니다. |
| 화면 라이브러리 | React 19.3.1 | 메뉴로 나뉜 화면과 자주 바뀌는 상태(필터, 좋아요 등)를 다루기 좋습니다. |
| 빌드 도구 | Vite 8.3.5 | 개발 중 화면을 빠르게 다시 불러와서 확인할 수 있게 해줍니다. |
| 라우팅 | react-router-dom 7.18.4 | 회원가입, 로그인, 공부 기록 등 화면 간 이동을 담당합니다. |

### 3.3 데이터베이스

| 환경 | 값 | 비고 |
| --- | --- | --- |
| 개발·테스트 | SQLite (내장, 버전 3.50.4) | 별도 설치 없이 바로 쓸 수 있어 Phase 1~12까지는 이것만 사용합니다. |
| 운영 | Supabase (PostgreSQL) | 실제 서비스를 배포할 때 연결합니다. 이 MVP 개발 기간에는 연결 정보만 준비하고, 실제 연결과 전환은 Phase 13에서 확인합니다. |

SQLAlchemy와 Alembic을 사용하므로, 서버 코드는 두 데이터베이스 중 어떤 것을 쓰든 같은 모델·API 코드로 동작합니다. 바뀌는 것은 `DATABASE_URL` 환경 변수 값뿐입니다.

FastAPI 0.162.0과 SQLAlchemy 2.0.55 모두 순수 Python 패키지(`py3-none-any`)로 배포되어 있어, Python 3.14.6과 별도의 호환성 문제가 없음을 실제 다운로드로 확인했습니다.

## 4. 개발 서버와 저장 위치

| 항목 | 값 |
| --- | --- |
| 백엔드 개발 서버 주소 | `http://127.0.0.1:8000` |
| 프론트엔드 개발 서버 주소 | `http://127.0.0.1:5173` |
| SQLite 데이터 파일 위치 | `database/buildlog.sqlite3` (Git 기록 제외) |
| 백엔드 가상환경 위치 | `backend/.venv` (Git 기록 제외) |
| 프론트엔드 패키지 위치 | `frontend/node_modules` (Git 기록 제외) |

## 5. 환경 변수 이름

실제 비밀값은 `.env`에만 두고 Git에는 올리지 않습니다. `.env.example`에는 항목 이름만 남깁니다.

| 환경 변수 이름 | 설명 |
| --- | --- |
| `DATABASE_URL` | 사용할 데이터베이스 주소. 개발·테스트: `sqlite:///./database/buildlog.sqlite3`. 운영: Supabase가 제공하는 PostgreSQL 연결 주소. |
| `JWT_SECRET_KEY` | 로그인 토큰을 안전하게 만드는 보안 키. Phase 1에서 임의 값을 생성해 로컬 `.env`에만 저장합니다. |
| `JWT_EXPIRE_MINUTES` | 로그인 토큰의 유효 시간(분). 개발 중 기본값은 60으로 둡니다. |
| `BACKEND_CORS_ORIGINS` | API 요청을 허용할 프론트엔드 주소. 개발 중에는 `http://127.0.0.1:5173`을 사용합니다. |
| `SUPABASE_URL` | 운영 환경에서 Supabase 프로젝트 주소. 개발·테스트 중에는 비워둡니다. |
| `SUPABASE_SERVICE_KEY` | 운영 환경에서 Supabase에 연결할 때 사용하는 키. 개발·테스트 중에는 비워둡니다. |
| `VITE_API_BASE_URL` | 프론트엔드가 호출할 백엔드 주소. 개발 중에는 `http://127.0.0.1:8000`을 사용합니다. |

## 6. 앞으로 사용할 기본 명령 (Phase 1부터 실제로 생성)

| 목적 | 명령 (예정) |
| --- | --- |
| 백엔드 가상환경 만들기 | `py -3.14 -m venv backend/.venv` |
| 백엔드 가상환경 활성화 (Windows) | `backend\.venv\Scripts\activate` |
| 백엔드 패키지 설치 | `pip install -r backend/requirements.txt` |
| 백엔드 서버 실행 | `uvicorn app.main:app --reload --app-dir backend` |
| 백엔드 테스트 실행 | `pytest backend` |
| 데이터 구조 변경 반영(마이그레이션) | `alembic upgrade head` (`backend` 폴더 안에서 실행) |
| 프론트엔드 패키지 설치 | `npm install --prefix frontend` |
| 프론트엔드 개발 서버 실행 | `npm run dev --prefix frontend` |

## 7. Phase 0 확인 결과

- [x] PRD·spec·plan 세 문서의 기능 범위가 충돌하지 않습니다.
- [x] 백엔드(FastAPI)·프론트엔드(React)·데이터베이스(SQLite/Supabase)의 사용 버전을 정했습니다.
- [x] SQLite 사용 가능 여부를 확인했습니다. (내장, 버전 3.50.4)
- [x] 개발 서버 주소, 데이터 파일 위치, 환경 변수 이름을 정리했습니다.
- [x] 아직 패키지를 설치하거나 데이터베이스를 만들지 않았습니다.
