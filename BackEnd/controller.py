from flask import request, jsonify, abort
from session import SESSION
from uuid import uuid4


def healthcheck():
    return 'It Works!'



def login():
    input_value = request.get_json()
    if 'username' not in input_value:
        abort(400, {'message': 'USERNAME_NOT_FOUND'})
    elif 'password' not in input_value:
        abort(400, {'message': 'PASSWORD_NOT_FOUND'})
    from model import User
    user = User.where(username=input_value['username']).first()
    if user is None:
        abort(400, {'message': 'INVALID_USERNAME'})
    elif user.password != input_value['password']:
        abort(400, {'message': 'INVALID_PASSWORD'})
    uuid = str(uuid4())
    SESSION[uuid] = user
    response_body = {
        'session_id': uuid,
        'username': user.username,
    }
    return jsonify(response_body)

def logout():
    session_id = request.headers.get('Authorization')
    if session_id and session_id in SESSION:
        del SESSION[session_id]
    return jsonify({'message': 'TOKEN_INVALIDATED'})

def register():
    input_data = request.get_json()
    if 'username' not in input_data:
        abort(400, {'message': 'USERNAME_NOT_FOUND'})
    elif 'password' not in input_data:
        abort(400, {'message': 'PASSWORD_NOT_FOUND'})
    from model import User
    if User.where(username=input_data['username']).first() is not None:
        abort(400, {'message': 'USERNAME_ALREADY_EXISTS'})
    user = User.create(
        username=input_data['username'],
        email=input_data['email'],
        mobile=input_data['mobile'],
        password=input_data['password'],
    )
    uuid = str(uuid4())
    SESSION[uuid] = user
    response_body = {
        'session_id': uuid,
        'username': user.username,
    }
    return jsonify(response_body)



def list_posts():
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import User
    posts_response = []
    for post in User.find(user.id).posts:
        posts_response.append({
            'id': post.id,
            'content': post.content
        })
    return jsonify(posts_response)

def create_post():
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    input_data = request.get_json()
    from model import Post
    post = Post()
    post.user_id = user.id
    post.content = input_data['content']
    post.save()
    return jsonify(post.to_dict())

def get_post(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Post
    post_exist = Post.find(post_id)   
    if post_exist is None:
        abort(400, {'message': 'POST_NOT_FOUND'})
    posts_response = {
        'content': post_exist.content
    }
    return jsonify(posts_response)

def update_post(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    input_data = request.get_json()
    from model import Post
    post_exist = Post.find(post_id)       
    if post_exist is None:
        abort(400, {'message': 'POST_NOT_FOUND'})
    post_exist.content = input_data['content']
    post_exist.save()
    return jsonify(post_exist.to_dict())

def delete_post(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Post
    post_exist = Post.find(post_id)   
    if post_exist is None:
        abort(400, {'message': 'POST_NOT_FOUND'})
    post_exist.delete()
    return "DELETED"

def get_comments(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Comment, Post
    p = Post.find(post_id)   
    s = p.comments
    if p is None:
        abort(400, {'message': 'COMMENT_NOT_FOUND'})
    comments_response = []
    for i in s:
        print(i.body)
        comments_response.append({
            'comment' : i.body
            })
    return jsonify(comments_response)

def create_comment(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    input_data = request.get_json()
    from model import Comment, Post   
    post_exist = Post.find(post_id)
    if post_exist is None:
        abort(400, {'message','POST_NOT_FOUND'})
    comment = Comment()
    comment.post_id = post_id
    comment.user_id = user.id
    comment.body = input_data['body']
    comment.save()
    return jsonify("Created.")

def delete_comment(post_id, comment_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Comment
    comment_exist = Comment.find(comment_id)   
    if comment_exist is None:
        abort(400, {'message': 'COMMENT_NOT_FOUND'})
    comment_exist.delete()
    return "DELETED"    
    # return jsonify()



def get_likes(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Like, Post
    p = Post.find(post_id)   
    s = p.likes
    if p is None:
        abort(400, {'message': 'NO_LIKES_FOUND'})
    likes_response = []
    for i in s:
        print(i.user_id)
        likes_response.append({
            'user' : i.user_id
            })
    return jsonify(likes_response)

 
def create_like(post_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    # input_data = request.get_json()
    from model import Like, Post   
    post_exist = Post.find(post_id)
    if post_exist is None:
        abort(400, {'message','POST_NOT_FOUND'})
    like = Like()
    like.post_id = post_id
    like.user_id = user.id
    like.save()
    return "Liked."

def delete_like(post_id, like_id):
    user = SESSION.get(request.headers.get('Authorization'))
    if user is None:
        abort(400, {'message': 'TOKEN_NOT_FOUND'})
    from model import Like
    like_exist = Like.find(like_id)   
    if like_exist is None:
        abort(400, {'message': 'NOT_YET_LIKED'})
    like_exist.delete()
    return jsonify("Deleted")
    
