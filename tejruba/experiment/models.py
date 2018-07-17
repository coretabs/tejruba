from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import slugify

class Experiment(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')

    def __str__(self):
        return self.content[:30]

    class Meta:
        ordering = ('created', )

    def save(self, *args, **kwargs):

        if not self.id:
            self.slug = slugify(self.content)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('experiment-detail', args=[str(self.id)])


class Useful(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usefuls')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='usefuls')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, Useful {self.experiment}'


class NotUseful(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notusefuls')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='notusefuls')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f'{self.user}, NotUseful {self.experiment}'

