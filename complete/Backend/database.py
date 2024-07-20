from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# データベースのURLを設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./test2.db"  # SQLiteを使用する例

# データベースエンジンの作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッションローカルクラスの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


