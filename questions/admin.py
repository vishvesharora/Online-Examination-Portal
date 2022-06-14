from django.contrib import admin

from questions.models import *

# Register your models here.
admin.site.register(Question_DB)

admin.site.register(Question_Paper)

admin.site.register(Exam_Model)

admin.site.register(StuExam_DB)

admin.site.register(Stu_Question)

admin.site.register(StuResults_DB)

