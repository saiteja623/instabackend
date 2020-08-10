from django.contrib import admin
from django.urls import path
from instalikes import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("update_user", views.update_user, name="update_user"),
    path("homePage", views.homePage, name="homePage"),
    path("increaseLikes", views.increaseLikes, name="increaseLikes"),
    path("decreaseLikes", views.decreaseLikes, name="decreaseLikes"),
    path("checkForLike", views.checkForLike, name="checkForLike"),
    path("ajaxgetLikes", views.ajaxgetLikes, name="ajaxgetLikes"),
    path("send_request", views.send_request, name="send_request"),
    path("accept_request", views.accept_request, name="accept_request"),
    path("decline_request", views.decline_request, name="decline_request"),
    path("unsend_request", views.unsend_request, name="unsend_request"),
    path("friend_requests", views.friend_requests, name="friend_requests"),
    path("checkFriend", views.checkFriend, name="checkFriend"),
    path("remove_friend", views.remove_friend, name="remove_friend"),
    path(
        "update_userdesc_ajax", views.update_userdesc_ajax, name="update_userdesc_ajax"
    ),
    path("user_profile", views.homepage_user, name="homepage_user"),
    path("friend_requests", views.homepage_user, name="homepage_user"),
    path("homePage", views.homepage_user, name="homepage_user"),
    path("search_user", views.search_user, name="search_user"),
    path("create_post", views.create_post, name="create_post"),
    path("get_save_comment", views.get_save_comment, name="get_save_comment"),
    path("logout", views.logout, name="logout"),
    path("getuserprofile<str:username>", views.getuserprofile, name="getuserprofile"),
    path("getprofile", views.getprofile, name="getprofile"),
    path("is_user", views.is_user, name="is_user"),
    path("getPosts", views.getPosts, name="getPosts"),
    path("increaseLikes1<int:id>", views.increaseLikes1, name="increaseLikes1"),
    path("decreaseLikes1<int:id>", views.decreaseLikes1, name="decreaseLikes1"),
    path("checkForLike1<int:id>", views.checkForLike1, name="checkForLike1"),
    path("get_comments1<int:id>", views.get_comments1, name="get_comments1",),
    path(
        "save_comments1<int:id><str:comment>",
        views.save_comments1,
        name="save_comments1",
    ),
    path("delete_comments1<int:id>", views.delete_comments1, name="delete_comments1",),
    path("get_likes1<int:id>", views.get_likes1, name="get_likes1"),
    path("save_post<int:id>", views.save_post, name="save_post"),
    path("unsave_post<int:id>", views.unsave_post, name="unsave_post"),
    path("checkForSave<int:id>", views.checkForSave, name="checkForSave"),
    path("deletePost1<int:id>", views.deletePost1, name="deletePost1"),
    path(
        "update_user_desc1<str:username>",
        views.update_user_desc1,
        name=" update_user_desc1",
    ),
    path("get_saved_posts", views.get_saved_posts, name="get_saved_posts"),
    path("checkFriend1<str:username2>", views.checkFriend1, name="checkFriend1"),
    path("get_suggestions", views.get_suggestions, name="get_suggestions"),
    path("send_request1<str:username2>", views.send_request1, name="send_request1"),
    path(
        "unsend_request1<str:username2>", views.unsend_request1, name="unsend_request1"
    ),
    path(
        "get_friend_requests1", views.get_friend_requests1, name="get_friend_requests1",
    ),
    path(
        "get_user_friends<str:username>",
        views.get_user_friends,
        name="get_user_friends",
    ),
    path("upload_post1<str:username>", views.upload_post1, name="upload_post1"),
    path(
        "accept_request1<str:username2>", views.accept_request1, name="accept_request1"
    ),
    path(
        "delete_request1<str:username2>", views.delete_request1, name="delete_request1"
    ),
    path("remove_friend1<str:username2>", views.remove_friend1, name="remove_friend1"),
    path("update_user1<str:username>", views.update_user1, name="update_user1"),
    path("get_users/", views.usersAPIView.as_view()),
    path("get__numof_requests", views.get__numof_requests, name="get__numof_requests",),
    path("register_user", views.register_user, name="register_user"),
    path("login1", obtain_auth_token, name="login1"),
    path("send_otp<str:gmail>", views.send_otp, name="send_otp"),
    path("recover_otp<str:username>",views.recover_otp,name="recover_otp"),
    path("reset_pass<str:username>/<str:password>",views.reset_pass,name="reset_pass")
]
