import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask import current_app
from sqlalchemy import orm


class Project(SqlAlchemyBase):
    __tablename__ = "projects"
    
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    max_members = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    description = sqlalchemy.Column(sqlalchemy.Text(200), default="", nullable=True)
    leader = orm.relationship("User", lazy="subquery")
    leader_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"))
    
    def set_leader(self, leader):
        self.leader = leader
        leader.projects.append(self)
    
    def add_member(self, member):
        self.members.append(member)