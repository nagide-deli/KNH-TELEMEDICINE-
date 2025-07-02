import json
from django.db import models
from django.conf import settings

class GoogleCredentials(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='google_credentials'
    )
    token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()  # JSON-encoded list
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google creds for {self.user.email}"

    def get_scopes(self):
        return json.loads(self.scopes)
