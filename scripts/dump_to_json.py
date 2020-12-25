import json
from src import BASE_DIR, Session
from src.models import *

sess = Session()


def dump_json(model):
    filename = model.__tablename__.lower()
    serialized = sess.query(model).all()
    serialized = [serialize.to_dict() for serialize in serialized]
    serialized = sorted(serialized, key=lambda x: x['id'])
    with open(BASE_DIR / 'scripts' / 'data' / f'{filename}.json', 'w') as f:
        json.dump(serialized, f, indent=2)
    print(f'Dumped {filename}')


def main():
    models = [Group, Member, Alias, TwitterAccount, TwitterChannel, VliveChannel]
    for model in models:
        dump_json(model)


if __name__ == '__main__':
    main()
