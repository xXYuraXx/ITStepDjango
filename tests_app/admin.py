from django.contrib import admin
from tests_app.models import Genre, Option, Question, Test

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Genre)
