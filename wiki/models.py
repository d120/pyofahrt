from django.db import models
from django.core.urlresolvers import reverse_lazy

# Create your models here.
class Article(models.Model):
    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"

        permissions = (
            ("can_use", "Wikikomponente nutzen"),
        )

    def __str__(self):
        return self.title

    title = models.CharField("Titel", max_length=255, primary_key=True)



class ArticleVersion(models.Model):
    class Meta:
        verbose_name = "Artikelversion"
        verbose_name_plural = "Artikelversionen"

    def get_absolute_url(self):
        return reverse_lazy("wiki:show", kwargs={'pk': self.article.title})

    def __str__(self):
        return self.article.title + " (" + self.timestamp.strftime("%A %d. %B %Y - %H:%M:%S") + "): " + self.text[:250]


    article = models.ForeignKey(Article, verbose_name="Zugehöriger Artikel")
    text = models.TextField("Text")
    timestamp = models.DateTimeField("Zeitstempel")
