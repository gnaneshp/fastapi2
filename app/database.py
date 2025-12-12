from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time
from app.config import settings
# my_posts=[{"title":"title of my post 1","content":"content of my post 1","id":1},
#           {"title":"title of my post 2","content":"content of my post 2","id":2}]
# while(True):
#     try:
#        conn = connect(dbname="fastapi", user="postgres", password="gnanesh", host="localhost",row_factory=dict_row)
#        print("Connected to the database successfully")
#        cursor=conn.cursor()
#        break
#     except Exception as e:
#         print("Unable to connect to the database")
#         print(e)
#         time.sleep(3)
#     finally:
#         conn.close()
    
# def find_post(post_id:int):
#     for post in my_posts:
#         if post["id"]==post_id:
#             return post

# def find_index(post_id:int):
#     for i,post in enumerate(my_posts):
#         if post["id"]==post_id:
#             return i    
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
