import os
from sqlalchemy import create_engine
from src.models import Base
from dotenv import load_dotenv


load_dotenv()

def main():
    engine = create_engine(f"postgresql+psycopg2://{os.environ['DATABASE_URL']}")
    Base.metadata.create_all(engine)
    print('Migrations completed.')


if __name__ == '__main__':
    main()
