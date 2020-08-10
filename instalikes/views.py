from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth, User
from mysite.settings import EMAIL_HOST_USER
from .models import (
    likedby,
    userProfile,
    customUser,
    FriendRequest,
    post,
    commentsby,
    saved,
    images,
)
from mysite import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
import datetime
from .serializers import (
    userprofileSerializer,
    imagesSerializer,
    postSerializer,
    customUserSerializer,
    commentsSerializer,
    likedbySerializer,
    savedSerializer,
    FriendRequestSerializer,
    userSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework import filters, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import random

# Create your views here.1


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session["user1"] = username
            return redirect("homePage")

        else:
            return render(request, "registertodo.html")
    else:
        if request.session.has_key("user1"):
            return redirect("homePage")
        else:
            return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        passw = request.POST["password"]
        passw1 = request.POST["password1"]
        email = request.POST["email"]
        if passw == passw1:
            if User.objects.filter(username=username).exists():
                return render(request, "registertodo.html")
            else:
                user1 = User.objects.create_user(
                    username=username, password=passw, email=email
                )
                user1.save()
                username = User.objects.get(username=username)
                ob = userProfile.objects.create(user=username)
                ob.save()
                ob2 = customUser.objects.create(user=username)
                ob2.save()
                return render(request, "login.html")
        else:
            return render(request, "registertodo.html")

    else:
        return render(request, "registertodo.html")


@login_required(login_url="login")
def homePage(request):
    posts = []
    l = post.objects.all().order_by("-created")
    username = request.session["user1"]
    user = User.objects.get(username=username)
    allusers = customUser.objects.exclude(id=user.customuser.id)
    for i in l:
        if i.user == user:
            posts.append(i)
        for k in user.customuser.friends.all():
            if i.user == k.user:
                posts.append(i)
    return render(
        request,
        "instalikes.html",
        {"posts": posts, "username": username, "user": user, "allusers": allusers,},
    )


@login_required(login_url="login")
def homepage_user(request, username):
    username_1 = request.session["user1"]
    user = User.objects.get(username=username_1)
    user2 = User.objects.get(username=username)
    if user.username == user2.username:
        return redirect("user_profile")
    else:
        num_of_friends = user2.customuser.friends.count()
        user3 = customUser.objects.get(id=user2.customuser.id)
        if FriendRequest.objects.filter(
            from_user=user.customuser.id, to_user=user3.id
        ).exists():
            friend = "requested"
        elif FriendRequest.objects.filter(
            from_user=user3.id, to_user=user.customuser.id
        ).exists():
            friend = "recieved"
        else:
            friend = "no"
        for i in user.customuser.friends.all():
            if i.user == user3.user:
                friend = "yes"
        if FriendRequest.objects.filter(
            from_user=user2.customuser.id, to_user=user.customuser.id
        ).exists():
            l = FriendRequest.objects.get(
                from_user=user2.customuser.id, to_user=user.customuser.id
            )
            frequestid = l.id
        else:
            frequestid = "none"
        posts = post.objects.filter(user=user2).order_by("-created")
        num_of_posts = post.objects.filter(user=user2).count()
        return render(
            request,
            "randomuser_profile.html",
            {
                "friend": friend,
                "posts": posts,
                "num_of_posts": num_of_posts,
                "num_of_friends": num_of_friends,
                "user2": user2,
                "frequestid": frequestid,
            },
        )


"""checks for friend using ajax when page loads"""


@login_required(login_url="login")
def checkFriend(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        id = int(request.POST.get("id"))
        user2 = customUser.objects.get(id=id)
        for i in user.customuser.friends.all():
            if i.user == user2.user:
                return JsonResponse({"friend": "yes"})
        if FriendRequest.objects.filter(
            from_user=user.customuser.id, to_user=user2.id
        ).exists():
            return JsonResponse({"friend": "requested"})
        else:
            return JsonResponse({"friend": "no"})


"""removes a friend by user"""


@login_required(login_url="login")
def remove_friend(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        user4 = customUser.objects.get(id=id)
        user1.friends.remove(user4)
        user4.friends.remove(user1)
        return JsonResponse({"status": "done"})


def increaseLikes(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        ob.likes = ob.likes + 1
        ob.save()
        user = request.session["user1"]
        liked_by = likedby(image=ob, name=user)
        liked_by.save()
        likes = ob.likes
        image = ob.image.url
        return JsonResponse({"likes": likes, "image": image})


def decreaseLikes(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        user = request.session["user1"]
        disliked = ob.likedby_set.get(name=user)
        disliked.delete()
        ob.likes = ob.likes - 1
        ob.save()
        likes = ob.likes
        image = ob.image.url
        return JsonResponse({"likes": likes, "image": image})


@login_required(login_url="login")
def checkForLike(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        user = request.session["user1"]
        if ob.likedby_set.filter(name=user).exists():
            return JsonResponse(
                {
                    "classname": "fas fa-heart",
                    "created": ob.created.date().strftime("%d %B,%Y"),
                    "day": ob.created.date().strftime("%d"),
                    "time": ob.created.time().strftime("%H"),
                    "exactTime": ob.created.time().strftime("%I:%M %p"),
                }
            )
        else:
            return JsonResponse(
                {
                    "classname": "far fa-heart",
                    "created": ob.created.date().strftime("%d %B,%Y"),
                    "day": ob.created.date().strftime("%d"),
                    "time": ob.created.time().strftime("%H"),
                    "minutes": ob.created.time().strftime("%M"),
                    "exactTime": ob.created.time().strftime("%I:%M %p"),
                }
            )


@login_required(login_url="login")
def ajaxgetLikes(request):
    if request.method == "POST":
        names = []
        images = []
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        usersLiked = ob.likedby_set.all()
        for i in usersLiked:
            user = User.objects.get(username=i.name)
            image = user.userprofile.image.url
            name = user.userprofile.name
            images.append(image)
            names.append(name)
        usersLiked = ob.likedby_set.all().values()
        return JsonResponse(
            {"usersLiked": list(usersLiked), "images": images, "names": names}
        )


@login_required(login_url="login")
def user_profile(request):
    username = request.session["user1"]
    user = User.objects.get(username=username)
    allfriends = user.customuser.friends.all()
    posts = post.objects.filter(user=user).order_by("-created")
    num_of_posts = post.objects.filter(user=user).count()
    num_of_friends = user.customuser.friends.count()
    return render(
        request,
        "profile.html",
        {
            "user": user,
            "num_of_friends": num_of_friends,
            "posts": posts,
            "allfriends": allfriends,
            "num_of_posts": num_of_posts,
        },
    )


@login_required(login_url="login")
def update_user(request):
    if request.method == "POST":
        username_changed = request.POST["username_changed"]
        username_before = request.session["user1"]
        user = User.objects.get(username=username_before)
        if (
            username_before != username_changed
            and User.objects.filter(username=username_changed).exists()
        ):
            allfriends = user.customuser.friends.all()
            return render(
                request,
                "profile.html",
                {
                    "user": user,
                    "allfriends": allfriends,
                    "message": "username already exists",
                },
            )
        else:
            email = request.POST["email"]
            name = request.POST["othername"]
            file = request.FILES.get("file_changed")
            if file is not None:
                user.userprofile.image = file
                user.userprofile.save()
            user.username = username_changed
            user.email = email
            user.userprofile.name = name
            user.userprofile.save()
            user.save()
            request.session["user1"] = username_changed
            return redirect("user_profile")


"""updates user bio from textarea via ajax when user clicks update-btn"""


@login_required(login_url="login")
def update_userdesc_ajax(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        desc = request.POST.get("bio")
        user.userprofile.desc = desc
        user.userprofile.save()
        return JsonResponse({"status": "done"})


@login_required(login_url="login")
def send_request(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        from_user = user.customuser
        to_user = customUser.objects.get(id=id)
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return HttpResponse("friend request sent")


@login_required(login_url="login")
def unsend_request(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        from_user = user.customuser
        to_user = customUser.objects.get(id=id)
        x = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        x.delete()
        return HttpResponse("friend request sent")


@login_required(login_url="login")
def accept_request(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        frequest = FriendRequest.objects.get(id=id)
        user2 = frequest.from_user
        user1.friends.add(user2)
        user2.friends.add(user1)
        ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
        ob.delete()
        return redirect("user_profile")


@login_required(login_url="login")
def decline_request(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        frequest = FriendRequest.objects.get(id=id)
        user2 = frequest.from_user
        ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
        ob.delete()
        return redirect("user_profile")


@login_required(login_url="login")
def friend_requests(request):
    username = request.session["user1"]
    user = User.objects.get(username=username)
    frequests = FriendRequest.objects.filter(to_user=user.customuser.id)
    return render(request, "frequests.html", {"frequests": frequests})


"""seach user using ajax"""


@login_required(login_url="login")
def search_user(request):
    if request.method == "POST":
        images = []
        names = []
        value = request.POST.get("user")
        users = User.objects.filter(username__startswith=value)
        for i in users:
            image = i.userprofile.image.url
            images.append(image)
            name = i.userprofile.name
            names.append(name)
        users = User.objects.filter(username__startswith=value).values()[:4]
        return JsonResponse({"users": list(users), "images": images, "names": names})


"""create post """


def create_post(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        image = request.FILES["image"]
        figcaption = request.POST.get("figcaption")
        x = post(user=user, image=image, figcaption=figcaption, username=username)
        x.save()
        return redirect("user_profile")
    else:
        return render(request, "post.html")


"""save or get the comment"""


def get_save_comment(request):
    if request.method == "POST":
        name = request.session["user1"]
        action = request.POST.get("action")
        if action == "save":
            id = int(request.POST.get("id"))
            comment = request.POST.get("comment")
            l = post.objects.get(id=id)
            x = commentsby.objects.create(image=l, name=name, comment=comment)
            x.save()
            return JsonResponse({"status": "done"})
        elif action == "get":
            images = []
            id = int(request.POST.get("id"))
            ob = post.objects.get(id=id)
            l = ob.commentsby_set.all()
            for i in l:
                user = User.objects.get(username=i.name)
                image = user.userprofile.image.url
                images.append(image)
            l = ob.commentsby_set.all().values()
            p = ob.likedby_set.all()
            liked = "no"
            for k in p:
                if name == k.name:
                    liked = "yes"
            return JsonResponse({"l": list(l), "images": images, "liked": liked})


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("login")


@api_view(["POST"])
def register_user(request):
    response = {}
    serializer = userSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
        )
        request.session["user1"] = request.data["username"]
        user.save()
        token = Token.objects.create(user=user)
        ob = userProfile.objects.create(user=user)
        ob.save()
        ob2 = customUser.objects.create(user=user)
        ob2.save()
        user1 = user.customuser
        if User.objects.filter(username="saiteja").exists():
            ob5 = User.objects.get(username="saiteja")
            user2 = ob5.customuser
            user1.friends.add(user2)
            user2.friends.add(user1)
        response["token"] = token.key
        response["username"] = user.username
        response["email"] = user.email
        response["type"] = "success"
    else:
        response["type"] = "error"
    return Response({"status": response})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def getuserprofile(request, username):
    user = User.objects.get(username=username)
    ob = user.userprofile
    serializer = userprofileSerializer(ob, many=False)
    num_of_friends = user.customuser.friends.count()
    num_of_posts = post.objects.filter(user=user).count()
    ob2 = post.objects.filter(user=user)
    post_serializer = postSerializer(ob2, many=True)
    details = []
    for i in ob2:
        detail = {
            "images": imagesSerializer(i.images_set.all(), many=True).data,
            "post": postSerializer(i, many=False).data,
        }
        details.append(detail)
    return Response(
        {
            "userdata": serializer.data,
            "num_of_friends": num_of_friends,
            "num_of_posts": num_of_posts,
            "details": details,
        }
    )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def getprofile(request):
    print(request.user)
    user = User.objects.get(username=request.user)
    ob = user.userprofile
    serializer = userprofileSerializer(ob, many=False)
    num_of_friends = user.customuser.friends.count()
    num_of_posts = post.objects.filter(user=user).count()
    ob2 = post.objects.filter(user=user)
    post_serializer = postSerializer(ob2, many=True)
    details = []
    for i in ob2:
        detail = {
            "images": imagesSerializer(i.images_set.all(), many=True).data,
            "post": postSerializer(i, many=False).data,
        }
        details.append(detail)
    return Response(
        {
            "userdata": serializer.data,
            "num_of_friends": num_of_friends,
            "num_of_posts": num_of_posts,
            "details": details,
        }
    )


@csrf_exempt
def is_user(request):
    if request.method == "POST":
        randomuser = request.POST.get("randomuser")
        exuser = User.objects.get(username=randomuser)
        user = customUser.objects.get(id=exuser.customuser.id)
        username = request.POST.get("username")
        loguser = User.objects.get(username=username)
        if FriendRequest.objects.filter(
            from_user=loguser.customuser.id, to_user=user.id
        ).exists():
            friend = "requested"
        elif FriendRequest.objects.filter(
            from_user=user.id, to_user=loguser.customuser.id
        ).exists():
            friend = "recieved"
        else:
            friend = "Add friend"
        for i in loguser.customuser.friends.all():
            if i.user == user.user:
                friend = "friends"
        return JsonResponse({"friend": friend})


"""
@api_view(["GET"])

@permission_classes((IsAuthenticated,))
def getPosts(request):
    posts = []
    l = post.objects.all().order_by("-created")
    username=request.user

    user = User.objects.get(username=username)
    for i in l:
        if i.user == user:
            o = {
                "details": postSerializer(i, many=False).data,
                "username": user.username,
                "profilepic": user.userprofile.image.url,
            }
            posts.append(o)
        for k in user.customuser.friends.all():
            if i.user == k.user:
                o = {
                    "details": postSerializer(i, many=False).data,
                    "username": k.user.username,
                    "profilepic": k.user.userprofile.image.url,
                }
                posts.append(o)
    return Response({"posts": posts})

"""


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def decreaseLikes1(request, id):
    ob = post.objects.get(id=id)
    user = request.user
    if ob.likedby_set.filter(name=user).exists():
        disliked = ob.likedby_set.get(name=user)
        disliked.delete()
        ob.likes = ob.likes - 1
        ob.save()
        likes = ob.likes
        image = ob.image.url
        return Response({"likes": likes, "image": image})
    else:
        return Response({"res": "no"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def increaseLikes1(request, id):
    ob = post.objects.get(id=id)
    ob.likes = ob.likes + 1
    ob.save()
    user = request.user
    liked_by = likedby(image=ob, name=user)
    liked_by.save()
    likes = ob.likes
    image = ob.image.url
    return Response({"likes": likes, "image": image})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def checkForLike1(request, id):
    ob = post.objects.get(id=id)
    user = request.user
    if ob.likedby_set.filter(name=user).exists():
        return Response({"liked": "yes"})
    else:
        return Response({"liked": "no"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_comments1(request, id):
    images = []
    ob = post.objects.get(id=id)
    l = ob.commentsby_set.all()
    for i in l:
        user = User.objects.get(username=i.name)
        o = {
            "comment": commentsSerializer(i, many=False).data,
            "profilepic": user.userprofile.image.url,
        }
        images.append(o)
    return Response({"comments": images})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_comments1(request, id, comment):
    name = request.user
    l = post.objects.get(id=id)
    x = commentsby.objects.create(image=l, name=name, comment=comment)
    x.save()
    return Response({"status": "done"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def delete_comments1(request, id):
    x = commentsby.objects.get(id=id)
    x.delete()
    return Response({"status": "deleted"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_likes1(request, id):
    liked = []
    ob = post.objects.get(id=id)
    usersLiked = ob.likedby_set.all()
    for i in usersLiked:
        user = User.objects.get(username=i.name)
        o = {
            "likedby": likedbySerializer(i, many=False).data,
            "userDetails": userprofileSerializer(user.userprofile, many=False).data,
        }
        liked.append(o)
    return Response({"liked": liked})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_post(request, id):
    username = request.user

    user = User.objects.get(username=username)
    postob = post.objects.get(id=id)
    l = saved.objects.create(user=user, post=postob)
    l.save()
    return Response({"status": "done"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def unsave_post(request, id):
    username = request.user

    user = User.objects.get(username=username)
    postob = post.objects.get(id=id)
    l = saved.objects.filter(post=postob, user=user)
    l.delete()
    return Response({"status": "done"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def checkForSave(request, id):
    user = User.objects.get(username=request.user)
    postob = post.objects.get(id=id)
    if saved.objects.filter(user=user, post=postob).exists():
        return Response({"isSaved": "true"})
    else:
        return Response({"isSaved": "false"})


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def deletePost1(request, id):
    postob = post.objects.get(id=id)
    postob.delete()
    return Response({"status": "done"})


@csrf_exempt
def update_user_desc1(request, username):
    if request.method == "POST":
        username = request.user
        user = User.objects.get(username=username)
        desc = request.POST.get("bio")
        print("bio is", desc)
        if desc != "":
            user.userprofile.desc = desc
            user.userprofile.save()
            return JsonResponse({"status": "done"})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_saved_posts(request):
    savedlist = []
    ob = User.objects.get(username=request.user)
    savedob = saved.objects.filter(user=ob)
    for i in savedob:
        x = userProfile.objects.get(user=i.user)
        o = {
            "profilepic": x.image.url,
            "details": {
                "images": imagesSerializer(i.post.images_set.all(), many=True).data,
                "post": postSerializer(i.post, many=False).data,
            },
        }
        savedlist.append(o)
    return Response({"saved": savedlist})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def checkFriend1(request, username2):
    x = User.objects.get(username=username2)
    username = request.user

    user = User.objects.get(username=username)
    user2 = x.customuser
    for i in user.customuser.friends.all():
        if i.user.username == user2.user.username:
            return Response({"friend": "yes"})
    if FriendRequest.objects.filter(
        from_user=user.customuser.id, to_user=user2.id
    ).exists():
        return Response({"friend": "requested"})
    else:
        return Response({"friend": "no"})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_suggestions(request):
    username = request.user

    ob = userProfile.objects.exclude(user=User.objects.get(username=username))
    serializer = userprofileSerializer(ob, many=True)
    return Response({"suggestions": serializer.data})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def send_request1(request, username2):
    user2 = User.objects.get(username=username2)
    id = user2.customuser.id
    username = request.user

    user = User.objects.get(username=username)
    from_user = user.customuser
    to_user = customUser.objects.get(id=id)
    FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    return Response({"status": "sent"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def unsend_request1(request, username2):
    user2 = User.objects.get(username=username2)
    username = request.user

    user = User.objects.get(username=username)
    from_user = user.customuser
    to_user = user2.customuser
    x = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
    x.delete()
    return Response({"status": "deleted"})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_friend_requests1(request):
    lists = []
    user = User.objects.get(username=request.user)
    frequests = FriendRequest.objects.filter(to_user=user.customuser.id)
    for i in frequests:
        user = i.from_user.user.userprofile
        o = {"details": userprofileSerializer(user, many=False).data}
        lists.append(o)
    return Response({"requests": lists})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user_friends(request, username):
    friendslist = []
    user = User.objects.get(username=username)
    friends = user.customuser.friends.all()
    for i in friends:
        x = i.user.userprofile
        o = {
            "friend-details": userprofileSerializer(x, many=False).data,
        }
        friendslist.append(o)
    return Response({"friends": friendslist})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getPosts(request):
    posts = []
    l = post.objects.all().order_by("-created")
    username = request.user

    user = User.objects.get(username=username)
    for i in l:
        if i.user == user:
            o = {
                "details": {
                    "images": imagesSerializer(i.images_set.all(), many=True).data,
                    "post": postSerializer(i, many=False).data,
                },
                "username": user.username,
                "profilepic": user.userprofile.image.url,
            }
            posts.append(o)
        for k in user.customuser.friends.all():
            if i.user == k.user:
                o = {
                    "details": {
                        "images": imagesSerializer(i.images_set.all(), many=True).data,
                        "post": postSerializer(i, many=False).data,
                    },
                    "username": k.user.username,
                    "profilepic": k.user.userprofile.image.url,
                }
                posts.append(o)
    return Response({"posts": posts})


@csrf_exempt
def upload_post1(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        length = int(request.POST.get("length"))
        figcaption = request.POST.get("caption")
        x = post(user=user, figcaption=figcaption, username=username)
        x.save()
        for i in range(0, length):
            image = request.FILES.get("images[" + str(i) + "]")
            l = images.objects.create(post=x, image=image)
            l.save()
        return JsonResponse({"dd": "dd"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def accept_request1(request, username2):
    username = request.user
    user = User.objects.get(username=username)
    user1 = user.customuser
    x = User.objects.get(username=username2)
    user2 = x.customuser
    user1.friends.add(user2)
    user2.friends.add(user1)
    ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
    ob.delete()
    return Response({"status": "done"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def delete_request1(request, username2):
    username = request.user
    user = User.objects.get(username=username)
    user1 = user.customuser
    x = User.objects.get(username=username2)
    user2 = x.customuser
    ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
    ob.delete()
    return Response({"status": "done"})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def remove_friend1(request, username2):
    x = User.objects.get(username=username2)
    user2 = x.customuser
    user1 = User.objects.get(username=request.user)
    user1 = user1.customuser
    user2.friends.remove(user1)
    user1.friends.remove(user2)
    return Response({"status": "done"})


@csrf_exempt
def update_user1(request, username):
    if request.method == "POST":
        username_before = username
        user = User.objects.get(username=username_before)
        username_changed = request.POST.get("username")
        nickname = request.POST.get("nickname")
        profilepic = request.FILES.get("image")
        if username_changed != username_before:
            if User.objects.filter(username=username_changed).exists():
                return JsonResponse({"status": "username"})
            else:
                user.username = username_changed
                user.save()
        email = request.POST.get("email")
        if profilepic is not None:
            user.userprofile.image = profilepic
            user.userprofile.save()
        user.email = email
        user.userprofile.name = nickname
        user.userprofile.save()
        user.save()
        return JsonResponse({"status": "done"})


class usersAPIView(generics.ListCreateAPIView):
    search_fields = ["^user__username"]
    filter_backends = (filters.SearchFilter,)
    queryset = userProfile.objects.all()
    serializer_class = userprofileSerializer


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get__numof_requests(request):
    user = User.objects.get(username=request.user)
    count = FriendRequest.objects.filter(to_user=user.customuser).count()
    return Response({"requests": count})


@csrf_exempt
def send_otp(request, gmail):
    s = random.randint(111111, 999999)
    subject = "Email Verification"
    otp = str(s)
    message = (
        "Hi someone tried to sign up for an Instagram account with "
        + gmail
        + ".If it was you then enter the OTP "
        + otp
        + " to sign up. Note: keep the OTP confidential"
    )
    send_mail(subject, message, EMAIL_HOST_USER, [gmail], fail_silently=False)
    return JsonResponse({"otp": otp})


@csrf_exempt
def recover_otp(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        gmail = user.email
        s = random.randint(111111, 999999)
        subject = "Password Recovery"
        otp = str(s)
        message = (
            "Hi someone tried to sign up for an Instagram account with "
            + gmail
            + ".If it was you then enter the OTP "
            + otp
            + " to sign up. Note: keep the OTP confidential"
        )
        send_mail(subject, message, EMAIL_HOST_USER, [gmail], fail_silently=False)
        return JsonResponse({"status": "done", "otp": otp})
    else:
        return JsonResponse({"status": "error"})


@csrf_exempt
def reset_pass(request, username, password):
    if request.method == "POST":
        print("username", username)
        print("password", password)
        user = User.objects.get(username=username)
        print(user)
        user.set_password(password)
        user.save()
        return JsonResponse({"status": "done"})

