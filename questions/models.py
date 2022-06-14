from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Question_DB(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "PROFESSOR"}, on_delete=models.CASCADE, null=True)
    qno = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    answer = models.CharField(max_length=200)
    max_marks = models.IntegerField(default=0)

    def __str__(self):
        #return f'Question No.{self.qno}: {self.question} '
        return f'{self.question} '

    class Meta:
        verbose_name_plural = 'Question DB'

class Question_Paper(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "PROFESSOR"}, on_delete=models.CASCADE)
    qPaperTitle = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question_DB)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return f' Question Paper Title :- {self.qPaperTitle}\n'
    
    class Meta:
        verbose_name_plural = 'Question Papers'

class Exam_Model(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "PROFESSOR"}, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    marks = models.IntegerField(default=0)
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, related_name='exams')
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Exams'

class Stu_Question(Question_DB):
    professor = None
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "STUDENT"}, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="E")

    def __str__(self):
        return str(self.student.username) + " "+ str(self.qno) +"-Stu_QuestionDB"

class StuExam_DB(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "STUDENT"}, on_delete=models.CASCADE, null=True)
    examname = models.CharField(max_length=100)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Stu_Question)
    score = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student.username) +" " + str(self.examname) + " " + str(self.qpaper.qPaperTitle) + "-StuExam_DB"

class StuResults_DB(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "STUDENT"}, on_delete=models.CASCADE, null=True)
    total_marks = models.IntegerField(default=0)
    scored_marks = models.IntegerField(default=0)
    exam = models.ForeignKey(Exam_Model,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.student.username) + ' ' + str(self.exam)

    class Meta:
        verbose_name_plural = 'Student Results'