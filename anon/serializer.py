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
        fields = ["email", "password", "username"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    """
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save
        return instance
     """


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = school
        fields = ["name"]
