# coding:utf8
from sqlalchemy.orm import foreign, remote

from app import db
from datetime import datetime
from sqlalchemy import and_



# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机
    info = db.Column(db.TEXT)  # 简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志服

    # 外键关系关联
    userlogs = db.relationship('Userlog', backref="user")
    comments = db.relationship('Comment', backref="user")  # 评论
    moviecols = db.relationship('Moviecol', backref="user")  # 收藏

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    # 定义外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    # 外键关系关联
    movies = db.relationship('Movie', backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 标号
    content = db.Column(db.Text)  # 品论内容

    # 外键
    movie_id = db.Column(db.Integer)  # 所属的电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属的用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.TEXT)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封 面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论个数
    # 外键
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时长
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    # 外键关联
    comments = db.relationship("Comment", backref=db.backref('movie', uselist=False, lazy='noload'), lazy='noload',
                            uselist=True, primaryjoin=and_(foreign(id) == remote(Comment.movie_id)))  # 评论
    moviecols = db.relationship('Moviecol', backref="movie")  # 收藏

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title





# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 标号

    # 外键
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属的电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属的用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 标号
    name = db.Column(db.String(255), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 标号
    name = db.Column(db.String(255), unique=True)  # 名称
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    admins = db.relationship('Admin', backref="role")
    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否是超级管理员 0 为是的

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属的角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    adminlogs = db.relationship('Adminlog', backref="admin")  # 评论
    oplogs = db.relationship('Oplog', backref="admin")

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

# 登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    # 定义外键
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属的管理员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    # 定义外键
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属的管理员
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))  # 操作的原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == '__main__':
    db.drop_all()
    db.create_all()





