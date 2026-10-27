from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ResumeTool(models.Model):

    name = models.CharField(max_length=200)

    website_url = models.URLField()

    description = models.TextField(blank=True)

    logo = models.ImageField(upload_to="resume_tools/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ResumeToolReview(models.Model):

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tool = models.ForeignKey(
        ResumeTool,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(choices=RATING_CHOICES)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.tool}"


class ResumeToolReaction(models.Model):

    REACTION_CHOICES = [
        ("good", "Good"),
        ("bad", "Bad"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tool = models.ForeignKey(ResumeTool,on_delete=models.CASCADE,related_name="reactions")

    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tool")