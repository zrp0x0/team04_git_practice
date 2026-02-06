from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "mem.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# 테이블 생성 함수
# - lifespan에서 딱 한 번 호출되도록 구현
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Depends를 활용하여 의존성 주입을 하기 위한 함수
def get_session():
    with Session(engine) as session:
        yield session
