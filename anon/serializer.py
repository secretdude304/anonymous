from rest_framework import serializers
from anon.models import *


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ["id", 'title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ["postid", 'timestamp', "text"]
