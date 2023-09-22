from rest_framework import serializers
from .models import Product, Lesson, UserLessonView
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Пользователя (User).

    Поля:
        id: Уникальный идентификатор пользователя.
        username: Имя пользователя.
    """
    class Meta:
        model = User
        fields = ['id', 'username']


class SimpleProductSerializer(serializers.ModelSerializer):
    """
        Сериализатор для представления базовой информации о продукте.

        Поля:
            id: Идентификатор продукта.
            title: Название продукта.
    """
    class Meta:
        model = Product
        fields = ['id', 'title']


class LessonSerializer(serializers.ModelSerializer):
    """
        Сериализатор для объектов урока.

        Отвечает за конвертацию объектов урока в формат JSON и обратно, предоставляя валидацию данных.
        Включает информацию о продуктах, в которых содержится урок, только для чтения.

        Поля:
        - id: Идентификатор урока.
        - title: Название урока.
        - video_link: Ссылка на видео урока.
        - duration: Длительность урока в секундах.


        Использование:
        - Выводит информацию о уроке при запросах на чтение.
        - Валидирует данные урока при запросах на создание и обновление.
        """
    included_in_products = SimpleProductSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class UserLessonViewSerializer(serializers.ModelSerializer):
    """
        Сериализатор для представления информации о просмотрах уроков пользователями.

        Поля:
            id: Идентификатор просмотра.
            user: Пользователь, который просматривал урок. Представлен сериализатором UserSerializer.
            lesson: Урок, который был просмотрен. Представлен сериализатором LessonSerializer.
            viewed_duration: Продолжительность просмотра урока в секундах.
            is_viewed: Булево значение, указывающее, был ли урок просмотрен.
            last_viewed_date: Дата и время последнего просмотра урока.
    """
    user = UserSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = UserLessonView
        fields = ['id', 'user', 'lesson', 'viewed_duration', 'is_viewed', 'last_viewed_date']


class ProductSerializer(serializers.ModelSerializer):
    """
        Сериализатор для представления информации о продукте.

        Поля:
            id: Идентификатор продукта.
            title: Название продукта.
            owner: Владелец продукта. Представлен сериализатором UserSerializer.
            users_with_access: Пользователи с доступом к продукту. Представлены сериализатором UserSerializer.
            lessons: Уроки, включенные в продукт. Представлены сериализатором LessonSerializer.
    """
    owner = UserSerializer()
    users_with_access = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'users_with_access', 'lessons']


#class ProductStatisticSerializer(serializers.Serializer):
 #   """
  #  Сериализатор для статистики продукта.
   # """
#
 #   product = serializers.CharField()  # Название продукта
  #  watched_lessons_count = serializers.IntegerField()  # Количество просмотренных уроков
   # total_viewed_time = serializers.IntegerField()  # Общее время просмотра в секундах
    #students_count = serializers.IntegerField()  # Количество студентов, изучающих продукт
    #acquisition_percentage = serializers.FloatField()  # Процент приобретения продукта
