from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Give each request its own database session, and always CLOSE it afterwards. 
    Also endpoints get a session with: db: Session = Depends(get_db)"""
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()