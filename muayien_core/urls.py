from django.contrib import admin
from django.urls import path, include
from api.views import RegisterView, CloseChatView, ClearHistoryView
from api.views import ChatListView, ChatMessagesView, MeView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('api.urls')),

    path("register/", RegisterView.as_view(), name="register"),

    path("chats/", ChatListView.as_view(), name="list_chats"),

    path("chat/<uuid:chat_id>/close/", CloseChatView.as_view(), name="close_chat"),
    
    path("chat/<uuid:chat_id>/clear/", ClearHistoryView.as_view(), name="clear_history"),

    path("chat/<uuid:chat_id>/messages/", ChatMessagesView.as_view(), name="chat_messages"),

    path("me/", MeView.as_view(), name="me"),
]

