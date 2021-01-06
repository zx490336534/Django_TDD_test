from django.db import models
from django.db.models import CASCADE
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')  # 清单中的待办事项必须是唯一的

    def __str__(self):
        return self.text
