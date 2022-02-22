from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from anon.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from anon.serializer import PostSerializer, UserSerializer
from anon.serializer import CommentSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
import json


class PostList(APIView):

    def get(self, request, format=None):
        posts = post.objects.all()
        posts = posts[::-1]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):

    def get_object(self, pk):
        try:
            return post.objects.get(pk=pk)
        except post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        posts = self.get_object(pk)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def postcomment(request):
    print(request)
    serializer = CommentSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# gets comment given id


@api_view(['GET'])
def getcomment(request, pk):
    comments = comment.objects.filter(postid=pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def VerifySchool(request):
    data = request.data
    email = data['email']
    sliced = email[email.index("@")+1:]
    slicedagain = sliced[0:sliced.index(".")]
    print(slicedagain)
    allschools = school()
    userschool = school.objects.filter(emailSegment=slicedagain)
    schoollist = []
    for userscho in userschool:
        schoollist.append(userscho.name)
    print(schoollist)
    schoollists = json.dumps(schoollist)

    """
    sliced = data[data.index("@")+1:]
    slicedagain = sliced[0:sliced.index(".")]
    print(slicedagain)
    allschools = school()
    userschool = allschools.filter(name=slicedagain)
    """
    print(schoollists)

    return Response(schoollists, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save
