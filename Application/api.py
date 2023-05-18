from flask_restful import Resource,Api,marshal_with,abort,request,reqparse,fields
from flask import current_app as app , jsonify , send_from_directory
from Application.database import db
from Application.models import *
from Application.token import token_r
from datetime import timedelta
from Application import tasks
from flask_caching import Cache
import jwt
import json
import time 
api=Api(app)

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')
create_user_parser.add_argument('image')
create_user_parser.add_argument('bio')


create_post = reqparse.RequestParser()
create_post.add_argument('post_name')
create_post.add_argument('image')
create_post.add_argument('post_descr')

user_fields={
    "user_name": fields.String,
    "user_id" : fields.Integer,
    "email" : fields.String,
    "password" : fields.String,
    "image" : fields.String,
    "bio" : fields.String,
}



app.config["CACHE_TYPE"] = "RedisCache"
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_HOST'] = "localhost"
app.config['CACHE_REDIS_PORT'] = 6379
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"  
app.config['CACHE_DEFAULT_TIMEOUT'] = 10
cache= Cache(app)

class Login(Resource):
    def post(self):
        args = create_user_parser.parse_args()
        user_name = args.get("user_name",None)
        password = args.get("password",None)
        if user_name is None:
            return {
                "message" : "User_name is required to login"
            } , 404
            
        if password is None:
           return {
                "message" : "Password is required to login"
            } ,404     

        user = User.query.filter(User.user_name == user_name).first()
        print(user)
        if user:
            if(user.password == password):
                u_id = user.user_id
                print(u_id)
                return jsonify({
                    "user_name":user.user_name,
                    # "email":user.email,
                    "password":user.password,
                    "user_id":user.user_id,
                    # "user_id":u_id,
                    "token" : jwt.encode({
                    'user_id': user.user_id,
                    'exp' : datetime.utcnow() + timedelta(minutes = 30)
                        }, app.config['SECRET_KEY'])
                     })
            else:
                abort(404, message="Provide Correct credentials")    

        else:
            abort(404, message="User doesn't exist")




