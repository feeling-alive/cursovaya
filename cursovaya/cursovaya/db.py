from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Конфигурация подключения
DB_CONFIG = {
    "user": "root",  # Имя пользователя MySQL
    "password": "23122005God",  # Пароль
    "host": "localhost",  # Хост MySQL
    "port": 3306,  # Порт
    "database": "torgcompany"  # Название базы
}

# Создаём движок SQLAlchemy
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Для выполнения запросов
def get_session():
    return SessionLocal()
