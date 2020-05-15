from django.db import models
from django.conf import settings

# Create your models here.

class MessegesModelManager(models.Manager):
    def last_10_messages(self):
        return Messages.objects.all().order_by('timestamp')[:10]


class Messages(models.Model):
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_messages', on_delete=models.CASCADE)
    content             = models.TextField(blank=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects = MessegesModelManager()


    def __str__(self):
        return self.author.username