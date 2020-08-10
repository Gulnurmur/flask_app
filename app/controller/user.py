from flask import jsonify, Blueprint, request
from http import  HTTPStatus
from marshmallow.exceptions import ValidationError
from app.schemas.schema import  UserSchema, PostSchema, UserUpdateSchema
from app.models.model import  User, Post
from app.utils.helper import check_existence, check_user, check_password
from flask_jwt_extended import  jwt_required, jwt_refresh_token_required, create_access_token,create_refresh_token,get_jwt_identity

user = Blueprint("user", __name__)


@user.route("/root", methods=["GET"])
@jwt_required
def test():

    return jsonify({"result": True})


@user.route("/users/login", methods=["POST"])
@jwt_required
def login():
    
    data  =  request.json

    user_data  =  User.query.filter_by(email=data.get("email")).first()

    if not user_data:
        return jsonify({"result": False,"message": f"No user found  with address {data.get('email')}"})

    result = check_password(user_data.password, data.get("password"))

    if result:
        schema = UserSchema()

        user =  schema.dump(user_data)
        print("userin melumat" ,user)
        print("userin modeli" ,user_data)

        access_token = create_access_token(identity=user_data.id)
        refresh_token =  create_refresh_token(identity= user_data.id)

        user.update(access=access_token,refresh=refresh_token)

        return jsonify(user)

    return jsonify({"message": "User email or password wrong!"})


@user.route("/refresh/token", methods=["POST"])
@jwt_refresh_token_required
def refresh_token():

    user_id = get_jwt_identity()

    user_data =  User.query.get(user_id)
    
    access_token = create_access_token(identity=user_data.id)

    refresh_token =  create_refresh_token(identity= user_data.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token":refresh_token
        })

# @user.route("/test/<uuid:id>", methods=["GET"])
# def test_func(id):

#     posts = Post.query.all()
#     print(posts)
#     for post in posts:

#         print(post.user.name)
#         print(post.user.email)

#     user_detail = User.query.filter_by(id=id).first()

#     for post in user_detail.posts:
#         print(post.title)
#         print(post.content)

#     return jsonify({"result": True})



@user.route("/users", methods = ["GET"])
def get_users():

    user = User.query.all()
    
    return UserSchema().jsonify(user, many=True),HTTPStatus.OK




@user.route("/user",methods=["GET"])
@jwt_required
def get_user():

    user_id  =  get_jwt_identity()
    print("user idsi", user_id)

    user = User.query.filter_by(id=user_id).first()
    
    if user:
        return UserSchema().jsonify(user), HTTPStatus.OK

    return jsonify({"result": False}),HTTPStatus.NOT_FOUND



@user.route("/user", methods=["POST"])
def create_user():

    try:
        data = request.get_json()

        result = check_existence(data.get("email"))

        if not result: return jsonify({"result": False, "message": f"User this {data.get('email')} already exists"}), HTTPStatus.NOT_FOUND

        user = UserSchema()
        new_user = user.load(data)
        print("122", new_user)
        
        new_user.save()
        

        user_id=new_user.id
        print("user_id", user_id)

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        user = user.dump(new_user)
        user.update(access=access_token, refresh=refresh_token)
        

        return jsonify(user), HTTPStatus.OK

    except ValidationError as err:

        return jsonify(err.messages), HTTPStatus.NOT_FOUND


@user.route("/user", methods=["PUT"])
@jwt_required
def put_user():

    try: 

        user_id  =  get_jwt_identity()
    
        user_data= User.query.filter_by(id=user_id).first()

        data = request.get_json()

        user = UserUpdateSchema().load(data)


        print(user)
        print(user_data)
        user_data.update(**user)

        return jsonify({"message": "Updated successfully"})
    
    
    except ValidationError as err:

        return jsonify(err.messages),HTTPStatus.NOT_FOUND
        
        


@user.route("/user/<uuid:id>", methods=["DELETE"])
@jwt_required
def delete_user(id):

    user_id  =  get_jwt_identity()

    user = User.query.get(id)
    

    if user:

        if str(user.id) == user_id:

            user.delete()
            return jsonify({"result": True}), HTTPStatus.OK

    return jsonify({"result": False}), HTTPStatus.NOT_FOUND




@user.route("/posts", methods=["GET"])
@jwt_required
def get_posts():

    user_id  =  get_jwt_identity()

    posts = Post.query.filter_by(user_id=user_id).all()

    return PostSchema().jsonify(posts, many=True), HTTPStatus.OK


@user.route("/post/<uuid:id>",methods=["GET"])
@jwt_required
def post_user(id):

    user_id = get_jwt_identity()
    print("user_id" , user_id)

    post = Post.query.filter_by(id=id).first()
    print("post" , post)
    print("post_id" , post.user_id)
    print( type(post.user_id))
    
    if post:

        if str(post.user_id) == user_id:

            return PostSchema().jsonify(post), HTTPStatus.OK


    return jsonify({"result": False}),HTTPStatus.NOT_FOUND



@user.route("/post", methods=["POST"])
@jwt_required
def create_post():
    print("headers" ,request.headers.get("Authorization").split(' ')[1])
    try:
        user_id = get_jwt_identity()

        data = request.json

        check = check_user(user_id)
        
        if not check: return jsonify({"result": False, "message": "error happened, check data if correct"}), HTTPStatus.BAD_REQUEST
        post = PostSchema().load(data)

        post.user_id = user_id

        post.save()

        return PostSchema().jsonify(post), HTTPStatus.OK


    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.NOT_FOUND


@user.route("/post/<uuid:id>", methods=["PUT"])
@jwt_required
def put_post(id):

    user_id = get_jwt_identity()

    data = request.get_json()
    
    post= Post.query.filter_by(id=id).first()
    
    if post:

        if str(post.user_id) == user_id:

            serializer = PostSchema()

            Posts = serializer.dump(data)

            post_update = post.update(**Posts)

            return PostSchema().jsonify(post), HTTPStatus.OK

    return jsonify({"result": False}), HTTPStatus.NOT_FOUND


@user.route("/post/<uuid:id>", methods=["DELETE"])
@jwt_required
def delete_post(id):
    
    user_id = get_jwt_identity()

    post = Post.query.filter_by(id=id).first()

    if post:
        
        if str(post.user_id) == user_id:

            post.delete()
            return jsonify({"result": True}), HTTPStatus.OK

    return jsonify({"result": False}), HTTPStatus.NOT_FOUND