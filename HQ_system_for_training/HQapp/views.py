from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
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
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = user.accessible_products.prefetch_related('lessons').all()
        accessible_lessons = Lesson.objects.filter(included_in_products__in=accessible_products).distinct()
        return accessible_lessons
