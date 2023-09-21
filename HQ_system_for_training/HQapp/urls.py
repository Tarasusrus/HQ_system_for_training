from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, LessonViewSet, UserLessonViewViewSet, AccessibleLessonsListView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'user_lesson_views', UserLessonViewViewSet)

urlpatterns = router.urls + [
    path('accessible_lessons/', AccessibleLessonsListView.as_view(), name='accessible-lessons-list'),
    path('login/', auth_views.LoginView.as_view(), name='login')
]
