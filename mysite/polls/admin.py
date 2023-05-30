from django.contrib import admin

# Register your models here.

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    #reorder the fields:
    #fields = ["pub_date", "question_text"]

    # split the fields into fieldsets
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    

admin.site.register(Question, QuestionAdmin)
