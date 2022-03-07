from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from anon import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('snippets/', views.PostList.as_view()),
    path('snippets/<int:pk>/', views.PostDetail.as_view()),
    path("comment/<int:pk>/", views.getcomment),
    path("comment/", views.postcomment),
    path("register/", views.RegisterView.as_view()),
    #path("login/", views.LoginView.as_view()),
    #path("user/", views.UserView.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("verifyschool/", views.VerifySchool),
    path("getinfofromtoken/", views.tokenwithinfo),
]

urlpatterns = format_suffix_patterns(urlpatterns)
