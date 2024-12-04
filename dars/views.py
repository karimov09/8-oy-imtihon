from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, filters, serializers, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Course,
    CourseGroup,
    Teacher,
    Student,
    Lesson,
    LessonVideo,
    Comment,
)
from .serializers import (
    CourseSerializer,
    CourseGroupSerializer,
    TeacherSerializer,
    UserSerializer,
    RegisterSerializer,
    StudentSerializer,
    LessonSerializer,
    LessonVideoSerializer,
    CommentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    Kurslar bilan ishlash uchun ViewSet.
    """
    queryset = Course.objects.all() 
    serializer_class = CourseSerializer  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]  
    ordering_fields = ['title', 'created_at']  
    search_fields = ['title', 'description', 'id']  
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        """
        Kurs yaratish va emailga jonatish funksiyasi.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Foydalanuvchi autentifikatsiya qilinmagan."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        
        user_email = request.user.email
        subject = "Yangi kurs yaratildi"
        message = f"Kurs '{serializer.data['title']}' muvaffaqiyatli yaratildi."
        send_update_email(user_email, subject, message)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def send_update(self, request, pk=None):
        """
        Kursga yangilanish haqida email jo'natish.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Foydalanuvchi autentifikatsiya qilinmagan."}, status=status.HTTP_401_UNAUTHORIZED)

        course = self.get_object()
        user_email = request.user.email
        subject = "Kurs yangilandi"
        message = f"Kurs '{course.title}' yangilandi."
        send_update_email(user_email, subject, message)
        return Response({"detail": "Email muvaffaqiyatli yuborildi."}, status=status.HTTP_200_OK)



class TeacherViewSet(viewsets.ModelViewSet):
    """
    O'qituvchilar bilan ishlash uchun ViewSet.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


    def send_update_email(self, user_email, teacher_email, subject, message):
        """
        Foydalanuvchi va o'qituvchiga email jo'natish.
        """
        recipients = [user_email]
        if teacher_email:
            recipients.append(teacher_email)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False,
        )

    def perform_create(self, serializer):
        """
        O'qituvchi yaratgandan keyin email jo'natish.
        """
        teacher = serializer.save()
        user_email = ""  
        teacher_email = teacher.email
        subject = f"Yangi o'qituvchi qo'shildi: {teacher.name}"
        message = (
            f"Tizimga yangi o'qituvchi qo'shildi.\n"
            f"Ismi: {teacher.name}\n"
            f"Email: {teacher.email}\n"
            f"Telefon: {teacher.phone_number}\n"
            f"Tajriba: {teacher.experience} yil"
        )
        self.send_update_email(user_email, teacher_email, subject, message)


class RegisterView(viewsets.ViewSet):
    """
    Foydalanuvchilarni royxatdan otkazish uchun ViewSet.
    """
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(viewsets.ModelViewSet):
    """
    Studentlar bilan ishlash uchun ViewSet.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Studentni o'chirish funksiyasi.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Student muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)


class LessonViewSet(viewsets.ModelViewSet):
    """
    Darslar bilan ishlash uchun ViewSet.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Darsni o'chirish funksiyasi.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Dars muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)


class LessonVideoViewSet(viewsets.ModelViewSet):
    """
    Dars videolari bilan ishlash uchun ViewSet.
    """
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Izohlar bilan ishlash uchun ViewSet.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CourseGroupViewSet(viewsets.ModelViewSet):
    """
    Kurs guruhlari bilan ishlash uchun ViewSet.
    """
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupSerializer


class RegisterAPIView(generics.CreateAPIView):
    """
    Ro'yxatdan o'tish uchun APIView.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
