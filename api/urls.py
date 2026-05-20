from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    MessageView,
    CloseChatView,
    ClearHistoryView,
    RegisterView,
    ChatListView,
    ChatMessagesView,
    MeView,
)

app_name = "api"

urlpatterns = [
    path("message/", MessageView.as_view(), name="send_message"),
    path("chat/<uuid:chat_id>/close/", CloseChatView.as_view(), name="close_chat"),
    path("chat/<uuid:chat_id>/clear/", ClearHistoryView.as_view(), name="clear_history"),
    path("chat/<uuid:chat_id>/messages/", ChatMessagesView.as_view(), name="chat_messages"),
    path("chats/", ChatListView.as_view(), name="list_chats"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
]