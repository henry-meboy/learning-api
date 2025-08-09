from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.text[:75] + '...') if len(self.text) > 75 else self.text
