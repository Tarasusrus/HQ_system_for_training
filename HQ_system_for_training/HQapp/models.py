from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Product(models.Model):
    """
        Модель Продукта, представляющая собой образовательный продукт или курс,
        содержащий несколько уроков.

        У каждого продукта есть заголовок, владелец, пользователи с доступом и связанные уроки.

        Поля:
        - title (CharField): Название продукта, строка максимальной длины 100 символов.
        - owner (ForeignKey): Владелец продукта, связь с моделью User.
        - users_with_access (ManyToManyField): Пользователи, имеющие доступ к продукту.
        - lessons (ManyToManyField): Уроки, включенные в продукт.

        Методы:
        - __str__(): Возвращает строковое представление продукта, в данном случае — его название.
        """
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products')
    users_with_access = models.ManyToManyField(User, related_name='accessible_products')
    lessons = models.ManyToManyField('Lesson', related_name='included_in_products')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
        Модель Урока, представляющая собой один урок или обучающий материал.

        У каждого урока есть заголовок, ссылка на видео и длительность.

        Поля:
        - title (CharField): Название урока, строка максимальной длины 100 символов.
        - video_link (URLField): URL-ссылка на видео урока.
        - duration (IntegerField): Длительность урока в секундах.

        Методы:
        - __str__(): Возвращает строковое представление урока, в данном случае — его название.
    """
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.IntegerField()  # В секундах.

    def __str__(self):
        return self.title


class UserLessonView(models.Model):
    """
        Модель Просмотра Урока Пользователем, представляющая собой информацию
        о просмотре конкретного урока конкретным пользователем.

        У каждого просмотра урока есть пользователь, урок, просмотренная длительность,
        статус просмотра и дата последнего просмотра.

        Поля:
        - user (ForeignKey): Пользователь, который просмотрел урок, связь с моделью User.
        - lesson (ForeignKey): Урок, который был просмотрен, связь с моделью Lesson.
        - viewed_duration (IntegerField): Просмотренная длительность урока в секундах, значение по умолчанию 0.
        - is_viewed (BooleanField): Статус просмотра, показывающий, был ли урок просмотрен, значение по умолчанию False.
        - last_viewed_date (DateTimeField): Дата и время последнего просмотра урока, обновляется автоматически.

        Методы:
        - __str__(): Возвращает строковое представление просмотра урока,
                     содержащее информацию о пользователе, уроке и дате последнего просмотра.
        """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_duration = models.IntegerField(default=0)  # В секундах.
    is_viewed = models.BooleanField(default=False)
    last_viewed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} посмотрел {self.lesson}, {self.last_viewed_date}"


@receiver(pre_save, sender=UserLessonView)
def update_is_viewed(sender, instance, **kwargs):
    """
        Обработчик сигнала pre_save для модели UserLessonView.

        Обновляет поле is_viewed экземпляра UserLessonView перед его сохранением,
        если просмотренная длительность урока составляет 80% или более от
        общей длительности урока.

        Параметры:
        - sender (Model): Модель, отправляющая сигнал. В данном случае, это UserLessonView.
        - instance (UserLessonView): Экземпляр модели UserLessonView, который сохраняется.
        - kwargs (dict): Дополнительные аргументы (не используются в данной функции).

        Возвращаемое значение:
        - Нет. Функция только обновляет поле is_viewed экземпляра UserLessonView, если необходимо.
    """
    lesson_duration = instance.lesson.duration
    if instance.viewed_duration >= lesson_duration * 0.8:
        instance.is_viewed = True
