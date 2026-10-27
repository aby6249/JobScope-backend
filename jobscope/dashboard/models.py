from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserActivity(models.Model):

    ACTIVITY_TYPE = (

        ("platform", "Platform"),

        ("resume", "Resume Tool"),

        ("community", "Community"),

    )


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )


    activity_type = models.CharField(

        max_length=20,

        choices=ACTIVITY_TYPE

    )


    object_id = models.IntegerField()

    visited_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return f"{self.user} - {self.activity_type}"