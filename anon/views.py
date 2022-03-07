from collections import UserDict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from anon.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
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
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt


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
    print(data)
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView, MyTokenObtainPairSerializer):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = request.data['username']
        users = User.objects.get(username=username)
        refresh = self.get_token(users)
        refreshtok = refresh
        print(refreshtok)
        access = refresh.access_token
        print(access)
        payload = {
            "refreshtoken": str(refreshtok),
            "accesstoken": str(access)
        }
        print(payload)

        return Response({
            "refreshtoken": str(refreshtok),
            "accesstoken": str(access)
        })


@api_view(['POST'])
def tokenwithinfo(request):
    print(request.headers)


"""



class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').encode('utf-8')

        return Response({
            'jwt': token
        })


class UserView(APIView):
    def post(self, request):
        token = request.data["jwt"]

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired token')
        user = User.objects.filter(id=payload[id]).first()

        serializer = UserSerializer(user)
        return Response(serializer.data)
"""
