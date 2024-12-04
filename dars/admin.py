from django.contrib import admin  
from .models import Course, CourseGroup, Teacher, Student, Lesson, LessonVideo, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  
    search_fields = ('title', 'description')  
    list_filter = ('created_at',)  


class CourseGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  
    list_filter = ['name']  
admin.site.register(CourseGroup, CourseGroupAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_working')  # Ko'rinadigan ustunlar.
    search_fields = ('name', 'email') 
    list_filter = ('is_working',) 


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_studying') 
    search_fields = ('user__username', 'user__email')  
    list_filter = ('is_studying',)  

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_group', 'start_time')  
    search_fields = ('title',)  
    list_filter = ('start_time',)  


@admin.register(LessonVideo)
class LessonVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson')  
    search_fields = ('name',) 

