import json
from sqlalchemy import func
from sqlalchemy import exc
from .mixins import ApiSerializerMixin
from .models import *
from . import Session


class GroupApi(ApiSerializerMixin):
    def get(self, name):
        sess = Session()
        if name == 'all':
            queryset = sess.query(Group).order_by(Group.id).all()
            response = [self.serialize(group) for group in queryset]
        else:
            query = sess.query(Group).filter(Group.name == name).first()
            response = self.serialize(query)
        sess.close()
        return json.dumps(response, indent=4)

    def create(self, name):
        sess = Session()
        g_id = sess.query(func.max(Group.id)) + 1
        obj = Group(id=g_id, name=name.lower())
        sess.add(obj)
        try:
            sess.commit()
            response = self.serialize(obj)
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)

    def update(self, old_name, new_name):
        sess = Session()
        query = sess.query(Group).filter(Group.name == old_name.lower()).first()
        query.name = new_name.lower()
        try:
            sess.commit()
            qid = query.id
            response = self.serialize(query)
            print(f"Updated Group {qid}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object update failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)


class MemberApi(ApiSerializerMixin):
    def get(self, group, name):
        sess = Session()
        if name == 'all':
            queryset = sess.query(Member).filter(Member.group.has(name=group)).all()
            response = [self.serialize(query) for query in queryset]
        else:
            query = sess.query(Group).filter(Group.name == group).filter(Group.members.has(stage_name=name)).first()
            if query:
                response = self.serialize(query)
            else:
                response = dict(error=f"No match for member with corresponding stage_name={name}")
        sess.close()
        return json.dumps(response, indent=4)

    def create(self, *args):
        params = ['group', 'stage_name', 'family_name', 'given_name']
        sess = Session()
        fields = dict(zip(params, args))
        m_id = sess.query(func.max(Member.id)).first()[0] + 1
        group_id = sess.query(Group).filter(Group.name == fields['group']).first().id
        fields['id'] = m_id
        fields['group_id'] = group_id
        del fields['group']
        obj = Member(**fields)
        try:
            sess.add(obj)
            sess.commit()
            m_id = obj.id
            response = self.serialize(obj)
            print(f"Created member {m_id}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        return json.dumps(response, indent=4)
