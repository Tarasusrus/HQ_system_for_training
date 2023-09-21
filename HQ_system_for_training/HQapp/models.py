from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Product(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products')
    users_with_access = models.ManyToManyField(User, related_name='accessible_products')
    lessons = models.ManyToManyField('Lesson', related_name='included_in_products')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.IntegerField()  # В секундах.

    def __str__(self):
        return self.title


class UserLessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_duration = models.IntegerField()  # В секундах.
    is_viewed = models.BooleanField(default=False)
    last_viewed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} посмотрел {self.lesson}, {self.last_viewed_date}"


@receiver(pre_save, sender=UserLessonView)
def update_is_viewed(sender, instance, **kwargs):
    lesson_duration = instance.lesson.duration
    if instance.viewed_duration >= lesson_duration * 0.8:
        instance.is_viewed = True
