from django.conf import settings
from django.db import models

class Genre(models.Model):
    name = models.CharField(default="other", max_length=100)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tests", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="test_images/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count_views = models.IntegerField(default=0)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.author}'

class Question(models.Model):
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE, null=True, blank=True)
    
    QUESTION_TYPES = [
        ("single_select", "Single select"),
        ("multi_select", "Multi select"),
        ("text_input", "Text input"),
        ("matching", "Matching"),
    ]
    
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=100)
    question_text = models.CharField(blank=False, null=False, max_length=1000)
    correct_val = models.FloatField()
    correct_text = models.CharField(max_length=255, blank=True, default="")
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']

# class TestQuestion(models.Model):
#     test = models.ForeignKey(Test, related_name="test_questions", on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, related_name="test_questions", on_delete=models.CASCADE)
#     order = models.IntegerField(default=1)


class Option(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    match_text = models.CharField(max_length=100, blank=True, default="")
    
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)


