import os, sys
sys.path.append('.')
sys.path.append('..')

from dotenv import load_dotenv
load_dotenv()

import sqlalchemy as sa
from sqlalchemy import orm, exc
from src.models import *


db = sa.create_engine(os.environ['DATABASE_URL'])
Session = orm.sessionmaker(bind=db)

def add_groups():
    sess = Session()
    new_groups = [
        Group(id=1, name='itzy'),
        Group(id=2, name='blackpink'),
        Group(id=3, name='twice'),
        Group(id=4, name='redvelvet'),
    ]
    for group in new_groups:
        query = sess.query(Group).filter(Group.id == group.id)
        obj = query.first()
        if obj:
            columns = [col.key for col in obj.__table__.columns]
            values = list(group.__dict__.values())[1:]
            query.update(dict(zip(columns, values)))
            status = 'Updated'
        else:
            sess.add(group)
            status = 'Created'
        print(f'{status} entry for {str(group)}')
    sess.commit()
    sess.close()

def main():
    add_groups()
    db.dispose()


if __name__ == '__main__':
    main()
