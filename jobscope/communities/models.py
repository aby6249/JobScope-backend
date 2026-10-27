from django.db import models
from django.conf import settings


class Community(models.Model):

    name = models.CharField(max_length=255)

    bio = models.TextField()

    logo = models.ImageField(upload_to='community_logos/',null=True,blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    
    reason = models.TextField()
  
    is_approved = models.BooleanField(default=False)

    is_admin_only = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.name



class Membership(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    community = models.ForeignKey(Community,on_delete=models.CASCADE)

    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='member')

    is_blocked = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)


    class Meta:

        unique_together = ['user', 'community']


    def __str__(self):

        return f"{self.user} - {self.community}"



class Message(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE
    )

    content = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="chat_images/",
        null=True,
        blank=True
    )

    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        if self.content:
            return f"{self.user}: {self.content[:30]}"

        return f"{self.user} sent image in {self.community}"




class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    related_community = models.ForeignKey(
        Community,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"{self.user} - {self.message[:40]}"
    


class Comment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):

        return f"{self.user} -> message {self.message.id}"



class CommentLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ["user", "comment"]

    def __str__(self):

        return f"{self.user} liked {self.comment.id}"