from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.http import Http404
from django.views.generic import ListView
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Lesson, UserLessonView
from .serializers import ProductSerializer, LessonSerializer, UserLessonViewSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLessonViewViewSet(viewsets.ModelViewSet):
    queryset = UserLessonView.objects.all()
    serializer_class = UserLessonViewSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccessibleLessonsListView(ListAPIView):
    """
    Получение списка уроков, доступных аутентифицированному пользователю.

    Предоставляет детализированный список уроков, к которым у текущего аутентифицированного пользователя есть доступ.
    Уроки выбираются на основе продуктов, к которым у пользователя есть доступ.
    Используется оптимизированный запрос с предварительной выборкой для минимизации количества обращений к базе данных.

    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = user.accessible_products.prefetch_related('lessons').all()
        accessible_lessons = Lesson.objects.filter(included_in_products__in=accessible_products).distinct()
        return accessible_lessons


class LessonsByProductView(APIView):
    """
    Класс для представления уроков, включенных в продукт, доступный текущему пользователю.
    Отображает информацию о каждом уроке, такую как название урока, видео, продолжительность,
    статус просмотра, просмотренное время и последнюю дату просмотра.
    """

    def get_object(self, product_id, user):
        """
        Получает продукт по идентификатору, проверяет, есть ли у пользователя доступ к продукту,
        и возвращает продукт, если пользователь имеет доступ.
        В противном случае вызывается исключение Http404.

        Args:
        product_id (int): Идентификатор продукта.
        user (User): Текущий пользователь.

        Returns:
        Product: Продукт, если пользователь имеет доступ.

        Raises:
        Http404: Если продукт не существует или у пользователя нет доступа.
        """
        try:
            product = Product.objects.get(pk=product_id)
            if user not in product.users_with_access.all():
                raise Http404
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, product_id, format=None):
        """
        Отправляет GET-запрос для получения уроков, включенных в продукт,
        и формирует ответ с информацией об уроках.

        Args:
        request (HttpRequest): HTTP-запрос.
        product_id (int): Идентификатор продукта.
        format (str, optional): Формат ответа. По умолчанию None.

        Returns:
        Response: Ответ с информацией о продукте и уроках.
        """
        user = request.user  # Текущий пользователь
        product = self.get_object(product_id, user)  # Получаем продукт с проверкой доступа пользователя
        lessons = Lesson.objects.filter(included_in_products=product)  # Получаем уроки, включенные в продукт

        lesson_data = []
        # Формируем данные для каждого урока
        for lesson in lessons:
            user_lesson_view, _ = UserLessonView.objects.get_or_create(user=user, lesson=lesson)
            lesson_data.append({
                'lesson_title': lesson.title,
                'video_link': lesson.video_link,
                'duration': lesson.duration,
                'is_viewed': user_lesson_view.is_viewed,
                'viewed_duration': user_lesson_view.viewed_duration,
                'last_viewed_date': user_lesson_view.last_viewed_date,
            })

        # Формируем итоговый ответ
        response_data = {
            'product_title': product.title,
            'lessons': lesson_data,
        }

        return Response(response_data)  # Отправляем ответ


class AccessibleProductsListView(LoginRequiredMixin, ListView):
    """
    Класс для представления списка продуктов, доступных текущему пользователю.

    Attributes:
    - template_name (str): Путь к шаблону, который будет использован для отображения продуктов.
    - context_object_name (str): Название контекстного объекта, содержащего продукты в шаблоне.
    - login_url (str): URL страницы входа, на которую будет перенаправлен неавторизованный пользователь.
    """

    template_name = 'accessible_products.html'
    context_object_name = 'accessible_products'
    login_url = '/path_to_your_login_page/'  # Замените на путь к вашей странице входа

    def get_queryset(self):
        """
        Определяет QuerySet продуктов, который будет использован для получения списка продуктов.

        Returns:
        QuerySet: Список продуктов, доступных текущему пользователю.
        """

        # Получаем текущего пользователя
        current_user = self.request.user

        # Возвращаем продукты, к которым у пользователя есть доступ
        return Product.objects.filter(users_with_access=current_user)


class LessonsByProductListView(ListAPIView):
    """
    Класс для представления списка уроков входящих в конкретный продукт.
    Предполагается, что пользователь имеет доступ к продукту.

    Attributes:
    - template_name (str): Путь к шаблону, который будет использован для отображения уроков.
    - context_object_name (str): Название контекстного объекта, содержащего уроки в шаблоне.
    - serializer_class: Класс сериализатора для преобразования объектов урока в JSON.
    """

    template_name = 'lessons_by_product.html'
    context_object_name = 'lessons'
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Получает и возвращает QuerySet уроков для продукта, доступного текущему пользователю.

        Returns:
        QuerySet: Список уроков, входящих в продукт.
        """

        # Получаем текущего пользователя и идентификатор продукта из параметров запроса
        user = self.request.user
        product_id = self.kwargs.get('product_id')

        # Получаем продукт, к которому у текущего пользователя есть доступ, или возвращаем 404
        product = get_object_or_404(Product, id=product_id, users_with_access=user)

        # Возвращаем все уроки, входящие в продукт
        return product.lessons.all()


class ProductStatisticView(APIView):
    """
    Представление для отображения статистики по продуктам.
    Этот API предоставляет статистику по каждому продукту, такую как количество просмотренных уроков,
    общее время просмотра, количество студентов и процент приобретения продукта.
    """
    permission_classes = [permissions.IsAuthenticated]  # Доступ разрешен только аутентифицированным пользователям

    def get(self, request, *args, **kwargs):
        # Получение списка всех продуктов и общего количества пользователей
        products = Product.objects.all()
        total_users = User.objects.count()

        data = []  # Итоговый список для хранения статистики каждого продукта
        for product in products:
            # Подсчет количества просмотренных уроков для каждого продукта
            watched_lessons_count = UserLessonView.objects.filter(
                lesson__included_in_products=product, is_viewed=True
            ).count()

            # Подсчет общего времени просмотра уроков для каждого продукта
            total_viewed_time = UserLessonView.objects.filter(
                lesson__included_in_products=product
            ).aggregate(total_time=models.Sum('viewed_duration'))['total_time'] or 0

            # Подсчет количества студентов для каждого продукта
            students_count = product.users_with_access.count()

            # Расчет процента приобретения продукта
            acquisition_percentage = (students_count / total_users) * 100 if total_users > 0 else 0

            # Добавление статистики продукта в итоговый список
            data.append({
                'product': product.title,
                'watched_lessons_count': watched_lessons_count,
                'total_viewed_time': total_viewed_time,
                'students_count': students_count,
                'acquisition_percentage': acquisition_percentage,
            })

        # Возвращение итогового списка статистики продуктов
        return Response(data)
