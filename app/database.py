## SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

# 'postgresql://<username>:<password>@<ip-address/host>:<port>/<dbname>
SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host = 'localhost',
#             database='fastapi',
#             user = 'postgres',
#             password='password',
#             port = 5432,
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('DB connection success')
#         break
#     except Exception as error:
#         print("connect failed")
#         print(error)
#         time.sleep(2)