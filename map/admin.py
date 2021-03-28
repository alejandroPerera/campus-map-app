from django.contrib import admin
from .models import ClassModel, CourseModel, ScheduleModel


class ClassAdmin(admin.ModelAdmin):
    search_fields = ['class_mnemonic', 'class_number', 'course_number', 'class_instructor']


# Register your models here.
admin.site.register(ClassModel, ClassAdmin)
admin.site.register(CourseModel)
admin.site.register(ScheduleModel)