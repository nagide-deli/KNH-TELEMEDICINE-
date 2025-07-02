from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class EducationalResource(models.Model):
    CATEGORY_CHOICES = [
        ('nutrition', 'Nutrition'),
        ('mental_health', 'Mental Health'),
        ('fitness', 'Fitness'),
        ('chronic_diseases', 'Chronic Disease'),
        ('feminine_health', 'Feminine Health'),
        ('general_health', 'General Health'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='educationalresources/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.title

class Question(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Answer to {self.question.title} by {self.doctor.first_name}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    resource = models.ForeignKey(EducationalResource, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.user.first_name}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.user.first_name} to {self.comment.id}'


# Create your models here.
