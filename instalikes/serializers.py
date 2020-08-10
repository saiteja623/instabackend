from rest_framework import serializers
from .models import (
    userProfile,
    customUser,
    post,
    commentsby,
    likedby,
    saved,
    FriendRequest,
    customUser,
    images,
)
from django.contrib.auth.models import User


class userprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = "__all__"
        depth = 1


class postSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = "__all__"


class commentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = commentsby
        fields = "__all__"


class likedbySerializer(serializers.ModelSerializer):
    class Meta:
        model = likedby
        fields = "__all__"


class savedSerializer(serializers.ModelSerializer):
    class Meta:
        model = saved
        fields = "__all__"
        depth = 1


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"
        depth = 2


class customUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = "__all__"
        depth = 1


class imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields = "__all__"


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

        def save(self):
            username = self.validated_data["username"]
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"username": "username exists"})
