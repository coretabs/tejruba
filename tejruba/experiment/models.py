from django.db import models
from django.contrib.auth.models import User


class Experiment(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')

    def __str__(self):
        return self.content[:30]


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

