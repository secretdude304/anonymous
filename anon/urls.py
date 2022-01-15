from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from anon import views

urlpatterns = [
    path('snippets/', views.PostList.as_view()),
    path('snippets/<int:pk>/', views.PostDetail.as_view()),
    path("comment/<int:pk>/", views.getcomment),
    path("comment/", views.postcomment)

]

urlpatterns = format_suffix_patterns(urlpatterns)
