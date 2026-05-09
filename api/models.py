import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
 
 
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
 
 
class User(AbstractBaseUser, PermissionsMixin):
    user_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
 
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
 
    objects = UserManager()
 
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
 
    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
 
    class Meta:
        verbose_name = "User"
        db_table     = "users"
 
 
class Chat(models.Model):
    chat_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time   = models.DateTimeField(null=True, blank=True)
 
    def __str__(self):
        return f"Chat {self.chat_id} — {self.user.email}"
 
    class Meta:
        verbose_name = "Chat"
        db_table     = "chats"
        ordering     = ["-start_time"]
 
 
class Message(models.Model):
    msg_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat      = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Message {self.msg_id} in Chat {self.chat_id}"
 
    class Meta:
        verbose_name = "Message"
        db_table     = "messages"
        ordering     = ["timestamp"]
 
 
class Answer(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        ERROR   = "error",   "Error"
        PENDING = "pending", "Pending"
 
    anw_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message   = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name="answer"
    )
    content   = models.TextField()
    status    = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SUCCESS
    )
    timestamp = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Answer to Message {self.message_id} [{self.status}]"
 
    class Meta:
        verbose_name = "Answer"
        db_table     = "answers"