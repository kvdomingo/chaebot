import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get('PYTHON_ENV') == 'development':
    DEBUG = True
elif os.environ.get('PYTHON_ENV') == 'production':
    DEBUG = False
else:
    raise RuntimeError('PYTHON_ENV environment variable is improperly configured.')

db = create_engine(os.environ.get('DATABASE_URL'), poolclass=NullPool)
Session = sessionmaker(bind=db)
