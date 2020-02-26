import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from Yukiblog.models import Manager, Category, Post, Comment
from Yukiblog.plugins import db


def fake_manager():
    manager = Manager(
        username='manager',
        blog_title='Yukiblog',
        blog_sub_title='This is a subtitle.',
        name='mana',
        about='mana Cierra tete'
    )
    manager.set_passwd('123456')
    db.session.add(manager)
    db.session.commit()


fake = Faker()
def fake_categories(count=10):
    # 先添加一个默认分类
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        # 避免字段名重复异常
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=60):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            text=fake.text(1500),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=300):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            text=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    bias = int(count*0.1)  # 百分之10的未审核评论
    for i in range(bias):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            text=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 来自manager的评论
        comment = Comment(
            author='mana',
            email='mana@example.com',
            site='fakesite.com',
            text=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_manager=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.sessoin.commit()

    # 评论内的回复
    for i in range(bias):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            text=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
