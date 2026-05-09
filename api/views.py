from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
 
from .models import Chat, Message, Answer
from .serializers import MessageInputSerializer, MessageResponseSerializer
 
 
def mock_sgm_model(text_input: str) -> dict:
    text_lower = text_input.lower()
 
    if "vacation" in text_lower or "leave" in text_lower or "day off" in text_lower:
        slot = "Unknown"
        days = ["monday", "tuesday", "wednesday", "thursday", "sunday", "saturday", "friday"]
        for day in days:
            if day in text_lower:
                slot = day.capitalize()
                break
        return {"intent": "Leave_Request", "slot": slot}
 
    if "laptop" in text_lower or "computer" in text_lower or "screen" in text_lower:
        return {"intent": "Report_IT_Issue", "slot": "Hardware"}
 
    if "password" in text_lower or "access" in text_lower or "login" in text_lower:
        return {"intent": "Report_IT_Issue", "slot": "Access"}
 
    return {"intent": "Unknown", "slot": "None"}
 
 
def build_system_reply(ai_result: dict) -> str:
    intent = ai_result.get("intent")
    slot   = ai_result.get("slot")
 
    if intent == "Leave_Request":
        if slot and slot != "Unknown":
            return (
                f"✅ Your leave request starting on {slot} has been submitted to HR. "
                f"You will receive a confirmation email within 24 hours."
            )
        return (
            "✅ Your leave request has been received by HR. "
            "Could you also specify which day you'd like to start?"
        )
 
    if intent == "Report_IT_Issue":
        if slot == "Hardware":
            return (
                "🖥️ A hardware support ticket has been opened for you (Ticket #IT-{auto}). "
                "An IT technician will contact you within 4 business hours."
            )
        if slot == "Access":
            return (
                "🔐 An access/credentials issue has been reported. "
                "IT Security will reset your account within 1 business hour."
            )
        return (
            "🛠️ Your IT issue has been logged. "
            "The support team will follow up with you shortly."
        )
 
    return (
        "🤖 I'm sorry, I didn't quite understand that. "
        "I can help with leave requests or IT issues. Could you rephrase?"
    )
 
 
class MessageView(APIView):
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        input_serializer = MessageInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(
                {"errors": input_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        validated = input_serializer.validated_data
        content   = validated["content"]
        chat_id   = validated.get("chat_id")
 
        try:
            if chat_id:
                chat = Chat.objects.get(chat_id=chat_id, user=request.user)
            else:
                chat = Chat.objects.create(user=request.user)
        except Chat.DoesNotExist:
            return Response(
                {"error": "Chat session not found or does not belong to you."},
                status=status.HTTP_404_NOT_FOUND
            )
 
        message = Message.objects.create(chat=chat, content=content)
 
        ai_result = mock_sgm_model(content)
 
        reply_text = build_system_reply(ai_result)
 
        answer = Answer.objects.create(
            message=message,
            content=reply_text,
            status=Answer.Status.SUCCESS
        )
 
        response_serializer = MessageResponseSerializer(
            message,
            context={"ai_result": ai_result}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
 
 
class CloseChatView(APIView):
    permission_classes = [IsAuthenticated]
 
    def patch(self, request, chat_id):
        try:
            chat = Chat.objects.get(chat_id=chat_id, user=request.user)
        except Chat.DoesNotExist:
            return Response(
                {"error": "Chat session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
 
        if chat.end_time:
            return Response(
                {"error": "This chat session is already closed."},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        chat.end_time = timezone.now()
        chat.save(update_fields=["end_time"])
        return Response(
            {"message": "Chat session closed.", "end_time": chat.end_time},
            status=status.HTTP_200_OK
        )

class ClearHistoryView(APIView):
    """
    FR-11: The system shall support a 'Clear History' option.
    This endpoint allows a user to delete all messages inside a specific chat session.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, chat_id):
        try:
            chat = Chat.objects.get(chat_id=chat_id, user=request.user)
            
            Message.objects.filter(chat=chat).delete()
            
            return Response(
                {"status": "success", "message": "Chat history successfully cleared."},
                status=status.HTTP_200_OK
            )
        except Chat.DoesNotExist:
            return Response(
                {"error": "Chat session not found or you do not have permission."},
                status=status.HTTP_404_NOT_FOUND
            )