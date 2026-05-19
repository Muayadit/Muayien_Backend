from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Message, Answer, Chat, User


class MessageInputSerializer(serializers.Serializer):
    content = serializers.CharField(
        min_length=1,
        max_length=2000,
        trim_whitespace=True,
        error_messages={
            "blank":      "Message content cannot be empty.",
            "max_length": "Message cannot exceed 2000 characters.",
        }
    )
    chat_id = serializers.UUIDField(required=False, allow_null=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["anw_id", "content", "status", "timestamp"]


class MessageResponseSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(read_only=True)
    ai_metadata = serializers.SerializerMethodField()

    def get_ai_metadata(self, obj):
        return self.context.get("ai_result", {})

    class Meta:
        model = Message
        fields = ["msg_id", "content", "timestamp", "chat_id", "answer", "ai_metadata"]


class ChatSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source="messages.count", read_only=True)

    class Meta:
        model = Chat
        fields = ["chat_id", "start_time", "end_time", "message_count"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "first_name", "last_name"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)