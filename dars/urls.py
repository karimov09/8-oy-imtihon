from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from . import models

app_name = 'dars'

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='course')
router.register('groups', views.LessonViewSet, basename='group')
router.register('teachers', views.TeacherViewSet, basename='teacher')
router.register('students', views.StudentViewSet, basename='student')
router.register('lessons', views.LessonViewSet, basename='lesson')
router.register('lesson-videos', views.LessonVideoViewSet, basename='lesson_video')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
urlpatterns.extend(router.urls)

