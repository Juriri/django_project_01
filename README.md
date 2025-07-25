# 🧾 Django Todo & Bookmark Project

이 프로젝트는 Django 프레임워크를 활용하여 만든 **Todo 관리 앱**과 **Bookmark 저장 기능**이 포함된 웹 애플리케이션입니다.  
현재 **Python3.12, Django 5.2** 기반에서 동작하도록 설계되어 있습니다.

---

## 📝 주요 기능

### ✅ Todo 기능 (`todolist` 앱)
- Todo 등록, 조회, 수정, 삭제
- 완료 여부 필터링 기능
- 시작일/종료일 기준 정렬
- 관리자 페이지에서 관리 가능

### 🔖 Bookmark 기능 (`bookmark` 앱)
- URL과 제목 기반 북마크 저장
- 북마크 목록 및 상세 조회

---

## 🗂 프로젝트 구조

```plaintext
📦 django_project_01/
├── config/        # 프로젝트 설정 (settings.py, urls.py 등)
├── bookmark/      # 북마크 앱
├── todolist/      # 투두리스트 앱
├── manage.py      # Django 명령어 관리 파일
├── requirements.txt
└── .venv/         # Python 가상환경 (Git에서는 제외됨)
```

---

## ⚙️ 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/yourname/your-repo.git
cd django_project_01/
```

### 2. 가상환경 생성 및 활성화

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 마이그레이션 & 서버 실행

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🔐 관리자 페이지 접속

```bash
python manage.py createsuperuser
```

이후 웹 브라우저에서 [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/) 으로 접속하여 로그인하세요.

---

## 💡 기타 참고

- HTML 템플릿은 Django 템플릿 사용 가능
- Django Admin 설정은 `admin.py` 에서 구성 가능
- 각 앱의 `models.py` / `views.py` / `urls.py` 확인

---