class Register(Resource):
    def post(self):

        args = create_user_parser.parse_args()
        user_name = args.get("user_name" ,None)
        email = args.get("email" ,None)
        password = args.get("password" ,None)
        bio = args.get("bio" ,None)
        image = args.get("image" ,None)
        print(image)

        user = User.query.filter(User.user_name == user_name).first()
        if user:
           abort(404, description="Provide other Username this Username already exists")  

        
        newuser = User(user_name = user_name, email = email, password=password,image=image,bio=bio)
        db.session.add(newuser)
        db.session.commit()
        
        return {
            "username":newuser.user_name,
            "email":newuser.email,
            "password":newuser.password,
            "user_id":newuser.user_id,
            "image":newuser.image,
            "token" : jwt.encode({
            'user_id': newuser.user_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        }
    

@token_r
@app.route('/api/export/<int:user_id>', methods=['GET'])
def export_list(user_id):
    post = Post.query.filter_by(user_id=user_id).all()
    with open(f'export/{user_id}_post.csv', 'w') as post_csv:
        post_csv.write("SNo,Post_description,Post_image\n")
        for i in range(len(post)):

            post_csv.write(f'{i+1},{post[i].post_descr},{post[i].image}\n')
            # list_csv.write(i,list.title,list.desc)
        
    return send_from_directory("export",f'{user_id}_post.csv')

class Search(Resource):
    def get(self,user_name):
        user = User.query.filter(User.user_name.like(user_name)).all()
        d=[]
        for i in range(len(user)):
            d.append({
                "user_name":user[i].user_name,
                "user_id":user[i].user_id,
                "bio":user[i].bio,
                "dp":user[i].image
            })
        return d



class NewUser(Resource):

    @token_r
    @marshal_with(user_fields)
    def get(self,user_id):
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            return user
        else:
            return None
        
class Profile(Resource):
    @token_r
    @cache.cached(timeout=7)
    @cache.memoize(timeout=7)
    def get(self,user_id):
        user = User.query.filter(User.user_id == user_id).first()
        user1 = User.query.all()
        print(user)
        if user:
            post = Post.query.filter(Post.user_id == user_id).all()
            a=[]
            b=[]
            for i in user1:
                if user.is_following(i):
                    a.append(i)
                if i.is_follower(user):
                    b.append(i)
            print(a)
            follower_count = len(a)
            print(b)
            following_count = len(b)
            
            print(post)
            data=[]
            if len(post)>0:
                for i in range(len(post)):
                    # time = post[i].post_time
                    # dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
                    # formatted_date = dt.strftime('%d/%m/%Y')
                    # print(formatted_date)
                    data.append({
                        'user_id': user.user_id,
                        'user_name':user.user_name,
                        'user_dp':user.image,
                        'user_bio':user.bio,
                        # 'post_time':post[i].post_time,
                        'post_id':post[i].post_id,
                        'post_image':post[i].image,
                        'post_descr':post[i].post_descr,
                        'following_count':following_count,
                        'follower_count':follower_count
                    })
                return data
            else:
                return abort(404, message="No Post Yet")
                
    @token_r
    @cache.memoize(timeout=7)
    def post(self,user_id):
        args = create_post.parse_args()
        post_name = args.get("post_name",None)
        image = args.get("image",None)
        post_descr = args.get("post_descr",None)

        user=User.query.filter(User.user_id == user_id).first()
        print(user)
        if user:
            newpost = Post(user_id = user_id , post_name = post_name ,post_descr = post_descr , image = image )
            db.session.add(newpost)
            db.session.commit()
            return {
            'user_name':user.user_name,
            'user_dp':user.image,
            'user_bio':user.bio,            
            "post_descr":newpost.post_descr,
            "post_image":newpost.image,
            "post_id":newpost.post_id,
            "user_id":newpost.user_id
            # "token" : jwt.encode({"email":
            #  newuser.email_id, "iat": time.time(),"exp":time.time()+1800}, app.config['SECRET_KEY'])
        }
        else:
            abort(404, message="Please Signup before posting") 
class Alluser(Resource):
    @token_r
    def get(self,user_id):
        user = User.query.filter(User.user_id == user_id).first()
        user1=User.query.all()
        data=[]
        if len(user1)>0:
            for i in range(len(user1)):
                if user1[i] != user:
                    data.append({
                        'user_id': user1[i].user_id,
                        'user_name':user1[i].user_name,
                        'user_dp':user1[i].image,
                    })
            return data
class Addfollower(Resource):
    @token_r
    def get(self,user_id,external_id):
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            dusra_user = User.query.filter(User.user_id == external_id).first()
            if not dusra_user.is_following(user):
                dusra_user.follow(user)
                db.session.commit()
                return {'status':'success'}
            else:
                return {'status':'fail'}
        else:
            return None
class Editprofile(Resource):
    @token_r
    def get(self,user_id):
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            return {
                'user_id' : user.user_id,
                'user_name' : user.user_name,
                'email':user.email,
                'image':user.image,
                'bio':user.bio
            }
    @token_r
    def put(self,user_id):
        
        args = create_user_parser.parse_args()
        user_name = args.get("user_name" ,None)
        email = args.get("email" ,None)
        bio = args.get("bio" ,None)
        image = args.get("image" ,None)

        user = User.query.filter(User.user_id == user_id).first()
        if user:
            user.user_name=user_name
            user.email = email
            user.bio = bio
            user.image = image
            db.session.add(user)
            db.session.commit()
            print(user.user_name)
            return {"user_name":user.user_name,
                    "bio":user.bio,
                    "image":user.image,
                    "email":user.email
                    }
        
class EditPost(Resource):
    @token_r
    def get(self,user_id,post_id):
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            post = Post.query.filter(Post.post_id == post_id).first()
            if post:
                return{
                    "image":post.image,
                    "descr":post.post_descr,
                    "user_name":user.user_name
                }
    @token_r
    def put(self,user_id,post_id):
        args = create_post.parse_args()
        image = args.get("image",None)
        post_descr = args.get("post_descr",None)
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            post = Post.query.filter(Post.post_id == post_id).first()
            if post:
                post.post_descr = post_descr
                post.image = image
                db.session.commit()
                return{
                    "descr":post.post_descr,
                    "image":post.image,
                    "user_id":user.user_id
                }
    @token_r
    def delete(self,user_id,post_id):
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            post = Post.query.filter(Post.post_id == post_id).first()
            if post:
                db.session.delete(post)
                db.session.commit()
                return {
                    "user_id" : user.user_id
                }






class following(Resource):
    @token_r
    def get(self,user_id):
        user1 = User.query.filter(User.user_id == user_id).first()
        user=User.query.all()
        follower=[]
        if len(user)>0:
            for i in range(len(user)):
                if user[i] != user1:
                    if user[i].is_following(user1):
                        follower.append({'user_id':user[i].user_id,
                                         'status':'Following'
                                         })
                    # else:
                    #     follower.append({'user_id':user[i].user_id,
                    #                      'status':'Follow'
                    #                      })

        print(follower)
        return follower
class unfollow(Resource):
    @token_r
    def get(self,user_id , external_id):
        user1 = User.query.filter(User.user_id == user_id).first()
        if user1:
            user = User.query.filter(User.user_id == external_id).first()
            if user.is_following(user1):
                user.unfollow(user1)
                db.session.commit()
                return {
                    "user_id":user.user_id
                }



class feed(Resource):
    @token_r
    def get(self,user_id):
        user1 = User.query.filter(User.user_id == user_id).first()
        user=User.query.all()
        follower=[]
        if len(user)>0:
            for i in range(len(user)):
                if user[i] != user1:
                    if user[i].is_follower(user1):
                        follower.append(user[i])
                        print(follower)
        allpost = []
        for i in range(len(follower)):
            post = Post.query.filter(Post.user_id == follower[i].user_id).all()
            print(post)
            for j in range(len(post)):
                allpost.append({
                    "user_id":follower[i].user_id,
                    "user_name":follower[i].user_name,
                    "user_dp":follower[i].image,
                    "post_image":post[j].image,
                    "post_descr":post[j].post_descr,
                    # "time":post[j].post_time

                        })
        print(follower)
        return allpost

            



api.add_resource(Register,"/api/register")
api.add_resource(Login,"/api/login")
api.add_resource(NewUser,"/api/newuser/<int:user_id>")
api.add_resource(Profile,"/api/post/<int:user_id>")
api.add_resource(Alluser,"/api/alluser/<int:user_id>")
api.add_resource(Addfollower,"/api/Addfollower/<int:user_id>/<int:external_id>")
api.add_resource(feed,"/api/feed/<int:user_id>")
api.add_resource(Editprofile,"/api/editprofile/<int:user_id>")
api.add_resource(following,"/api/following/<int:user_id>")
api.add_resource(EditPost,"/api/editpost/<int:user_id>/<int:post_id>")
api.add_resource(unfollow,"/api/unfollow/<int:user_id>/<int:external_id>")
api.add_resource(Search,"/api/search/<string:user_name>")
