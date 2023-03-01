import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborations = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    team_leader_relation = orm.relationship('User')

    def __repr__(self):
        return f'<Colonist> {self.id} {self.team_leader}'
