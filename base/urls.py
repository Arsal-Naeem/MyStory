from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("stories/", views.stories, name='stories'),
    path("register/", views.registerUser, name='register'),
    path("login/", views.loginUser, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("user/<str:username>/", views.user, name='user'),
    path("user/<str:username>/<str:id>/", views.story, name='story'),
    path("editor/", views.storyWriter, name='editor'),
    path("user/<str:username>/<str:pk>/editor/", views.storyEditor, name='editor'),
    path("user/<str:username>/<str:pk>/delete/", views.storyDeleter, name='deleter')
]