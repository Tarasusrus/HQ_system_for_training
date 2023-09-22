from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, LessonViewSet, UserLessonViewViewSet, AccessibleLessonsListView, \
    LessonsByProductView, AccessibleProductsListView, ProductStatisticView

"""router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'user_lesson_views', UserLessonViewViewSet)"""

urlpatterns = [
    path('accessible_lessons/', AccessibleLessonsListView.as_view(), name='accessible-lessons-list'),
    path('accessible_products/', AccessibleProductsListView.as_view(), name='accessible-products-list'),
    path('products/<int:product_id>/lessons/', LessonsByProductView.as_view(), name='lessons-by-product'),
    path('product-statistics/', ProductStatisticView.as_view(), name='product-statistics'),

]
