from django.contrib import admin
from django.urls import path, include
from api.views import RegisterView
from api.views import ChatListView, ChatMessagesView, MeView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('api.urls')),

    path("register/", RegisterView.as_view(), name="register"),

    path("chats/", ChatListView.as_view(), name="list_chats"),

    path("chat/<uuid:chat_id>/messages/", ChatMessagesView.as_view(), name="chat_messages"),

    path("me/", MeView.as_view(), name="me"),
]

