from django.contrib import admin

# Register your models here.

from .models import Choice, Question

# ordinary display:
#class ChoiceInline(admin.StackedInline):
# compact display:
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #reorder the fields:
    #fields = ["pub_date", "question_text"]

    # split the fields into fieldsets
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
