from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import slugify


class Experiment(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')
    usefuls = models.ManyToManyField(User, related_name="usefuls", blank=True)
    notusefuls = models.ManyToManyField(User, related_name="notusefuls", blank=True)

    def __str__(self):
        return self.content[:30]

    def useful_count(self):
        return self.usefuls.count()

    def notuseful_count(self):
        return self.notusefuls.count()

    class Meta:
        ordering = ('created', )

    def save(self, *args, **kwargs):

        if not self.id:
            self.slug = slugify(self.content)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('experiment-detail', args=[str(self.id)])