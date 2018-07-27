from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Experiment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
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
        return reverse_lazy('experiment-detail', args=[str(self.pk)])

    def get_useful_url(self):
        return reverse_lazy('experiment_useful', args=[str(self.pk)])

    def get_notuseful_url(self):
        return reverse_lazy('experiment_notuseful', args=[str(self.pk)])
# user profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} Profile"

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()