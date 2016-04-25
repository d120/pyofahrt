from django.contrib import admin
from .models import Question, FaqCategory

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('text', 'category')
    pass


@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    pass
