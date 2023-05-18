from datetime import datetime 
from Application.database import db

follow = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.user_id')),
                     db.Column('following_id', db.Integer,
                               db.ForeignKey('user.user_id'))
                     )

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, auto_increment = True)
    email = db.Column(db.String(50), unique=True, index=True,nullable=False)
    user_name = db.Column(db.String(50), unique=True, index=True , nullable = False)
    user_time = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String(50),nullable = False)
    bio = db.Column(db.Text())
    image = db.Column(db.String(1000))
    posts = db.relationship("Post",backref= "user",lazy = True)

    followed = db.relationship(
        'User', secondary=follow,
        primaryjoin=(follow.c.follower_id == user_id),
        secondaryjoin=(follow.c.following_id == user_id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            follow.c.following_id == user.user_id).count() > 0
    def is_follower(self, user):
        return self.followed.filter(
            follow.c.following_id == user.user_id).count() > 0


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer,primary_key = True, auto_increment = True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.user_id"),nullable = False)
    image = db.Column(db.String(100),nullable = False)
    post_time = db.Column(db.DateTime(), default=datetime.utcnow)
    post_name = db.Column(db.String(50) , nullable = False )
    post_descr = db.Column(db.String(500) , nullable = False )
    # likes = db.Column(db.Integer)
    # followers = db.relationship("Follower",backref="post",lazy=True)
    # following = db.relationship("Following",backref="post",lazy=True)

# class Follower(db.Model):
#     __tablename__ = 'follower'
#     follower_id = db.Column(db.Integer, primary_key = True )
#     user_id = db.Column(db.Integer , db.ForeignKey("user.user_id"),nullable = False)
#     post_id = db.Column(db.Integer , db.ForeignKey("user.user_id"),nullable = False)



# class Following(db.Model):
#     __tablename__ = 'following'
#     following_id = db.Column(db.Integer, primary_key = True )
#     user_id = db.Column(db.Integer , db.ForeignKey("user.user_id"),nullable = False)
#     post_id = db.Column(db.Integer , db.ForeignKey("user.user_id"),nullable = False)
