from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxValueValidator
class Course(models.Model):
    """
    Ushbu model onlayn ta'lim platformasidagi kurslar.

    Atributlar:
        title (str): Kursning noyob nomi, maksimal uzunligi 255 belgidan oshmasligi kerak.
        description (str): Kurs mazmuni haqida  ma'lumot.
        author (User): Kursni yaratgan oqtuvchi, Django User modeli bilan bog'langan 
                       foreign key orqali bog'lanadi. Agar user o'chirilsa, unga tegishli 
                       kurslar ham o'chiriladi.
        created_at (datetime): Kurs yaratilgan sana va vaqtni ifodalaydi, avtomatik ravishda 
                               yaratish vaqtida o'rnatiladi.
    """

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseGroup(models.Model):
    """
    Ushbu model kurslar guruhi, u bir nechta kurslarni birlashtirish uchun ishlatiladi.

    Atributlar:
        name (str): Kurslar guruhining nomi, maksimal uzunligi 255 belgidan oshmasligi kerak.
        description (str): Guruh haqida qoshimcha ma'lumot ixtiyoriy
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    Oqituvchi modeli, foydalanuvchi bilan bog'langan va  ma'lumotlarni saqlaydi.

    Atributlar:
        user (User): Foydalanuvchi modeli bilan one-to-one bog'lanadi. Agar foydalanuvchi o'chirilsa, o'qituvchi ham o'chiriladi.
        name (str): O'qituvchining ismi, maksimal uzunligi 50 belgidan oshmasligi kerak.
        email (str): O'qituvchining elektron pochtasi.
        phone_number (str): Telefon raqami, maksimal uzunligi 15 ta belgidan iborat nomer ixtiyoriy
        biography (str): O'qituvchining biografiyasi ixtiyoriy
        experience (int): Tajriba yillari, maksimal qiymati 35.
        is_working (bool): O'qituvchining faol yoki faol emasligini ko'rsatadi.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, unique=True
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    experience = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(35)])
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Student(models.Model):
    """
    Talaba modeli, foydalanuvchi va kurslar guruhi bilan bog'liq.

    Atributlar:
        user (User): Foydalanuvchi modeli bilan one-to-one bog'lanadi.
        groups (CourseGroup): Talaba a'zo bo'lgan kurslar guruhlari.
        is_studying (bool): Talabaning hozirda o'qiyapti yoki yo'qligini ko'rsatadi.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    groups = models.ManyToManyField(CourseGroup, related_name="students")
    is_studying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Lesson(models.Model):
    """
    Dars modeli, kurs guruhi bilan bog'liq va darsga oid ma'lumotlarni saqlaydi.

    Atributlar:
        course_group (CourseGroup): Ushbu dars tegishli bo'lgan kurs guruhi.
        title (str): Dars mavzusi, maksimal uzunligi 250 belgidan oshmasligi kerak.
        start_time (datetime): Dars boshlanish vaqti, avtomatik tarzda o'rnatiladi.
        likes (int): Darsga berilgan like soni.
        dislikes (int): Darsga berilgan dislike soni.
    """

    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=250, help_text="Dars mavzusi")
    start_time = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class LessonVideo(models.Model):
    """
    Dars videolari modeli, darsga tegishli videolarni saqlaydi.

    Atributlar:
        name (str): Video nomi, maksimal uzunligi 155 belgidan oshmasligi kerak.
        lesson (Lesson): Ushbu video tegishli bo'lgan dars.
        video_file (FileField): Yuklangan video fayl (faqat mp4 va avi formatda bo'lishi mumkin).
    """

    name = models.CharField(max_length=155)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    video_file = models.FileField(
        upload_to='lesson/videos/',
        validators=[FileExtensionValidator(['mp4', 'avi'])],
    )

    def __str__(self):
        return self.name

LIKE_CHOICES = (
    ('like', 'Like'), 
    ('dislike', 'Dislike'),  
)

class Comment(models.Model):
    """
    Darsga foydalanuvchilar tomonidan qoldirilgan izohlar va reaktsiyalar modeli.

    Atributlar:
        lesson (Lesson): Ushbu izoh tegishli bo'lgan dars.
        author (User): Izoh oquvchi.
        content (str): Izoh matni.
        liked (str): Foydalanuvchi reaksiyasi (like yoki dislike).
        created_at (datetime): Izoh yaratilgan sana va vaqt, avtomatik o'rnatiladi.
    """

    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    liked = models.CharField(choices=LIKE_CHOICES, max_length=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} tomonidan {self.lesson.title} darsiga izoh"
