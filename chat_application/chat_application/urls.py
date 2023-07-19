"""
URL configuration for chat_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from chatapp.views import UserRegistrationView, UserLoginView, SendMessageAPIView, SendGroupMessageAPIView, UserReceivedMessagesAPIView, UserReceivedGroupMessagesAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('sendmessage/', SendMessageAPIView.as_view()),
    path('sendgroupmessage/', SendGroupMessageAPIView.as_view()),
    path('messages/<str:sender>/<str:receiver>', UserReceivedMessagesAPIView.as_view()),
    path('groupmessages/<str:receiver>/<str:groupname>', UserReceivedGroupMessagesAPIView.as_view()),
    
    
]


