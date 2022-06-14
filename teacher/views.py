from distutils.log import info
from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

# Create your views here.


@login_required(login_url='teacher_login')
def home(request):
    return render(request, 'teacher_home.html')

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def register(request):
    userForm = forms.TeacherForm()
    teacherForm = forms.TeacherInfoForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherForm(request.POST)
        teacherForm = forms.TeacherInfoForm(request.POST)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.is_active = True
            user.set_password(user.password)
            user.save()

            messages.success(
                request, "Your Professor account created Succesfully.",extra_tags='prof_login')

            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()

            Group.objects.get_or_create(name='PROFESSOR')
            """ my_student_group[0].user_set.add(user) """
            return redirect('teacher_register')

    return render(request, 'teacher_signup.html', context=mydict)


""" def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            exis = User.objects.filter(username=username).exists()
            if exis:
                user_ch = User.objects.get(username=username)
                if user_ch.is_staff:

                    return redirect('home')
        user = auth.authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('teacher_home')

        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'teacher_login.html')
 """

def logout(request):

    auth.logout(request)
    """ messages.success(request, 'You are now Logged Out') """
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        has_grp = False
        if username and password:
            user = auth.authenticate(username=username, password=password)
            exist = User.objects.filter(username=username).exists()
            if user and exist:
                has_grp = has_group(user,"PROFESSOR")
                if has_grp:
                    auth.login(request, user)
                    messages.success(request,f"You are now logged in as {username}.")
                    return redirect('teacher_home')
                else:
                    messages.info(request,"Please ask the admin to grant you the permission to login as professor")
            
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'teacher_login.html')
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'teacher_login.html') 
                 
    return render(request, 'teacher_login.html')

           

                


           
