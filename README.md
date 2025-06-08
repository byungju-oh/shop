물론입니다! 아래는 **Flask 기반 전자상거래 웹 애플리케이션**의 전체 내용을 **한국어**로 번역한 버전입니다:

---

# Flask 전자상거래 쇼핑몰 🛒

Flask로 구축된 현대적인 전자상거래 웹 애플리케이션입니다. 사용자 인증, 상품 관리, Google Cloud Storage 이미지 업로드, Prometheus를 통한 실시간 모니터링 기능을 제공합니다.

## 🌟 주요 기능

* **사용자 인증**: 회원가입, 로그인, 로그아웃 기능
* **상품 카테고리**: 패션, 전자제품, 보석류 섹션
* **이미지 관리**: GCS(Google Cloud Storage) 연동 이미지 업로드 및 삭제
* **장바구니**: 장바구니 담기 기능 (로그인 필요)
* **비동기 처리**: Celery를 이용한 사용자 등록 등의 백그라운드 작업 처리
* **모니터링**: Prometheus 메트릭을 통한 애플리케이션 성능 추적
* **반응형 디자인**: 모바일 친화적 UI (Bootstrap 기반)
* **다국어 지원**: 영어/한국어 인터페이스 요소

## 🏗️ 아키텍처 구조

```
├── app/
│   ├── __init__.py          # 앱 팩토리 및 설정
│   ├── models.py            # 데이터베이스 모델 (User, Item, Cart, Image)
│   ├── routes.py            # 라우팅 및 뷰 함수
│   ├── forms.py             # WTForms 기반 사용자 입력 검증
│   ├── tasks.py             # Celery 백그라운드 작업
│   ├── celery.py            # Celery 설정
│   └── templates/           # Jinja2 템플릿
├── requirements.txt         # Python 의존성
├── run.py                   # 애플리케이션 실행 진입점
├── Dockerfile               # 도커 설정 파일
└── .env                     # 환경 변수 파일
```

## 🚀 빠른 시작

### 사전 준비사항

* Python 3.9 이상
* MySQL 데이터베이스
* Redis 서버 (Celery용)
* Google Cloud Storage 계정

### 설치 방법

1. **레포지토리 클론**

   ```bash
   git clone <repository-url>
   cd flask-ecommerce-shop
   ```

2. **의존성 설치**

   ```bash
   pip install -r requirements.txt
   ```

3. **환경 변수 설정**
   루트 디렉토리에 `.env` 파일을 생성:

   ```env
   DATABASE_URI=mysql+pymysql://username:password@host/database
   SECRET_KEY=your-secret-key-here
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
   GCS_BUCKET_NAME=your-bucket-name
   ```

4. **GCS 설정**

   * GCS 버킷 생성
   * 서비스 계정 키 다운로드
   * `.env`에 경로 지정

5. **Redis 서버 실행**

   ```bash
   redis-server
   ```

6. **Celery 워커 실행**

   ```bash
   celery -A app.celery worker --loglevel=info
   ```

7. **애플리케이션 실행**

   ```bash
   python run.py
   ```

* 웹 애플리케이션 주소: `http://localhost:5000`
* Prometheus 메트릭 주소: `http://localhost:8000`

## 🐳 Docker로 배포

1. **Docker 이미지 빌드**

   ```bash
   docker build -t flask-shop .
   ```

2. **Docker Compose 사용 (권장)**

   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DATABASE_URI=mysql+pymysql://user:pass@db/shopdb
         - SECRET_KEY=your-secret-key
       depends_on:
         - db
         - redis
     
     db:
       image: mysql:8.0
       environment:
         - MYSQL_ROOT_PASSWORD=rootpass
         - MYSQL_DATABASE=shopdb
         - MYSQL_USER=user
         - MYSQL_PASSWORD=pass
     
     redis:
       image: redis:alpine
     
     celery:
       build: .
       command: celery -A app.celery worker --loglevel=info
       depends_on:
         - redis
         - db
   ```

## 📊 API 엔드포인트

### 인증

* `GET /register` - 회원가입 폼
* `POST /register` - 회원가입 처리
* `GET /login` - 로그인 폼
* `POST /login` - 로그인 처리
* `GET /logout` - 로그아웃

### 상품 관리

* `GET /` - 메인 페이지 (추천 상품)
* `GET /fashion` - 패션 상품 목록 및 이미지 관리
* `GET /electronic` - 전자제품 목록
* `GET /jewellery` - 보석류 목록
* `GET /search` - 상품 검색

### 이미지 관리

* `GET /add_image` - 이미지 업로드 폼 (로그인 필요)
* `POST /add_image` - GCS로 이미지 업로드 (로그인 필요)
* `POST /delete_image/<id>` - 이미지 삭제 (로그인 필요)

### 쇼핑

* `GET /cart` - 장바구니 보기 (로그인 필요)

## 🛠️ 기술 스택

* **백엔드**: Flask 2.0.2, SQLAlchemy, Flask-Login
* **DB**: MySQL + PyMySQL
* **작업 큐**: Celery + Redis
* **스토리지**: Google Cloud Storage
* **모니터링**: Prometheus
* **프론트엔드**: Bootstrap 4, jQuery, Font Awesome
* **폼 처리**: Flask-WTF (CSRF 방지 및 유효성 검증)
* **보안**: Bcrypt 비밀번호 해시

## 📈 모니터링

Prometheus를 통한 다음 메트릭 제공:

* 요청 처리 시간
* 현재 처리 중인 요청 수
* 총 HTTP 요청 수

메트릭 주소: `http://localhost:8000/metrics`

## 🔧 설정 예시

`app/__init__.py` 주요 설정:

```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['GCS_BUCKET_NAME'] = os.getenv('GCS_BUCKET_NAME')
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
```

## 🗄️ 데이터베이스 모델

### 사용자 (User)

* `id`: 기본 키
* `username`: 고유 사용자명
* `phone_number`: 전화번호
* `password`: Bcrypt 해시 비밀번호
* `image_file`: 프로필 이미지 (`default.jpg` 기본값)

### 이미지 (Image)

* `id`: 기본 키
* `url`: GCS URL

### 상품 (Item)

* `id`: 기본 키
* `name`: 상품 이름
* `price`: 가격
* `description`: 설명
* `image_file`: 상품 이미지
* `user_id`: 사용자 참조 키

### 장바구니 (Cart & CartItem)

* 수량 추적을 포함한 장바구니 기능

## 🚦 개발 모드 실행

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python run.py
```

### 테스트 실행

```bash
# 테스트 의존성 설치
pip install pytest pytest-flask

# 테스트 실행
pytest
```

## 📝 기여 방법

1. 레포지토리를 포크하세요
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경 사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 제공됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 확인하세요.

## 🔮 향후 개선 예정

* [ ] 결제 시스템 연동
* [ ] 주문 관리 시스템
* [ ] 상품 리뷰 및 평점
* [ ] 재고 관리
* [ ] 이메일 알림 기능
* [ ] 관리자 대시보드
* [ ] 고급 검색 및 필터
* [ ] 위시리스트 기능
* [ ] 다중 판매자 지원

---

