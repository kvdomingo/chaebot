import json

from sqlalchemy import exc
from sqlalchemy import func

from . import Session
from .models import *


class GroupApi:
    def get(self, name):
        sess = Session()
        if name == 'all':
            queryset = sess.query(Group).order_by(Group.id).all()
            response = [group.to_dict() for group in queryset]
        else:
            query = sess.query(Group).filter(Group.name == name).first()
            response = query.to_dict()
        sess.close()
        return json.dumps(response, indent=4)

    def create(self, name):
        sess = Session()
        g_id = sess.query(func.max(Group.id)) + 1
        obj = Group(id=g_id, name=name.lower())
        sess.add(obj)
        try:
            sess.commit()
            response = obj.to_dict()
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
            response = query.to_dict()
            print(f"Updated Group {qid}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object update failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)


class MemberApi:
    def get(self, group, name):
        sess = Session()
        if name == 'all':
            queryset = sess.query(Member).filter(Member.group.has(name=group)).all()
            response = [query.to_dict() for query in queryset]
        else:
            query = sess.query(Member).filter(Member.group.has(name=group)).filter(Member.stage_name == name).first()
            if query:
                response = query.to_dict()
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
            response = obj.to_dict()
            print(f"Created member {m_id}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)


class AccountApi:
    def get(self, group, member):
        sess = Session()
        accounts = sess.query(Member).filter(Member.group.has(name=group)).filter(Member.stage_name == member).first().twitter_accounts
        response = [acc.to_dict() for acc in accounts]
        sess.close()
        return json.dumps(response, indent=4)

    def create(self, *args):
        params = ['group', 'member', 'account_name']
        fields = dict(zip(params, args))
        sess = Session()
        a_id = sess.query(func.max(TwitterAccount.id)).first()[0] + 1
        member_id = sess.query(Member).filter(Member.group.has(name=fields['group'])).filter(Member.stage_name == fields['member']).first().id
        fields['id'] = a_id
        fields['member_id'] = member_id
        del fields['member'], fields['group']
        obj = TwitterAccount(**fields)
        try:
            sess.add(obj)
            sess.commit()
            a_id = obj.id
            response = obj.to_dict()
            print(f"Created twitter account {a_id}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)

    def update(self, *args):
        params = ['group', 'member', 'old_account', 'new_account']
        fields = dict(zip(params, args))
        sess = Session()
        obj = sess.query(TwitterAccount).join(TwitterAccount.member).filter(Member.group.has(name=fields['group'])).filter(Member.stage_name == fields['member']).filter(TwitterAccount.account_name == fields['old_account']).first()
        obj.account_name = fields['new_account']
        try:
            sess.commit()
            m_id = obj.id
            response = obj.to_dict()
            print(f"Updated twitter account {m_id}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)


class AliasApi:
    def get(self, group, member):
        sess = Session()
        query = sess.query(Alias).join(Alias.member).filter(Member.group.has(name=group)).filter(Member.stage_name == member).all()
        response = [obj.to_dict() for obj in query]
        sess.close()
        return json.dumps(response, indent=4)

    def create(self, *args):
        params = ['group', 'member', 'alias']
        fields = dict(zip(params, args))
        sess = Session()
        a_id = sess.query(func.max(Alias.id)).first()[0] + 1
        m_id = sess.query(Member).filter(Member.group.has(name=fields['group'])).filter(Member.stage_name == fields['member']).first().id
        fields['member_id'] = m_id
        fields['id'] = a_id
        del fields['member'], fields['group']
        obj = Alias(**fields)
        try:
            sess.add(obj)
            sess.commit()
            a_id = obj.id
            response = obj.to_dict()
            print(f"Created alias {a_id}")
        except exc.SQLAlchemyError as e:
            response = dict(error=f"Object creation failed with the following error: {e}")
        sess.close()
        return json.dumps(response, indent=4)