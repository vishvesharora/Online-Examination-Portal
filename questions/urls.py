from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    
    path('prof/addquestions/',views.add_questions,name='faculty-addquestions'),
    path('prof/displayquest/',views.showquestions,name="teacher_questions"),
    path('prof/displaypapers/',views.showpapers,name="teacher_papers"),
    path('student/displayexam/',views.view_exams_student,name="student_exams"),
    path('student/displayresult',views.show_student_result,name='student_results'),
    path('student/appear/<int:id>',views.appear_exam,name = "appear_exam"),
    path('student/afterexam',views.after_exam,name="after_exam"),
    path('prof/addnewquestionpaper/',views.add_question_paper,name="faculty-add_question_paper"),
    path('prof/viewexams/',views.view_exams_prof,name="view_exams"),

]
