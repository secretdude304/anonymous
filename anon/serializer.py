from rest_framework import serializers
from anon.models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ["id", 'title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ["postid", 'timestamp', "text"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username", "password"]


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = school
        fields = ["name"]
