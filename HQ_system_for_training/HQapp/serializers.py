from rest_framework import serializers
from .models import Product, Lesson, UserLessonView
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']


class LessonSerializer(serializers.ModelSerializer):
    included_in_products = SimpleProductSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class UserLessonViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = UserLessonView
        fields = ['id', 'user', 'lesson', 'viewed_duration', 'is_viewed', 'last_viewed_date']


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    users_with_access = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'users_with_access', 'lessons']


class ProductStatisticSerializer(serializers.Serializer):
    """
    Сериализатор для статистики продукта.
    """

    product = serializers.CharField()  # Название продукта
    watched_lessons_count = serializers.IntegerField()  # Количество просмотренных уроков
    total_viewed_time = serializers.IntegerField()  # Общее время просмотра в секундах
    students_count = serializers.IntegerField()  # Количество студентов, изучающих продукт
    acquisition_percentage = serializers.FloatField()  # Процент приобретения продукта
