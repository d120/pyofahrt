from django.db import models
import bbcode

class FaqCategory(models.Model):
    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
class Question(models.Model):
    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    category = models.ForeignKey(FaqCategory, verbose_name="Kategorie")

    text = models.CharField("Frage", max_length=255)
    answer = models.TextField("Antwort")

    def __str__(self):
        return self.text

    def bbanswer(self):
        return bbcode.Parser().format(self.answer)        
