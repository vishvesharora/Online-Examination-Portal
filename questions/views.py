from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@login_required(login_url='/teacher/login')
def add_questions(request):

    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False 
    if prof:
        
        permissions = has_group(prof,"PROFESSOR")
    if permissions:
        new_Form = QForm()
        """ messages.info(request, f"Professor name is {prof.username}.") """
        if request.method == 'POST' and permissions:
            form = QForm(request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.save()
                messages.success(request,"Question Added Successfully")
                #form.save_m2m()
                return redirect('faculty-addquestions')

        #exams = Exam_Model.objects.filter(professor=prof)
        """ return render(request, 'exam/addquestions.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        }) """

        return render(request, 'teacher_addquestion.html', {
             'examform': new_Form, 'prof': prof,
        })
    else:
        """ return redirect('view_exams_student') """
        return redirect('/')

@login_required(login_url='teacher_login')
def showquestions(request):
    if request.user.is_authenticated:
        user = request.user
        quest = Question_DB.objects.filter(professor = user)
        return render(request,'teacher_questions.html',{'quest':quest})

def showpapers(request):
    user = request.user
    permissions = False
    if user:
        permissions = has_group(user,"PROFESSOR")
    else:
        return redirect('/')
    if permissions:
        papers = Question_Paper.objects.filter(professor = user)
        return render(request,'teacher_papers.html',{'papers':papers})

def show_student_result(request):
    user = request.user
    permissions = False
    if user:
        permissions = has_group(user,"STUDENT")
    else:
        return redirect('/')
    if permissions:
        result = StuResults_DB.objects.filter(student = user)
        return render(request,'student_results.html',{'results':result})



@login_required(login_url='/teacher/login')
def add_question_paper(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"PROFESSOR")
    if permissions:
        new_Form = QPForm(prof_user)
        if request.method == 'POST' and permissions:
            form = QPForm(prof_user,request.POST)
            if form.is_valid():
                quest = form.cleaned_data.get('questions')
                marks = 0
                for q in quest:
                    marks += q.max_marks

                
                messages.success(request,"Question Paper Added Successfully. " + f"Total marks-{marks}")
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.marks = marks
                exam.save()
                form.save_m2m()
                return redirect('faculty-add_question_paper')

       # exams = Exam_Model.objects.filter(professor=prof)
        """ return render(request, 'exam/addquestionpaper.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        }) """
        return render(request, 'teacher_addquestionpaper.html', {
             'examform': new_Form, 'prof': prof,
        })
    else:
        #return redirect('view_exams_student')
        return redirect('/')


@login_required(login_url='teacher_login')
def view_exams_prof(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"PROFESSOR")
    if permissions:
        new_Form = ExamForm(prof_user)
        if request.method == 'POST' and permissions:
            form = ExamForm(prof_user,request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof
                exam.marks = form.cleaned_data.get('question_paper').marks
                exam.save()
                form.save_m2m()
                return redirect('view_exams')

        exams = Exam_Model.objects.filter(professor=prof)
        return render(request, 'teacher_addexam.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('/')

def view_exams_student(request):
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'student_exams.html',{
        'exams':list_un,
        #'completed':list_of_completed
    })

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    min += hour*60
    return "%02d:%02d" % (min, sec) 


def appear_exam(request,id):
    student = request.user
    if request.method == 'GET':
        exam = Exam_Model.objects.get(pk=id)
        time_delta = exam.end_time - exam.start_time
        time = convert(time_delta.seconds)
        time = time.split(":")
        mins = time[0]
        secs = time[1]
        context = {
            "exam":exam,
            "marks":exam.question_paper.marks,
            "question_list":exam.question_paper.questions.all(),
            "secs":secs,
            "mins":mins
        }
        return render(request,'student_exampage.html',context)
    if request.method == 'POST' :
        student = User.objects.get(username=request.user.username)
        paper = request.POST['paper']
        examMain = Exam_Model.objects.get(name = paper)
        stuExam = StuExam_DB.objects.get_or_create(examname=paper, student=student,qpaper = examMain.question_paper)[0]
        
        qPaper = examMain.question_paper
        stuExam.qpaper = qPaper
         
        qPaperQuestionsList = examMain.question_paper.questions.all()
        for ques in qPaperQuestionsList:
            student_question = Stu_Question(student=student,question=ques.question, optionA=ques.optionA, optionB=ques.optionB,optionC=ques.optionC, optionD=ques.optionD,
            answer=ques.answer)
            student_question.save()
            stuExam.questions.add(student_question)
            stuExam.save()

        stuExam.completed = 1
        stuExam.save()
        examQuestionsList = StuExam_DB.objects.filter(student=request.user,examname=paper,qpaper=examMain.question_paper,questions__student = request.user)[0]
        #examQuestionsList = stuExam.questions.all()
        examScore = 0
        list_i = examMain.question_paper.questions.all()
        queslist = examQuestionsList.questions.all()
        i = 0
        for j in range(list_i.count()):
            ques = queslist[j]
            max_m = list_i[i].max_marks
            ans = request.POST.get(ques.question, False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            if ans.lower() == ques.answer.lower() or ans == ques.answer:
                examScore = examScore + max_m
            i+=1

        stuExam.score = examScore
        stuExam.save()
        stu = StuExam_DB.objects.filter(student=request.user,examname=examMain.name)  
        results = StuResults_DB.objects.get_or_create(student=request.user,total_marks = qPaper.marks,scored_marks=examScore,exam=examMain)[0]
        
        return redirect('after_exam')


def after_exam(request):
    return render(request,'student_afterexam.html')


