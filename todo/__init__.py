import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todo.constants import DATA_DIR, DB_DIR, DB_PATH, GIT_REPO_DIR
from dotenv import load_dotenv

load_dotenv()

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
    os.mkdir(DB_DIR)
    os.mkdir(GIT_REPO_DIR)

engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)