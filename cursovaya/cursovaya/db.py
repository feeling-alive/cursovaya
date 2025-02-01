from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Конфигурация подключения (локальная и удалённая)
DB_CONFIG = {
    "dialect": "mysql",
    "driver": "pymysql",
    "user": "root",
    "password": "23122005God",
    "host": "localhost",
    "port": 3306,
    "database": "torgcompany",
    "use_remote": False  # Если True к удалённой БД
}


DB_URL = f"{DB_CONFIG['dialect']}+{DB_CONFIG['driver']}://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(DB_URL, pool_size=10, max_overflow=20)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для получения сессии
def get_session():
    return SessionLocal()
