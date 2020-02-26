from Yukiblog.plugins import db
from datetime import datetime


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    passwd_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(120))
    name = db.Column(db.String(40))
    about = db.Column(db.Text)

    # TODO 临时的密码设置验证，后期需要更改
    def set_passwd(self, passwd):
        self.passwd_hash = passwd

    def validate_passwd(self, passwd):
        if passwd == self.passwd_hash:
            return True
        return False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 与Category表有关的外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    # 与Comment表有关的外键
    comments = db.relationship('Comment', backref='post', casecade='all')  # 级联删除


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    text = db.Column(db.Text)
    from_manager = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 与Post表有关的外键
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    # 邻接列表(Adjacency List Relationship)
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    relplies = db.relationship('Comment', back_populates='replied', casecade='all')
