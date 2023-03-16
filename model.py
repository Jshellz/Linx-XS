from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin

from app import db

UserGrop = db.Table(
    'user_grop', db.Model.metadata,
    db.Model('user_id', db.Integer, db.ForeignKey('user_id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups_id'))
)

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class UserModel(db.Model):
    __tableName__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGrop)


class Group(db.Model, RestrictionsMixin):
    __tableName__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tableName__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Article(db.Model, PermissionsMixin):
    __tableName__ = 'articles'
    __permission__ = dict(
        owner=['read', 'update', 'delete', 'rework'],
        group=['read', 'update'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text)
