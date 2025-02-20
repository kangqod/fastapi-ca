

## 작성 순서 (ex: Note)

1. 도메인 계층 구현
    - Domain class 정의
        - note/domain/note.py
    - 노트를 데이터베이스에 저장하고 다루는 저장소의 인터페이스 작성
        - note/domain/repository/note_repo.py

2. 애플리케이션 계층 구현
애플리케이션 계층에는 note_service 모듈을 가진다.
    - 이 모듈을 구현하기 전에 dependency_injector 로 NoteRepository를 주입받을 수 있도록 컨테이너에 추가한다.  
    (이 시점에는 application, infra 쪽 구현부가 없어서 에러날 수 있음)
        - containers.py
    - 유스케이스를 구현한다.
        - note/infra/repository/note_repo.py
    - 애플리케이션에서 서비스를 구현한다.
        - note/application/note_service.py
        CRUD 구현

3. 인터페이스 계층 구현
Note 의 CRUD 유스케이스를 호출하는 컨트롤러를 만들 차례.  
note_controller 모듈은 외부로부터 요청이 전달되는 엔드포인트 함수를 가진다.  
이 컨트롤러를 만들고 FastAPI 애플리케이션 객체에 라우터로 등록한다.  

4. 인프라 계층 구현
마지막으로 데이터베이스를 다루는 인프라 계층을 구현한다.  
가장 먼저 해야 할 일은 데이터베이스 모델을 생성하고, SQLAlchemy로 테이블을 만드는 일이다.
    - note/infra/db_models/note.py
    - database_models.py
    - (다음으로 테이블 마이그레이션을 한다.)
    - alembic revision --autogenerate -m "add Note, Tag"
    - alembic upgrade head

