from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.users import User
from user_parcer import parser


def get_or_abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return session, user


class UserResource(Resource):
    def get(self, user_id):
        session, user = get_or_abort_if_user_not_found(user_id)
        return jsonify({'user': user.to_dict(
            rules=('-jobs',))})

    def delete(self, user_id):
        session, user = get_or_abort_if_user_not_found(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'ok'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users':
                            [item.to_dict(only=('id', 'name', 'surname', 'email', 'jobs.id', 'jobs.job'), )
                             for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(args.get('id'))
        if user:
            return jsonify({'error': 'Id already exist'})
        user = User(
            surname=args.get('surname'),
            name=args.get('name'),
            age=args.get('age'),
            position=args.get('position'),
            speciality=args.get('speciality'),
            address=args.get('address'),
            email=args.get('email'),
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
