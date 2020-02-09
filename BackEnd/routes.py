from controller import healthcheck, login, logout, register, list_posts, create_post, get_post, update_post, delete_post, get_comments, create_comment, delete_comment, get_likes, create_like, delete_like

ROUTES = [
    ('GET', '/', healthcheck),

    ('POST', '/login', login),
    ('DELETE', '/logout', logout),
    ('POST', '/register', register),

    ('GET', '/posts', list_posts),
    ('POST', '/posts', create_post),
    ('GET', '/posts/<int:post_id>', get_post),
    ('PUT', '/posts/<int:post_id>', update_post),
    ('DELETE', '/posts/<int:post_id>', delete_post),

    ('GET', '/posts/<int:post_id>/comments', get_comments),
    ('POST', '/posts/<int:post_id>/comments',  create_comment),
    ('DELETE', '/posts/<int:post_id>/comments/<int:comment_id>', delete_comment),

    ('GET', '/posts/<int:post_id>/likes', get_likes),
    ('POST', '/posts/<int:post_id>/likes', create_like),
    ('DELETE', '/posts/<int:post_id>/likes/<int:like_id>', delete_like),

]