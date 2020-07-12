import os, json
import sqlalchemy as sa
from sqlalchemy import orm, exc
from src.models import *


db = sa.create_engine(os.environ['DATABASE_URL'])
Session = orm.sessionmaker(bind=db)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def add_from_json(Model, namespace=None):
    filename = Model.__name__.lower()
    filename = 'account' if filename == 'twitteraccount' else filename
    with open(os.path.join(BASE_DIR, f'update_models/{filename}.json'), 'r') as f:
        data = json.load(f)
    sess = Session()
    new_data = []
    for dat in data:
        if namespace is not None:
            dat['fields'][f'{namespace}_id'] = dat['fields'][namespace]
            del dat['fields'][namespace]
        new_data.append(Model(id=dat['pk'], **dat['fields']))
    for dat in new_data:
        query = sess.query(Model).filter(Model.id == dat.id)
        obj = query.first()
        if obj:
            columns = [col.key for col in obj.__table__.columns]
            values = list(dat.__dict__.values())[1:]
            query.update(dict(zip(columns, values)))
            status = 'Updated'
        else:
            sess.add(dat)
            status = 'Created'
        print(f'{status} entry for {repr(dat)}')
    sess.commit()
    sess.close()


def main():
    add_from_json(Group)
    add_from_json(Member, 'group')
    add_from_json(Alias, 'member')
    add_from_json(TwitterAccount, 'member')
    add_from_json(Channel, 'group')
    Session.close_all()
    db.dispose()


if __name__ == '__main__':
    main()
