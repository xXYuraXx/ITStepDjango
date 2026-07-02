from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)

class Genre(models.Model):
    name = models.CharField(default="other", max_length=100)

class Test(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="tests", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count_views = models.IntegerField(default=0)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.author}'

class Question(models.Model):
    QUESTION_TYPES = [
        ("single_select", "Single select"),
        #("multy_select", "Multy select"),
    ]
    
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=100)
    question_text = models.CharField(blank=False, null=False, max_length=1000)
    correct_val = models.FloatField()
    
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
    
class Option(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)


