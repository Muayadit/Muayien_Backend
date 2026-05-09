from .views import MessageView, CloseChatView, ClearHistoryView

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MessageView, CloseChatView
 
app_name = "api"
 
urlpatterns = [
    path(
        "message/",
        MessageView.as_view(),
        name="send_message"
    ),
 
    path(
        "chat/<uuid:chat_id>/close/",
        CloseChatView.as_view(),
        name="close_chat"
    ),
 
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
 
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    path(
        "chat/<uuid:chat_id>/clear/",
        ClearHistoryView.as_view(),
        name="clear_history"
    ),
]